# Session log — 2026-08-16 — AR-023a kickoff-prompt adversarial iteration

- **Target:** AR-023a kickoff prompt (`ar/AR-023a_KICKOFF_PROMPT.md`)
  and the spec voids it exposed.
- **Mode:** ADVERSARIAL (spec review against the committed scaffold
  state at 07ab256; no S1/S2 code written, no gate values changed).

## Outcome summary

1. Cross-checked the kickoff prompt (v1, 07ab256) against AR-023,
   AR-023a, AR-020e, the hardware scaffold, the committed manifest,
   and the frozen comparator artifact.
2. **Defect (blocking):** the instruction "the QPY bundle [is a]
   frozen input — verify their hashes, never regenerate them" had no
   committed referent: no bundle bytes and no bundle hashes exist
   anywhere in the repository (the 2026-08-16 double build wrote both
   only to draft directories outside the repo). Verification as
   written was impossible. Fixed via Amendment A1.2
   (rebuild-twice → byte-identical → commit → frozen thereafter).
3. **Defect (factual):** AR-023a §1 escalation step (ii)
   ("reduce 37 → 25, re-check quadrature") is dead on arrival — the
   25-grid quadrature error 0.13276 > 0.025 is already on record
   (`sector_comparator_N10_run0.json`) and is a deterministic property
   of the grid. Fixed via Amendment A1.1: the permitted escalation is
   768 → 896 shots on the 37-grid (≈ 416.9 s rough formula, ≈ 33 s
   margin under the 450 s cap); 1,024 stays over-cap, 960 is
   margin-free and not permitted.
4. **Void:** AR-023 §6 success-rule clause 5 ("no dominance") has no
   numeric operationalization anywhere, yet S1-G2 requires mechanical
   evaluation of all five clauses 100 times; clause 4 (raw vs M3) is
   undefined in a noiseless S1. Fixed via Amendment A1.3 (S1/S2-scoped
   numbers: leave-one-out excursions within 25% of median Δ, no sign
   flip, projection shift < 0.02; S1 runs M3 against the ideal backend
   as a plumbing check). Hardware-run numbers remain an L4 freeze with
   these as the default proposal — owner attention flagged below.
5. **Voids (minor):** fake-backend pair selection made deterministic
   (A1.4, lexicographic among qualifying Herons); comparator-artifact
   scope of record clarified (A1.5 — the frozen minimal 4-array NPZ at
   `manifest/`, not the AR-023 §11.3 full array list at the §11.3
   path); S1-G4 byte-determinism scoped (A1.7 — no wall-clock inside
   the reports, meta sidecar excluded); efficient S2 implementation
   sanctioned explicitly (A1.8 — per-condition density matrix, then
   multinomial sampling).
6. Compute-scale estimate added to the kickoff as a binding
   engineering note: the S1 battery alone is ~10^5 full analysis
   passes (~2×10^8 pair-RDM reconstructions); a naive per-pair Python
   loop would not finish in useful wall-clock time.
7. Kickoff prompt rewritten as v2: adds the strict pre-sampling order
   of operations (verify comparator → freeze bundle → compute
   ε_sector^(37) → commit BASE seed), the inherited-scaffold reading
   list, the reuse-don't-reimplement pointer to `experiment.py` /
   `circuits.py`, and the 16-test green-baseline first action.
   AR-023a §4's embedded copy retired (A1.6) so exactly one canonical
   prompt exists.

## Delta list

- `ar/AR-023a_s1s2-simulation-spec-2026-08-16.md` §4: embedded kickoff
  blockquote (already diverged from the standalone file) → superseded
  pointer to `ar/AR-023a_KICKOFF_PROMPT.md` — single canonical prompt.
- `ar/AR-023a_s1s2-simulation-spec-2026-08-16.md`: no §5 → §5
  Amendment 1 (A1.1–A1.8), dated, authoring-side, pre-implementation —
  sanctioned amendment mechanism per the spec's own status line; no
  gate value changed.
- `ar/AR-023a_KICKOFF_PROMPT.md`: v1 → v2 — impossible
  bundle-verification instruction replaced by the A1.2 bootstrap;
  dead escalation path replaced by A1.1; pre-sampling order of
  operations and binding engineering notes added.
- Canonical substrate files (KB-001..005): no changes.

## ADR candidates

None.

## Open items

- **Owner review requested:** the A1.3 dominance numbers (25% / no
  sign flip / 0.02) bind S1/S2 now and are the default proposal for
  the hardware-run clause-5 freeze at L4 — confirm or replace before
  L4.
- Implementing session's first milestone commit must be the A1.2
  bundle freeze (bundle bytes + hashes into the repo).
- If S1/S2 wall-clock exceeds the workstation run discipline despite
  vectorization, the implementing session proposes a scope amendment
  (e.g., reduced grid coverage for the envelope, never for the gates)
  rather than silent shortcuts.
- Unchanged from prior log: no QPU call before a frozen bundle, green
  L0–L4, and explicit owner `QPU-GO`.
