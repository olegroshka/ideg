# Kickoff prompt — AR-023a S1/S2 implementation session

Copy-paste everything below the line into the new session as its first
message.

---

Read CLAUDE.md first. Then read, in order:
`ar/AR-023_hardware-pilot-2026-08-16.md` (design of record),
`ar/AR-023a_s1s2-simulation-spec-2026-08-16.md` (this session's spec —
its gates are frozen), `hardware/ibm_exp1/README.md`, and the anchors
in `ar/AR-020e_sector-2026-08-16.md`.

**Single target: implement and close S1 and S2 per AR-023a** (ideal
finite-shot and noisy end-to-end simulations with their numeric
gates), in `hardware/ibm_exp1/`. Definition of done: S1-G1..G4 and
S2-G1..G4 evaluated and reported in committed `s1_report.json` /
`s2_report.json` with the operating envelope; README status updated;
a dated session log in `sessions/`; every gate result stated
pass/fail with its measured number — no rounding a fail into a pass.

Constraints: do not modify `paper/`, `substrate/`, or `ar/AR-023*.md`
(deviations from AR-023a = dated amendments proposed in the session
log, applied only to AR-023a); no IBM credentials or network calls;
no QPU submission — `QPU-GO` does not exist in this session's
vocabulary. The comparator artifact
(`hardware/ibm_exp1/manifest/sector_comparator_N10_run0.*`) and the
QPY bundle are frozen inputs — verify their hashes, never regenerate
them. Before any sampling, compute and record the exact 37-grid
endpoint ε_sector^(37) (AR-023a §0 — the S1 reference is NOT the
361-grid value 0.2241). If a gate fails, follow the escalation ladder
in AR-023a §1 and record it; a failed gate honestly reported is a
valid session outcome (negative results are results). Commit at every
milestone — do not leave a dirty worktree at session end.
