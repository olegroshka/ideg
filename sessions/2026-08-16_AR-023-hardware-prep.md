# Session log — 2026-08-16 — AR-023 IBM hardware preparation

- **Target:** AR-023 — IBM Quantum hardware pilot for the quasiperiodic
  stationary-impostor result.
- **Mode:** EXPERIMENT + IMPLEMENT.

## Outcome summary

1. Read AR-023 and the canonical paper source; froze the operational target to
   `TA_ii_quasiperiodic`, `N=10`, manifest run 0, paper seed `2100294288`.
2. Created and verified the IBM Open instance in `us-east`: status open, zero
   usage, 10 minutes remaining, three allocated Heron r2 QPUs.  No workload was
   submitted and no quota was consumed.
3. Added `hardware/ibm_exp1/` with the 27-row GF(3) covering array,
   endianness contract, pair-RDM reconstruction/PSD projection, metric-parity
   helpers, manifest schema/builder, secure credential helper, and tests.
4. Added an opt-in T3-only export path to `scripts/ar020e_sector_suite.py`;
   default AR-020e behavior and its existing JSON path are unchanged when the
   export environment variable is absent.
5. Replayed the comparator in the recorded Python-3.11 / NumPy-2.3.2 /
   SciPy-1.15.3 stack: objective `0.224107754075805`, within `2.3e-10` of the
   committed run-0 value; full-density recheck agrees; frozen JSON/NPZ written
   with hashes and ten ordered populations.
6. The originally proposed 25-time grid failed the registered quadrature gate
   (`0.13276066 > 0.025`).  The first declared fallback, 37 points, passed
   (`0.01464894`); 49 also passed (`0.00345662`) but was not selected.
7. At 37 points, 1,024 shots gives a rough estimate above the 450-second cap.
   The registered degradation ladder therefore selects 768 shots: 1,323
   circuits, 1,016,064 executions, rough estimate `357.6224 s`, pending
   finite-shot power and backend/M3 overhead checks.
8. Clean Python-3.11 hardware environment resolved and tested:
   Qiskit 2.5.2, Aer 0.17.2, Runtime 0.49.0, M3 3.0.0; focused suite 9/9
   passing.  The manifest remains explicitly DRAFT.
9. Credential-helper follow-up: the managed shell cannot create Qiskit's
   default `USERPROFILE/.qiskit` directory.  The helper now uses the private
   `Documents/Codex/.credentials/ideg-qiskit-ibm.json` path outside the
   repository; path creation and empty-profile access were verified.
10. Read the user-provided key from `IBM_QUANTUM` without displaying it,
    saved and verified the `ideg-open` profile, and confirmed Runtime API
    access to `ibm_fez`, `ibm_kingston`, and `ibm_marrakesh`.  No QPU workload
    was submitted.
11. Implemented the local logical-circuit milestone: exact registered-state
    regeneration, canonical eigenmode phases, the nine-step excitation-
    preserving `XXPlusYY` ladder, a generic Qiskit comparison candidate,
    tomography rotations, deterministic control-bracketed shuffling, the
    complete circuit registry, and QPY serialization.  The focused suite is
    16/16 green.  The draft bundle contains 1,323 ten-qubit circuits for 47
    unique targets; maximum ladder infidelity is `6.67e-16`.
12. Rebuilt the logical bundle in a fresh output directory.  QPY, registry,
    target-state, and bundle hashes reproduced byte for byte.  The draft is
    explicitly not submission-ready and no IBM service was contacted.

## Delta list

- `scripts/ar020e_sector_suite.py`: default analysis-only script → default
  behavior plus opt-in, run-0 T3 population export — closes AR-023 Gate-L0
  serialization dependency without changing normal output.
- `hardware/ibm_exp1/`: missing → initial fail-closed implementation scaffold,
  comparator artifact, schema, version pins, secure account helper, and tests.
- `hardware/ibm_exp1/scripts/circuits.py` and `build_circuits.py`: missing →
  deterministic logical-circuit synthesis, validation, registry, and QPY
  bundle generation without IBM access or submission side effects.
- `hardware/ibm_exp1/manifest/hardware_manifest.json`: missing → DRAFT
  37-time/768-shot scientific manifest; not frozen and not submission-ready.
- Canonical substrate files: no changes in this session.

## ADR candidates

None.

## Open items

- Persist a versioned backend-property snapshot and score candidate physical
  paths before selecting the execution backend.
- Implement backend-path scoring and compilation, finite-shot and noisy S1-S2
  pipelines, M3 calibration budgeting, bootstrap analysis, and remaining
  L2-L4 tests.  Persist a frozen bundle only after backend-specific comparison.
- Resolve the dirty worktree and freeze a new manifest/bundle only after all
  local gates pass.
- No QPU call before an identified frozen bundle and explicit user `QPU-GO`.
