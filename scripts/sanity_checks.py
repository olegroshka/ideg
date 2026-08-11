"""AR-009 §6.3 class-label sanity checks — run BEFORE any pilot/confirmatory
analysis. A failed check stops confirmatory runs for that class (spec §6.3).

Symmetry-sector handling (implementation note, session log): level statistics
are computed inside a single symmetry sector — reflection-even for the
uniform-field Ising models (open chain reflection symmetry would otherwise
mix two independent GOE blocks and depress <r>), Sz = N/2-down sector for
the particle-number-conserving chains."""

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ideg.evolve import floquet_states                      # noqa: E402
from ideg.models import (floquet_dtc, mixed_field_ising,    # noqa: E402
                         xx_chain, xxz_disordered)
from ideg.pauli import (reflection_sector_basis,            # noqa: E402
                        sz_diag, sz_sector_indices)
from ideg.states import z_product_state                     # noqa: E402
from ideg.stats import r_statistic                          # noqa: E402
from ideg.witnesses import subharmonic_peak                 # noqa: E402

N = 10
OUT = Path(__file__).resolve().parent.parent / "results" / "AR-010"
OUT.mkdir(parents=True, exist_ok=True)

GOE_WINDOW = (0.51, 0.55)
POISSON_WINDOW = (0.36, 0.42)
DTC_EPS = 0.03
DTC_REALIZATIONS = 20
DTC_PERIODS = 100
DTC_PEAK_PRESENT = 0.5  # "peak present" = majority of spectral power at w/2
SEED = 20260811

results = {}
t0 = time.time()

# --- (iii)/scrambling: mixed-field Ising, reflection-even sector, GOE ---
h = mixed_field_ising(N)
basis = reflection_sector_basis(N, even=True)
h_even = basis.T @ h @ basis
evals = np.linalg.eigvalsh(h_even)
bulk = evals[len(evals) // 10: -len(evals) // 10]  # drop spectral edges
r_chaotic = r_statistic(bulk)
results["chaotic_mixed_field_ising"] = {
    "r": r_chaotic, "window": GOE_WINDOW,
    "pass": GOE_WINDOW[0] <= r_chaotic <= GOE_WINDOW[1],
    "sector": "reflection-even", "sector_dim": int(h_even.shape[0]),
}

# --- (ii)/integrable: XX chain, free-spectrum reconstruction ---
# (spec §6.3 as amended 2026-08-11, §8 Amendment 2: construction-based
# certificate; the Poisson window is inapplicable to a free model)
from itertools import combinations                          # noqa: E402

h = xx_chain(N)
idx = sz_sector_indices(N, N // 2)
mb = np.sort(np.linalg.eigvalsh(h[np.ix_(idx, idx)]))
hop = np.zeros((N, N))
for i in range(N - 1):
    hop[i, i + 1] = hop[i + 1, i] = 1.0
e1 = np.linalg.eigvalsh(hop)
pred = np.sort([sum(c) for c in combinations(e1, N // 2)])
dev = float(np.max(np.abs(mb - pred)))
results["integrable_xx"] = {
    "free_spectrum_max_dev": dev, "threshold": 1e-8,
    "pass": dev < 1e-8,
    "sector": "Sz=0", "sector_dim": int(len(idx)),
    "certificate": "many-body = subset sums of single-particle (Amendment 2)",
}

# --- localized: XXZ W=8, Sz sector, Poisson (5 realizations) ---
rng = np.random.default_rng(SEED)
rs = []
for _ in range(5):
    h = xxz_disordered(N, rng)
    evals = np.linalg.eigvalsh(h[np.ix_(idx, idx)])
    bulk = evals[len(evals) // 10: -len(evals) // 10]
    rs.append(r_statistic(bulk))
r_mbl = float(np.mean(rs))
results["localized_xxz_W8"] = {
    "r_mean": r_mbl, "r_each": rs, "window": POISSON_WINDOW,
    "pass": POISSON_WINDOW[0] <= r_mbl <= POISSON_WINDOW[1],
    "sector": "Sz=0", "realizations": 5,
}

# --- T-B DTC regime: subharmonic peak at eps = 0.03, >= 18/20 ---
rng = np.random.default_rng(SEED + 1)
zdiags = np.array([sz_diag(N, i) for i in range(N)])
present = 0
peaks = []
for _ in range(DTC_REALIZATIONS):
    u_f, _ = floquet_dtc(N, eps=DTC_EPS, rng=rng)
    psi0 = z_product_state(N, rng)
    traj = floquet_states(u_f, psi0, DTC_PERIODS)[1:]
    mags = np.array([[float(np.sum(z * np.abs(s) ** 2)) for z in zdiags]
                     for s in traj])
    pk = subharmonic_peak(mags)
    peaks.append(pk)
    present += int(pk > DTC_PEAK_PRESENT)
results["dtc_regime_eps0.03"] = {
    "present": present, "of": DTC_REALIZATIONS, "required": 18,
    "pass": present >= 18,
    "peak_mean": float(np.mean(peaks)), "peak_min": float(np.min(peaks)),
    "present_definition": f"subharmonic power fraction > {DTC_PEAK_PRESENT}",
}

results["_meta"] = {
    "N": N, "seed": SEED, "runtime_s": round(time.time() - t0, 1),
    "date": "2026-08-11", "spec": "ar/AR-009_spec.md §6.3",
}

with open(OUT / "sanity_checks.json", "w") as f:
    json.dump(results, f, indent=2)

all_pass = all(v["pass"] for k, v in results.items() if k != "_meta")
print(json.dumps(results, indent=2))
print(f"\nALL PASS: {all_pass}")
sys.exit(0 if all_pass else 1)
