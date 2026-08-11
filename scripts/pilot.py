"""AR-010 calibration pilot (spec §5.2.1, EXPLORATORY) — reads the committed
manifest, runs the lambda/gamma grids on T-A + T-C at N = 10, writes
results/AR-010/pilot_results.json.

Per-run outputs: baseline stationarity (max dPhi over the window, drift),
witness snapshot (PR_A, Xi), and for each perturbation strength the primary
log-ratio effect measure, the descriptive retention R, and the exploratory
failure-threshold flags (max dPhi_pert > epsilon_phi)."""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import (delta_phi, mutual_information_matrix,  # noqa: E402
                          phi_distance_matrix, phi_series)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, tfim, xx_chain, xxz_disordered)
from ideg.protocols import (dephasing_run, log_rho_effect,  # noqa: E402
                            quench_run, retention_r)
from ideg.states import (all_up, ground_state,              # noqa: E402
                         haar_product_state, magnon_superposition, neel)
from ideg.witnesses import (bohr_measure_pr,                # noqa: E402
                            xi_offdiagonal_pure)

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "manifest.json").read_text())

N = MAN["n_sites"]
T_EQ, T_END, DT = (MAN["window"]["t_eq"], MAN["window"]["t_end"],
                   MAN["window"]["dt_sample"])
T_P = MAN["t_p"]
EPS_PHI = MAN["epsilon_phi"]
FLOOR = MAN["delta_floor"]
WINDOW = np.arange(T_EQ, T_END + 1e-9, DT)
POST = np.arange(DT, T_END - T_P + 1e-9, DT)  # offsets after t_p
DEPH_DT = MAN["dephasing"]["dt_step"]
DEPH_STRIDE = MAN["dephasing"]["phi_sample_stride_steps"]


def build_run(group: str, seed: int, run_idx: int):
    """Returns (H, psi0) for one pilot run. Run 0 of the T-C clean regimes
    uses the Neel primary state (spec §1 T-C); later runs random product."""
    rng = np.random.default_rng(seed)
    if group == "TA_i_fixed_point":
        h = tfim(N, g=1.5)
        return h, ground_state(h)
    if group == "TA_ii_quasiperiodic":
        psi, _ = magnon_superposition(N, rng)
        return xx_chain(N), psi
    if group == "TA_iii_chaotic":
        return mixed_field_ising(N), haar_product_state(N, rng)
    if group == "TA_iv_metastable":
        dg = rng.uniform(-0.01, 0.01, size=N)
        return ferro_ising_weak_tf(N, g=0.05, dg=dg), all_up(N)
    if group == "TC_scrambling":
        psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
        return mixed_field_ising(N), psi
    if group == "TC_integrable":
        psi = neel(N) if run_idx == 0 else haar_product_state(N, rng)
        return xx_chain(N), psi
    if group == "TC_localized":
        return xxz_disordered(N, rng), neel(N)
    raise ValueError(group)


RUNS = MAN["runs_per_group"]
# optional CLI arg: run a single group (per-group background execution);
# each group writes its own pilot_<group>.json, merged at analysis time
only = sys.argv[1] if len(sys.argv) > 1 else None
groups_to_run = ({only: MAN["group_seeds"][only]} if only
                 else MAN["group_seeds"])
results = {"_manifest": "manifest.json", "groups": {}}
t_start = time.time()

for group, seeds in groups_to_run.items():
    runs_out = []
    for run_idx, seed in enumerate(seeds):
        rng = np.random.default_rng(seed + 7)  # protocol randomness stream
        h, psi0 = build_run(group, seed, run_idx)
        ev = EigenEvolver(h)

        # --- unperturbed baseline over the full window ---
        states = ev.states_at(psi0, WINDOW)
        d_series = phi_series(states, N)
        delta, dbar = delta_phi(d_series)
        post_mask = WINDOW > T_P
        max_unpert_post = float(np.max(delta[post_mask]))
        rec = {
            "seed": seed,
            "baseline": {
                "max_delta_phi": float(np.max(delta)),
                "max_delta_phi_post": max_unpert_post,
                "stationary": bool(np.max(delta) < EPS_PHI),
                "pr_A": bohr_measure_pr(ev, psi0),
                "xi": xi_offdiagonal_pure(ev, psi0),
            },
            "quench": {}, "dephasing": {},
        }

        # --- protocol 1: quench grid ---
        site = int(rng.integers(N))
        rec["quench_site"] = site
        for lam in MAN["lambda_grid"]:
            post_states = quench_run(h, ev, psi0, lam, site, N, T_P, POST)
            d_post = phi_series(post_states, N)
            dp, _ = delta_phi(d_post, d_ref=dbar)
            mx = float(np.max(dp))
            rec["quench"][str(lam)] = {
                "max_delta_phi_pert": mx,
                "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
                "retention_R": retention_r(mx, max_unpert_post),
                "fails_stationarity": bool(mx > EPS_PHI),
            }

        # --- protocol 2: dephasing grid ---
        for gam in MAN["gamma_grid"]:
            deltas = []
            for t, rho in dephasing_run(h, ev, psi0, gam, N, T_P, T_END,
                                        dt=DEPH_DT,
                                        sample_every=DEPH_STRIDE):
                mi = mutual_information_matrix(rho, N, mixed=True)
                d = phi_distance_matrix(mi)
                deltas.append(float(np.linalg.norm(d - dbar)
                                    / np.linalg.norm(dbar)))
            mx = float(np.max(deltas))
            rec["dephasing"][str(gam)] = {
                "max_delta_phi_pert": mx,
                "log_rho": log_rho_effect(mx, max_unpert_post, FLOOR),
                "retention_R": retention_r(mx, max_unpert_post),
                "fails_stationarity": bool(mx > EPS_PHI),
            }

        runs_out.append(rec)
        print(f"[{time.time() - t_start:7.1f}s] {group} run {run_idx} done",
              flush=True)
    results["groups"][group] = runs_out

results["_runtime_s"] = round(time.time() - t_start, 1)
outname = f"pilot_{only}.json" if only else "pilot_results.json"
with open(OUT / outname, "w") as f:
    json.dump(results, f, indent=2)
print(f"\npilot complete in {results['_runtime_s']}s -> {outname}")
