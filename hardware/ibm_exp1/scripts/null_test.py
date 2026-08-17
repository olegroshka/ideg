"""Null test for the AR-023a Amendment 2 success rule.

AR-010's criterion (a) failed because a witness fired on the §4.4 null.
A rule that scores 100/100 is only meaningful if it also reports NO
separation when none exists.  This constructs exactly that case.

Null construction: replace the sector comparator with an INDEPENDENT
reconstruction of the same moving time-average.  Concretely, D-bar is
built from half-shot arm h1 and the "comparator" metric from arm h2 of
the same dynamic circuits.  Both estimate the same true D-bar, so the
true endpoint is exactly zero and any measured epsilon is pure
reconstruction noise.  The success rule MUST NOT fire.

A rule that fires here would be declaring a stationary impostor
distinguishable from the moving geometry when the "impostor" IS the
moving geometry -- the AR-010 failure mode, transplanted.

No IBM credentials, no network access, no QPU submission.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import sampling  # noqa: E402
from sampling import (N_OUT, StateIndex, aggregation_weights,  # noqa: E402
                      hermitize_project_batch, load_bundle,
                      mi_from_pair_rdms, pair_rdms_from_counts,
                      phi_from_mi, reconstruction_basis_rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiments", type=int, default=30)
    parser.add_argument("--bootstrap", type=int, default=300)
    parser.add_argument("--shots", type=int, default=768)
    parser.add_argument("--base-seed", type=int, default=24002)
    parser.add_argument(
        "--cache", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "results"
        / "sim_common_v2" / "exact_probs.npz")
    parser.add_argument(
        "--out", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "results"
        / "sim_s1_null" / "null_report.json")
    args = parser.parse_args()

    manifest, registry, basis_rows = load_bundle(ROOT)
    index = StateIndex(registry["circuits"], basis_rows)
    recon = reconstruction_basis_rows(basis_rows)
    w1, w2 = aggregation_weights(recon)
    probs = np.load(args.cache, allow_pickle=False)["probs"]
    half = args.shots // 2
    canonical = index.canonical_index

    def metric_average(source):
        """Time-averaged metric from one count source over dynamic states."""
        phi = []
        for state_id in index.dynamic_ids:
            counts = source[index.rows_for[state_id]].astype(float)
            raw = pair_rdms_from_counts(counts, w1, w2)
            used, _ = hermitize_project_batch(raw, True)
            phi.append(phi_from_mi(mi_from_pair_rdms(used)))
        return np.mean(phi, axis=0)

    rows = []
    for r in range(args.experiments):
        halves = np.empty((len(probs), 2, N_OUT), dtype=np.uint16)
        for c in range(len(probs)):
            rng = np.random.default_rng(np.random.SeedSequence(
                [args.base_seed, int(canonical[c]), r]))
            halves[c] = rng.multinomial(half, probs[c], size=2)

        # arm h1 -> D-bar ; arm h2 -> the null "comparator"
        dbar = metric_average(halves[:, 0])
        star_null = metric_average(halves[:, 1])
        eps_null = float(np.linalg.norm(star_null - dbar)
                         / np.linalg.norm(dbar))

        # bootstrap the same construction for the interval on Delta
        emp = halves.sum(axis=1).astype(float) / args.shots
        boot_root = np.random.SeedSequence(
            [args.base_seed, 10 ** 6 + r, 77])
        children = boot_root.spawn(len(probs))
        eps_b = []
        n_boot = args.bootstrap
        draws = np.empty((len(probs), n_boot, 2, N_OUT), dtype=np.uint16)
        for c in range(len(probs)):
            rng = np.random.default_rng(children[c])
            draws[c] = rng.multinomial(half, emp[c], size=(n_boot, 2))
        for b in range(n_boot):
            d1 = metric_average(draws[:, b, 0])
            d2 = metric_average(draws[:, b, 1])
            eps_b.append(float(np.linalg.norm(d2 - d1)
                               / np.linalg.norm(d1)))
        eps_b = np.asarray(eps_b)
        # floor: same endpoint-level split construction as A2.1
        floor = float(np.median(eps_b))
        delta_b = eps_b - floor
        ci_low = float(np.quantile(delta_b, 0.025))
        fires = bool(ci_low > 0.0)
        rows.append({"experiment": r, "eps_null": eps_null,
                     "eps_boot_median": float(np.median(eps_b)),
                     "floor": floor, "delta_ci_low": ci_low,
                     "clause_1_fires": fires})
        print(f"null exp {r}: eps={eps_null:.4f} floor={floor:.4f} "
              f"CI_low={ci_low:+.4f} fires={fires}", flush=True)

    fired = int(sum(row["clause_1_fires"] for row in rows))
    report = {
        "schema_version": 1,
        "test": "AR-023a Amendment 2 null test",
        "construction": "comparator replaced by an independent half-shot "
                        "reconstruction of the same moving time-average; "
                        "true endpoint is exactly zero",
        "shots": args.shots,
        "base_seed": args.base_seed,
        "n_experiments": args.experiments,
        "bootstrap_replicates": args.bootstrap,
        "eps_null_median": float(np.median(
            [row["eps_null"] for row in rows])),
        "separation_declared_count": fired,
        "verdict": ("PASS - rule does not declare separation on the null"
                    if fired == 0 else
                    f"FAIL - rule declared separation in {fired} of "
                    f"{args.experiments} null experiments"),
        "experiments": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(json.dumps({k: report[k] for k in
                      ("eps_null_median", "separation_declared_count",
                       "verdict")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
