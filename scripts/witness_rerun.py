"""Amendment-4 criterion-(a) re-adjudication runs (witness-only, fresh
seeds from confirmatory_manifest_addendum2.json).

    python scripts/witness_rerun.py <group> <n_sites>

Writes results/AR-010/confirmatory/rerun_<group>_N<n>.json. Computes
{pr_A, w2_mean, xi} (+ w2_min descriptively) per run — no Phi, no OTOC,
no protocols.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, tfim, xx_chain, xxz_disordered)
from ideg.states import (all_up, ground_state,              # noqa: E402
                         haar_product_state, magnon_superposition, neel)
from ideg.witnesses import (bohr_measure_pr,                # noqa: E402
                            recurrence_distance, xi_offdiagonal_pure)

import os                                                   # noqa: E402
OUT = ROOT / "results" / "AR-010"
CONF = OUT / "confirmatory"
ADD2 = json.loads(Path(os.environ.get(
    "IDEG_ADDENDUM",
    OUT / "confirmatory_manifest_addendum2.json")).read_text())
PREFIX = ADD2.get("output_prefix", "rerun_")

GROUP = sys.argv[1]
N = int(sys.argv[2])
SEEDS = ADD2["seeds"][GROUP][str(N)]
WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)


def build(group, seed, run_idx, rng):
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
        h = xxz_disordered(N, rng)
        return h, [neel(N)] + [haar_product_state(N, rng) for _ in range(4)]
    raise ValueError(group)


results = {"group": GROUP, "n_sites": N,
           "manifest": "confirmatory_manifest_addendum2.json", "runs": []}
t0 = time.time()
for run_idx, seed in enumerate(SEEDS):
    rng = np.random.default_rng(seed)
    h, psis = build(GROUP, seed, run_idx, rng)
    ev = EigenEvolver(h)
    states_rec = []
    for psi0 in psis:
        w2 = recurrence_distance(ev.states_at(psi0, WINDOW))
        states_rec.append({
            "pr_A": bohr_measure_pr(ev, psi0),
            "w2_mean": float(np.mean(w2)),
            "w2_min": float(np.min(w2)),
            "xi": xi_offdiagonal_pure(ev, psi0),
        })
    results["runs"].append({"seed": seed, "states": states_rec})
    print(f"[{time.time() - t0:7.1f}s] {GROUP} N={N} run {run_idx} done",
          flush=True)

results["_runtime_s"] = round(time.time() - t0, 1)
outpath = CONF / f"rerun_{GROUP}_N{N}.json"
with open(outpath, "w") as f:
    json.dump(results, f, indent=2)
print(f"done: {outpath} ({results['_runtime_s']}s)")
