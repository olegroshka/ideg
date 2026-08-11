---
id: KB-005
title: "IDEG Research Program — Agentic Protocol, Phases, Gates, and Backlog"
status: DRAFT
owner: shared
last_reviewed: 2026-08-11
version: 0.3
research_layer: R4
epistemic_status: NOT_APPLICABLE
sources:
  - "https://github.com/olegroshka/shared-substrate (accessed 2026-08-11)"
depends_on: [KB-001, KB-002, KB-003, KB-004]
referenced_by: []
changelog:
  - "0.1: initial program, AR-001..014, gates G0–G6 (Sol/ChatGPT, 2026-08-11)"
  - "0.2: review revision (Claude, 2026-08-11) — see §18"
  - "0.3: Track E3 G1 cleared; AR-009 spec drafted (DONE, owner review pending); AR-015 partial packet recorded (Claude, 2026-08-11) — see §19"
---

# Research Program and Agentic Protocol

> This file owns **execution**: how research sessions run, how agentic work is packaged, what order the work happens in, and what evidence is required before promotion. Canonical intent lives in KB-001; terminology in KB-002; external theory in KB-003; hypotheses in KB-004.

## 1. Operating model

The programme runs as **substrate-mediated sessions** (Shared Substrate discipline, SRC-001): every session reads the KB files first, works against explicit IDs, and ends by reconciling deltas into the KB with changelog entries. No result exists until it is recorded.

Two execution styles:

- **interactive sessions** — human + assistant working through a question against the substrate;
- **agentic runs** — packaged `AR-*` investigations executed with explicit mode, inputs, and required outputs, producing evidence artifacts for reconciliation.

**(v0.2)** Interpretation discipline: agentic runs and drafting sessions may propose reformulations of intent, but reformulations become canonical only through ADRs in KB-001 §13. The v0.1 drafting session itself demonstrated the failure mode this rule prevents (silent demotion of INT-001's scope).

---

## 2. Agent modes

| Mode | Purpose | Typical output |
|---|---|---|
| EXPLORE | map a space, enumerate candidates, find seams | annotated candidate lists, structure maps |
| VERIFY | check claims against primary sources; reproduce derivations | claim-by-claim verification tables, corrected TH-* text |
| ADVERSARIAL | attack a hypothesis with the KB-004 §7 checklist | objection lists, countermodels, triviality proofs |
| SYNTHESIZE | find common mathematical structure across TH-* clusters | candidate shared skeletons, seam-matrix updates |
| FORMALIZE | state a HYP-*/BH-* in full discriminant-template form | completed templates, definitions, lemmas |
| EXPERIMENT | build/run computational models | code, results, analysis notebooks, negative results |

Every `AR-*` declares exactly one primary mode (secondary modes allowed but named).

---

## 3. AR record schema

```yaml
id: AR-0XX
title:
mode: EXPLORE | VERIFY | ADVERSARIAL | SYNTHESIZE | FORMALIZE | EXPERIMENT
parent: RQ-* | HYP-* | BH-* | TH-*        # v0.2: OQ-* removed (namespace reserved, unused)
priority: P0 | P1 | P2 | P3
inputs: [KB ids, SRC ids]
question:            # the single question this run must answer
deliverable:         # the artifact that answers it
promotion_effect:    # what KB change a successful run licenses
kill_effect:         # what KB change a failed run licenses
status: PLANNED | RUNNING | DONE | RECONCILED | ABANDONED
```

**Evidence packet requirement:** a `DONE` AR must ship: (1) the deliverable; (2) sources actually consulted with exact locations (theorem/equation/section); (3) confidence notes and open gaps; (4) proposed KB deltas as explicit edits. Reconciliation (§12) turns deltas into KB changes.

---

## 4. Research phases and gates

```text
Phase A  Foundation          G0: substrate coherent, ADRs recorded
Phase B  Verified landscape  G1: load-bearing TH-* verified          [rescoped v0.2]
Phase C  Synthesis           G2: seam skeleton candidates identified [rescoped v0.2]
Phase D  Formal bridges      G3: ≥1 BH-* in full template form
Phase E  Models              G4: toy-model results (positive or negative)   [promoted v0.2]
Phase F  Consolidation       G5: first paper submitted
Phase G  Iteration           G6: next-cycle decision recorded (ADR)
```

### Gate definitions (v0.2 revisions marked)

- **G0 — Foundation gate.** KB-001..005 internally consistent; ID references resolve; ADR-001/ADR-002 recorded. *(Met by the v0.2 revision itself, pending owner review.)*
- **G1 — Verification gate (rescoped).** v0.1 required verifying the full TH catalogue before proceeding — a multi-month serial bottleneck. **v0.2:** G1 is satisfied per-workstream: a workstream may pass its own G1 when the TH-*/SRC-* entries **it actually cites** are primary-source verified. Track E3 cites TH-033, TH-037 (+ optionally TH-034/035 for framing): that is its G1 scope. Full-landscape verification proceeds in parallel (AR-002 series) without blocking model work. **(v0.3) Track E3's G1 scope cleared 2026-08-11:** SRC-042..044 + SRC-049 verified (AR-015 partial, `ar/AR-015_partial-2026-08-11_trackE3-G1.md`); TH-034/035 remain framing-only pending their own verification.
- **G2 — Synthesis gate (rescoped).** Seam-skeleton search (AR-012) scoped to TH-* clusters cited by P0/P1 items, not the entire matrix.
- **G3 — Formalization gate.** At least one BH-* completed in the KB-004 §6 template, survived one ADVERSARIAL run.
- **G4 — Model gate (promoted).** The Track E3 toy-model family has produced recorded results — positive, negative, or mixed — sufficient to adjudicate BH-004's question. **v0.2: G4 work begins immediately after Track E3's G1 scope clears; it does not wait for G2/G3.** (Phases are now partially concurrent by design; the gate letters index deliverables, not a serial calendar.)
- **G5 — Consolidation gate.** First paper (per ADR-002: the toy-model family paper) drafted, internally reviewed against HYP-000, and submitted to an appropriate venue (see §14 sociology note).
- **G6 — Iteration gate.** An ADR records: continue/pivot/park, informed by G4/G5 outcomes and the census.

---

## 5. Workstreams

- **Track V (verify):** AR-001, AR-002 series, AR-016, AR-017 — primary-source verification.
- **Track S (synthesize):** AR-012, AR-013 — seam skeletons, cross-framework structure.
- **Track F (formalize):** AR-006, AR-007, AR-018 — bridge templates, no-go attempts, clock adversary.
- **Track E1 (census):** AR-015 — cross-level persistence census (second deliverable).
- **Track E2 (redistribution):** AR-005, AR-008 — reconstruction-front and redistribution work.
- **Track E3 (toy models):** AR-009 (spec), AR-010 (build/run), AR-011 (adversarial analysis) — **first deliverable (ADR-002)**.

---

## 6. Backlog — AR registry

> v0.1 entries AR-001..014 retained (renumbered references to OQ-* replaced by RQ-*/HYP-* parents). New v0.2 entries: AR-015..018. Priorities follow KB-004 §8.

### AR-001 — Historical provenance completion (Yukawa/Markov/Hawking)
`mode: VERIFY` · `parent: TH-026..028` · `priority: P3` · Confirm/extend the provenance correction; archive primary texts. Kill_effect: none (already non-load-bearing).

### AR-002a — Verify holographic entropy cluster (TH-005..007)
`mode: VERIFY` · `parent: TH-005..007` · `priority: P1` · Exact statements, assumptions, corrections (quantum, higher-derivative).

### AR-002b — Verify entanglement-dynamics cluster (TH-008..010)
`mode: VERIFY` · `parent: TH-008..010, BH-001` · `priority: P0` · The verification anchor: reproduce the first-law → linearized-Einstein derivation step by step; record the exact axioms used (feeds AR-006).

### AR-002c — Verify QES/island cluster (TH-014..017)
`mode: VERIFY` · `parent: TH-014..017` · `priority: P1`.

### AR-002d — Verify thermodynamic-gravity cluster (TH-029, TH-030) *(new scope v0.2)*
`mode: VERIFY` · `parent: TH-029, TH-030` · `priority: P1` · Jacobson 1995 assumptions in full; catalog the known objections to entropic-gravity claims so the programme inherits neither their ambitions nor their errors.

### AR-003 — Abstract the axioms of BH-001
`mode: FORMALIZE` · `parent: BH-001` · `priority: P0` · From AR-002b's output, state the minimal axiom set (monotonicity? first law? modular structure? algebra inclusion?) under which an information variation law constrains geometry; identify which axioms fail outside holography.

### AR-004 — Map non-AdS footholds
`mode: EXPLORE` · `parent: RQ-012` · `priority: P1` · Which seams (TH-029 lineage, TH-031, entanglement equilibrium) survive outside AdS; what replaces the boundary.

### AR-005 — Reconstruction-front formalization (BH-002)
`mode: FORMALIZE` · `parent: BH-002, HYP-006` · `priority: P0` · Define \(\mathcal A_R(t)\) precisely in a controlled model; characterize the Page transition as algebra change; state what "flow" language can/cannot capture.

### AR-006 — Bridge no-go attempt
`mode: ADVERSARIAL` · `parent: BH-001, BH-003` · `priority: P1` · Attempt to prove the *triviality* of candidate bridges (KC-001 test). A clean no-go is a publishable success (SC-005).

### AR-007 — HYP-003 preconditions audit
`mode: ADVERSARIAL` · `parent: HYP-003` · `priority: P2` · Including the v0.2 internal-clock requirement: enumerate what any autonomous \(F[X]\) must supply; check candidates against the circularity and hidden-time kill conditions.

### AR-008 — Redistribution generality survey
`mode: EXPLORE` · `parent: HYP-006` · `priority: P1` · Where does the redistribution picture have evidence beyond AdS (moving mirrors, ensemble models, flat-space toy models)?

### AR-009 — Toy-model family specification *(rewritten v0.2)*
`mode: FORMALIZE` · `parent: BH-004, HYP-009` · `priority: P0` · Produce the full specification of the Track E3 family (§7 below): state spaces, dynamics classes, coarse-graining maps, \(\Phi\) functionals, witnesses, clocks, null comparators, success/failure metrics, and preregistered analysis plan. Deliverable: a spec document reviewable before any code runs (lookahead discipline: metrics fixed before results). **(v0.3) Status: DONE 2026-08-11 — spec drafted at `ar/AR-009_spec.md`; owner review of preregistered thresholds required before AR-010 is licensed.**

### AR-010 — Toy-model implementation and runs
`mode: EXPERIMENT` · `parent: BH-004` · `priority: P0` · Implement and run the family; negative results recorded with equal care.

### AR-011 — Toy-model adversarial analysis
`mode: ADVERSARIAL` · `parent: BH-004, BH-005` · `priority: P0` · Attack the results with KB-004 §7: representation-dependence checks, stationary-state indistinguishability (item 12), sustained-by vs compatible-with tests, hidden-clock audit.

### AR-012 — Seam-skeleton search
`mode: SYNTHESIZE` · `parent: RQ-006` · `priority: P1` *(rescoped to P0/P1-cited clusters)* · Is there a common mathematical skeleton across the first-law/modular/QES/crossed-product seams?

### AR-013 — Entropy–complexity phase-portrait study
`mode: EXPERIMENT` · `parent: BH-006, HYP-007` · `priority: P1` · Compute \((S(t),\mathcal C(t))\) portraits in tractable models; identify when entropy alone is insufficient.

### AR-014 — Observables menu
`mode: EXPLORE` · `parent: RQ-010` · `priority: P2` · What could ever empirically distinguish an information-dynamical formulation (kept at EL-5 watch level until a model reaches EL-4).

### AR-015 — Cross-level persistence census *(new v0.2; second deliverable)*
`mode: VERIFY + SYNTHESIZE` · `parent: HYP-009, RQ-013, SC-006` · `priority: P0` ·
**Question:** for each known persistence-through-dynamics instance (TH-033..036 plus candidates found in the run), what are its level (OL-k), clock, invariant witness, null comparator, and CON-036 classification (sustained-by vs compatible-with)?
**Deliverable:** the census table + verified metadata for SRC-042..051 + a canonical QNM review selected for the reserved SRC slot + a sharply posed statement of the open OL-4 rung.
**Promotion_effect:** HYP-009 sub-geometric part confirmed `GROUNDED` with complete evidence chain; census paper drafted (M2).
**Kill_effect:** if instances collapse to compatible-with everywhere, HYP-009 downgraded per KC-007 — recorded as a substantive negative result.
**(v0.3) Progress:** partial packet 2026-08-11 (`ar/AR-015_partial-2026-08-11_trackE3-G1.md`): SRC-042..044 + SRC-049 verified as warm-up remediation for AR-009 (KB-005 §17). Status: RUNNING.

### AR-016 — Phase–gravity coupling audit *(new v0.2)*
`mode: VERIFY` · `parent: BH-007, TH-035, RQ-008` · `priority: P1` ·
**Question:** what exactly is established, contested, and refuted in the internal-clock/gravity literature (Compton-clock and matter-wave-redshift debate included), and does any of it constrain — rather than decorate — emergent-geometry constructions?
**Deliverable:** claim-by-claim table with the Wolf-et-al. critique fully represented; verified SRC-046..048 metadata; a go/no-go recommendation on formal investment in BH-007.

### AR-017 — Algebraic structure and thermal time verification *(new v0.2)*
`mode: VERIFY` · `parent: TH-031, TH-032, RQ-014, CAND-002` · `priority: P1` ·
**Question:** verify the crossed-product/Type II results at the level IDEG uses them (clock ⇒ well-defined entropy), and the exact content of the thermal-time hypothesis; verify SRC-039..041 metadata.
**Deliverable:** corrected TH-031/032 text with exact theorem locations; assessment of whether modular/thermal clocks can serve HYP-003's internal-clock requirement.

### AR-018 — Clock/time-variable adversary *(new v0.2)*
`mode: ADVERSARIAL` · `parent: NC-010, INV-R-009, all BH-*` · `priority: P1` ·
**Question:** for every current BH-* and the Track E3 spec: what clock is assumed, is it available without the target geometry, and does any claimed dynamics smuggle temporal structure? Standing run to be repeated at each gate.

---

## 7. Track E3 — first deliverable specification (v0.2)

**Goal (BH-004/HYP-009 geometric part, ADR-002):** finite, fully understandable models in which an emergent-geometry functional is (approximately) stationary while microdynamics is provably nonstationary and invariantly witnessed — comparing dynamical classes to find whether stationarity-with-witnessed-dynamics behaves differently across them.

**Model family (initial; AR-009 finalizes):**

- **T-A — Closed finite quantum system.** \(N\)-qubit (or qudit) system; Hamiltonian classes: (i) fixed point (eigenstate/frustration-free ground sector), (ii) quasiperiodic (few incommensurate gaps), (iii) chaotic (random-matrix-class \(H\)), (iv) metastable code subspace (perturbed degenerate sector). Clock: external lab clock, scope-noted (admissible for toy models; the OL-4 caveat recorded).
- **T-B — Driven/Floquet system.** Includes a discrete-time-crystal regime (TH-033 template): subharmonic witness available by construction; question is whether drive-stabilized order also stabilizes the emergent-geometry functional.
- **T-C — Interacting spin chain with MI-graph geometry.** \(\Phi[X]\) = mutual-information-graph metric (TH-037/SRC-049): compute emergent distances from \(I(i:j)\) structure; evolve under scrambling vs integrable vs localized dynamics; ask when \(\Phi\) is stationary, for how long, and with what witness of the underlying motion (relative phases, OTOCs, recurrence distances).

**Mandatory controls (KB-004 §7, AR-011):** representation-invariance of every witness; the stationary-state comparator (an exactly stationary state matched on \(\Phi\) — if no observable distinguishes it from the dynamical model, the "sustained-by" claim fails, per checklist item 12); the switch-off test (where meaningful, quench the dynamics and record whether \(\Phi\)-stationarity degrades — operationalizing CON-036); preregistered metrics (AR-009 before AR-010; lookahead discipline).

**Success metric:** at least one regime in which (a) an invariant witness cleanly distinguishes dynamical classes, **and** (b) the robustness of \(\Phi\)-stationarity (to perturbation, noise, or subsystem loss) *differs by class*. Outcome (b)'s presence or absence is the paper's finding either way — the robustness differential is the novel question, and a clean null is publishable (SC-005).

**Explicit non-goals:** no claim that T-A/B/C are gravity; no OL-4 conclusions beyond "the pattern does/does not have a nontrivial model realization"; scope walls per collision rule 10.

---

## 8. First wave (revised execution order, v0.2)

```text
Immediately:  AR-009 (spec)  +  AR-015 (census, low intensity)  +  AR-002b (anchor verification)
Then:         AR-010/AR-011 (runs + adversarial)   ∥   AR-003 (axiom abstraction)
              AR-016 (clock audit)  →  go/no-go on BH-007
Then:         AR-005, AR-008   ∥   AR-012 (rescoped), AR-013, AR-017
Standing:     AR-018 at every gate
```

v0.1's first wave was verification-only (AR-002 series before anything else). v0.2 interleaves: one verification anchor runs from day one, but the deliverable-bearing tracks start immediately rather than after full Phase B.

---

## 9. Session protocol

Every working session:

1. **Load:** read KB-001..005 headers + the sections relevant to the session goal; note versions.
2. **Declare:** one primary target (AR-*, HYP-*, or KB defect) per session.
3. **Work:** against explicit IDs; new claims get provisional IDs immediately.
4. **Reconcile:** end with an explicit delta list (KB file, section, old → new, reason); apply or queue.
5. **Log:** append to the session log (date, target, outcome, deltas, open items).

**(v0.2)** Rule 4a: any delta that reinterprets intent (KB-001 §3–4) is queued as an ADR candidate, never applied directly.

---

## 10. Evidence and promotion rules

- No `TH-*` may be cited as load-bearing until its `VERIFY` run is `RECONCILED` (per-workstream G1 scope).
- No `HYP-*` promotion without the KB-004 §6 template complete, including clock and level/witness fields.
- `EXPERIMENT` results promote only after their `ADVERSARIAL` companion run.
- Negative results are recorded with the same care as positive ones and count toward SC-005.
- **(v0.2)** SRC-036..051 verification is distributed: AR-015 owns SRC-042..051 (exemplars/constructions), AR-016 owns SRC-046..048, AR-017 owns SRC-039..041, AR-002d owns SRC-036..038.

---

## 11. Source quality policy

Tier 1: peer-reviewed primary literature and rigorous preprints by established groups; Tier 2: authoritative reviews (mapping only); Tier 3: talks/lectures (leads only); Tier 4: social media and popularizations (provenance triggers only, never evidence — cf. the programme's own origin, TH-026..028). Every load-bearing claim needs Tier 1 anchoring with exact locations.

---

## 12. Reconciliation protocol

Deltas are applied in dependency order (KB-002 definitions → KB-003 theory → KB-004 hypotheses → KB-005 program → KB-001 only via ADR). A delta that would invalidate a downstream item marks it `STALE` rather than silently editing it. Version numbers bump on any non-typographic change; changelogs are mandatory. Conflicts between two runs' deltas are resolved in a named reconciliation session, recorded in the log.

---

## 13. Stopping / pivot rules

- A track that fails its kill test twice is parked with an ADR, not silently continued.
- If BH-004 fails cleanly (no regime with a witnessed sustained-by structure), the negative is written up, HYP-009's geometric part is marked `CHALLENGED`, and G6 decides between the census-led fallback (M2 as primary output) and a pivot to BH-002/BH-006.
- If HYP-000 survives all bridges after Phase D, the programme's honest output is a rigorous null-and-census result — recorded as success class SC-005/SC-006, not failure.
- Portfolio rule: IDEG is one project among several (seam paper, book, SMIM/harp, trading). A standing WIP cap applies; IDEG advances by scheduled sessions, not by displacement.

---

## 14. Publication and venue strategy (sociology-aware)

- First paper: toy-model family (M1) — venue class: quantum-information / mathematical-physics friendly (where finite-model results with honest scope are normal), not a gr-qc grand-claims venue. arXiv category chosen to match content (quant-ph primary is acceptable; endorsement constraints noted for gr-qc/hep-th).
- No strong-claim framing: titles and abstracts state models and findings, never "information is fundamental."
- The census (M2) is positioned as a review-adjacent research note with a sharp open problem.
- Every submission passes an HYP-000 read: would a skeptical referee say "this is standard QM relabelled"? If the answer is not clearly "no," the draft returns to ADVERSARIAL.

---

## 15. ADR candidates (open decisions)

- **ADR-003 (candidate A):** choice of primary state-space candidate (CAND-001..007) after AR-003/AR-012 results.
- **ADR-004 (candidate B):** whether BH-007 receives formal investment (decided by AR-016's go/no-go).
- **ADR-005 (candidate C):** venue and authorship policy for M1.
- **ADR-006 (candidate D):** whether to reconstruct and record the prior unrecorded sessions (information-fundamentalism, MDL) as substrate appendices.
- **ADR-007 (candidate E):** HYP-008 (MDL bridge) priority after first toy-model results — promotion to P1 or continued P2.
- **ADR-008 (candidate F):** whether Phase E extends to a second model generation (e.g., algebraic/crossed-product toy models per AR-017 findings).

*(Decided: ADR-001 reading of INT-001; ADR-002 first deliverable — recorded in KB-001 §13.)*

---

## 16. Milestones (revised v0.2)

- **M0 — Substrate coherent (G0).** v0.2 files reconciled and owner-reviewed.
- **M1 — First paper: toy-model family.** AR-009..011 complete; paper drafted, adversarially reviewed, submitted. *(v0.1's M1 — full landscape verification — is retired as a milestone; verification is continuous per-workstream.)*
- **M2 — Census paper.** AR-015 complete; census written up with the open-rung statement.
- **M3 — Formal bridge adjudicated.** AR-003/AR-006 produce either a minimal-axioms result or a no-go; ADR-003 decides the state-space bet.
- **M4 — Cycle decision (G6).** Continue / pivot / park, recorded as an ADR.

---

## 17. Warm-up prompt for future sessions

> "Load KB-001..005 (IDEG v0.2+). Confirm versions and changelog tips. Today's single target is: ___. Before working: does the target's parent chain (INT-001 → RQ/HYP → TH → SRC) resolve? If any link is unverified, either narrow the target or convert the session to the corresponding VERIFY run. End with a delta list; intent-touching deltas become ADR candidates."

---

## 18. Changelog v0.1 → v0.2

1. Recorded the interpretation-discipline rule (§1) — reformulations of intent require ADRs; motivated by the v0.1 drafting failure.
2. Rescoped G1 to per-workstream verification and G2 to P0/P1-cited clusters; promoted G4 to begin after Track E3's G1 scope clears (phases now partially concurrent).
3. Added AR-015 (cross-level census; second deliverable), AR-016 (phase–gravity audit), AR-017 (algebra/thermal-time verification), AR-018 (standing clock adversary), AR-002d (thermodynamic-gravity cluster).
4. Rewrote AR-009 as the full Track E3 family specification; added §7 with models T-A/T-B/T-C, mandatory controls (stationary-state comparator, switch-off test, preregistered metrics), and the robustness-differential success metric.
5. Replaced dangling `OQ-*` parents with `RQ-*/HYP-*` in the AR schema (OQ-* reserved, unused).
6. Revised first wave (§8) to interleave deliverable tracks with a single verification anchor.
7. Distributed SRC-036..051 verification ownership across AR-015/016/017/002d (§10).
8. Added §13 portfolio rule and BH-004-failure branch; added §14 sociology-aware publication strategy (venue class, endorsement constraints, HYP-000 referee test).
9. Recorded ADR-001/002 as decided; renumbered open candidates ADR-003..008, adding E (HYP-008 priority) and F (second model generation).
10. Revised milestones: M1 = toy-model paper (was: landscape verification), M2 = census; updated warm-up prompt to v0.2 with intent-chain check.

---

## 19. Changelog v0.2 → v0.3

1. §4 G1: Track E3's G1 scope recorded as cleared 2026-08-11 (SRC-042..044, SRC-049 verified; AR-015 partial packet).
2. §6 AR-009: status DONE — full spec drafted at `ar/AR-009_spec.md` (models T-A/T-B/T-C concretized; Φ per verified TH-037 eqs. 13–14; witness battery W1–W5 with invariance arguments; stationary-state comparator, switch-off, representation, and null controls; preregistered thresholds; analysis plan). Owner review of thresholds gates AR-010.
3. §6 AR-015: status RUNNING; first partial packet recorded (warm-up remediation for AR-009 per §17).
4. Process note: the §17 warm-up check fired as designed on this session's first target (unverified load-bearing sources) and was resolved by an in-session VERIFY partial before FORMALIZE work.
