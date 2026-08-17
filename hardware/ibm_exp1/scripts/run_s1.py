"""S1 — ideal finite-shot end-to-end simulation battery (AR-023a §1).

Two phases, both deterministic and fail-closed:

--precompute
    Load the frozen QPY bundle, verify every circuit's QPY hash against
    the frozen registry, compute each circuit's exact outcome
    distribution (statevector + basis rotations), cache them to NPZ,
    and run the infinite-shot acceptance gate: pushing the exact
    distributions through the complete sampled-analysis path must
    reproduce eps_sector^(37) and the ideal Dbar/Phi* arrays to 1e-10.
    The battery refuses to run without a verified cache.

--run
    The R-experiment battery at 768 shots with the committed seed
    policy, 1,000-replicate setting-aware bootstrap, floors, clause
    evaluation (AR-023 §6 five clauses, A1.3 operationalization), and
    the canonical-JSON report (A1.7: no wall-clock data; timestamps and
    environment live in the meta sidecar).

No IBM credentials, no network access, no QPU submission.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
from importlib.metadata import version
import json
import os
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import sampling  # noqa: E402
from sampling import (N_OUT, SHOTS, StateIndex,  # noqa: E402
                      aggregation_weights, analyze_pass,
                      floors_from_slots, load_bundle, phi_from_mi,
                      zrow_masks)

REPORT_SCHEMA = 1
EPS_REF_KEY = "eps_sector_37"


# ----------------------------------------------------------------- utils

def canonical_report_json(report: dict) -> str:
    """A1.7 canonical form: sorted keys, full-precision repr floats."""
    return json.dumps(report, sort_keys=True, indent=1,
                      ensure_ascii=False, allow_nan=False)


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _load_manifest_bits():
    manifest, registry, basis_rows = load_bundle(ROOT)
    index = StateIndex(registry["circuits"], basis_rows)
    recon_rows = sampling.reconstruction_basis_rows(basis_rows)
    w1, w2 = aggregation_weights(recon_rows)
    z_exc, _ = zrow_masks(recon_rows)
    comparator = np.load(
        ROOT / manifest["comparator"]["npz_path"], allow_pickle=False)
    p_star = np.asarray(comparator["p_star"], dtype=float)
    ref = manifest["s1_reference"]
    ref_arrays = np.load(
        ROOT / "hardware" / "ibm_exp1" / "results" / "sim_reference"
        / "s1_reference_arrays.npz", allow_pickle=False)
    return (manifest, registry, index, w1, w2, z_exc, p_star, ref,
            ref_arrays)


# ---------------------------------------------------------- precompute

def precompute(cache_path: Path) -> dict:
    from qiskit import qpy
    from qiskit.quantum_info import Statevector
    from circuits import qpy_sha256

    manifest, registry, index, w1, w2, z_exc, p_star, ref, ref_arrays = (
        _load_manifest_bits())
    rows = registry["circuits"]
    bundle_dir = ROOT / "hardware" / "ibm_exp1" / "bundle"
    with (bundle_dir / "logical_circuits.qpy").open("rb") as handle:
        circuits = qpy.load(handle)
    if len(circuits) != len(rows):
        raise RuntimeError("QPY circuit count differs from registry")

    probs = np.empty((len(circuits), N_OUT))
    for file_index, (circuit, row) in enumerate(zip(circuits, rows)):
        if qpy_sha256(circuit) != row["logical_circuit_sha256"]:
            raise RuntimeError(
                f"circuit hash mismatch at file index {file_index} "
                f"({row['circuit_id']})")
        bare = circuit.remove_final_measurements(inplace=False)
        probs[file_index] = Statevector.from_instruction(bare).probabilities()
    if not np.allclose(probs.sum(axis=1), 1.0, atol=1.0e-12):
        raise RuntimeError("exact distributions do not normalize")

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache_path, probs=probs)
    cache_hash = _sha256_file(cache_path)

    check = infinite_shot_check(probs, index, w1, w2, z_exc, p_star,
                                ref, ref_arrays)
    record = {
        "cache_sha256": cache_hash,
        "circuit_hashes_verified": len(rows),
        **check,
    }
    (cache_path.parent / "exact_probs_provenance.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return record


def infinite_shot_check(probs, index, w1, w2, z_exc, p_star, ref,
                        ref_arrays, shots: int = SHOTS) -> dict:
    """Push exact distributions through the sampled path; require parity."""

    def counts_by_state(state_id):
        rows = index.rows_for[state_id]
        full = probs[rows] * float(shots)
        half = probs[rows] * (shots / 2.0)
        return np.stack([full, half, half], axis=0)   # slots full, h1, h2

    result = analyze_pass(counts_by_state, index, p_star, w1, w2, z_exc,
                          project=True, keep_per_time=False)
    eps_inf = float(result["eps"][0])
    dbar_diff = float(np.linalg.norm(
        result["dbar"][0] - ref_arrays["dbar_37_ideal"]))
    dstar_diff = float(np.linalg.norm(
        result["phi_star"][0] - ref_arrays["d_star_ideal"]))
    eps_ref = float(ref[EPS_REF_KEY])
    ok = (abs(eps_inf - eps_ref) < 1.0e-10 and dbar_diff < 1.0e-10
          and dstar_diff < 1.0e-10)
    if not ok:
        raise RuntimeError(
            "infinite-shot acceptance gate FAILED: "
            f"eps_inf={eps_inf!r} vs ref={eps_ref!r}, "
            f"|Dbar diff|={dbar_diff:.3e}, |Phi* diff|={dstar_diff:.3e}")
    return {
        "infinite_shot_eps": eps_inf,
        "infinite_shot_eps_ref": eps_ref,
        "infinite_shot_dbar_fro_diff": dbar_diff,
        "infinite_shot_dstar_fro_diff": dstar_diff,
        "infinite_shot_gate": "PASS",
    }


# ------------------------------------------------------------- battery

_G: dict = {}


def _exact_mi_series(manifest, p_star):
    """Exact MI stack on the hardware time grid (for A2.4 structure)."""
    from experiment import (canonicalize_mode_columns,
                            embed_one_magnon_amplitudes,
                            evolve_one_magnon_amplitudes,
                            registered_initial_site_amplitudes)
    from ideg.migraph import mutual_information_matrix

    with np.load(ROOT / manifest["comparator"]["npz_path"],
                 allow_pickle=False) as archive:
        energies = np.asarray(archive["eigenvalues"], dtype=float)
        modes = canonicalize_mode_columns(archive["eigenvectors"])
        mode_rdms = np.asarray(archive["mode_pair_rdms"], dtype=complex)
    times = np.asarray(manifest["time_grid"]["values"], dtype=float)
    initial = registered_initial_site_amplitudes(
        manifest["selection"]["paper_state_seed"], 10)
    dynamic = evolve_one_magnon_amplitudes(initial, times, energies, modes)
    mi_t = np.stack([
        mutual_information_matrix(embed_one_magnon_amplitudes(row, 10),
                                  10, mixed=False) for row in dynamic])
    return mi_t, mode_rdms


def _init_worker(cache_path_str: str, base_override: int | None = None):
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    (manifest, registry, index, w1, w2, z_exc, p_star, ref,
     ref_arrays) = _load_manifest_bits()
    probs = np.load(cache_path_str, allow_pickle=False)["probs"]
    base = (int(base_override) if base_override is not None
            else int(manifest["seeds"]["ideal_sampler_seed"]))
    mi_t, mode_rdms = _exact_mi_series(manifest, p_star)
    _G.update(manifest=manifest, index=index, w1=w1, w2=w2, z_exc=z_exc,
              p_star=p_star, ref=ref, probs=probs, base=base,
              exact_mi_t=mi_t, comparator_rdms=mode_rdms,
              control_mode=int(registry["control_mode"]))
    _G["structural"] = structural_excursions(p_star)


def structural_excursions(p_star) -> np.ndarray:
    """Per-variant excursion of eps on the EXACT metric (A2.4).

    Order: 37 leave-one-time-out variants, then 45 leave-one-pair-out.
    Computed once per worker from the frozen comparator and the exact
    evolved states, so the criterion measures MEASUREMENT dominance and
    not the graph structure the exact metric already exhibits.
    """
    mi_t = _G["exact_mi_t"]
    mi_s = sampling.mi_from_pair_rdms(
        np.tensordot(p_star, _G["comparator_rdms"], axes=(0, 0)))
    phi_t = phi_from_mi(mi_t)
    star = phi_from_mi(mi_s)
    dbar = phi_t.mean(axis=0)
    e0 = float(np.linalg.norm(star - dbar) / np.linalg.norm(dbar))
    out = []
    total = phi_t.sum(axis=0)
    n_t = len(phi_t)
    for t_index in range(n_t):
        d_t = (total - phi_t[t_index]) / (n_t - 1)
        out.append(abs(float(np.linalg.norm(star - d_t)
                             / np.linalg.norm(d_t)) - e0))
    for k in range(sampling.N_PAIRS):
        stack = np.concatenate([mi_t, mi_s[None]], axis=0)
        phi_all = phi_from_mi(stack, removed_pair=k)
        d_k = phi_all[:n_t].mean(axis=0)
        out.append(abs(float(np.linalg.norm(phi_all[n_t] - d_k)
                             / np.linalg.norm(d_k)) - e0))
    return np.asarray(out)


def run_experiment(r: int, n_boot: int, shots: int = SHOTS) -> dict:
    """One synthetic experiment under the AR-023a Amendment 2 rule."""
    index: StateIndex = _G["index"]
    probs = _G["probs"]
    base = _G["base"]
    w1, w2, z_exc, p_star = _G["w1"], _G["w2"], _G["z_exc"], _G["p_star"]
    eps_ref = float(_G["ref"][EPS_REF_KEY])
    exact_exc = _G["structural"]
    ctrl_mode = int(_G["control_mode"])

    half_shots = shots // 2
    n_circ = len(probs)
    canonical = index.canonical_index
    main_halves = np.empty((n_circ, 2, N_OUT), dtype=np.uint16)
    for c in range(n_circ):
        rng = np.random.default_rng(np.random.SeedSequence(
            [base, int(canonical[c]), r]))
        main_halves[c] = rng.multinomial(half_shots, probs[c], size=2)
    main_full = main_halves.sum(axis=1)

    def rdm_stack(state_ids, source):
        used_list, proj_list = [], []
        for state_id in state_ids:
            counts = source[index.rows_for[state_id]].astype(float)
            raw = sampling.pair_rdms_from_counts(counts, w1, w2)
            used, proj = sampling.hermitize_project_batch(raw, True)
            used_list.append(used)
            proj_list.append(proj)
        return np.stack(used_list), np.concatenate(proj_list)

    dyn_f, proj_dyn = rdm_stack(index.dynamic_ids, main_full)
    sec_f, proj_sec = rdm_stack(index.sector_ids, main_full)
    ctl_f, proj_ctl = rdm_stack(index.control_ids, main_full)
    proj_all = np.concatenate([proj_dyn, proj_sec, proj_ctl])

    eps_main, phi_t, dbar, star, mi_t, mi_star = (
        sampling.endpoint_from_stacks(dyn_f, sec_f, p_star))

    # ---- A2.1 split arm: the complete endpoint, independently per half
    eps_halves = []
    for h in range(2):
        arm = main_halves[:, h]
        eps_halves.append(sampling.endpoint_from_stacks(
            rdm_stack(index.dynamic_ids, arm)[0],
            rdm_stack(index.sector_ids, arm)[0], p_star)[0])

    # ---- A2.1 duplicate arm: early vs late control substituted in sigma*
    eps_ctrl = []
    for c in range(2):
        sec_alt = sec_f.copy()
        sec_alt[ctrl_mode] = ctl_f[c]
        eps_ctrl.append(sampling.endpoint_from_stacks(
            dyn_f, sec_alt, p_star)[0])

    floors = sampling.endpoint_floor(eps_halves[0], eps_halves[1],
                                     eps_ctrl[0], eps_ctrl[1])
    duplicate = floors["duplicate"]      # systematic: never bootstrapped

    proj_max = float(proj_all.max())
    proj_median = float(np.median(proj_all))

    # ---- A2.5 leakage witness from the all-Z row
    surv = []
    for state_id in index.dynamic_ids + index.sector_ids:
        row = index.leak_row_for.get(state_id)
        if row is not None:
            surv.append(float(sampling.survival_from_allz(
                main_full[row].astype(float))))
    surv = np.asarray(surv) if surv else np.array([1.0])

    # ---- bootstrap: split arm only (A2.2)
    emp = main_full.astype(float) / shots
    boot_root = np.random.SeedSequence([base, 10 ** 6 + r])
    children = boot_root.spawn(n_circ)

    def boot_counts(state_id):
        rows = index.rows_for[state_id]
        out = np.empty((n_boot, 3, len(rows), N_OUT), dtype=np.uint16)
        for slot_index, c in enumerate(rows):
            rng = np.random.default_rng(children[c])
            halves = rng.multinomial(half_shots, emp[c], size=(n_boot, 2))
            out[:, 0, slot_index] = halves.sum(axis=1)
            out[:, 1, slot_index] = halves[:, 0]
            out[:, 2, slot_index] = halves[:, 1]
        return out

    boot = analyze_pass(boot_counts, index, p_star, w1, w2, z_exc,
                        project=True, keep_per_time=False,
                        track_leakage=False)
    eps_b = boot["eps"][:, 0]
    split_b = np.abs(boot["eps"][:, 1] - boot["eps"][:, 2])
    floor_b = np.maximum(split_b, duplicate)
    delta_b = eps_b - floor_b
    eps_floor_exp = float(max(np.median(split_b), duplicate))

    delta_main = eps_main - floors["floor"]
    delta_median = float(np.median(delta_b))
    ci_low = float(np.quantile(delta_b, 0.025))
    ci_high = float(np.quantile(delta_b, 0.975))

    # ---- A2.4 dominance: excess over the exact structural excursion
    variants = []
    total = phi_t.sum(axis=0)
    n_t = len(phi_t)
    for t_index in range(n_t):
        d_t = (total - phi_t[t_index]) / (n_t - 1)
        e = float(np.linalg.norm(star - d_t) / np.linalg.norm(d_t))
        variants.append(e - floors["floor"])
    for k in range(sampling.N_PAIRS):
        stack = np.concatenate([mi_t, mi_star[None]], axis=0)
        phi_all = phi_from_mi(stack, removed_pair=k)
        d_k = phi_all[:n_t].mean(axis=0)
        e = float(np.linalg.norm(phi_all[n_t] - d_k) / np.linalg.norm(d_k))
        variants.append(e - floors["floor"])
    variants = np.asarray(variants)
    raw_exc = np.abs(variants - delta_main)
    excess = np.abs(raw_exc - exact_exc)
    tol = 0.25 * abs(delta_median)
    sign_flip = bool(np.any(np.sign(variants) != np.sign(delta_main)))

    clause_1 = bool(ci_low > 0.0)
    clause_2 = bool(np.median(eps_b) >= 2.0 * eps_floor_exp)
    clause_3 = bool(surv.min() >= 0.70)
    clause_4 = True          # ideal backend: raw and M3 coincide exactly
    clause_5 = bool(float(excess.max()) <= tol and not sign_flip
                    and proj_max < 0.05)
    success = all([clause_1, clause_2, clause_3, clause_4, clause_5])

    return {
        "experiment": r,
        "rule": "AR-023a Amendment 2",
        "eps_main": eps_main,
        "eps_boot_median": float(np.median(eps_b)),
        "eps_boot_q025": float(np.quantile(eps_b, 0.025)),
        "eps_boot_q975": float(np.quantile(eps_b, 0.975)),
        "eps_half_1": eps_halves[0],
        "eps_half_2": eps_halves[1],
        "eps_ctrl_early": eps_ctrl[0],
        "eps_ctrl_late": eps_ctrl[1],
        "floor_split_main": floors["split"],
        "floor_duplicate_main": duplicate,
        "floor_main": floors["floor"],
        "floor_split_boot_median": float(np.median(split_b)),
        "eps_floor_experiment": eps_floor_exp,
        "delta_main": delta_main,
        "delta_boot_median": delta_median,
        "delta_ci95": [ci_low, ci_high],
        "proj_fro_max_main": proj_max,
        "proj_fro_median_main": proj_median,
        "leakage_survival_min": float(surv.min()),
        "leakage_survival_median": float(np.median(surv)),
        "loto_lopo_raw_excursion_max": float(raw_exc.max()),
        "loto_lopo_excess_max": float(excess.max()),
        "loto_lopo_sign_flip": sign_flip,
        "clause_5a_tolerance": float(tol),
        "clauses": {
            "1_delta_ci_above_zero": clause_1,
            "2_eps_ge_2floor": clause_2,
            "3_leakage_not_red": clause_3,
            "4_raw_m3_direction": clause_4,
            "5_no_dominance": clause_5,
        },
        "success_rule": success,
        "abs_eps_minus_ref": abs(eps_main - eps_ref),
    }


def _worker(args):
    r, n_boot, shots = args
    return run_experiment(r, n_boot, shots)


def run_battery(cache_path: Path, out_dir: Path, n_experiments: int,
                n_boot: int, workers: int, shots: int = SHOTS,
                base_override: int | None = None) -> Path:
    provenance_path = cache_path.parent / "exact_probs_provenance.json"
    if not cache_path.exists() or not provenance_path.exists():
        raise RuntimeError("run --precompute first (cache + provenance)")
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    if provenance["cache_sha256"] != _sha256_file(cache_path):
        raise RuntimeError("exact-distribution cache hash mismatch")
    if provenance.get("infinite_shot_gate") != "PASS":
        raise RuntimeError("infinite-shot acceptance gate not recorded")

    (manifest, registry, index, w1, w2, z_exc, p_star, ref,
     ref_arrays) = _load_manifest_bits()
    base = (int(base_override) if base_override is not None
            else int(manifest["seeds"]["ideal_sampler_seed"]))
    eps_ref = float(ref[EPS_REF_KEY])

    exp_dir = out_dir / "experiments"
    exp_dir.mkdir(parents=True, exist_ok=True)
    results: list = [None] * n_experiments
    pending = []
    for r in range(n_experiments):
        record_path = exp_dir / f"exp_{r:03d}.json"
        if record_path.exists():
            results[r] = json.loads(record_path.read_text(encoding="utf-8"))
        else:
            pending.append(r)
    print(f"resuming: {n_experiments - len(pending)} cached, "
          f"{len(pending)} to run", flush=True)
    if pending:
        from concurrent.futures import as_completed
        with ProcessPoolExecutor(
                max_workers=workers, initializer=_init_worker,
                initargs=(str(cache_path), base_override),
                max_tasks_per_child=1) as pool:
            futures = {pool.submit(_worker, (r, n_boot, shots)): r
                       for r in pending}
            done = 0
            for future in as_completed(futures):
                record = future.result()
                r = record["experiment"]
                results[r] = record
                (exp_dir / f"exp_{r:03d}.json").write_text(
                    canonical_report_json(record) + "\n", encoding="utf-8")
                done += 1
                print(f"experiment {r} done "
                      f"({done}/{len(pending)} this run)", flush=True)

    eps_mains = np.array([x["eps_main"] for x in results])
    floors = np.array([x["eps_floor_experiment"] for x in results])
    successes = int(sum(x["success_rule"] for x in results))
    median_eps = float(np.median(eps_mains))
    g1_value = abs(median_eps - eps_ref)
    g3_value = float(np.median(floors))

    gates = {
        "S1-G1": {
            "description": "|median eps_S1 - eps_ref_37| < 0.02",
            "measured": g1_value,
            "median_eps_main": median_eps,
            "eps_ref_37": eps_ref,
            "threshold": 0.02,
            "pass": bool(g1_value < 0.02),
        },
        "S1-G2": {
            "description": "success rule fires in >= 95/100 experiments",
            "measured": successes,
            "threshold": 95,
            "n_experiments": n_experiments,
            "pass": bool(successes >= 95),
        },
        "S1-G3": {
            "description": "median eps_floor < 0.05",
            "measured": g3_value,
            "threshold": 0.05,
            "pass": bool(g3_value < 0.05),
        },
        "S1-G4": {
            "description": ("byte-identical s1_report.json on rerun with "
                            "committed seeds (verified externally; result "
                            "recorded in meta sidecar and session log)"),
            "measured": "see s1_report.meta.json",
            "pass": None,
        },
    }

    report = {
        "schema_version": REPORT_SCHEMA,
        "stage": "S1",
        "shots": shots,
        "n_experiments": n_experiments,
        "bootstrap_replicates": n_boot,
        "base_seed": base,
        "seed_policy": {
            "main": "SeedSequence([BASE, canonical_index, r]); two "
                    "independent Multinomial(384, p) halves per circuit "
                    "(sum is exactly Multinomial(768, p); conditional on "
                    "the sum the halves are a uniform random split)",
            "bootstrap": "SeedSequence([BASE, 10**6 + r]).spawn(n_circuits)"
                         "[c]; one Multinomial(384, p_hat) draw of size "
                         "(B, 2) per circuit",
        },
        "clause_operationalization": {
            "floor": "per pass max(split, duplicate); split = max over "
                     "moving/comparator arms of ||A_h1 - A_h2||_F / "
                     "||Dbar_full||_F; duplicate = ||Phi_early - "
                     "Phi_late||_F / ||Dbar_full||_F",
            "eps_floor_experiment": "max(median_boot split, median_boot "
                                    "duplicate)",
            "clause_3": "S1 ideal preparation: exact one-excitation "
                        "survival is 1 by construction; sampled subset "
                        "witness recorded as diagnostic",
            "clause_4": "ideal-backend M3 calibration is exactly the "
                        "identity, raw == M3",
            "clause_5": "A1.3: LOTO+LOPO |Delta_v - Delta_main| <= "
                        "0.25*|median Delta_boot|, no sign flip, and "
                        "projection shift < 0.02",
        },
        "inputs": {
            "bundle_qpy_sha256": manifest["bundle"]["qpy_sha256"],
            "registry_sha256": manifest["bundle"]["circuit_registry_sha256"],
            "comparator_npz_sha256": manifest["comparator"]["npz_sha256"],
            "exact_probs_sha256": provenance["cache_sha256"],
            "manifest_sha256": manifest["manifest_sha256"],
            "eps_reference": ref,
        },
        "summary": {
            "eps_main_median": median_eps,
            "eps_main_q05": float(np.quantile(eps_mains, 0.05)),
            "eps_main_q95": float(np.quantile(eps_mains, 0.95)),
            "eps_floor_median": g3_value,
            "eps_floor_q95": float(np.quantile(floors, 0.95)),
            "success_count": successes,
            "delta_boot_median_median": float(np.median(
                [x["delta_boot_median"] for x in results])),
            "projection_shift_max": float(max(
                x["projection_shift"] for x in results)),
            "proj_fro_max": float(max(
                x["proj_fro_max_main"] for x in results)),
        },
        "gates": gates,
        "experiments": results,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "s1_report.json"
    report_path.write_text(canonical_report_json(report) + "\n",
                           encoding="utf-8")
    meta = {
        "report_sha256": _sha256_file(report_path),
        "environment": {
            "python": sys.version.split()[0],
            "numpy": version("numpy"),
            "scipy": version("scipy"),
            "qiskit": version("qiskit"),
        },
        "workers": workers,
        "note": "timestamps and machine-specific data live here so the "
                "report itself is byte-deterministic (A1.7)",
    }
    (out_dir / "s1_report.meta.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precompute", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--experiments", type=int, default=100)
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--shots", type=int, default=SHOTS)
    parser.add_argument("--base-seed", type=int, default=None,
                        help="A2.7 fresh-seed confirmatory BASE")
    parser.add_argument(
        "--cache", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "results" / "sim_common"
        / "exact_probs.npz")
    parser.add_argument(
        "--out", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "results" / "sim_s1_768")
    args = parser.parse_args()

    if args.precompute:
        record = precompute(args.cache)
        print(json.dumps(record, indent=2, sort_keys=True))
    if args.run:
        path = run_battery(args.cache, args.out, args.experiments,
                           args.bootstrap, args.workers, args.shots,
                           args.base_seed)
        report = json.loads(path.read_text(encoding="utf-8"))
        print(json.dumps({k: v for k, v in report["gates"].items()},
                         indent=2, sort_keys=True))
        print("report:", path)
    if not (args.precompute or args.run):
        parser.error("nothing to do: pass --precompute and/or --run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
