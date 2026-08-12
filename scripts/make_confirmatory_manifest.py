"""Fix the AR-010 CONFIRMATORY run manifest (seeds, sizes, ensembles, all
implementation parameters) BEFORE execution, per spec §6.2.

Deterministic; commit the output, then run scripts/confirmatory.py.
The first confirmatory execution closes the AR-019 instrument-upgrade
window (spec §8, AR-019 outcome entry).
"""

import json
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results" / "AR-010"
OUT.mkdir(parents=True, exist_ok=True)

MASTER_SEED = 20260812

# group -> (sizes, runs per size). TC_localized runs are realizations
# (5 initial states each, spec §6.1); TA_i is the single deterministic
# ground-state run (spec §1: 20 identical runs collapse to 1).
GROUPS = {
    "TA_i_fixed_point": ([8, 10], 1),
    "TA_ii_quasiperiodic": ([8, 10], 20),
    "TA_iii_chaotic": ([8, 10], 20),
    "TA_iv_metastable": ([8, 10], 20),
    "TC_scrambling": ([8, 10, 12], 20),
    "TC_integrable": ([8, 10, 12], 20),
    "TC_localized": ([8, 10, 12], 20),
}
TB_REALIZATIONS = 20
TB_STATES = 5

ss = np.random.SeedSequence(MASTER_SEED)
seeds = {}
for group, (sizes, runs) in GROUPS.items():
    seeds[group] = {}
    for n in sizes:
        seeds[group][str(n)] = [int(s.generate_state(1)[0])
                                for s in ss.spawn(runs)]
seeds["TB"] = {"10": [int(s.generate_state(1)[0])
                      for s in ss.spawn(TB_REALIZATIONS)]}

manifest = {
    "date_fixed": "2026-08-12",
    "spec": "ar/AR-009_spec.md (§8 Amendments 1-3 + AR-019 no-change entry); "
            "KB-005 v0.6",
    "phase": "CONFIRMATORY (spec §5.1 criterion (a), §5.2 criterion (b), "
             "§5.3 adjudication). Executing this manifest closes the AR-019 "
             "instrument-upgrade window.",
    "window": {"t_eq": 20.0, "t_end": 200.0, "dt_sample": 0.5},
    "t_p": 100.0,
    "epsilon_phi": 0.25,
    "delta_floor": 1e-3,
    "lambda": 0.1,
    "gamma": 0.01,
    "loss_k": 2,
    "sizes": {g: v[0] for g, v in GROUPS.items()} | {"TB": [10]},
    "runs_per_size": {g: v[1] for g, v in GROUPS.items()},
    "size_plan": {
        "TA": "N = 8 and 10 (spec §5.1 budget clause: T-A at N = 12 adds "
              "~20 dense 4096-dim diagonalizations per class for no "
              "criterion gain; the clause licenses (8, 10))",
        "TC": "witnesses + quench + loss at N = 10 and 12 (spec §5.1 "
              "primary); dephasing at N = 8 and 10 (spec §6.2 bounds the "
              "density-matrix protocol at N <= 10, so its two-size "
              "replication uses (8, 10)); N = 8 runs also record witnesses "
              "(reported, not thresholded)",
        "TB": "N = 10 (spec §1)",
    },
    "ensembles": {
        "TA_i_fixed_point": "single deterministic ground-state run; "
                            "exact-value witness treatment (spec §5.1)",
        "TA_ii_quasiperiodic": "20 incommensurate magnon triples",
        "TA_iii_chaotic": "20 Haar product states",
        "TA_iv_metastable": "|all-up>, 20 weak-disorder dressings of H",
        "TC_scrambling": "run 0 = Neel (primary), runs 1-19 Haar product",
        "TC_integrable": "run 0 = Neel (primary), runs 1-19 Haar product",
        "TC_localized": "20 disorder realizations x 5 initial states "
                        "(state 0 = Neel, states 1-4 random product); "
                        "realization = resampling unit (spec §6.1)",
        "TB": "20 disorder realizations x 5 random z-product states; "
              "realization = resampling unit; realizations and states "
              "PAIRED across eps and comparator regimes (same seed -> same "
              "J, h fields and states)",
    },
    "protocol_randomness": "per-run rng seeded seed+7 draws quench site "
                           "then the k=2 non-adjacent loss pair; for "
                           "disordered groups (TC_localized, TB) drawn per "
                           "REALIZATION (shared across its states; H' "
                           "eigendecomposition economy, site is a nuisance "
                           "draw and realization is the resampling unit)",
    "dephasing_impl": {"dt_step": 0.5, "phi_sample_stride_steps": 5,
                       "note": "Trotter split at dt=0.5, Phi sampled every "
                               "2.5 time units (as pilot)"},
    "comparator_quench_stride_steps": 5,
    "otoc": {"i0": "N//2", "r_stat": "r_max = N-1-i0 (spec §5.1 statistics)",
             "times": "0..t_end step 0.5 (t* resolvable pre-window; C_sat "
                      "over last quarter of the window per spec §3)",
             "full_r_profile": "run 0 only (diagnostic figure)"},
    "w1_bin_width": 1e-3,
    "xi_degeneracy_tol": 1e-10,
    "implementation_clarifications": [
        "Xi (W4) sums over ENERGY-DISTINCT eigenpairs (degeneracy grouping "
        "tol 1e-10): required by the spec's own defining property 'Xi > 0 "
        "iff the state moves under H', which fails for label-based m != n "
        "on the degenerate XX spectrum. Session-log delta; exploratory "
        "pilot Xi values for XX-based groups shift slightly.",
        "log rho numerator floored at delta_floor as well as the "
        "denominator: binds only where perturbed drift is exactly zero "
        "(stationary objects under subsystem loss), where the spec formula "
        "is log 0; reads as log rho = 0 ('no effect').",
        "Subsystem-loss drift: perturbed series = reduced-graph Phi of the "
        "post-t_p states vs the reduced reference (shortest paths "
        "recomputed on the surviving subgraph of the unperturbed mean MI); "
        "denominator = the run's full-graph unperturbed post-t_p max drift "
        "(same treatment as protocols 1-2).",
        "Switch-off (§4.2) for T-A/T-C coincides with the §4.1 diagonal "
        "ensemble: dephasing psi(t_off) in the H eigenbasis yields exactly "
        "rho_bar (populations are conserved), so one computation serves "
        "both; reported under both headings.",
        "Comparator (§4.1) fair-perturbation at N = 10 only: the dephasing "
        "protocol is spec-bound to N <= 10 and the comparison is kept "
        "within one size; quench/loss comparator runs included at N = 10. "
        "Comparator drift is measured against the comparator's own "
        "reference geometry Phi[rho_bar].",
        "T-B robustness protocols (quench lambda into H2 from period 100; "
        "dephasing channel per period at gamma in lab-time units, "
        "T_period = 2; loss k = 2) are DESCRIPTIVE: criterion (b) is "
        "preregistered over T-A classes / T-C regimes; T-B's preregistered "
        "instrument is the rigidity curve h_sub(eps). Scope: eps = 0.03 "
        "and r2 only.",
        "Battery (§4.3) identity items: the 1e-10 tolerance binds on the "
        "witness statistics and the MI matrices (the objects the "
        "transforms provably preserve); the Phi-space deviation is "
        "REPORTED alongside, because the preregistered -log weight cap "
        "(x_min = 1e-6) amplifies machine-epsilon MI jitter by up to "
        "1/x_min, giving near-cap classes (metastable) an irreducible "
        "~1e-9 numerical floor in Phi that is not "
        "representation-dependence (measured in the N = 6 smoke test).",
    ],
    "slope_bootstrap": {"block_len_samples": 40, "n_resamples": 1000},
    "battery": {"scope": "run 0 per group x size", "n_times": 8,
                "tol": 1e-10, "seed_offset": 13},
    "criterion_a": {"auc_threshold": 0.95, "min_statistics": 2,
                    "statistics": ["pr_A", "w2_min", "otoc_c_sat",
                                   "otoc_t_star", "xi"],
                    "size_pairs": {"TA": [8, 10], "TC": [10, 12]},
                    "class_i_rule": "exact-value separation (spec §5.1)"},
    "criterion_b": {"effect_threshold_ln": 0.4054651081081644,
                    "bootstrap": "BCa 1000, 95%",
                    "size_pairs": {"quench": {"TA": [8, 10],
                                              "TC": [10, 12]},
                                   "loss": {"TA": [8, 10], "TC": [10, 12]},
                                   "dephasing": {"TA": [8, 10],
                                                 "TC": [8, 10]}}},
    "TB": {
        "n_sites": 10,
        "realizations": TB_REALIZATIONS,
        "states_per_realization": TB_STATES,
        "eps_dtc": [0.03, 0.06, 0.10],
        "eps_curve": [0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.10, 0.12,
                      0.14, 0.16, 0.20],
        "comparator_regimes": {"r1_no_interactions": 0.03,
                               "r2_no_disorder": 0.03},
        "window_periods": [20, 200],
        "n_off": 100,
        "rigidity_note": "h_sub(eps) = mean subharmonic power fraction on "
                         "the window vs eps; eps_c located descriptively "
                         "(measured, not assumed; spec §1 T-B)",
    },
    "master_seed": MASTER_SEED,
    "seeds": seeds,
    "pilot_exclusion": "pilot data (manifest.json seeds, 2026-08-11) are "
                       "excluded from all confirmatory statistics "
                       "(spec §5.2.1)",
    "sanity_checks": "per-size §6.3 checks in sanity_checks.json (N=10, "
                     "2026-08-11) and sanity_checks_N8.json / "
                     "sanity_checks_N12.json (2026-08-12, pre-execution)",
}

with open(OUT / "confirmatory_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"confirmatory manifest written: {OUT / 'confirmatory_manifest.json'}")
sys.exit(0)
