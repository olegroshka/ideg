"""AR-010 confirmatory runs, T-B Floquet/DTC (spec §1 T-B, §3 W5, §4.2).

    python scripts/confirmatory_tb.py main       -> TB_main.json
    python scripts/confirmatory_tb.py protocols  -> TB_protocols.json

main: rigidity curve h_sub(eps) over the manifest eps grid, full witnesses
+ Phi at the three preregistered DTC eps and the r1/r2 comparator regimes,
switch-off at n_off. protocols: DESCRIPTIVE quench/dephasing/loss at the
calibrated strengths (manifest implementation clarification — criterion (b)
is preregistered over T-A classes / T-C regimes).

Implementation notes (recorded here, consistent with the manifest):
- W5 is computed on stroboscopic periods 21..200 (180 samples, even count:
  the rfft Nyquist bin is then the exact period-2T line); Phi and W2 use
  the spec window periods 20..200.
- Switch-off continuation is lab-time evolution under H2 alone, sampled at
  the period boundaries t = 2n (drive removed, clock kept).
- Realizations and initial states are PAIRED across eps and regimes: the
  per-realization rng (manifest seed) draws J, h first (unconditionally,
  see models.floquet_dtc), then the 5 z-product states.
"""

import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import (FloquetDephasingEvolver,           # noqa: E402
                         floquet_states)
from ideg.migraph import (above_cap_mask, delta_phi,        # noqa: E402
                          delta_phi_subgraph,
                          mutual_information_matrix,
                          phi_distance_matrix, phi_series)
from ideg.models import floquet_dtc                         # noqa: E402
from ideg.pauli import sz_diag                              # noqa: E402
from ideg.protocols import (log_rho_effect,                 # noqa: E402
                            restrict_reference, retention_r,
                            subsystem_loss_series)
from ideg.states import z_product_state                     # noqa: E402
from ideg.stats import slope_block_bootstrap                # noqa: E402
from ideg.witnesses import (bohr_measure_pr_floquet,        # noqa: E402
                            floquet_eigenbasis, recurrence_distance,
                            subharmonic_peak,
                            xi_offdiagonal_pure_floquet)

# IDEG_MANIFEST / IDEG_CONF_OUT: scratch overrides for smoke tests only
import os                                                   # noqa: E402
OUT = ROOT / "results" / "AR-010"
CONF = Path(os.environ.get("IDEG_CONF_OUT", OUT / "confirmatory"))
CONF.mkdir(parents=True, exist_ok=True)
MAN = json.loads(Path(os.environ.get(
    "IDEG_MANIFEST", OUT / "confirmatory_manifest.json")).read_text())
TB = MAN["TB"]

STAGE = sys.argv[1]
N = TB["n_sites"]
N0, N1 = TB["window_periods"]          # 20, 200
N_OFF = TB["n_off"]
EPS_PHI = MAN["epsilon_phi"]
FLOOR = MAN["delta_floor"]
LAM = MAN["lambda"]
GAM = MAN["gamma"]
SEEDS = MAN["seeds"]["TB"][str(N)]
ZDIAGS = np.array([sz_diag(N, i) for i in range(N)])
NONADJ_PAIRS = [(i, j) for i, j in combinations(range(N), 2) if j - i > 1]

REGIMES = ([("dtc", e) for e in TB["eps_dtc"]]
           + [("r1_no_interactions", TB["comparator_regimes"]
               ["r1_no_interactions"]),
              ("r2_no_disorder", TB["comparator_regimes"]["r2_no_disorder"])])


def build(seed, eps, regime="dtc"):
    """(u_f, h2, states5) with pairing across eps/regime via seed reset."""
    rng = np.random.default_rng(seed)
    u_f, h2 = floquet_dtc(
        N, eps=eps, rng=rng,
        interactions=(regime != "r1_no_interactions"),
        disorder=(regime != "r2_no_disorder"))
    psis = [z_product_state(N, rng) for _ in range(TB
                                                   ["states_per_realization"])]
    return u_f, h2, psis


def mags_of(states):
    return np.array([[float(np.sum(z * np.abs(s) ** 2)) for z in ZDIAGS]
                     for s in states])


results = {"stage": STAGE, "manifest": "confirmatory_manifest.json"}
t0 = time.time()

if STAGE == "main":
    # --- rigidity curve h_sub(eps): W5 only, all eps, paired ---
    curve = {str(e): [] for e in TB["eps_curve"]}
    for seed in SEEDS:
        for eps in TB["eps_curve"]:
            u_f, _, psis = build(seed, eps)
            peaks = []
            for psi0 in psis:
                traj = floquet_states(u_f, psi0, N1)
                peaks.append(subharmonic_peak(mags_of(traj[N0 + 1:N1 + 1])))
            curve[str(eps)].append(float(np.mean(peaks)))  # realization mean
        print(f"[{time.time() - t0:7.1f}s] curve seed {seed} done",
              flush=True)
    results["rigidity_curve"] = curve

    # --- full witnesses + Phi + switch-off at the regime points ---
    regimes_out = {}
    for regime, eps in REGIMES:
        key = f"{regime}_eps{eps}"
        real_out = []
        for seed in SEEDS:
            u_f, h2, psis = build(seed, eps, regime)
            theta, z = floquet_eigenbasis(u_f)
            ph_off = np.exp(-2.0j * h2)  # H2-alone evolution over one period
            states_rec = []
            for psi0 in psis:
                traj = floquet_states(u_f, psi0, N1)
                win = traj[N0:N1 + 1]
                d_series = phi_series(win, N)
                delta, dbar = delta_phi(d_series)
                mi_bar = np.mean([mutual_information_matrix(s, N)
                                  for s in win], axis=0)
                cap_mask = above_cap_mask(mi_bar)
                periods = np.arange(N0, N1 + 1, dtype=float)
                slope, slo, shi = slope_block_bootstrap(
                    periods, delta,
                    block_len=MAN["slope_bootstrap"]["block_len_samples"],
                    n_resamples=MAN["slope_bootstrap"]["n_resamples"],
                    rng=np.random.default_rng(seed + 21))
                post = delta[periods > N_OFF]
                w2 = recurrence_distance(win)

                # switch-off: H2-alone continuation from period N_OFF
                psi_off = traj[N_OFF].copy()
                off_states = np.empty((N1 - N_OFF, len(psi_off)),
                                      dtype=complex)
                for k in range(N1 - N_OFF):
                    psi_off = ph_off * psi_off
                    off_states[k] = psi_off
                d_off = phi_series(off_states, N)
                delta_off = np.array([
                    float(np.linalg.norm(d - dbar) / np.linalg.norm(dbar))
                    for d in d_off])

                states_rec.append({
                    "baseline": {
                        "max_delta_phi": float(np.max(delta)),
                        "max_delta_phi_post": float(np.max(post)),
                        "stationary": bool(np.max(delta) < EPS_PHI),
                        "drift_slope": slope, "drift_slope_ci": [slo, shi],
                        "cap_max_delta_phi_subgraph": float(np.max(
                            delta_phi_subgraph(d_series, dbar, cap_mask))),
                        "cap_above_fraction": float(np.mean(
                            cap_mask[np.triu_indices(N, 1)])),
                    },
                    "witnesses": {
                        "pr_A": bohr_measure_pr_floquet(theta, z, psi0),
                        "w2_min": float(np.min(w2)),
                        "w2_mean": float(np.mean(w2)),
                        "xi": xi_offdiagonal_pure_floquet(theta, z, psi0),
                        "w5": subharmonic_peak(
                            mags_of(traj[N0 + 1:N1 + 1])),
                    },
                    "switchoff": {
                        "w5_post_on": subharmonic_peak(
                            mags_of(traj[N_OFF + 1:N1 + 1])),
                        "w5_post_off": subharmonic_peak(mags_of(off_states)),
                        "max_delta_phi_off": float(np.max(delta_off)),
                        "mean_delta_phi_off": float(np.mean(delta_off)),
                        "max_delta_phi_post_on": float(np.max(post)),
                    },
                })
            real_out.append({"seed": seed, "states": states_rec})
            print(f"[{time.time() - t0:7.1f}s] {key} seed {seed} done",
                  flush=True)
        regimes_out[key] = real_out
    results["regimes"] = regimes_out

elif STAGE == "protocols":
    # DESCRIPTIVE protocols at eps = 0.03 (DTC) and r2 (thermal comparator)
    prot_out = {}
    for regime, eps in [("dtc", 0.03),
                        ("r2_no_disorder",
                         TB["comparator_regimes"]["r2_no_disorder"])]:
        key = f"{regime}_eps{eps}"
        real_out = []
        for seed in SEEDS:
            u_f, h2, psis = build(seed, eps, regime)
            prot_rng = np.random.default_rng(seed + 7)
            site = int(prot_rng.integers(N))
            lost = NONADJ_PAIRS[int(prot_rng.integers(len(NONADJ_PAIRS)))]
            # quench: H2 -> H2 + lam Z_site from period N_OFF
            u_f_q = np.exp(-1.0j * LAM * sz_diag(N, site))[:, None] * u_f
            states_rec = []
            for psi0 in psis:
                traj = floquet_states(u_f, psi0, N1)
                win = traj[N0:N1 + 1]
                d_series = phi_series(win, N)
                delta, dbar = delta_phi(d_series)
                mi_bar = np.mean([mutual_information_matrix(s, N)
                                  for s in win], axis=0)
                periods = np.arange(N0, N1 + 1, dtype=float)
                max_unpert_post = float(np.max(delta[periods > N_OFF]))
                rec = {"quench_site": site, "lost": list(lost)}

                q_states = floquet_states(u_f_q, traj[N_OFF],
                                          N1 - N_OFF)[1:]
                dq = np.array([float(np.linalg.norm(d - dbar)
                                     / np.linalg.norm(dbar))
                               for d in phi_series(q_states, N)])
                mx = float(np.max(dq))
                rec["quench"] = {
                    "max_delta_phi_pert": mx,
                    "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
                    "retention_R": retention_r(mx, max_unpert_post),
                }

                rho = np.outer(traj[N_OFF], traj[N_OFF].conj())
                deph = FloquetDephasingEvolver(u_f, N, GAM)
                deltas = []
                for _, r in deph.run(rho, N1 - N_OFF, sample_every=5):
                    d = phi_distance_matrix(
                        mutual_information_matrix(r, N, mixed=True))
                    deltas.append(float(np.linalg.norm(d - dbar)
                                        / np.linalg.norm(dbar)))
                mx = float(np.max(deltas))
                rec["dephasing"] = {
                    "max_delta_phi_pert": mx,
                    "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
                    "retention_R": retention_r(mx, max_unpert_post),
                }

                post_mask = periods > N_OFF
                d_red, keep = subsystem_loss_series(win[post_mask], N, lost)
                d_ref_red = restrict_reference(mi_bar, keep)
                denom = np.linalg.norm(d_ref_red)
                dl = np.array([np.linalg.norm(d - d_ref_red) / denom
                               for d in d_red])
                mx = float(np.max(dl))
                rec["loss"] = {
                    "max_delta_phi_pert": mx,
                    "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
                    "retention_R": retention_r(mx, max_unpert_post),
                }
                states_rec.append(rec)
            real_out.append({"seed": seed, "states": states_rec})
            print(f"[{time.time() - t0:7.1f}s] protocols {key} seed {seed} "
                  f"done", flush=True)
        prot_out[key] = real_out
    results["protocols"] = prot_out

else:
    raise ValueError(STAGE)

results["_runtime_s"] = round(time.time() - t0, 1)
outpath = CONF / f"TB_{STAGE}.json"
with open(outpath, "w") as f:
    json.dump(results, f, indent=2)
print(f"done: {outpath} ({results['_runtime_s']}s)")
