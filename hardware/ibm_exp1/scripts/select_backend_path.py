"""L4 — outcome-blind backend and ten-qubit path selection (AR-023 §7).

Reads operational QPUs and their calibration data, enumerates every
connected ten-qubit simple path, scores each path BEFORE any outcome
data exists, and filters against the frozen envelope pre-commitment
derived from S2 (AR-023b §2).

Read-only with respect to the QPU: this queries backend properties and
nothing else.  It never builds a job, never calls run(), and cannot
submit.  `QPU-GO` is not part of this script's vocabulary.

Scoring is the AR-023 §7 lexicographic formula:
    (max 2q error, median 2q error, max readout, median readout)
with the worst edge as the final tie-break.  Lower is better on every
component, and the ordering is fixed here so it cannot be adjusted
after seeing the table.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

CREDENTIAL_FILE = (Path.home() / "Documents" / "Codex" / ".credentials"
                   / "ideg-qiskit-ibm.json")
PROFILE = "ideg-open"
PATH_LENGTH = 10

# Frozen envelope pre-commitment (AR-023b §2, from the S2 report),
# plus AR-023c L4-A1 (owner ruling 2026-08-19): a MAXIMUM readout bound.
# The A2.5 leakage witness is a joint ten-qubit measurement scaled by
# prod(1 - p_i), so a bound on the median is provably blind to the single
# outlier that dominates the product.  Without this, the scan's top pick
# carried a 0.31 readout qubit and would have presented a true 0.97 state
# as 0.59 -- below the registered RED kill threshold.
ENVELOPE = {
    "median_two_qubit_error_max": 1.0e-2,
    "median_readout_error_max": 3.0e-2,
    "max_edge_two_qubit_error_max": 1.0e-2,
    "max_readout_error_max": 5.0e-2,            # L4-A1
}

# AR-023c L4-A2 (owner ruling 2026-08-19): readout is promoted above
# two-qubit error.  S2 established that the binding constraint under
# drift is LEAKAGE, which is readout-driven, and both surviving
# candidates sit far inside the envelope on two-qubit error.  The
# superseded ordering is retained for the dual record.
SCORE_KEYS = ("median_readout_error", "max_readout_error",
              "max_2q_error", "median_2q_error")
SCORE_KEYS_SUPERSEDED = ("max_2q_error", "median_2q_error",
                         "max_readout_error", "median_readout_error")


def service(profile: str = PROFILE):
    from qiskit_ibm_runtime import QiskitRuntimeService

    return QiskitRuntimeService(name=profile,
                                filename=str(CREDENTIAL_FILE))


def error_maps(backend):
    """(edge -> 2q error, qubit -> readout error) from the live target."""
    target = backend.target
    twoq: dict[tuple[int, int], float] = {}
    for op_name in target.operation_names:
        try:
            props = target[op_name]
        except Exception:                                  # noqa: BLE001
            continue
        for qargs, inst in (props or {}).items():
            if qargs is None or len(qargs) != 2:
                continue
            err = getattr(inst, "error", None)
            if err is None or not np.isfinite(err):
                continue
            edge = tuple(sorted(qargs))
            twoq[edge] = min(twoq.get(edge, 1.0), float(err))
    readout: dict[int, float] = {}
    try:
        for qargs, inst in (target["measure"] or {}).items():
            err = getattr(inst, "error", None)
            if err is not None and np.isfinite(err):
                readout[qargs[0]] = float(err)
    except Exception:                                      # noqa: BLE001
        pass
    return twoq, readout


def enumerate_paths(twoq, readout, length: int = PATH_LENGTH,
                    limit: int = 400000):
    """Every connected simple path of `length` qubits, scored.

    Deduplicates reversals.  Returns rows sorted by the frozen
    lexicographic score; `truncated` reports whether the walk hit the
    safety limit (never silently).
    """
    adjacency: dict[int, set[int]] = {}
    for a, b in twoq:
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    rows = []
    visited_count = 0
    truncated = False

    def walk(path, seen):
        nonlocal visited_count, truncated
        if truncated:
            return
        if len(path) == length:
            visited_count += 1
            if visited_count > limit:
                truncated = True
                return
            if path[0] > path[-1]:
                return                                  # reversal dedupe
            edges = [tuple(sorted((path[i], path[i + 1])))
                     for i in range(length - 1)]
            e2 = np.array([twoq[e] for e in edges])
            ro = np.array([readout.get(q, np.nan) for q in path])
            if np.any(~np.isfinite(ro)):
                return
            rows.append({
                "path": list(path),
                "max_2q_error": float(e2.max()),
                "median_2q_error": float(np.median(e2)),
                "max_readout_error": float(ro.max()),
                "median_readout_error": float(np.median(ro)),
                "worst_edge": [int(x) for x in
                               edges[int(np.argmax(e2))]],
            })
            return
        for nxt in sorted(adjacency.get(path[-1], ())):
            if nxt not in seen:
                seen.add(nxt)
                path.append(nxt)
                walk(path, seen)
                path.pop()
                seen.discard(nxt)

    for start in sorted(adjacency):
        walk([start], {start})
        if truncated:
            break

    rows.sort(key=lambda r: tuple(r[k] for k in SCORE_KEYS))
    return rows, truncated


def meets_envelope(row) -> bool:
    return (row["median_2q_error"] <= ENVELOPE["median_two_qubit_error_max"]
            and row["median_readout_error"]
            <= ENVELOPE["median_readout_error_max"]
            and row["max_2q_error"]
            <= ENVELOPE["max_edge_two_qubit_error_max"]
            and row["max_readout_error"]
            <= ENVELOPE["max_readout_error_max"])          # L4-A1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default=PROFILE)
    parser.add_argument("--top", type=int, default=5,
                        help="paths to report per backend")
    parser.add_argument(
        "--out", type=Path,
        default=ROOT / "hardware" / "ibm_exp1" / "results" / "l4")
    args = parser.parse_args()

    svc = service(args.profile)
    backends = [b for b in svc.backends(operational=True, simulator=False)
                if b.num_qubits >= PATH_LENGTH]
    print(f"operational QPUs with >= {PATH_LENGTH} qubits: "
          f"{[b.name for b in backends]}", flush=True)

    report = {
        "schema_version": 1,
        "stage": "L4 backend/path selection",
        "path_length": PATH_LENGTH,
        "envelope_precommitment": ENVELOPE,
        "score_formula": "AR-023c L4-A2: lexicographic "
                         + ", ".join(SCORE_KEYS),
        "score_formula_superseded": "AR-023 §7: lexicographic "
                                    + ", ".join(SCORE_KEYS_SUPERSEDED),
        "submission": "none - this script cannot submit",
        "backends": [],
    }

    for backend in backends:
        twoq, readout = error_maps(backend)
        rows, truncated = enumerate_paths(twoq, readout)
        qualifying = [r for r in rows if meets_envelope(r)]
        entry = {
            "name": backend.name,
            "num_qubits": int(backend.num_qubits),
            "processor_type": dict(getattr(backend, "processor_type", {})
                                   or {}),
            "paths_found": len(rows),
            "paths_meeting_envelope": len(qualifying),
            "enumeration_truncated": truncated,
            "best_paths": rows[:args.top],
            "best_qualifying_path": qualifying[0] if qualifying else None,
        }
        report["backends"].append(entry)
        best = entry["best_qualifying_path"]
        print(f"  {backend.name}: {len(rows)} paths, "
              f"{len(qualifying)} meet the envelope"
              + (f" | best median2q={best['median_2q_error']:.2e} "
                 f"medianRO={best['median_readout_error']:.2e}"
                 if best else " | NONE QUALIFY"), flush=True)

    ranked = [b for b in report["backends"]
              if b["best_qualifying_path"] is not None]
    ranked.sort(key=lambda b: tuple(
        b["best_qualifying_path"][k] for k in SCORE_KEYS))
    report["recommended"] = (
        {"backend": ranked[0]["name"],
         **ranked[0]["best_qualifying_path"]} if ranked else None)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "backend_scan.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    meta = {"queried_utc": datetime.now(timezone.utc).isoformat(),
            "profile": args.profile,
            "note": "calibration data is time-varying; re-run before "
                    "freezing a submission bundle"}
    (args.out / "backend_scan.meta.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")

    print()
    if report["recommended"]:
        rec = report["recommended"]
        print("RECOMMENDED (outcome-blind, envelope-qualifying):")
        print(f"  backend {rec['backend']}  path {rec['path']}")
        print(f"  max 2q {rec['max_2q_error']:.3e} | median 2q "
              f"{rec['median_2q_error']:.3e}")
        print(f"  max RO {rec['max_readout_error']:.3e} | median RO "
              f"{rec['median_readout_error']:.3e}")
    else:
        print("NO PATH ON ANY OPERATIONAL BACKEND MEETS THE ENVELOPE.")
        print("Per AR-023b §7 this is a stop condition, not a prompt to "
              "relax the pre-commitment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
