# Session log — 2026-08-16 — provenance correction: no fictional review history

- **Target:** paper-1 provenance defect (owner-flagged) — the paper and
  substrate framed the owner's multi-model adversarial audit passes as
  "external pre-submission review" / "review rounds", fabricating a
  submission history that never happened.
- **Mode:** VERIFY / mechanical correction (owner-directed).

## Outcome summary

1. **Paper purged** of all review-history framing (9 sites): abstract
   ("two prompted by external review" → "each caught by the study's own
   audit mechanisms"), §1 corrections narrative, §6 opening + staged-search
   stage (iii)/(v) attributions (now agentless: "prompted by the
   observation that…"), §9 methods paragraph, acknowledgements (external-
   review sentence deleted), App-C rows ("Adversarial audit of the draft",
   "audit-prompted", "Draft revision", "Second adversarial audit").
   Verified: zero grep hits for external-review vocabulary; remaining
   "review"/"external" uses are the internal threshold review, laboratory
   clocks, and funding. Rebuilt clean.
2. **Substrate corrected via dated notes, not rewrites** (KB-005 §9
   discipline): KB-004 → v0.10 (changelog + body provenance note under the
   BH-004 v0.9 entry); KB-005 → v0.17 (§33); spec §8 dated provenance
   note; CLAUDE.md living block reworded + standing vocabulary rule.
3. **Standing rule of record:** owner-run multi-model audit passes are
   "adversarial audits (multi-model, internal)" — never "external
   review" — in all future paper and substrate text.

## Delta list (applied, dependency order)

- KB-004: v0.9 → **v0.10** — provenance correction (no scientific change).
- KB-005: v0.16 → **v0.17** — §33 provenance correction + vocabulary rule.
- ar/AR-009_spec.md §8: dated provenance note appended.
- paper/latex/main.tex: 9-site purge; rebuild.
- CLAUDE.md: current-state block reworded; standing rule recorded.

## ADR candidates

None (provenance/vocabulary correction; no intent change).

## Open items

- Owner proof pass of the cleaned build; then retag `paper-v1`,
  endorsement outreach, arXiv/Quantum submission (unchanged).
- Parked: AR-022; BH-005 sequencing; AR-015 census; SRC-036..058 backlog.
