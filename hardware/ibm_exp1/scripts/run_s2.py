"""S2 — noisy end-to-end simulation battery (AR-023a §2, A1.4/A1.8).

Phases:

--prepare [--only fake_a|fake_b|sweep]
    Build per-condition noisy outcome distributions: two Heron-class
    fake backends (A1.4 lexicographic selection, opt-3 no-SWAP
    transpilation onto the best-scored 10-qubit line) and the 3x3
    synthetic sweep (two-qubit depolarizing p2, p1 = p2/10, symmetric
    readout).  One density-matrix simulation per circuit per noise
    source; readout confusion applied analytically (A1.8).  Also caches
    M3 calibration distributions and the exact one-excitation survival
    of every prepared state.

--run --condition <id>
    R-experiment battery at the cached condition, identical machinery
    to S1 plus the M3 branch (per-experiment calibration counts ->
    per-clbit confusion estimates -> inverse applied to counts ->
    identical pipeline).

--report
    Aggregate condition batteries into s2_report.json with gates
    S2-G1..G4, the operating envelope, and the frozen L4 path-quality
    requirement.

No IBM credentials, no network access, no QPU submission.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
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
                      floors_from_slots, hermitize_project_batch,
                      load_bundle, pair_rdms_from_counts, phi_from_mi,
                      zrow_masks)
import s2lib  # noqa: E402
from run_s1 import canonical_report_json, _sha256_file  # noqa: E402

S2_DIR = ROOT / "hardware" / "ibm_exp1" / "results" / "sim_s2"
COND_DIR = S2_DIR / "conditions"
MILDEST = "grid_p2-0.003_ro-0.01"
DRIFT = "drift_ramp"


def condition_order():
    """Frozen condition enumeration; index feeds the seed streams."""
    _, fake_names = s2lib.select_fakes()
    conds = [f"fake_{name}" for name in fake_names]
    for p2 in s2lib.GRID_P2:
        for ro in s2lib.GRID_RO:
            conds.append(f"grid_p2-{p2:g}_ro-{ro:g}")
    conds.append(DRIFT)            # A2.6
    return conds


# ------------------------------------------------------------ prepare

def _load_qpy_circuits():
    from qiskit import qpy

    bundle = ROOT / "hardware" / "ibm_exp1" / "bundle"
    with (bundle / "logical_circuits.qpy").open("rb") as handle:
        return qpy.load(handle)


def _prep_only_circuits():
    """47 unique preparation circuits (37 dynamic + 10 modes), no meas."""
    from circuits import preparation_circuit

    targets = np.load(
        ROOT / "hardware" / "ibm_exp1" / "bundle" / "target_states.npz",
        allow_pickle=False)
    dyn = targets["dynamic_site_amplitudes"]
    modes = targets["one_magnon_modes_site"]
    circuits, labels = [], []
    for t in range(dyn.shape[0]):
        circuits.append(preparation_circuit(
            dyn[t], "xxplusyy", name=f"prep_dynamic_t{t:03d}"))
        labels.append(f"dynamic_t{t:03d}")
    for k in range(modes.shape[1]):
        circuits.append(preparation_circuit(
            modes[:, k], "xxplusyy", name=f"prep_sector_e{k:02d}"))
        labels.append(f"sector_e{k:02d}")
    return circuits, labels


def _survival_for_states(prep_probs: np.ndarray, labels: list[str],
                         index: StateIndex, control_mode: int):
    surv_unique = s2lib.survival_from_probs(prep_probs)
    by_label = dict(zip(labels, surv_unique))
    out = {}
    for state in index.dynamic_ids + index.sector_ids:
        out[state] = float(by_label[state])
    for state in index.control_ids:
        out[state] = float(by_label[f"sector_e{control_mode:02d}"])
    return out


def _write_condition(cond: str, p_noisy, p_cal, survival: dict,
                     provenance: dict):
    cond_dir = COND_DIR / cond
    cond_dir.mkdir(parents=True, exist_ok=True)
    cache = cond_dir / "cache.npz"
    np.savez_compressed(
        cache, p_noisy=p_noisy, p_cal=p_cal,
        survival_values=np.array([survival[k] for k in sorted(survival)]),
    )
    provenance = dict(provenance)
    provenance["survival"] = {k: survival[k] for k in sorted(survival)}
    provenance["cache_sha256"] = s2lib.file_sha256(cache)
    (cond_dir / "provenance.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")


def _calibration_circuits(n_qubits: int = 10):
    from qiskit import QuantumCircuit

    idle = QuantumCircuit(n_qubits, n_qubits, name="cal_zero")
    idle.measure(range(n_qubits), range(n_qubits))
    ones = QuantumCircuit(n_qubits, n_qubits, name="cal_one")
    for q in range(n_qubits):
        ones.x(q)
    ones.measure(range(n_qubits), range(n_qubits))
    return [idle, ones]


def prepare_fake(name: str, index: StateIndex):
    backend = s2lib.get_fake(name)
    line = s2lib.score_paths(backend)
    path = line["path"]
    logical = _load_qpy_circuits()
    transpiled, treport = s2lib.transpile_bundle(
        logical, backend=backend, initial_layout=path)
    noise_no_ro = s2lib.backend_noise_model(backend, readout=False)
    dm_probs = s2lib.dm_probabilities(transpiled, noise_no_ro)
    confusions = None
    # per-clbit physical order from the first circuit (identical family)
    phys_order = s2lib.measured_qubit_order(transpiled[0])
    confusions = s2lib.backend_readout_confusions(backend, phys_order)
    p_noisy = s2lib.apply_confusion(dm_probs, confusions)

    cal_transpiled, _ = s2lib.transpile_bundle(
        _calibration_circuits(), backend=backend, initial_layout=path)
    cal_dm = s2lib.dm_probabilities(cal_transpiled, noise_no_ro)
    p_cal = s2lib.apply_confusion(cal_dm, confusions)

    prep_circuits, labels = _prep_only_circuits()
    prep_transpiled, _ = s2lib.transpile_bundle(
        prep_circuits, backend=backend, initial_layout=path)
    from qiskit_aer import AerSimulator
    prep_probs = np.empty((len(prep_transpiled), N_OUT))
    simulator = AerSimulator(method="density_matrix",
                             noise_model=noise_no_ro)
    for start in range(0, len(prep_transpiled), 32):
        chunk = prep_transpiled[start:start + 32]
        jobs = []
        for circuit in chunk:
            bare = circuit.copy()
            bare.save_probabilities(qubits=path, label="p")
            jobs.append(bare)
        result = simulator.run(jobs).result()
        for offset in range(len(chunk)):
            prep_probs[start + offset] = np.asarray(
                result.data(offset)["p"], dtype=float)

    registry = json.loads(
        (ROOT / "hardware" / "ibm_exp1" / "bundle"
         / "circuit_registry.json").read_text(encoding="utf-8"))
    survival = _survival_for_states(prep_probs, labels, index,
                                    int(registry["control_mode"]))
    provenance = {
        "condition": f"fake_{name}",
        "backend": name,
        "processor_type": dict(backend.processor_type),
        "path": path,
        "path_score": line["score"],
        "paths_scored": line["paths_scored"],
        "score_formula": line["score_formula"],
        "transpile_report": treport,
        "noise_model": "NoiseModel.from_backend(gate_error, thermal_"
                       "relaxation; readout stripped, applied "
                       "analytically per A1.8)",
        "readout_confusions_per_clbit": confusions.tolist(),
        "basis_gates": list(backend.target.operation_names),
    }
    _write_condition(f"fake_{name}", p_noisy, p_cal, survival, provenance)
    return provenance


def prepare_sweep(index: StateIndex):
    from qiskit.transpiler import CouplingMap

    logical = _load_qpy_circuits()
    coupling = CouplingMap.from_line(10)
    transpiled, treport = s2lib.transpile_bundle(
        logical, coupling_map=coupling, basis_gates=s2lib.SWEEP_BASIS,
        initial_layout=list(range(10)))
    cal_transpiled, _ = s2lib.transpile_bundle(
        _calibration_circuits(), coupling_map=coupling,
        basis_gates=s2lib.SWEEP_BASIS, initial_layout=list(range(10)))
    prep_circuits, labels = _prep_only_circuits()
    prep_transpiled, _ = s2lib.transpile_bundle(
        prep_circuits, coupling_map=coupling,
        basis_gates=s2lib.SWEEP_BASIS, initial_layout=list(range(10)))
    registry = json.loads(
        (ROOT / "hardware" / "ibm_exp1" / "bundle"
         / "circuit_registry.json").read_text(encoding="utf-8"))
    control_mode = int(registry["control_mode"])

    from qiskit_aer import AerSimulator
    for p2 in s2lib.GRID_P2:
        noise = s2lib.sweep_noise_model(p2)
        dm_probs = s2lib.dm_probabilities(transpiled, noise)
        cal_dm = s2lib.dm_probabilities(cal_transpiled, noise)
        simulator = AerSimulator(method="density_matrix",
                                 noise_model=noise)
        prep_probs = np.empty((len(prep_transpiled), N_OUT))
        for start in range(0, len(prep_transpiled), 32):
            chunk = prep_transpiled[start:start + 32]
            jobs = []
            for circuit in chunk:
                bare = circuit.copy()
                bare.save_probabilities(qubits=list(range(10)), label="p")
                jobs.append(bare)
            result = simulator.run(jobs).result()
            for offset in range(len(chunk)):
                prep_probs[start + offset] = np.asarray(
                    result.data(offset)["p"], dtype=float)
        survival = _survival_for_states(prep_probs, labels, index,
                                        control_mode)
        # A2.6 needs the readout-free distributions to build the drift ramp
        level_dir = COND_DIR / "_sweep_levels"
        level_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(level_dir / f"dm_p2-{p2:g}.npz",
                            dm_probs=dm_probs, cal_dm=cal_dm,
                            survival=np.array(
                                [survival[k] for k in sorted(survival)]))
        for ro in s2lib.GRID_RO:
            confusions = s2lib.symmetric_confusions(ro)
            _write_condition(
                f"grid_p2-{p2:g}_ro-{ro:g}",
                s2lib.apply_confusion(dm_probs, confusions),
                s2lib.apply_confusion(cal_dm, confusions),
                survival,
                {
                    "condition": f"grid_p2-{p2:g}_ro-{ro:g}",
                    "noise_model": "depolarizing p2 on cz, p1=p2/10 on "
                                   "sx/x, rz noiseless (virtual), "
                                   "thermal relaxation off",
                    "p2": p2,
                    "p1": p2 / 10.0,
                    "readout_rate": ro,
                    "transpile_report": treport,
                    "coupling": "10-qubit line, trivial layout",
                    "basis_gates": s2lib.SWEEP_BASIS,
                })
    return {"sweep": "done"}


def prepare_drift(index: StateIndex):
    """A2.6: build a condition whose noise ramps across the job.

    Circuit array index equals submission (pub) position, so a
    monotonic ramp in that index is exactly the systematic the
    bracketing early/late control duplicates are designed to straddle.
    Gate error steps through the three cached sweep levels; readout
    error ramps continuously from 1e-2 to 3e-2.  This is the only test
    in S1/S2 of the duplicate-arm floor against a real systematic
    rather than shot noise.
    """
    level_dir = COND_DIR / "_sweep_levels"
    levels = []
    for p2 in s2lib.GRID_P2:
        path = level_dir / f"dm_p2-{p2:g}.npz"
        if not path.exists():
            raise RuntimeError(
                "run --prepare --only sweep first (drift reuses its "
                f"readout-free levels; missing {path.name})")
        levels.append(np.load(path, allow_pickle=False))

    dm_stack = [np.asarray(lv["dm_probs"], dtype=float) for lv in levels]
    n_circ = dm_stack[0].shape[0]
    fraction = np.arange(n_circ) / max(n_circ - 1, 1)
    level_of = np.clip((fraction * len(dm_stack)).astype(int),
                       0, len(dm_stack) - 1)
    readout_of = 0.01 + 0.02 * fraction

    p_noisy = np.empty_like(dm_stack[0])
    for c in range(n_circ):
        confusion = s2lib.symmetric_confusions(float(readout_of[c]))
        p_noisy[c] = s2lib.apply_confusion(dm_stack[level_of[c]][c],
                                           confusion)

    # calibration is taken at the job midpoint, as a real run would
    mid_conf = s2lib.symmetric_confusions(float(0.01 + 0.02 * 0.5))
    p_cal = s2lib.apply_confusion(
        np.asarray(levels[len(levels) // 2]["cal_dm"], dtype=float),
        mid_conf)

    # exact survival follows the gate-error level each state sits at
    registry = json.loads(
        (ROOT / "hardware" / "ibm_exp1" / "bundle"
         / "circuit_registry.json").read_text(encoding="utf-8"))
    control_mode = int(registry["control_mode"])
    survival_by_level = [
        dict(zip(sorted(_state_keys(index)),
                 np.asarray(lv["survival"], dtype=float)))
        for lv in levels]
    survival = {}
    for state in _state_keys(index):
        rows = index.rows_for[state]
        mean_level = int(round(float(level_of[rows].mean())))
        survival[state] = float(
            survival_by_level[mean_level].get(state, 1.0))

    _write_condition(DRIFT, p_noisy, p_cal, survival, {
        "condition": DRIFT,
        "noise_model": "A2.6 drift ramp: gate-error level steps through "
                       "the three cached sweep levels with submission "
                       "position; readout ramps 1e-2 -> 3e-2 linearly",
        "p2_levels": list(s2lib.GRID_P2),
        "readout_start": 0.01,
        "readout_end": 0.03,
        "level_boundaries_fraction": [1 / 3, 2 / 3],
        "calibration_taken_at_fraction": 0.5,
        "control_mode": control_mode,
        "purpose": "exercise the duplicate-control floor against a "
                   "systematic; static conditions cannot do this",
    })
    return {"condition": DRIFT, "circuits": int(n_circ)}


def _state_keys(index: StateIndex):
    return index.dynamic_ids + index.sector_ids + index.control_ids


# ------------------------------------------------------------ battery

_G2: dict = {}


def _init_worker_s2(cond: str, cond_index: int):
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    manifest, registry, basis_rows = load_bundle(ROOT)
    index = StateIndex(registry["circuits"], basis_rows)
    recon_rows = sampling.reconstruction_basis_rows(basis_rows)
    w1, w2 = aggregation_weights(recon_rows)
    z_exc, _ = zrow_masks(recon_rows)
    comparator = np.load(
        ROOT / manifest["comparator"]["npz_path"], allow_pickle=False)
    cache = np.load(COND_DIR / cond / "cache.npz", allow_pickle=False)
    provenance = json.loads(
        (COND_DIR / cond / "provenance.json").read_text(encoding="utf-8"))
    registry_json = json.loads(
        (ROOT / "hardware" / "ibm_exp1" / "bundle"
         / "circuit_registry.json").read_text(encoding="utf-8"))
    _G2.update(
        control_mode=int(registry_json["control_mode"]),
        manifest=manifest, index=index, w1=w1, w2=w2, z_exc=z_exc,
        p_star=np.asarray(comparator["p_star"], dtype=float),
        probs=np.asarray(cache["p_noisy"], dtype=float),
        p_cal=np.asarray(cache["p_cal"], dtype=float),
        survival=provenance["survival"],
        eps_ref=float(manifest["s1_reference"]["eps_sector_37"]),
        base=int(manifest["seeds"]["noisy_sampler_seed"]),
        cond=cond, cond_index=cond_index)


def run_s2_experiment(r: int, n_boot: int, shots: int = SHOTS) -> dict:
    index: StateIndex = _G2["index"]
    probs = _G2["probs"]
    base, cond_index = _G2["base"], _G2["cond_index"]
    w1, w2, z_exc, p_star = (_G2["w1"], _G2["w2"], _G2["z_exc"],
                             _G2["p_star"])
    survival = _G2["survival"]
    half_shots = shots // 2
    n_circ = len(probs)
    canonical = index.canonical_index

    main_halves = np.empty((n_circ, 2, N_OUT), dtype=np.uint16)
    for c in range(n_circ):
        rng = np.random.default_rng(np.random.SeedSequence(
            [base, cond_index, int(canonical[c]), r]))
        main_halves[c] = rng.multinomial(half_shots, probs[c], size=2)
    main_full = main_halves.sum(axis=1)

    def main_counts(state_id):
        rows = index.rows_for[state_id]
        h = main_halves[rows]
        return np.stack([main_full[rows], h[:, 0], h[:, 1]],
                        axis=0).astype(float)

    main = analyze_pass(main_counts, index, p_star, w1, w2, z_exc,
                        project=True, keep_per_time=True)
    eps_main = float(main["eps"][0])

    # ---- A2.1 endpoint-level floor (identical construction to S1)
    def rdm_stack(state_ids, source):
        out = []
        for state_id in state_ids:
            counts = source[index.rows_for[state_id]].astype(float)
            raw = pair_rdms_from_counts(counts, w1, w2)
            used, _ = hermitize_project_batch(raw, True)
            out.append(used)
        return np.stack(out)

    dyn_f = rdm_stack(index.dynamic_ids, main_full)
    sec_f = rdm_stack(index.sector_ids, main_full)
    ctl_f = rdm_stack(index.control_ids, main_full)
    eps_halves = []
    for h in range(2):
        arm = main_halves[:, h]
        eps_halves.append(sampling.endpoint_from_stacks(
            rdm_stack(index.dynamic_ids, arm),
            rdm_stack(index.sector_ids, arm), p_star)[0])
    eps_ctrl = []
    for c in range(2):
        sec_alt = sec_f.copy()
        sec_alt[int(_G2["control_mode"])] = ctl_f[c]
        eps_ctrl.append(sampling.endpoint_from_stacks(
            dyn_f, sec_alt, p_star)[0])
    floors_main = sampling.endpoint_floor(
        eps_halves[0], eps_halves[1], eps_ctrl[0], eps_ctrl[1])
    duplicate = floors_main["duplicate"]   # systematic: never bootstrapped

    unproj = analyze_pass(main_counts, index, p_star, w1, w2, z_exc,
                          project=False, keep_per_time=False,
                          track_leakage=False)
    projection_shift = abs(eps_main - float(unproj["eps"][0]))

    # per-RDM projection medians for S2-G3 (full pass, slot 0)
    proj_values = []
    for state_id in (index.dynamic_ids + index.sector_ids
                     + index.control_ids):
        rho_raw = pair_rdms_from_counts(main_counts(state_id), w1, w2)
        _, proj_fro = hermitize_project_batch(rho_raw, project=True)
        proj_values.append(proj_fro[0])
    proj_values = np.concatenate(proj_values)
    proj_median = float(np.median(proj_values))
    proj_max = float(np.max(proj_values))

    # ---- M3 branch: per-experiment calibration -> inverse confusion
    cal_root = np.random.SeedSequence([base, cond_index, 5 * 10 ** 6 + r])
    cal_children = cal_root.spawn(2)
    p_cal = _G2["p_cal"]
    cal_counts = np.stack([
        np.random.default_rng(cal_children[k]).multinomial(
            shots, np.clip(p_cal[k], 0.0, None) / p_cal[k].clip(0).sum())
        for k in range(2)])
    confusion_hat = s2lib.estimate_confusions(cal_counts)
    inverses = s2lib.confusion_inverses(confusion_hat)

    def m3_counts(state_id):
        return s2lib.apply_confusion(main_counts(state_id), inverses)

    m3 = analyze_pass(m3_counts, index, p_star, w1, w2, z_exc,
                      project=True, keep_per_time=False,
                      track_leakage=False)
    eps_m3 = float(m3["eps"][0])
    m3_full = s2lib.apply_confusion(main_full.astype(float), inverses)
    m3_h = [s2lib.apply_confusion(main_halves[:, h].astype(float), inverses)
            for h in range(2)]
    eps_m3_halves = [sampling.endpoint_from_stacks(
        rdm_stack(index.dynamic_ids, arm),
        rdm_stack(index.sector_ids, arm), p_star)[0] for arm in m3_h]
    sec_m3 = rdm_stack(index.sector_ids, m3_full)
    dyn_m3 = rdm_stack(index.dynamic_ids, m3_full)
    ctl_m3 = rdm_stack(index.control_ids, m3_full)
    eps_m3_ctrl = []
    for c in range(2):
        alt = sec_m3.copy()
        alt[int(_G2["control_mode"])] = ctl_m3[c]
        eps_m3_ctrl.append(sampling.endpoint_from_stacks(
            dyn_m3, alt, p_star)[0])
    floors_m3 = sampling.endpoint_floor(
        eps_m3_halves[0], eps_m3_halves[1],
        eps_m3_ctrl[0], eps_m3_ctrl[1])
    delta_m3 = eps_m3 - float(floors_m3["floor"])

    # ---- bootstrap (raw branch)
    emp = main_full.astype(float) / shots
    boot_root = np.random.SeedSequence([base, cond_index, 10 ** 6 + r])
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
    # A2.2: bootstrap the split arm; the duplicate arm is a systematic
    eps_floor_exp = float(max(np.median(split_b), duplicate))
    delta_main = eps_main - float(floors_main["floor"])
    delta_median = float(np.median(delta_b))
    ci_low = float(np.quantile(delta_b, 0.025))
    ci_high = float(np.quantile(delta_b, 0.975))

    # ---- clause 5 (A1.3): LOTO / LOPO on the raw main pass
    phi_star_main = main["phi_star"][0]
    phi_t_main = np.stack([p[0] for p in main["phi_t"]], axis=0)
    mi_t_main = np.stack([m_[0] for m_ in main["mi_t"]], axis=0)
    mi_star_main = main["mi_star"][0]
    floor_main_value = float(floors_main["floor"])
    n_t = len(phi_t_main)
    variants = []
    dbar_sum = phi_t_main.sum(axis=0)
    for t in range(n_t):
        dbar_t = (dbar_sum - phi_t_main[t]) / (n_t - 1)
        eps_t = float(np.linalg.norm(phi_star_main - dbar_t)
                      / np.linalg.norm(dbar_t))
        variants.append(eps_t - floor_main_value)
    for k in range(sampling.N_PAIRS):
        stack = np.concatenate([mi_t_main, mi_star_main[None]], axis=0)
        phi_all = phi_from_mi(stack, removed_pair=k)
        dbar_k = phi_all[:n_t].mean(axis=0)
        eps_k = float(np.linalg.norm(phi_all[n_t] - dbar_k)
                      / np.linalg.norm(dbar_k))
        variants.append(eps_k - floor_main_value)
    variants = np.asarray(variants)
    excursion_max = float(np.max(np.abs(variants - delta_main)))
    sign_flip = bool(np.any(np.sign(variants) != np.sign(delta_main)))
    tol_5a = 0.25 * abs(delta_median)

    # A2.5(c): the traffic light uses READOUT-CORRECTED counts; raw
    # ten-qubit survival is scaled by ~(1-p_ro)^10 and would read AMBER
    # (or RED at 3% readout) for a perfectly good state.
    surv_corrected, surv_raw_measured = [], []
    for state_id in index.dynamic_ids + index.sector_ids:
        row = index.leak_row_for.get(state_id)
        if row is None:
            continue
        raw_counts = main_full[row].astype(float)
        surv_raw_measured.append(float(
            sampling.survival_from_allz(raw_counts)))
        corrected = s2lib.apply_confusion(raw_counts, inverses)
        surv_corrected.append(float(sampling.survival_from_allz(
            corrected, project=True)))
    surv_values = (np.array(surv_corrected) if surv_corrected
                   else np.array([survival[k] for k in sorted(survival)]))
    surv_raw_measured = (np.array(surv_raw_measured)
                         if surv_raw_measured else surv_values)
    clause_1 = bool(ci_low > 0.0)
    clause_2 = bool(np.median(eps_b) >= 2.0 * eps_floor_exp)
    clause_3 = bool(surv_values.min() >= 0.70)
    clause_4 = bool(np.sign(delta_m3) == np.sign(delta_main))
    # A2.3 + A2.10: per-RDM MEDIAN correction (the statistic the 0.05
    # threshold was calibrated for); the maximum stays a diagnostic.
    clause_5 = bool(excursion_max <= tol_5a and not sign_flip
                    and proj_median < 0.05)
    success = all([clause_1, clause_2, clause_3, clause_4, clause_5])

    return {
        "experiment": r,
        "eps_main": eps_main,
        "eps_boot_median": float(np.median(eps_b)),
        "eps_m3_main": eps_m3,
        "delta_m3_main": delta_m3,
        "eps_m3_minus_raw": eps_m3 - eps_main,
        "projection_shift": projection_shift,
        "proj_fro_median_main": proj_median,
        "proj_fro_max_main": proj_max,
        "floor_main": floor_main_value,
        "floor_split_main": floors_main["split"],
        "floor_duplicate_main": duplicate,
        "floor_split_boot_median": float(np.median(split_b)),
        "eps_half_1": eps_halves[0],
        "eps_half_2": eps_halves[1],
        "eps_ctrl_early": eps_ctrl[0],
        "eps_ctrl_late": eps_ctrl[1],
        "leakage_survival_corrected_min": float(surv_values.min()),
        "leakage_survival_corrected_median": float(np.median(surv_values)),
        "leakage_survival_raw_min": float(surv_raw_measured.min()),
        "leakage_survival_raw_median": float(np.median(surv_raw_measured)),
        "floor_m3_main": float(floors_m3["floor"]),
        "eps_floor_experiment": eps_floor_exp,
        "delta_main": delta_main,
        "delta_boot_median": delta_median,
        "delta_ci95": [ci_low, ci_high],
        "loto_lopo_excursion_max": excursion_max,
        "loto_lopo_sign_flip": sign_flip,
        "clause_5a_tolerance": float(tol_5a),
        "leakage_witness_min_main": float(
            np.asarray(main["witness_min"])[0]),
        "clauses": {
            "1_delta_ci_above_zero": clause_1,
            "2_eps_ge_2floor": clause_2,
            "3_leakage_not_red": clause_3,
            "4_raw_m3_direction": clause_4,
            "5_no_dominance": clause_5,
        },
        "success_rule": success,
    }


def _worker_s2(args):
    r, n_boot, shots = args
    return run_s2_experiment(r, n_boot, shots)


def run_condition(cond: str, n_experiments: int, n_boot: int,
                  workers: int, shots: int) -> Path:
    conds = condition_order()
    cond_index = conds.index(cond)
    exp_dir = COND_DIR / cond / "experiments"
    exp_dir.mkdir(parents=True, exist_ok=True)
    results: list = [None] * n_experiments
    pending = []
    for r in range(n_experiments):
        record_path = exp_dir / f"exp_{r:03d}.json"
        if record_path.exists():
            results[r] = json.loads(record_path.read_text(encoding="utf-8"))
        else:
            pending.append(r)
    print(f"{cond}: {n_experiments - len(pending)} cached, "
          f"{len(pending)} to run", flush=True)
    if pending:
        from concurrent.futures import as_completed
        with ProcessPoolExecutor(
                max_workers=workers, initializer=_init_worker_s2,
                initargs=(cond, cond_index),
                max_tasks_per_child=1) as pool:
            futures = {pool.submit(_worker_s2, (r, n_boot, shots)): r
                       for r in pending}
            done = 0
            for future in as_completed(futures):
                record = future.result()
                r = record["experiment"]
                results[r] = record
                (exp_dir / f"exp_{r:03d}.json").write_text(
                    canonical_report_json(record) + "\n", encoding="utf-8")
                done += 1
                print(f"{cond} experiment {r} done "
                      f"({done}/{len(pending)} this run)", flush=True)

    provenance = json.loads(
        (COND_DIR / cond / "provenance.json").read_text(encoding="utf-8"))
    surv = np.array(sorted(provenance["survival"].values()))
    report = {
        "condition": cond,
        "condition_index": cond_index,
        "shots": shots,
        "n_experiments": n_experiments,
        "bootstrap_replicates": n_boot,
        "success_count": int(sum(x["success_rule"] for x in results)),
        "survival_median": float(np.median(surv)),
        "survival_min": float(surv.min()),
        "traffic_light": (
            "GREEN" if np.median(surv) >= 0.90 and surv.min() >= 0.80
            else "AMBER" if np.median(surv) >= 0.80
            else "RED"),
        "eps_main_median": float(np.median(
            [x["eps_main"] for x in results])),
        "eps_m3_median": float(np.median(
            [x["eps_m3_main"] for x in results])),
        "delta_median": float(np.median(
            [x["delta_boot_median"] for x in results])),
        "floor_median": float(np.median(
            [x["eps_floor_experiment"] for x in results])),
        "proj_fro_median_of_medians": float(np.median(
            [x["proj_fro_median_main"] for x in results])),
        "projection_shift_median": float(np.median(
            [x["projection_shift"] for x in results])),
        "raw_m3_direction_agree": int(sum(
            x["clauses"]["4_raw_m3_direction"] for x in results)),
        "clause_pass_counts": {
            key: int(sum(x["clauses"][key] for x in results))
            for key in results[0]["clauses"]},
        "experiments": results,
    }
    out = COND_DIR / cond / "battery_report.json"
    out.write_text(canonical_report_json(report) + "\n", encoding="utf-8")
    return out


# ------------------------------------------------------------- report

def traffic_light_from_records(battery: dict) -> dict:
    """A2.5(c): traffic light from M3-CORRECTED measured leakage.

    The per-condition battery_report stores a traffic light computed
    from the simulator's exact survival, which (i) is unavailable on
    hardware and (ii) is blind to readout error.  A2.5(c) requires the
    readout-corrected measured witness.  Both are recomputed here from
    the per-experiment records so every condition is judged uniformly,
    regardless of when its battery ran.
    """
    records = battery["experiments"]
    key_corr = "leakage_survival_corrected_median"
    key_raw = "leakage_survival_raw_median"
    if key_corr not in records[0]:
        return {"traffic_light": battery.get("traffic_light", "UNKNOWN"),
                "basis": "legacy exact survival (pre-A2.5c record)"}
    corr_med = float(np.median([r[key_corr] for r in records]))
    corr_min = float(min(r["leakage_survival_corrected_min"]
                         for r in records))
    raw_med = float(np.median([r[key_raw] for r in records]))
    raw_min = float(min(r["leakage_survival_raw_min"] for r in records))

    def light(median_value, min_value):
        if median_value >= 0.90 and min_value >= 0.80:
            return "GREEN"
        if median_value >= 0.80:
            return "AMBER"
        return "RED"

    return {
        "traffic_light": light(corr_med, corr_min),
        "basis": "A2.5(c) M3-corrected measured all-Z witness",
        "corrected_median": corr_med, "corrected_min": corr_min,
        "raw_median": raw_med, "raw_min": raw_min,
        "raw_traffic_light": light(raw_med, raw_min),
    }


def aggregate_report() -> Path:
    manifest, _, _ = load_bundle(ROOT)
    enumeration, fake_names = s2lib.select_fakes()
    conds = condition_order()
    batteries = {}
    for cond in conds:
        path = COND_DIR / cond / "battery_report.json"
        if path.exists():
            batteries[cond] = json.loads(path.read_text(encoding="utf-8"))
    missing = [c for c in conds if c not in batteries]

    lights = {c: traffic_light_from_records(b)
              for c, b in batteries.items()}

    fake_conds = [f"fake_{n}" for n in fake_names]
    g1_points = fake_conds + [MILDEST]
    g1_pass = all(
        lights[c]["traffic_light"] == "GREEN"
        for c in g1_points if c in batteries) and not any(
        c in missing for c in g1_points)

    def _sc(c):
        return batteries[c]["success_count"] if c in batteries else None

    g2_mildest = _sc(MILDEST)
    g2_fakes = {c: _sc(c) for c in fake_conds}
    g2_pass = (g2_mildest is not None and g2_mildest >= 90
               and any(v is not None and v >= 90
                       for v in g2_fakes.values()))

    op = batteries.get(MILDEST)
    g3_median = op["proj_fro_median_of_medians"] if op else None
    g3_shift = op["projection_shift_median"] if op else None
    # A2.3: the endpoint-shift half of S2-G3 is RETIRED (it penalised
    # the projection for removing bias).  S2-G3 keeps its per-RDM half.
    # The retired form is still computed and reported for the dual record.
    g3_pass = (op is not None and g3_median < 0.05)
    g3_pass_retired_form = (op is not None and g3_median < 0.05
                            and g3_shift < 0.02)
    g4_agree = op["raw_m3_direction_agree"] if op else None
    g4_pass = (op is not None
               and g4_agree >= 0.95 * op["n_experiments"])

    envelope = []
    for cond in conds:
        if cond not in batteries:
            continue
        b = batteries[cond]
        envelope.append({
            "condition": cond,
            "success_count": b["success_count"],
            "delta_median": b["delta_median"],
            "floor_median": b["floor_median"],
            "eps_main_median": b["eps_main_median"],
            "eps_m3_median": b["eps_m3_median"],
            "traffic_light": lights[cond]["traffic_light"],
            "traffic_light_raw": lights[cond].get("raw_traffic_light"),
            "leakage_corrected_median": lights[cond].get("corrected_median"),
            "leakage_raw_median": lights[cond].get("raw_median"),
            "survival_exact_median": b["survival_median"],
        })

    # L4 handoff: strictest grid point where the success rule held >= 90
    passing = [row for row in envelope
               if row["condition"].startswith("grid_")
               and row["success_count"] is not None
               and row["success_count"] >= 90]
    l4 = None
    if passing:
        def _params(cond):
            parts = cond.replace("grid_p2-", "").split("_ro-")
            return float(parts[0]), float(parts[1])
        worst = max(passing, key=lambda row: _params(row["condition"]))
        p2_max, ro_max = _params(worst["condition"])
        l4 = {
            "median_two_qubit_error_max": p2_max,
            "median_readout_error_max": ro_max,
            "statement": (
                f"L4 path-quality requirement (frozen pre-commitment): "
                f"median two-qubit error on the selected path <= "
                f"{p2_max:g} and median readout error <= {ro_max:g}"),
        }

    report = {
        "schema_version": 1,
        "stage": "S2",
        "conditions_expected": conds,
        "conditions_missing": missing,
        "fake_enumeration_a14": enumeration,
        "fake_selection_a14": fake_names,
        "operating_point": MILDEST,
        "gates": {
            "S2-G1": {
                "description": "leakage GREEN on both fakes and mildest "
                               "grid point (median >= 0.90, min >= 0.80)",
                "points": {c: lights[c]["traffic_light"]
                           for c in g1_points if c in batteries},
                "basis": "A2.5(c) M3-corrected measured witness",
                "points_raw_for_contrast": {
                    c: lights[c].get("raw_traffic_light")
                    for c in g1_points if c in batteries},
                "pass": bool(g1_pass),
            },
            "S2-G2": {
                "description": "success rule >= 90/100 at mildest grid "
                               "point and on >= 1 fake backend",
                "mildest": g2_mildest,
                "fakes": g2_fakes,
                "pass": bool(g2_pass),
            },
            "S2-G3": {
                "description": "median per-RDM PSD correction < 0.05 at "
                               "the operating point (A2.3: the "
                               "endpoint-shift half is retired)",
                "proj_fro_median": g3_median,
                "threshold": 0.05,
                "pass": bool(g3_pass),
                "retired_form": {
                    "description": "pre-A2.3: also required "
                                   "projection-attributable endpoint "
                                   "shift < 0.02",
                    "projection_shift_median": g3_shift,
                    "pass": bool(g3_pass_retired_form),
                    "note": "retired because the shift is the projection "
                            "REMOVING estimator bias (+0.0059 projected "
                            "vs +0.1004 unprojected); recorded for the "
                            "dual record, not a gate",
                },
            },
            "S2-G4": {
                "description": "raw and M3 endpoints agree in direction "
                               "of Delta in >= 95% of experiments at the "
                               "operating point",
                "agree_count": g4_agree,
                "pass": bool(g4_pass),
            },
        },
        "envelope": envelope,
        "l4_requirement": l4,
        "inputs": {
            "manifest_sha256": manifest["manifest_sha256"],
            "bundle_qpy_sha256": manifest["bundle"]["qpy_sha256"],
            "comparator_npz_sha256": manifest["comparator"]["npz_sha256"],
        },
    }
    out = S2_DIR / "s2_report.json"
    out.write_text(canonical_report_json(report) + "\n", encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--only", choices=["fake_a", "fake_b",
                                       "sweep", "drift"])
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--condition")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--experiments", type=int, default=100)
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--shots", type=int, default=SHOTS)
    args = parser.parse_args()

    manifest, registry, basis_rows = load_bundle(ROOT)
    index = StateIndex(registry["circuits"], basis_rows)

    if args.prepare:
        _, fake_names = s2lib.select_fakes()
        if args.only in (None, "fake_a"):
            print(json.dumps(prepare_fake(fake_names[0], index),
                             indent=2, sort_keys=True, default=str))
        if args.only in (None, "fake_b"):
            print(json.dumps(prepare_fake(fake_names[1], index),
                             indent=2, sort_keys=True, default=str))
        if args.only in (None, "sweep"):
            print(json.dumps(prepare_sweep(index), indent=2))
        if args.only in (None, "drift"):
            print(json.dumps(prepare_drift(index), indent=2))
    if args.run:
        if not args.condition:
            parser.error("--run requires --condition")
        path = run_condition(args.condition, args.experiments,
                             args.bootstrap, args.workers, args.shots)
        print("battery report:", path)
    if args.report:
        print("s2 report:", aggregate_report())
    if not (args.prepare or args.run or args.report):
        parser.error("nothing to do")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
