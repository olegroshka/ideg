"""Pre-draft quality sprint, T-B items (descriptive extensions; no
preregistered verdict touched; seeds = the committed TB manifest seeds,
paired design preserved).

    python scripts/quality_sprint_tb.py

(1) Rigidity-curve completion: eps in {0.25, 0.30, 0.35, 0.40, 0.45,
    0.50} appended to the manifest grid — locate eps_c instead of the
    bound.
(2) Long-window run: DTC eps = 0.03 and r2 to 2000 periods; W5 in
    sliding 180-period windows -> does the r2 prethermal plateau end?

Output: results/AR-010/quality_sprint_tb.json
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import floquet_states                      # noqa: E402
from ideg.models import floquet_dtc                         # noqa: E402
from ideg.pauli import sz_diag                              # noqa: E402
from ideg.states import z_product_state                     # noqa: E402
from ideg.witnesses import subharmonic_peak                 # noqa: E402

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
TB = MAN["TB"]
N = TB["n_sites"]
SEEDS = MAN["seeds"]["TB"]["10"]
ZD = np.array([sz_diag(N, i) for i in range(N)])
EPS_EXT = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
LONG_PERIODS = 2000
WIN = 180          # sliding W5 window length (even; Nyquist-exact)
WIN_STARTS = [20, 500, 1000, 1500, LONG_PERIODS - WIN]


def build(seed, eps, regime="dtc"):
    rng = np.random.default_rng(seed)
    u_f, h2 = floquet_dtc(N, eps=eps, rng=rng,
                          interactions=True,
                          disorder=(regime != "r2_no_disorder"))
    psis = [z_product_state(N, rng)
            for _ in range(TB["states_per_realization"])]
    return u_f, psis


def mags_of(states):
    return np.array([[float(np.sum(z * np.abs(s) ** 2)) for z in ZD]
                     for s in states])


t0 = time.time()
out = {"date": "2026-08-13", "note": "descriptive extensions; paired "
       "manifest seeds; no preregistered verdict touched"}

# (1) rigidity extension
curve = {str(e): [] for e in EPS_EXT}
for seed in SEEDS:
    for eps in EPS_EXT:
        u_f, psis = build(seed, eps)
        peaks = [subharmonic_peak(mags_of(
            floquet_states(u_f, p, 200)[21:201])) for p in psis]
        curve[str(eps)].append(float(np.mean(peaks)))
    print(f"[{time.time() - t0:7.1f}s] rigidity-ext seed {seed} done",
          flush=True)
out["rigidity_extension"] = {
    e: {"mean": float(np.mean(v)), "min": float(np.min(v)),
        "max": float(np.max(v))} for e, v in curve.items()}

# (2) long-window prethermal check
long_out = {}
for regime in ("dtc", "r2_no_disorder"):
    per_window = {str(w0): [] for w0 in WIN_STARTS}
    for seed in SEEDS:
        u_f, psis = build(seed, 0.03, regime)
        for psi0 in psis:
            traj = floquet_states(u_f, psi0, LONG_PERIODS)
            for w0 in WIN_STARTS:
                per_window[str(w0)].append(subharmonic_peak(
                    mags_of(traj[w0 + 1:w0 + 1 + WIN])))
        print(f"[{time.time() - t0:7.1f}s] long {regime} seed {seed} done",
              flush=True)
    long_out[regime] = {w0: {"w5_mean": float(np.mean(v)),
                             "w5_min": float(np.min(v))}
                        for w0, v in per_window.items()}
out["long_window"] = {"periods": LONG_PERIODS, "window": WIN,
                      "starts": WIN_STARTS, "regimes": long_out}

with open(OUT / "quality_sprint_tb.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"done ({time.time() - t0:.1f}s)")
print(json.dumps(out["rigidity_extension"], indent=1))
for r, v in long_out.items():
    print(r, {k: round(x["w5_mean"], 3) for k, x in v.items()})
