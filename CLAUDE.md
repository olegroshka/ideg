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
- Substrate versions: KB-001/002/004 v0.2, KB-003 v0.3, KB-005 v0.4
  (2026-08-11). G0 owner review still pending.
- Track E3 G1 scope **cleared** (SRC-042..044, SRC-049 verified —
  `ar/AR-015_partial-2026-08-11_trackE3-G1.md`).
- **AR-009 spec DONE and threshold-reviewed by owner** (spec §8
  Amendment 1: criterion (b) → log-ratio instrument + calibration pilot).
  AR-010 licensing gated on **G0 review only**.
- AR-019 queued (advisory, non-blocking): robustness-instrument survey by
  analogy; may upgrade criterion (b) via spec §8 amendment before
  confirmatory runs.
- AR-015 census: RUNNING (first partial done).
- Next session target: **G0 owner review**, then **AR-010** (EXPERIMENT);
  AR-019 or AR-015 continuation are the parallel low-intensity options.
