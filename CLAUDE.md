# IDEG — Claude Code session protocol

This repo is the substrate for the IDEG research programme (Information Dynamics
and Emergent Geometry). It follows the Shared Substrate discipline (SRC-001,
https://github.com/olegroshka/shared-substrate): **no result exists until it is
recorded**, and canonical intent lives in the substrate files, not in any chat.

## Before doing anything

1. Read the frontmatter (id, version, changelog tip) of all five files in
   `substrate/`:
   - `00_RESEARCH_CHARTER.md` (KB-001) — intent, INT-001, non-claims, ADRs, kill criteria
   - `01_ONTOLOGY_AND_CONCEPTS.md` (KB-002) — CON-* definitions, semantic collision rules
   - `02_THEORY_LANDSCAPE.md` (KB-003) — TH-* external theory, SRC-* bibliography
   - `03_HYPOTHESIS_SPACE.md` (KB-004) — HYP-*/BH-* hypotheses, adversarial checklist
   - `04_RESEARCH_PROGRAM.md` (KB-005) — AR-* backlog, gates, session protocol
2. Read the most recent file in `sessions/` to see where the last session ended.
3. Confirm with the user the **single primary target** for this session
   (one AR-*, HYP-*, or KB defect). If the user names more than one, ask them
   to pick; park the rest in the session log's open-items list.

## Warm-up check (KB-005 §17)

Before working: does the target's parent chain (INT-001 → RQ/HYP → TH → SRC)
resolve? If any load-bearing TH-*/SRC-* link is unverified, either narrow the
target or convert the session into the corresponding VERIFY run. SRC-036..051
are metadata-verification-pending — do not treat them as checked.

## Hard rules

- **Vocabulary:** use KB-002 definitions. Every use of "information",
  "oscillation", "dynamics", "emergent" must resolve to a CON-* meaning.
  Oscillation claims name their level (OL-k), clock (CON-035), and witness
  (CON-034) — see collision rules 15–18.
- **Clock discipline (NC-010 / INV-R-009):** every dynamical statement and every
  model declares its clock type. Standing adversarial question: *did we hide
  time in the dynamics?*
- **Intent is frozen:** INT-001 and KB-001 §3–4 may not be reworded. Any change
  that reinterprets intent becomes an **ADR candidate** queued in the session
  log — never a direct edit (KB-005 §9 rule 4a).
- **AR-009 before AR-010:** the toy-model spec (metrics, thresholds, witnesses,
  comparators) is preregistered before implementation code is written. Do not
  add post-hoc metrics during AR-010 runs; queue them as spec-amendment
  candidates instead.
- **Negative results are results.** Record them with the same care (SC-005).
- **Sources:** claims about literature cite TH-*/SRC-* IDs; new papers get new
  SRC-* entries flagged `verify` until checked against the primary source.
  Never invent or "recall" bibliographic metadata as settled.

## Ending a session (mandatory)

1. Write `sessions/YYYY-MM-DD_<target>.md` containing:
   - target, mode (EXPLORE/VERIFY/ADVERSARIAL/SYNTHESIZE/FORMALIZE/EXPERIMENT)
   - outcome summary (3–10 lines)
   - **delta list**: every proposed substrate change as
     `KB-file §section: old → new — reason`
   - ADR candidates raised (if any)
   - open items
2. Apply deltas only in dependency order (KB-002 → KB-003 → KB-004 → KB-005;
   KB-001 only via ADR), bumping `version:` and appending to the file's
   changelog. If a delta invalidates a downstream item, mark it `STALE` rather
   than silently editing it.
3. AR evidence packets go in `ar/AR-0XX_*.md` per the KB-005 §3 schema.

## Repo layout

```
substrate/   canonical KB files (KB-001..005) — the only source of truth
sessions/    session logs, one file per session, dated
ar/          AR-* evidence packets and specs (e.g. AR-009_spec.md)
src/ideg/    Python package for Track E3 models (AR-010+)
notebooks/   exploratory notebooks (nothing here is canonical)
results/     run outputs, figures, serialized data (gitignored where large)
```

## Current state (update this block when it changes)

- Repo: https://github.com/olegroshka/ideg (private), created 2026-08-11.
- Substrate versions: KB-001 v0.3, KB-002 v0.2, KB-003 v0.8, KB-004 v0.10,
  KB-005 v0.17 (2026-08-16).
- **AR-020b hardened probe (2026-08-13):** comparator class-split
  CORRECTED — metastable/integrable matchable within ε_Φ (20/20 each),
  localized boundary; **quasiperiodic = sole motion-borne survivor
  (0/40, both sizes, median 0.32–0.34)**, coinciding with the
  negative-dephasing class. Two instruments, one survivor = the paper's
  corrected headline. Paper outline (paper/OUTLINE.md) reflects this;
  §6 drafting gate cleared. AR-022 (philosophy survey, NOT paper
  content) queued PROPOSED.
- **AR-020 EXECUTED/RECONCILED (2026-08-13):** Amendment 4 ratified +
  applied ({PR_A, w2_mean, Ξ}; W3 descriptive); comparator probe
  class-split (chaotic matchable at 0.066 — ETH; quasiperiodic/
  metastable/localized miss ≳ ε_Φ — motion-borne geometry); fresh-seed
  (a) re-adjudication FAILS on scrambling|integrable at N = 10 only
  (passes N = 12; original-seed 18/18 was partly seed luck — fresh-seed
  discipline vindicated). See `ar/AR-020_reformalization-2026-08-13.md`.
- **Owner rulings 2026-08-13:** BH-004 → PLAUSIBLE (BH-004 only; HYP-009
  geometric part stays SPECULATIVE); AR-020 APPROVED as scoped;
  amendment candidates folded into AR-020; decay-rate-law deferred until
  paper draft. See `sessions/2026-08-13_owner-rulings.md`.
- **G0 PASSED / M0 met** (owner review 2026-08-11; see session log and
  KB-005 §4). Mechanical-fix rule for KB-001 recorded in KB-005 §12.
- Track E3 G1 scope **cleared** (SRC-042..044, SRC-049 verified —
  `ar/AR-015_partial-2026-08-11_trackE3-G1.md`).
- **AR-019 DONE/RECONCILED; window CLOSED** at first confirmatory
  execution (2026-08-12).
- AR-015 census: RUNNING (first partial done).
- **AR-010 EXECUTED/RECONCILED (2026-08-12/13):** confirmatory campaign
  run against the pre-committed manifest (+ Addendum 1: T-A(ii)
  certificate exhaustively unsatisfiable at N = 8 → T-A sizing (10, 12)).
  Verdicts: **criterion (a) FAILS** — W3 fires on the §4.4 null
  (discarded), leaving scrambling|localized singly witnessed → witness
  scheme to FORMALIZE (SC-005; → AR-020 PROPOSED); **criterion (b)
  HOLDS** (dephasing, both tracks, two-size replication, class ordering
  as piloted); **§5.3 sustained-by for all six dynamical classes** (the
  stationary comparator is far more fragile than the dynamical state);
  T-B: DTC ε = 0.03 stationary-with-witness 100/100, switch-off →
  compatible-with (W5 collapses, Φ persists), rigidity ε_c > 0.20
  (bound, grid never crosses 0.5), r2 comparator prethermal — not a
  valid thermalizing control at 200 periods. See
  `ar/AR-010_confirmatory-2026-08-12.md` and
  `sessions/2026-08-12_AR-010-confirmatory.md`.
- **AR-011 EXECUTED/RECONCILED (2026-08-13):** verdict-preserving,
  interpretation-correcting. §5.3 verdicts + criterion (b) SURVIVE; the
  "fragile comparator" direction was a floored-denominator artifact
  (corrected, dated, in the AR-010 packet + KB-004 v0.4) — the
  load-bearing sustained-by evidence is the switch-off geometry change
  (43–90% of ‖D̄‖); spec §4.1's Φ-matching assumption refuted (MI
  nonlinearity — no Φ-matched motionless comparator exists as designed);
  metastable Ξ tolerance-robust; Φ partition-dependence 9–20% (standing
  scope wall). Item-13 kill condition NOT met. See
  `ar/AR-011_adversarial-2026-08-13.md`.
- **AR-021 DONE/RECONCILED (2026-08-13):** dephasing-stabilization
  literature check — mechanism KNOWN (Zeno/damping family, SRC-059),
  object NOT FOUND in survey scope (SRC-060..063 checked); paper novelty
  language restricted to conditional diagnostic/framing level. See
  `ar/AR-021_note-2026-08-13_dephasing-stabilization-lit.md`.
- **AR-020 CLOSED with the FINAL verdict (owner Amendment 5, n = 40):
  criterion (a) HOLDS** — 18/18 pair × size checks on fresh addendum-3
  seeds (`results/AR-010/rerun40_summary.json`). Dual record mandatory:
  the original preregistered battery failed its own null test; the
  reformalized battery passes. §5.4 row 1 standing: **BH-004 supported
  in-model; BH-005 LICENSED; HYP-009 geometric part has its first model
  realization.**
- **Paper 1 BUILT (2026-08-14):** draft complete (paper/draft.md v0.3,
  frozen — canonical source is now paper/latex/main.tex) → figures 1–6
  (paper/figures/, validated palette, fixed class-color identity) →
  SRC-059..063 verified (KB-003 v0.6) → **LaTeX compiled clean**
  (paper/latex/main.pdf, 14 pp, 0 errors, all figures + amendment-log
  appendix embedded).
- **Adversarial audit round 1 (owner-run multi-model) + major draft revision (2026-08-14/15):** audit core accepted; AR-020c unrestricted search REFUTED the single-survivor claim (every class matchable; qp 20/20 at N=12) -> surviving discriminator = the smooth-ensemble NATURALNESS GAP; paper rewritten (question-form title, non-commutation + complexity-split thesis, renames, tempered OTOC, stages table, self-contained numerics; 15 pp clean build). KB-003 v0.7, KB-004 v0.8, KB-005 v0.15.
- **Adversarial audit round 2 + second major draft revision (2026-08-15):** degeneracy
  criticism accepted and decisive — AR-020d block-coherent commutant search
  matches quasiperiodic essentially exactly (N=10: 20/20, median 0.0052;
  containment check caught an objective sign error pre-record); GGE matches
  integrable (0.14–0.17), fails qp (0.47–0.63); smooth price curve flat ~0.32
  to K=96; window-vs-infinite-time gaps measured. **Corrected claim of record:
  RESOURCE SPLIT — every class has a stationary impostor; classes differ in the
  stationary resource (thermal window / GGE charges / degenerate-block
  coherence); discriminator = SMOOTH-IN-ENERGY REPRESENTATION GAP** (sixth
  correction, audit-triggered). Paper rewritten (physics-first
  abstract, five-stage search, price table tab:price, App-A optimizer specs,
  SRC-065..068 cited). See `sessions/2026-08-15_review-round2.md`. **Provenance rule (2026-08-16):** these audits were owner-run multi-model adversarial passes (internal) — never call them 'external review'; the paper carries no review-history framing (KB-004 v0.10, KB-005 v0.17).
- N=12 block search LANDED (qp 20/20 median 0.0035, containment clean) ->
  in tab:price; clean rebuild. Next: **owner proof pass of revision 2**, then
  retag paper-v1 -> endorsement -> arXiv + Quantum.
- Superseded gates note: original **owner gates to submission** — proof pass on main.pdf;
  acknowledgements/affiliation/funding TODO markers in main.tex; repo
  public + submission tag (expand App.-C hashes); SciPost class swap
  (one-line, fetch current template at submission). Then arXiv +
  SciPost. Parked: AR-022 (philosophy survey); BH-005 sequencing;
  AR-015 census; SRC-036..058 verification backlog (not
  paper-blocking).
