# Kickoff prompt — AR-023a S1/S2 implementation session

v2, 2026-08-16 — supersedes the 07ab256 text; aligned with AR-023a
Amendment 1 (A1.1–A1.8). Copy-paste everything below the line into the
new session as its first message.

---

Read CLAUDE.md first. Then read, in order:
`ar/AR-023_hardware-pilot-2026-08-16.md` (design of record),
`ar/AR-023a_s1s2-simulation-spec-2026-08-16.md` (this session's spec —
its gates are frozen and **its Amendment 1 is part of the spec**),
`hardware/ibm_exp1/README.md`, the anchors in
`ar/AR-020e_sector-2026-08-16.md`, and
`sessions/2026-08-16_AR-023-hardware-prep.md` (the scaffold state you
inherit). Reuse — do not reimplement — the reconstruction/metric
helpers in `hardware/ibm_exp1/scripts/experiment.py` and the circuit
family in `hardware/ibm_exp1/scripts/circuits.py`. First action: run
`python -m pytest hardware/ibm_exp1/tests -q` in the Python-3.11
hardware environment (`requirements-hardware.txt`) and confirm the
recorded 16-test green baseline before changing anything.

**Single target: implement and close S1 and S2 per AR-023a** (ideal
finite-shot and noisy end-to-end simulations with their numeric
gates), in `hardware/ibm_exp1/`. Definition of done: S1-G1..G4 and
S2-G1..G4 evaluated and reported in committed `s1_report.json` /
`s2_report.json`; the operating envelope translated into the frozen
L4 path-quality requirement (AR-023a §2 deliverable); README status
updated; a dated session log in `sessions/`; every gate result stated
pass/fail with its measured number — no rounding a fail into a pass.

Strict order of operations BEFORE any sampled counts are inspected:

1. Verify the comparator artifact hashes
   (`hardware/ibm_exp1/manifest/sector_comparator_N10_run0.*`; the NPZ
   sha256 is recorded in both the JSON sidecar and the draft
   manifest). It is a frozen input — never regenerate it.
2. Freeze the circuit bundle per Amendment A1.2: rebuild twice with
   `build_circuits.py` into fresh directories, require byte-identical
   QPY/registry/target-state/bundle hashes across the two builds,
   commit the bundle + hash record under `hardware/ibm_exp1/bundle/`,
   and write the hashes into the draft manifest. From that commit on
   it is a frozen input.
3. Compute and record the exact 37-grid endpoint ε_sector^(37)
   (AR-023a §0 — the S1 reference is NOT the 361-grid value 0.2241)
   from the frozen comparator arrays plus the registered state
   regenerated from the committed confirmatory manifest, through the
   same finite-grid pipeline.
4. Commit the S1 BASE seed to the manifest, and wire the clause-4 /
   clause-5 operationalizations (Amendment A1.3) into the report
   scaffolding.

Only then sample.

Constraints: do not modify `paper/`, `substrate/`, or `ar/AR-023*.md`
(deviations from AR-023a = dated amendments proposed in the session
log, applied only to AR-023a); no IBM credentials or network calls; no
QPU submission — `QPU-GO` does not exist in this session's vocabulary.
If a gate fails at 768 shots, the escalation ladder is Amendment A1.1:
the 37 → 25 time-grid reduction is DEAD (the 25-grid quadrature error
0.13276 > 0.025 is already on record and is deterministic); the one
permitted step is 896 shots (≈ 417 s rough formula), then the AR-023
§8 ladder. Record every escalation as a dated amendment. A failed gate
honestly reported is a valid session outcome (negative results are
results).

Engineering notes (binding): the S1 gate battery is ≈ 100 experiments
× (1 main + 2 split-halves + 1,000 bootstrap replicates) ≈ 10^5 full
analysis passes ≈ 2×10^8 pair-RDM reconstructions — vectorize the
RDM/entropy path (stacked 4×4 `eigh`), precompute each circuit's exact
outcome distribution once and multinomial-sample from it; implement S2
per Amendment A1.8 (noisy density matrix once per circuit per noise
condition, readout confusion applied analytically, then sample). Run
long batteries as detached background jobs with capped BLAS threads
per the established run discipline. Reports must satisfy A1.7: no
timestamps, hostnames, or absolute paths inside `s?_report.json`
(canonical JSON; meta sidecars carry timestamps and the environment
freeze and are excluded from the S1-G4 byte comparison). Commit
reports, hashes, figures, and the environment freeze; keep bulk raw
counts local under `hardware/ibm_exp1/results/sim_<id>/` with
checksums — they are reproducible from committed seeds, which is
exactly what S1-G4 proves. Commit at every milestone — do not leave a
dirty worktree at session end.
