---
id: KB-005
title: "IDEG Research Program — Agentic Protocol, Phases, Gates, and Backlog"
status: DRAFT
owner: shared
last_reviewed: 2026-08-15
version: 0.16
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
  - "0.4: AR-009 thresholds owner-reviewed (spec §8 Amendment 1: criterion (b) instrument → log-ratio + calibration pilot); AR-019 added, advisory/non-blocking (owner + Claude, 2026-08-11) — see §20"
  - "0.5: G0 PASSED at owner review; §12 mechanical-fix rule for KB-001 recorded; AR-010 licensed (owner + Claude, 2026-08-11) — see §21"
  - "0.6: AR-019 executed and reconciled (Claude, 2026-08-12) — recommendation KEEP the §5.2 log-ratio instrument, no spec threshold changed; KB-003 → v0.4 (SRC-052..058, verify) — see §22"
  - "0.7: AR-010 confirmatory EXECUTED/RECONCILED (Claude, 2026-08-12/13) — (a) fails via preregistered W3 null-discard, (b) holds, §5.3 sustained-by across dynamical classes; AR-020 (witness reformalization) queued PROPOSED; AR-019 window closed; KB-004 → v0.3 — see §23"
  - "0.8: AR-011 EXECUTED/RECONCILED (Claude, 2026-08-13) — verdicts survive, fragility-direction and §4.1 Φ-matching refuted with dated corrections (KB-004 → v0.4); partition-dependence scope wall; AR-020 requirements sharpened; §10 adversarial gate met — see §24"
  - "0.9: AR-021 added + executed (Claude, 2026-08-13) — dephasing-stabilization literature check: mechanism known, object not found in scope, conditional framing novelty only; KB-003 → v0.5 (SRC-059..063, verify) — see §25"
  - "0.10: owner rulings 2026-08-13 — BH-004 → PLAUSIBLE (KB-004 v0.5); AR-020 APPROVED as scoped (next work item); amendment candidates folded into AR-020; decay-rate-law deferred until paper draft — see §26"
  - "0.11: AR-020 EXECUTED/RECONCILED (Claude + owner ratification, 2026-08-13) — Amendment 4 applied; comparator class-split; fresh-seed (a) re-adjudication FAILS on scrambling|integrable at N = 10 (finite-size, seed-luck finding); forward-path ruling queued — see §27"
  - "0.12: AR-020 CLOSED with the FINAL verdict (owner Amendment 5, n = 40): criterion (a) HOLDS (18/18); §5.4 row 1 — BH-004 supported in-model, BH-005 LICENSED, HYP-009 geometric first realization; KB-004 → v0.6; next: first-paper drafting — see §28"
  - "0.13: paper-1 reflection rulings folded into the outline (test-first framing, boundary-case localized, no-firstness, fenced cross-discipline, hardened probe gate); AR-022 philosophical-context survey added PROPOSED (not paper content) — see §29"
  - "0.14: AR-020b hardened probe — comparator class-split corrected (metastable/integrable matchable; quasiperiodic sole motion-borne survivor, 0/40 both sizes); KB-004 → v0.7; paper §6 gate cleared — see §30"
  - "0.15: external review + AR-020c (Claude, 2026-08-15) — survivor claim refuted at unrestricted scope; naturalness gap = the surviving discriminator; paper-1 major revision executed; KB-003 → v0.7, KB-004 → v0.8 — see §31"
  - "0.16: second review round + AR-020d (Claude, 2026-08-15) — block-coherent commutant matches quasiperiodic (sixth correction, second externally triggered); GGE/price-curve/window-gap battery; discriminator = smooth-in-energy representation gap; paper-1 second major revision; KB-003 → v0.8, KB-004 → v0.9 — see §32"
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

- **G0 — Foundation gate.** KB-001..005 internally consistent; ID references resolve; ADR-001/ADR-002 recorded. **PASSED 2026-08-11 (owner review, session 2026-08-11_AR-009):** full ID-reference sweep clean except one mispointer (KB-001 SC-002 "§§N–O" → fixed to "§§C, M, O" under the mechanical-fix rule below); known-quirks logged, not fixed: KB-003 non-sequential section lettering (A–J, M, O, P, K, L, N, M2) and §M/§M2 near-collision; TL-* historical IDs in KB-003 §Q (linked to ADR candidate D); TH-036 SRC slot reserved (AR-015).
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
**(v0.7) Status: EXECUTED/RECONCILED 2026-08-12/13** — implementation + §6.3 sanity (2026-08-11); calibration pilot with owner rulings (spec Amendment 3); confirmatory campaign executed against the pre-committed manifest (+ Addendum 1: T-A(ii) certificate exhaustively unsatisfiable at N = 8, T-A sizing reverted to spec-primary (10, 12)). Results of record (`ar/AR-010_confirmatory-2026-08-12.md`, `results/AR-010/confirmatory_summary.json`): **criterion (a) FAILS** (single cause: W3 fires on the §4.4 null and is discarded, leaving scrambling|localized with one statistic) → witness scheme returns to FORMALIZE (SC-005 negative, → AR-020); **criterion (b) HOLDS** (dephasing, both tracks, two sizes, direction-consistent); **§5.3 sustained-by affirmed for all six dynamical classes**, class (i) compatible-with; T-B: DTC ε = 0.03 stationary-with-witness 100/100, switch-off → compatible-with, rigidity ε_c > 0.20 (measured), r2 comparator non-thermalizing at 200 periods (prethermal plateau). AR-011 adversarial companion is the required next step before any promotion (§10).

### AR-011 — Toy-model adversarial analysis
`mode: ADVERSARIAL` · `parent: BH-004, BH-005` · `priority: P0` · Attack the results with KB-004 §7: representation-dependence checks, stationary-state indistinguishability (item 12), sustained-by vs compatible-with tests, hidden-clock audit.
**(v0.8) Status: EXECUTED/RECONCILED 2026-08-13** (`ar/AR-011_adversarial-2026-08-13.md`). Attack A refuted the AR-010 fragility-direction interpretation (floored-denominator artifact; corrections issued dated in the AR-010 packet, KB-004 v0.4, spec §8) and the §4.1 Φ-matching assumption (MI nonlinearity — no Φ-matched motionless comparator exists in the family as designed); the §5.3 formal verdicts and criterion-(b) result SURVIVE, with the switch-off geometry change (43–90% of ‖D̄‖) promoted to the load-bearing sustained-by evidence. Attack B: metastable Ξ margins tolerance-robust. Attack C: Φ partition-dependence quantified at 9–20% (same order as ε_Φ) — standing scope wall. Items 1–4, 7–8, 10–11 audited PASS/scope-noted. Item-13 kill condition NOT met. AR-020 inherits two design requirements: null-silent scrambling|localized witness AND a Φ-matched motionless comparator (or impossibility proof).

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

### AR-019 — Robustness-instrument survey by analogy *(new v0.4; advisory, non-blocking)*
`mode: EXPLORE` · `parent: BH-004, AR-009 §5.2` · `priority: P1` ·
**Question:** what do analogous perturbation-response literatures — fidelity/Loschmidt-echo decay classes in quantum chaos, DTC rigidity/critical-strength curves (cf. the verified SRC-044 protocol), MBL stability analyses, dose–response calibration methodology — suggest as the best-instrumented effect measure for AR-009's criterion (b): fixed-strength response vs failure-threshold (λ*-style), ratio vs difference measures?
**Deliverable:** short comparative note with an adopt/keep recommendation; any new sources entered as SRC-* flagged `verify`.
**Promotion_effect:** AR-009 §8 amendment replacing/augmenting the confirmatory instrument — valid only before AR-010 confirmatory runs begin.
**Kill_effect:** none (advisory; the preregistered log-ratio instrument stands if AR-019 has not run in time). Explicitly non-blocking: AR-010 does not wait on it.
**(v0.6) Outcome:** DONE 2026-08-12, reconciled in-session — `ar/AR-019_note-2026-08-12_robustness-instruments.md`. Recommendation **KEEP**: the §5.2 log-ratio primary stands unchanged (promotion effect not exercised; dated no-change entry in spec §8). λ*-style thresholds rejected as primary — grid-censored in the pilot, criterion-derived (meaning shifted under Amendment 3.1), and threshold-location estimators are finite-size-fragile by analogy (SRC-055/056; NOEC critique SRC-057). Curve-style instruments remain where the spec already places them (T-B h_sub(ε); §5.2.1 exploratory curves). Advisory riders: calibrated-strength framing discipline for the confirmatory write-up; decay-rate-law analysis queued as a follow-up AR candidate only if criterion (b) is positive. Status: RECONCILED.
**(v0.7) Window closed:** AR-010 confirmatory runs began 2026-08-12 (manifest b91ad54); the instrument-upgrade window is closed for good.

### AR-020 — Witness-battery reformalization *(new v0.7; APPROVED as scoped — owner ruling 2026-08-13; next work item)*
`mode: FORMALIZE` · `parent: BH-004, CON-034, AR-010 outcome` · `priority: P0 candidate` ·
**Question:** reformalize the CON-034 witness battery so that (1) every witness is null-silent by construction and (2) the scrambling|localized distinction is doubly witnessed. Candidates from the AR-010 record: a null-subtracted/null-compatible OTOC variant (W3 fired on the frozen null — c_sat ≈ 1.11, t* = 1.5 — because the OTOC probes operator spreading, not state motion); w2_mean alongside/in place of min d_phys (min is structurally uninformative for slow classes — recurrence depth returns ~0). Both were identified in-session and NOT applied post-hoc (preregistration discipline).
**Deliverable:** amended witness section as an AR-009 §8 amendment (owner-reviewed) + rerun of the criterion-(a) analysis on the existing confirmatory data where valid, new runs where the witness definition demands them.
**Promotion_effect:** criterion (a) becomes re-adjudicable; BH-004's witnessed-stationarity leg unblocks.
**Kill_effect:** if no null-silent witness pair can separate scrambling|localized, that inseparability is recorded as a substantive negative about witnessing scrambling-class motion beneath stationary geometry.
**(v0.11) Status: EXECUTED/RECONCILED 2026-08-13** (`ar/AR-020_reformalization-2026-08-13.md`). Amendment 4 owner-ratified and applied (statistic set {PR_A, w2_mean, Ξ}; W3 descriptive; §4.1 corrected). Requirement 1 met (null-silent set; scrambling|localized passes both sizes on fresh seeds). Requirement 2 answered class-split (Φ-matched motionless comparator EXISTS for chaotic — microcanonical, miss 0.066; natural families MISS for quasiperiodic/metastable/localized — sustained-by evidence sharpened along class lines). Fresh-seed re-adjudication: **criterion (a) still FAILS** — scrambling|integrable at N = 10 (threshold-straddling AUCs; passes at N = 12); obstruction is finite-size resolving power, not witness structure; the original-seed 18/18 validation was partly seed luck (fresh-seed discipline vindicated). Forward paths queued for owner: accept-and-report / sizes (12, 14) via Krylov / ensemble n = 40.
**(v0.12, FINAL) Owner chose n = 40 (Amendment 5); verdict: criterion (a) HOLDS** — all 18 pair × size checks on addendum-3 fresh seeds (`results/AR-010/rerun40_summary.json`); the marginal pair stabilized above threshold (scrambling|integrable N = 10: 0.9788/0.9519/0.9563). Dual record mandatory downstream: the original preregistered battery failed its own null test; the reformalized battery passes. §5.4 row-1 effects recorded: BH-004 supported in-model; **BH-005 LICENSED**; HYP-009 geometric part gains its first model realization (KB-004 v0.6). AR-020 CLOSED.

### AR-022 — Philosophical-context survey: instantiated vs maintained emergence *(new v0.13; PROPOSED — owner personal interest, NOT paper-1 content)*
`mode: EXPLORE` · `parent: CON-036, BH-004 outcome; owner reflection 2026-08-13` · `priority: P2` ·
**Question:** where does the operationalized sustained-by/compatible-with distinction (an emergent property *actively maintained* by substrate dynamics vs *merely instantiated* by a static configuration) sit relative to the philosophy-of-emergence literature (weak/strong emergence, e.g. Bedau; transformational emergence, e.g. Humphreys — names to be verified, not cited from memory) and to process-philosophy framings (stability of things as stability of patterns of process)?
**Deliverable:** comparative note (AR-019/AR-021 style, sources flagged verify); possibly a standalone essay. **Explicitly NOT paper-1 content** (owner ruling 2026-08-13: at most one citation-free sentence in the paper's discussion).
**Promotion_effect:** none on physics claims; may seed a separate philosophical companion piece.
**Kill_effect:** none (contextual survey).

### AR-021 — Dephasing-stabilization literature check *(new v0.9; executed in-session)*
`mode: VERIFY + EXPLORE` · `parent: AR-010/AR-011 outcome; first-paper framing` · `priority: P1` ·
**Question:** is the AR-010 negative-log ρ effect (weak dephasing pins oscillating MI-graph geometry to its mean, class-resolved sign structure) known physics — at mechanism, object, or framing level?
**(v0.9) Outcome:** DONE 2026-08-13, reconciled in-session — `ar/AR-021_note-2026-08-13_dephasing-stabilization-lit.md`. Verdict: **mechanism KNOWN** (decoherence damping of coherence-carried oscillations; continuous-Zeno family in the strong-coupling limit, SRC-059) — no mechanism-novelty claim licensed; **object NOT FOUND in survey scope** (closest works: static MI-network attack robustness SRC-060, stationary MI-metricity diagnostics SRC-061; adjacent noise-stabilizes-MOTION literature SRC-062/063 is a different object and direction). Permitted paper language: conditional diagnostic/framing novelty only. SRC-059..063 entered in KB-003 v0.5, all `verify`. Status: RECONCILED.

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

Deltas are applied in dependency order (KB-002 definitions → KB-003 theory → KB-004 hypotheses → KB-005 program → KB-001 only via ADR). **(v0.5, decided at G0 owner review 2026-08-11):** the "KB-001 only via ADR" rule is scoped per §9 rule 4a — it governs changes that touch intent (KB-001 §3–4) or reinterpret scope/claims; **mechanical fixes** to KB-001 (typos, wrong cross-references, formatting) outside §3–4 are ordinary deltas applied with version bump and changelog, no ADR required. A delta that would invalidate a downstream item marks it `STALE` rather than silently editing it. Version numbers bump on any non-typographic change; changelogs are mandatory. Conflicts between two runs' deltas are resolved in a named reconciliation session, recorded in the log.

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

---

## 20. Changelog v0.3 → v0.4

1. AR-009 threshold review completed by owner 2026-08-11. Layers 1–2 (stationarity; class separation) accepted unchanged. Criterion (b) amended pre-run per spec §8 Amendment 1: primary effect measure → scale-free log drift ratio (|Δ mean log ρ| > ln 1.5, disjoint CIs); calibration pilot with preregistered grids added (§5.2.1); λ*/γ* failure thresholds collected as exploratory candidate instrument; original R measure demoted to descriptive.
2. §6: AR-019 added (robustness-instrument survey by analogy) — advisory, non-blocking; may upgrade the criterion-(b) instrument via spec §8 amendment only before confirmatory runs.
3. AR-010 licensing now gated on G0 owner review of the substrate only (threshold-review gate cleared).

---

## 21. Changelog v0.4 → v0.5

1. §4 G0: **PASSED** at owner review 2026-08-11 (evidence-based ID-reference sweep; findings and known-quirks recorded in the gate entry and session log). Milestone M0 met.
2. §12: mechanical-fix rule for KB-001 recorded (decided at G0): non-intent mechanical fixes are ordinary deltas; ADRs reserved for intent-touching changes per §9 rule 4a.
3. Effect: with the threshold review (v0.4) and G0 both cleared, **AR-010 is licensed** against `ar/AR-009_spec.md` (subject to the §5.2.1 pilot-before-confirmatory ordering and the AR-019 instrument-upgrade window).
4. sessions/TEMPLATE.md extended (versions-at-close, infrastructure-notes fields) — template is not a KB file; recorded here for traceability.

---

## 22. Changelog v0.5 → v0.6

1. §6 AR-019: executed 2026-08-12 (EXPLORE), status RECONCILED. Deliverable: `ar/AR-019_note-2026-08-12_robustness-instruments.md`. Recommendation **KEEP** the preregistered §5.2 log-ratio criterion-(b) instrument; the instrument-upgrade promotion effect was **not** exercised — no AR-009 threshold changed; a dated no-change entry records the outcome in spec §8.
2. Sources: KB-003 → v0.4 (SRC-052..058 added, all flagged `verify`; methodology-analogy only, not load-bearing).
3. Effect: the AR-019 advisory window is spent as an open decision item; it formally closes when AR-010 confirmatory runs begin (unchanged rule). Next scheduled work: AR-010 confirmatory phase.

---

## 23. Changelog v0.6 → v0.7

1. §6 AR-010: confirmatory campaign EXECUTED/RECONCILED 2026-08-12/13 against the pre-committed manifest (b91ad54; Addendum 1 a76db0e). Full record: `ar/AR-010_confirmatory-2026-08-12.md`, `sessions/2026-08-12_AR-010-confirmatory.md`, spec §8 dated outcome entry. Headline verdicts: (a) FAILS (W3 null-discard → scrambling|localized singly witnessed; §5.4 row 3 — witness scheme to FORMALIZE, SC-005), (b) HOLDS (dephasing, both tracks, two-size replication), §5.3 sustained-by for all six dynamical classes, T-B compatible-with under switch-off with rigidity ε_c > 0.20.
2. §6 AR-020 added (PROPOSED, owner review pending): witness-battery reformalization — null-compatible W3 variant, w2_mean candidate; P0 candidate priority.
3. AR-019 window closed for good (first confirmatory execution, 2026-08-12).
4. KB-004 → v0.3 (BH-004 dated evidence note; no epistemic-status change — AR-011-gated).
5. Next scheduled work: **AR-011 adversarial companion** (required before any promotion, §10) and owner review of AR-020 + the two amendment candidates.

---

## 24. Changelog v0.7 → v0.8

1. §6 AR-011: EXECUTED/RECONCILED 2026-08-13 (`ar/AR-011_adversarial-2026-08-13.md`). Verdict-preserving, interpretation-correcting: §5.3 formal verdicts and criterion (b) survive; the AR-010 fragility-direction reading and the spec §4.1 Φ-matching assumption are refuted (corrections issued, dated, in the AR-010 packet, KB-004 → v0.4, spec §8); switch-off geometry change is the load-bearing sustained-by evidence; Φ partition-dependence quantified 9–20% (standing scope wall); item-13 kill condition not met.
2. §6 AR-020: inherits two design requirements from AR-011 (null-silent scrambling|localized witness; Φ-matched motionless comparator or impossibility proof). Owner review still pending.
3. Next scheduled work: owner decisions — AR-020 scope, the two spec §8 amendment candidates, the live AR-019 decay-rate-law follow-up, and whether BH-004's epistemic status moves on the corrected record (promotion decision now unblocked: the §10 adversarial-companion requirement is met).

---

## 25. Changelog v0.8 → v0.9

1. §6 AR-021 added and executed in-session 2026-08-13 (owner approved the sequencing "literature check first"): dephasing-stabilization literature check. Verdict: mechanism KNOWN (Zeno/damping family), object NOT FOUND in survey scope; paper novelty language restricted to conditional diagnostic/framing level. Deliverable: `ar/AR-021_note-2026-08-13_dephasing-stabilization-lit.md`; KB-003 → v0.5 (SRC-059..063, verify).
2. Owner decision block unchanged and now fully informed: BH-004 status (recommendation on the table: SPECULATIVE → PLAUSIBLE), AR-020 scope, spec amendment candidates, decay-rate-law follow-up. Next scheduled work: those rulings, then AR-020.

---

## 26. Changelog v0.9 → v0.10 — owner rulings 2026-08-13

Owner ruled on the full decision block (recorded in
`sessions/2026-08-13_owner-rulings.md`):

1. **BH-004: SPECULATIVE → PLAUSIBLE** (KB-004 → v0.5; explicit Status line added; HYP-009 geometric part unchanged).
2. **AR-020 APPROVED as scoped** — next work item: null-silent W3 replacement + Φ-matched motionless comparator (or impossibility proof), then criterion-(a) re-adjudication on existing data where valid.
3. **Spec §8 amendment candidates FOLDED INTO AR-020** (no piecemeal spec edits; dated disposition line in spec §8).
4. **AR-019 decay-rate-law follow-up DEFERRED until paper draft** (funded only if the mechanism section needs it).

Next scheduled work: **AR-020**, then first-paper drafting.

---

## 27. Changelog v0.10 → v0.11

1. §6 AR-020: EXECUTED/RECONCILED 2026-08-13. Amendment 4 (owner-ratified) applied to the spec; comparator probe answered class-split; fresh-seed criterion-(a) re-adjudication FAILS on scrambling|integrable at N = 10 only (passes N = 12; two-size replication broken) — recorded negative with the seed-luck finding (original-seed validation 18/18 vs fresh-seed fail: AUC threshold-straddling at n = 20).
2. BH-004 status unchanged (PLAUSIBLE — grounded on criterion (b) + switch-off, independent of (a)).
3. Next scheduled work: owner ruling on the criterion-(a) forward path (accept-and-report / sizes (12, 14) Krylov / ensemble n = 40), then first-paper drafting.

---

## 28. Changelog v0.11 → v0.12

1. §6 AR-020 CLOSED with the FINAL verdict: owner chose Amendment 5 (n = 40, fresh addendum-3 seeds); **criterion (a) HOLDS** — all 18 checks, marginal pair stabilized above threshold. Dual record (original battery failed its null test; reformalized battery passes) is mandatory in all downstream use.
2. §5.4 row-1 effects: BH-004 supported in-model; **BH-005 LICENSED** (not scheduled — owner sequencing); HYP-009 geometric part first model realization. KB-004 → v0.6.
3. Ops incident recorded (AR-020 session log): first Amendment-5 launch overwrote Amendment-4 outputs (runner prefix defect, mine); recovered byte-identical from 5efaa73; n = 40 data preserved as rerun40_*; runner fixed. No data lost.
4. Next scheduled work: **first-paper drafting** (AR-021 framing constraints; dual-record framing; candidate leads: dephasing-stabilization sign structure, class-split comparator finding). BH-005 sequencing decision available whenever the owner wants it.

---

## 29. Changelog v0.12 → v0.13

1. Paper-1 outline reflection (owner + Claude, 2026-08-13; `paper/OUTLINE.md`, session log): test-first reframing of the thesis; localized class demoted to boundary case; no-firstness rule; cross-disciplinary template fenced as proposed-not-demonstrated; hardened comparator probe (full ensembles, both sizes, smooth-f(H) general optimization) required before §6 is drafted.
2. §6 AR-022 added (PROPOSED, P2): philosophical-context survey on instantiated-vs-maintained emergence — owner personal interest, explicitly NOT paper-1 content.
3. Paper classification of record: instrument paper executed as a registered study; claim types = instrument + measured in-model facts + methodological demonstration; zero mechanism/universality/gravity/firstness claims.

---

## 30. Changelog v0.13 → v0.14

1. **AR-020b hardened probe executed (both sizes, full ensembles, smooth-f(H) optimization) — comparator class-split CORRECTED:** metastable and integrable are matchable within ε_Φ (20/20 each), localized boundary (3–6/20); **the size-robust motion-borne survivor is the quasiperiodic class alone (0/40, median 0.32–0.34)** — the same class singled out by the negative dephasing log ρ. Dated corrections applied: AR-020 packet, spec §8, KB-004 → v0.7, paper outline §0/§6. Third internal self-correction of the cycle (family-probe overclaim caught before drafting).
2. §6 gate for paper §6 CLEARED; drafting may begin (§2 first per the writing plan).

---

## 31. Changelog v0.14 → v0.15 — external review + AR-020c

1. **External pre-submission review received 2026-08-14** (owner-relayed). Core criticisms accepted: (i) narrative mismatch — the "survivor" class is not metric-stationary; the unmatched object was the time average; (ii) smooth-f(H) is not all stationary states. Production claim (column-gutter overlap) NOT reproduced (independent rasterization clean; text-extraction artifact of the review tooling); page-13 float isolation confirmed real.
2. **AR-020c executed (review response): unrestricted diagonal-population search, analytic gradient, both sizes.** Result: EVERY class matchable (quasiperiodic 12/20 at N = 10 median 0.241; **20/20 at N = 12 median 0.025**). The single-survivor claim is refuted (fifth major self-correction; first externally triggered). Surviving class-resolved object: the smooth-ensemble NATURALNESS GAP (chaotic ~0.04 vs quasiperiodic ~0.32, both sizes). KB-004 → v0.8 (dated correction); KB-003 → v0.7 (SRC-054 verified, SRC-064 added for the tempered OTOC discussion).
3. Paper-1 major revision executed per the accepted review: non-commutation thesis; naturalness-gap results; renamed coherence-removal/drive-removal tests; tempered OTOC framing; "DTC-like" wording; registered/amended/pre-committed stages table; self-contained numerics; threshold-sensitivity panel; page-13 fix; question-form title.
4. Next: owner proof pass of the revised build; then endorsement/submission path as parked.

## 32. Changelog v0.15 → v0.16 — second review round + AR-020d

1. **Second external review round received 2026-08-15** (owner-relayed; verdict: major revision). Central criticisms accepted: (i) the "unrestricted" search was not — degenerate spectra (XX: 243/1024 distinct at N = 10, 729/4096 at N = 12) leave the commutant much larger than the diagonal family; (ii) "description complexity" overclaimed — misses are best-found upper bounds; (iii) finite-window vs infinite-time averaging needed measurement, not assertion. Alleged page-10/12 gutter collisions again NOT reproduced by independent rasterization (extraction artifact; second occurrence).
2. **AR-020d executed (review response), five stages** (`scripts/ar020d_stationary_suite.py`, `results/AR-010/ar020d_*.json`): (a) block-coherent commutant search (σ = ⊕ A_B A_B†/Z, analytic gradient, containment-checked run-by-run against AR-020c) — quasiperiodic matched essentially exactly at N = 10 (20/20, median 0.0052, best 1e-9; integrable 0.0077); a designed monotone-descent validity check caught a sign error in the objective pre-results (bug fixed, relaunched) and flags one integrable run where the diagonal five-start optimum (1e-8) beat the warm-started block search (0.02) — honesty row in paper App. A; (b) GGE over exact free-fermion charges — matches integrable (20/20, 0.14/0.17 at N = 10/12), fails quasiperiodic (0/20 both sizes, 0.63/0.47); (c) Chebyshev price curve K = 2..96 — smooth plateau ~0.32 (not parameter starvation); (d) sparse top-k supports — ~0.23–0.25 scraping the threshold, optimizer regression above k = 32 recorded; (e) window-vs-infinite-time gap measured per class (relaxing classes 0.003–0.23; metastable N = 10 slow-doublet exception 0.84, 0.02 at N = 12). Reviewer's qp window spot-check (0.012) reproduced exactly.
3. **Corrected claim of record (sixth major self-correction, second externally triggered): resource split.** Every class has a near-exact stationary impostor; classes differ in the stationary resource required — thermal window (chaotic, ETH), GGE charges (generic integrable), degenerate-block coherence (quasiperiodic). Class discriminator renamed: SMOOTH-IN-ENERGY REPRESENTATION GAP (qp 0.32 vs 0.005; chaotic 0.04 vs 0.01 at N = 10). KB-004 → v0.9; KB-003 → v0.8 (SRC-065..068: Rigol 2008, D'Alessio 2016, Vidmar–Rigol 2016, Abanin 2019 — all verified).
4. Paper-1 second major revision executed: physics-first abstract; resource-split §6 with the price table (tab:price); five-stage search narrative; window-gap paragraph; §2.3 infinite-time/degeneracy qualifications; App. A GGE/block/sparse specs incl. the optimizer-shortfall honesty note; representation-gap vocabulary throughout; reversal typo fixed ("matched in 0 of 80"); title retained.
5a. Start-parity control (owner-directed, same day): block stage rerun with
five starts at both sizes — all quasiperiodic optima unchanged (medians
0.0052/0.0035); the single flagged integrable run closed to 3e-10; containment
clean; tab:price start-count-insensitive (`ar020d_blocks5_N{10,12}.json`).
5. N = 12 block-coherent confirmation LANDED (20/20, median 0.0035, containment clean; `results/AR-010/ar020d_blocks_N12.json`) and is in tab:price. Next: owner proof pass of revision 2; then endorsement/submission path as parked.
