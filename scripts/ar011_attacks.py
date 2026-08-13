"""AR-011 adversarial computations B and C (session 2026-08-13).

B: metastable Xi degeneracy-tolerance sensitivity — recompute W4 for the
   TA_iv ensembles at N = 10, 12 under tol in {1e-8, 1e-10, 1e-12}.
   (Attack: does the (i, iv) exact-value separation or the §5.3 check-1
   margin depend on the grouping tolerance?)
C: Phi partition-dependence probe — one representative chaotic and one
   localized run at N = 10; fixed random TWO-SITE (nonlocal, adjacent-pair
   entangling) basis change applied to the state only; Phi recomputed on
   the original site partition. The §4.3 battery proved single-site-frame
   invariance; TH-037's posited-factorization caveat lives HERE.

Usage: python scripts/ar011_attacks.py -> results/AR-010/ar011_attacks.json
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import (mutual_information_matrix,        # noqa: E402
                          phi_distance_matrix)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, xxz_disordered)
from ideg.states import all_up, haar_product_state, neel    # noqa: E402
from ideg.witnesses import xi_offdiagonal_pure              # noqa: E402

OUT = ROOT / "results" / "AR-010"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
ADD = json.loads((OUT / "confirmatory_manifest_addendum1.json").read_text())

out = {"date": "2026-08-13", "session": "AR-011"}

# ---------- B: Xi tolerance sweep, TA_iv ----------
b = {}
for n, seeds in [(10, MAN["seeds"]["TA_iv_metastable"]["10"]),
                 (12, ADD["seeds"]["TA_iv_metastable"]["12"])]:
    per_tol = {"1e-08": [], "1e-10": [], "1e-12": []}
    for seed in seeds:
        rng = np.random.default_rng(seed)
        dg = rng.uniform(-0.01, 0.01, size=n)
        ev = EigenEvolver(ferro_ising_weak_tf(n, g=0.05, dg=dg))
        psi = all_up(n)
        for tol_key, tol in [("1e-08", 1e-8), ("1e-10", 1e-10),
                             ("1e-12", 1e-12)]:
            per_tol[tol_key].append(
                xi_offdiagonal_pure(ev, psi, degeneracy_tol=tol))
        print(f"B: N={n} seed {seed} done", flush=True)
    b[str(n)] = {k: {"min": float(np.min(v)), "max": float(np.max(v)),
                     "mean": float(np.mean(v))} for k, v in per_tol.items()}
out["B_xi_tolerance_sweep"] = b

# ---------- C: nonlocal partition probe, N = 10 ----------
N = 10
WINDOW = np.arange(MAN["window"]["t_eq"], MAN["window"]["t_end"] + 1e-9,
                   MAN["window"]["dt_sample"])
SAMPLE = WINDOW[:: len(WINDOW) // 8][:8]  # 8 representative window times


def two_site_unitary(rng):
    m = rng.normal(size=(4, 4)) + 1.0j * rng.normal(size=(4, 4))
    q, r = np.linalg.qr(m)
    return q * (np.diag(r) / np.abs(np.diag(r)))[None, :].conj()


def apply_pair_unitary(psi, n, i, u4):
    """Apply a 4x4 unitary on adjacent sites (i, i+1)."""
    t = psi.reshape([2] * n)
    t = np.moveaxis(t, (i, i + 1), (0, 1)).reshape(4, -1)
    t = (u4 @ t).reshape([2, 2] + [2] * (n - 2))
    return np.moveaxis(t, (0, 1), (i, i + 1)).ravel()


c = {}
rng = np.random.default_rng(20260813)
pairs = [(1, 2), (4, 5), (7, 8)]  # fixed nonlocal-entangling pair set
u4s = [two_site_unitary(rng) for _ in pairs]
for label, h, psi0 in [
        ("chaotic", mixed_field_ising(N),
         haar_product_state(N, np.random.default_rng(
             MAN["seeds"]["TA_iii_chaotic"]["10"][0]))),
        ("localized", xxz_disordered(N, np.random.default_rng(
            MAN["seeds"]["TC_localized"]["10"][0])), neel(N))]:
    ev = EigenEvolver(h)
    devs, base_norms = [], []
    for t in SAMPLE:
        s = ev.state_at(psi0, float(t))
        d0 = phi_distance_matrix(mutual_information_matrix(s, N))
        s2 = s
        for (i, _), u4 in zip(pairs, u4s):
            s2 = apply_pair_unitary(s2, N, i, u4)
        d2 = phi_distance_matrix(mutual_information_matrix(s2, N))
        devs.append(float(np.linalg.norm(d2 - d0) / np.linalg.norm(d0)))
        base_norms.append(float(np.linalg.norm(d0)))
    c[label] = {"rel_phi_change_mean": float(np.mean(devs)),
                "rel_phi_change_max": float(np.max(devs)),
                "n_times": len(SAMPLE),
                "pairs": pairs}
    print(f"C: {label} done", flush=True)
out["C_partition_probe"] = c

with open(OUT / "ar011_attacks.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps({"B": out["B_xi_tolerance_sweep"],
                  "C": out["C_partition_probe"]}, indent=1))
