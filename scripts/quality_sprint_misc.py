"""Pre-draft quality sprint: (a) partition-dependence distribution and
(b) N = 14 witness point for the marginal scrambling|integrable pair.

    python scripts/quality_sprint_misc.py partition
    python scripts/quality_sprint_misc.py n14

(a) All 7 groups x 3 manifest runs x 3 random adjacent-pair-set draws x
    8 window times at N = 10 -> distribution behind the 9-20% scope
    wall (was n = 2 runs).
(b) scrambling|integrable at N = 14 (shared H per group: 2 dense eigh):
    {pr_A, w2_mean, xi} for 40 fresh-seeded states/group -> AUC at a
    third size. w2 needs only eigenbasis coefficients
    (|<psi(t0)|psi(t)>|^2 = |sum p_n e^{-i E_n dt}|^2), so no state
    evolution is required.

Outputs: results/AR-010/quality_sprint_partition.json / _n14.json
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import (mutual_information_matrix,        # noqa: E402
                          phi_distance_matrix)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, tfim, xx_chain, xxz_disordered)
from ideg.states import (all_up, ground_state,              # noqa: E402
                         haar_product_state, magnon_superposition, neel)
from ideg.stats import auc                                  # noqa: E402
from ideg.witnesses import _binned_pr, _level_starts        # noqa: E402

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
MODE = sys.argv[1]
t0 = time.time()

if MODE == "partition":
    N = 10
    WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)
    SAMPLE = WINDOW[:: len(WINDOW) // 8][:8]
    GROUPS = ["TA_i_fixed_point", "TA_ii_quasiperiodic", "TA_iii_chaotic",
              "TA_iv_metastable", "TC_scrambling", "TC_integrable",
              "TC_localized"]

    def build(group, seed, run_idx):
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

    def two_site_u(rng):
        m = rng.normal(size=(4, 4)) + 1.0j * rng.normal(size=(4, 4))
        q, r = np.linalg.qr(m)
        return q * (np.diag(r) / np.abs(np.diag(r)))[None, :].conj()

    def apply_pair(psi, i, u4):
        t = psi.reshape([2] * N)
        t = np.moveaxis(t, (i, i + 1), (0, 1)).reshape(4, -1)
        t = (u4 @ t).reshape([2, 2] + [2] * (N - 2))
        return np.moveaxis(t, (0, 1), (i, i + 1)).ravel()

    rng = np.random.default_rng(20260817)
    pair_sets = [[(1, 2), (4, 5), (7, 8)], [(0, 1), (3, 4), (6, 7)],
                 [(2, 3), (5, 6), (8, 9)]]
    out = {"date": "2026-08-13", "n_sites": N, "groups": {}}
    for group in GROUPS:
        seeds = MAN["seeds"][group]["10"][:3]
        devs = []
        for run_idx, seed in enumerate(seeds):
            h, psi0 = build(group, seed, run_idx)
            ev = EigenEvolver(h)
            for pset in pair_sets:
                u4s = [two_site_u(rng) for _ in pset]
                for t in SAMPLE:
                    s = ev.state_at(psi0, float(t))
                    d0 = phi_distance_matrix(
                        mutual_information_matrix(s, N))
                    s2 = s
                    for (i, _), u4 in zip(pset, u4s):
                        s2 = apply_pair(s2, i, u4)
                    d2 = phi_distance_matrix(
                        mutual_information_matrix(s2, N))
                    devs.append(float(np.linalg.norm(d2 - d0)
                                      / np.linalg.norm(d0)))
        out["groups"][group] = {
            "n_samples": len(devs), "mean": float(np.mean(devs)),
            "p10": float(np.percentile(devs, 10)),
            "p90": float(np.percentile(devs, 90)),
            "max": float(np.max(devs))}
        print(f"[{time.time() - t0:7.1f}s] {group}: "
              f"mean {out['groups'][group]['mean']:.3f}", flush=True)
    with open(OUT / "quality_sprint_partition.json", "w") as f:
        json.dump(out, f, indent=2)
    print("done")

elif MODE == "n14":
    N = 14
    SEED = 20260818
    N_STATES = 40
    WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)
    out = {"date": "2026-08-13", "n_sites": N, "seed": SEED,
           "n_states": N_STATES,
           "note": "descriptive third-size point for the marginal "
                   "scrambling|integrable pair; fresh in-script seeds",
           "groups": {}}
    vals = {}
    for group, hbuild in [("scrambling", mixed_field_ising),
                          ("integrable", xx_chain)]:
        h = hbuild(N)
        print(f"[{time.time() - t0:7.1f}s] eigh {group} start", flush=True)
        evals, evecs = np.linalg.eigh(h)
        print(f"[{time.time() - t0:7.1f}s] eigh {group} done", flush=True)
        labels = _level_starts(evals)
        rng = np.random.default_rng(SEED if group == "scrambling"
                                    else SEED + 1)
        recs = []
        for k in range(N_STATES):
            psi = neel(N) if k == 0 else haar_product_state(N, rng)
            c = evecs.T @ psi
            p = np.abs(c) ** 2
            span = float(evals[-1] - evals[0])
            keep = p > 1e-12
            pk, ek = p[keep], evals[keep]
            n_bins = int(round(span / 1e-3)) + 2
            pr = _binned_pr(lambda i0, i1: np.abs(ek[i0:i1, None]
                                                  - ek[None, :]),
                            pk, 1e-3, n_bins)
            # w2 from coefficients alone
            dt = WINDOW - WINDOW[0]
            ov = np.abs(np.exp(-1.0j * np.outer(dt, evals)) @ p) ** 2
            w2_mean = float(np.mean(1.0 - ov))
            xi = float(1.0 - np.sum(np.bincount(labels, weights=p) ** 2))
            recs.append({"pr_A": pr, "w2_mean": w2_mean, "xi": xi})
            if k % 10 == 0:
                print(f"[{time.time() - t0:7.1f}s] {group} state {k}",
                      flush=True)
        out["groups"][group] = recs
        vals[group] = recs
    aucs = {s: auc(np.array([r[s] for r in vals["scrambling"]]),
                   np.array([r[s] for r in vals["integrable"]]))
            for s in ("pr_A", "w2_mean", "xi")}
    out["auc_scrambling_vs_integrable"] = aucs
    with open(OUT / "quality_sprint_n14.json", "w") as f:
        json.dump(out, f, indent=2)
    print("done", {k: round(v, 4) for k, v in aucs.items()})
