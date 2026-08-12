"""AR-010 confirmatory runs, T-A / T-C (spec §4, §5.1, §5.2, §5.3).

Reads the committed confirmatory manifest and runs ONE (group, size) unit:

    python scripts/confirmatory.py <group> <n_sites>

writing results/AR-010/confirmatory/<group>_N<n>.json. T-B lives in
scripts/confirmatory_tb.py. Executing this script on manifest seeds is a
confirmatory run: it closes the AR-019 instrument-upgrade window.
"""

import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.battery import run_battery                        # noqa: E402
from ideg.evolve import DephasingEvolver, EigenEvolver      # noqa: E402
from ideg.migraph import (above_cap_mask, delta_phi,        # noqa: E402
                          delta_phi_subgraph,
                          mutual_information_matrix,
                          phi_distance_matrix, phi_series)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, tfim, xx_chain, xxz_disordered)
from ideg.protocols import (comparator_quench_stream,       # noqa: E402
                            diagonal_ensemble, log_rho_effect, quench_run,
                            restrict_reference, retention_r,
                            subsystem_loss_series)
from ideg.states import (all_up, ground_state,              # noqa: E402
                         haar_product_state, magnon_superposition, neel)
from ideg.stats import slope_block_bootstrap                # noqa: E402
from ideg.witnesses import (bohr_measure_pr, otoc_series,   # noqa: E402
                            recurrence_distance, xi_offdiagonal_pure,
                            xi_offdiagonal_rho)

# IDEG_MANIFEST / IDEG_CONF_OUT: scratch overrides for smoke tests only;
# confirmatory runs use the committed defaults
import os                                                   # noqa: E402
OUT = ROOT / "results" / "AR-010"
CONF = Path(os.environ.get("IDEG_CONF_OUT", OUT / "confirmatory"))
CONF.mkdir(parents=True, exist_ok=True)
MAN = json.loads(Path(os.environ.get(
    "IDEG_MANIFEST", OUT / "confirmatory_manifest.json")).read_text())

GROUP = sys.argv[1]
N = int(sys.argv[2])

T_EQ, T_END, DT = (MAN["window"]["t_eq"], MAN["window"]["t_end"],
                   MAN["window"]["dt_sample"])
T_P = MAN["t_p"]
EPS_PHI = MAN["epsilon_phi"]
FLOOR = MAN["delta_floor"]
LAM = MAN["lambda"]
GAM = MAN["gamma"]
WINDOW = np.arange(T_EQ, T_END + 1e-9, DT)
POST = np.arange(DT, T_END - T_P + 1e-9, DT)       # offsets after t_p
POST_MASK = WINDOW > T_P
LASTQ_MASK = WINDOW >= T_END - (T_END - T_EQ) / 4  # last quarter of the window
OTOC_TIMES = np.arange(0.0, T_END + 1e-9, DT)
DEPH_DT = MAN["dephasing_impl"]["dt_step"]
DEPH_STRIDE = MAN["dephasing_impl"]["phi_sample_stride_steps"]
COMP_STRIDE = MAN["comparator_quench_stride_steps"]
I0_SITE = N // 2
R_MAX = N - 1 - I0_SITE

SEEDS = MAN["seeds"][GROUP][str(N)]
DO_DEPHASING = N <= 10
DO_COMPARATOR = N == MAN.get("comparator_size", 10)

NONADJ_PAIRS = [(i, j) for i, j in combinations(range(N), 2) if j - i > 1]


def build_base(group, seed, run_idx, rng):
    """(H, list of psi0) for one run unit. Clean groups: one state.
    TC_localized: one realization, 5 states (state 0 = Neel)."""
    if group == "TA_i_fixed_point":
        h = tfim(N, g=1.5)
        return h, [ground_state(h)]
    if group == "TA_ii_quasiperiodic":
        psi, _ = magnon_superposition(N, rng)
        return xx_chain(N), [psi]
    if group == "TA_iii_chaotic":
        return mixed_field_ising(N), [haar_product_state(N, rng)]
    if group == "TA_iv_metastable":
        dg = rng.uniform(-0.01, 0.01, size=N)
        return ferro_ising_weak_tf(N, g=0.05, dg=dg), [all_up(N)]
    if group == "TC_scrambling":
        psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
        return mixed_field_ising(N), [psi]
    if group == "TC_integrable":
        psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
        return xx_chain(N), [psi]
    if group == "TC_localized":
        h = xxz_disordered(N, rng)  # fields drawn first (manifest order)
        states = [neel(N)] + [haar_product_state(N, rng) for _ in range(4)]
        return h, states
    raise ValueError(group)


PERT_EV_CACHE = {}


def pert_evolver(h, site, cache_key):
    """EigenEvolver of H + lam Z_site, cached where H is shared."""
    from ideg.pauli import sz_diag
    key = (cache_key, site)
    if key not in PERT_EV_CACHE:
        PERT_EV_CACHE[key] = EigenEvolver(h + np.diag(LAM * sz_diag(N, site)))
    if cache_key is None:
        return PERT_EV_CACHE.pop(key)
    return PERT_EV_CACHE[key]


def measure_state(ev, h, psi0, site, lost, share_key, slope_rng,
                  full_otoc=False):
    """All per-state confirmatory measurements (witnesses, baseline,
    protocols, comparator)."""
    states = ev.states_at(psi0, WINDOW)
    d_series = phi_series(states, N)
    delta, dbar = delta_phi(d_series)
    mi_bar = np.mean([mutual_information_matrix(s, N) for s in states],
                     axis=0)
    cap_mask = above_cap_mask(mi_bar)
    delta_sub = delta_phi_subgraph(d_series, dbar, cap_mask)
    max_unpert_post = float(np.max(delta[POST_MASK]))
    slope, slo, shi = slope_block_bootstrap(
        WINDOW, delta, block_len=MAN["slope_bootstrap"]["block_len_samples"],
        n_resamples=MAN["slope_bootstrap"]["n_resamples"], rng=slope_rng)

    w2 = recurrence_distance(states)
    rs = list(range(1, R_MAX + 1)) if full_otoc else [R_MAX]
    c = otoc_series(ev, psi0, N, I0_SITE, [I0_SITE + r for r in rs],
                    OTOC_TIMES)
    otoc_window = np.isin(np.round(OTOC_TIMES, 6), np.round(WINDOW, 6))
    cw = c[:, otoc_window]  # columns aligned to WINDOW (361 samples)
    c_main = c[-1]  # r_max row over the full time range
    above = np.nonzero(c_main >= 0.1)[0]
    t_star = float(OTOC_TIMES[above[0]]) if len(above) else np.inf

    rec = {
        "baseline": {
            "max_delta_phi": float(np.max(delta)),
            "max_delta_phi_post": max_unpert_post,
            "stationary": bool(np.max(delta) < EPS_PHI),
            "drift_slope": slope, "drift_slope_ci": [slo, shi],
            "cap_max_delta_phi_subgraph": float(np.max(delta_sub)),
            "cap_above_fraction": float(np.mean(cap_mask[
                np.triu_indices(N, 1)])),
            "norm_drift": abs(float(np.linalg.norm(states[-1])) - 1.0),
        },
        "witnesses": {
            "pr_A": bohr_measure_pr(ev, psi0),
            "w2_min": float(np.min(w2)), "w2_mean": float(np.mean(w2)),
            "otoc_c_sat": float(np.mean(cw[-1][LASTQ_MASK])),
            "otoc_t_star": t_star,
            "xi": xi_offdiagonal_pure(ev, psi0),
        },
        "protocols": {},
    }
    if full_otoc:
        rec["otoc_profile"] = {
            "r": rs,
            "c_sat": [float(np.mean(cw[k][LASTQ_MASK]))
                      for k in range(len(rs))],
        }

    # --- protocol 1: quench ---
    ev_p = pert_evolver(h, site, share_key)
    psi_tp = ev.state_at(psi0, T_P)
    post_states = ev_p.states_at(psi_tp, POST)
    dp, _ = delta_phi(phi_series(post_states, N), d_ref=dbar)
    mx = float(np.max(dp))
    rec["protocols"]["quench"] = {
        "site": site, "max_delta_phi_pert": mx,
        "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
        "retention_R": retention_r(mx, max_unpert_post),
        "fails_stationarity": bool(mx > EPS_PHI),
    }

    # --- protocol 2: dephasing (N <= 10, spec §6.2) ---
    if DO_DEPHASING:
        rho = np.outer(psi_tp, psi_tp.conj())
        deph = DephasingEvolver(h, N, GAM, dt=DEPH_DT)
        n_steps = int(round((T_END - T_P) / DEPH_DT))
        deltas = []
        tr_drift = 0.0
        for _, r in deph.run(rho, n_steps, sample_every=DEPH_STRIDE):
            d = phi_distance_matrix(mutual_information_matrix(r, N,
                                                              mixed=True))
            deltas.append(float(np.linalg.norm(d - dbar)
                                / np.linalg.norm(dbar)))
            tr_drift = abs(float(np.trace(r).real) - 1.0)
        mx = float(np.max(deltas))
        rec["protocols"]["dephasing"] = {
            "max_delta_phi_pert": mx,
            "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
            "retention_R": retention_r(mx, max_unpert_post),
            "fails_stationarity": bool(mx > EPS_PHI),
            "trace_drift": tr_drift,
        }

    # --- protocol 3: subsystem loss ---
    d_red, keep = subsystem_loss_series(states[POST_MASK], N, lost)
    d_ref_red = restrict_reference(mi_bar, keep)
    denom = np.linalg.norm(d_ref_red)
    dl = np.array([np.linalg.norm(d - d_ref_red) / denom for d in d_red])
    mx = float(np.max(dl))
    rec["protocols"]["loss"] = {
        "lost": list(lost), "max_delta_phi_pert": mx,
        "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
        "retention_R": retention_r(mx, max_unpert_post),
        "fails_stationarity": bool(mx > EPS_PHI),
    }

    # --- §4.1 comparator / §4.2 switch-off (N = 10; one computation serves
    # both — dephasing psi(t_off) in the H eigenbasis IS rho_bar) ---
    if DO_COMPARATOR:
        rho_bar = diagonal_ensemble(ev, psi0)
        mi_rho = mutual_information_matrix(rho_bar, N, mixed=True)
        d_rho = phi_distance_matrix(mi_rho)
        comp = {
            "xi_rho_bar": xi_offdiagonal_rho(ev, rho_bar),
            "switchoff_delta_vs_run": float(np.linalg.norm(d_rho - dbar)
                                            / np.linalg.norm(dbar)),
            "protocols": {},
        }
        denom_rho = np.linalg.norm(d_rho)

        deltas = []
        for _, r in comparator_quench_stream(h, rho_bar, LAM, site, N,
                                             POST[COMP_STRIDE - 1::
                                                  COMP_STRIDE]):
            d = phi_distance_matrix(mutual_information_matrix(r, N,
                                                              mixed=True))
            deltas.append(float(np.linalg.norm(d - d_rho) / denom_rho))
        mx = float(np.max(deltas))
        comp["protocols"]["quench"] = {
            "max_delta_phi_pert": mx,
            "log_rho": log_rho_effect(mx, 0.0, FLOOR),
        }

        deph = DephasingEvolver(h, N, GAM, dt=DEPH_DT)
        n_steps = int(round((T_END - T_P) / DEPH_DT))
        deltas = []
        for _, r in deph.run(rho_bar.astype(complex), n_steps,
                             sample_every=DEPH_STRIDE):
            d = phi_distance_matrix(mutual_information_matrix(r, N,
                                                              mixed=True))
            deltas.append(float(np.linalg.norm(d - d_rho) / denom_rho))
        mx = float(np.max(deltas))
        comp["protocols"]["dephasing"] = {
            "max_delta_phi_pert": mx,
            "log_rho": log_rho_effect(mx, 0.0, FLOOR),
        }

        d_red_c, keep_c = subsystem_loss_series([rho_bar], N, lost,
                                                mixed=True)
        d_ref_red_c = restrict_reference(mi_rho, keep_c)
        mx = float(np.linalg.norm(d_red_c[0] - d_ref_red_c)
                   / np.linalg.norm(d_ref_red_c))
        comp["protocols"]["loss"] = {
            "max_delta_phi_pert": mx,
            "log_rho": log_rho_effect(mx, 0.0, FLOOR),
        }
        rec["comparator"] = comp

    return rec


results = {"group": GROUP, "n_sites": N,
           "manifest": "confirmatory_manifest.json", "runs": []}
t0 = time.time()

for run_idx, seed in enumerate(SEEDS):
    rng = np.random.default_rng(seed)
    h, psis = build_base(GROUP, seed, run_idx, rng)
    ev = EigenEvolver(h)
    prot_rng = np.random.default_rng(seed + 7)
    site = int(prot_rng.integers(N))
    lost = NONADJ_PAIRS[int(prot_rng.integers(len(NONADJ_PAIRS)))]
    # H' economy: clean shared-H groups cache by site; per-run H groups don't
    share_key = (GROUP if GROUP in ("TA_ii_quasiperiodic", "TA_iii_chaotic",
                                    "TC_scrambling", "TC_integrable",
                                    "TA_i_fixed_point")
                 else ("real", GROUP, run_idx)
                 if GROUP == "TC_localized" else None)

    run_rec = {"seed": seed, "states": []}
    for s_idx, psi0 in enumerate(psis):
        rec = measure_state(ev, h, psi0, site, lost, share_key,
                            np.random.default_rng(seed + 21 + s_idx),
                            full_otoc=(run_idx == 0 and s_idx == 0))
        run_rec["states"].append(rec)
        print(f"[{time.time() - t0:8.1f}s] {GROUP} N={N} run {run_idx}"
              f" state {s_idx} done", flush=True)
    if GROUP == "TC_localized":
        # drop this realization's cached H' evolver
        PERT_EV_CACHE.pop((("real", GROUP, run_idx), site), None)

    if run_idx == 0:
        bat_rng = np.random.default_rng(seed + MAN["battery"]["seed_offset"])
        bat_times = np.linspace(T_EQ, T_END, MAN["battery"]["n_times"])
        run_rec["battery"] = run_battery(h, psis[0], N, bat_times, bat_rng,
                                         tol=MAN["battery"]["tol"])
        print(f"[{time.time() - t0:8.1f}s] {GROUP} N={N} battery done "
              f"(all_must_pass={run_rec['battery']['all_must_pass']})",
              flush=True)
    results["runs"].append(run_rec)

results["_runtime_s"] = round(time.time() - t0, 1)
outpath = CONF / f"{GROUP}_N{N}.json"
with open(outpath, "w") as f:
    json.dump(results, f, indent=2)
print(f"done: {outpath} ({results['_runtime_s']}s)")
