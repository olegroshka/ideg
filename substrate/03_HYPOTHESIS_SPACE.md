---
id: KB-004
title: "IDEG Hypothesis Space — Nulls, Bridges, Strong Forms, and Falsifiers"
status: DRAFT
owner: shared
last_reviewed: 2026-08-13
version: 0.5
research_layer: R3
epistemic_status: SPECULATIVE_TO_PLAUSIBLE
sources:
  - "Cites canonical TH-* and SRC-* in KB-003"
depends_on: [KB-001, KB-002, KB-003]
referenced_by: [KB-005]
changelog:
  - "0.1: initial hypothesis space, HYP-000..008, BH-001..006 (Sol/ChatGPT, 2026-08-11)"
  - "0.2: review revision (Claude, 2026-08-11) — see §10"
  - "0.3: BH-004 dated evidence note from AR-010 confirmatory (Claude, 2026-08-13) — sustained-by clause supported in-model, criterion (a) witness-scheme negative recorded; no epistemic-status change (AR-011-gated); see ar/AR-010_confirmatory-2026-08-12.md"
  - "0.4: BH-004 evidence note corrected per AR-011 (Claude, 2026-08-13) — fragility direction withdrawn (floored-denominator artifact); switch-off geometry change promoted to load-bearing sustained-by evidence; §4.1 Φ-matching assumption refuted; partition-dependence quantified 9–20%; see ar/AR-011_adversarial-2026-08-13.md"
  - "0.5: BH-004 epistemic status SPECULATIVE → PLAUSIBLE (owner ruling 2026-08-13, post-AR-011/AR-021); explicit Status line added; HYP-009 geometric part unchanged (SPECULATIVE)"
---

# Hypothesis Space

> This file owns **our conjectures**, not external theory. A hypothesis may be `STABLE` as a well-specified research object while remaining epistemically `SPECULATIVE`.

## 1. Two orthogonal status systems

### Artefact maturity
`MISSING → DRAFT → STABLE → STALE → DEPRECATED` — *is the hypothesis recorded clearly and consistently?*

### Epistemic status
`SPECULATIVE → PLAUSIBLE → GROUNDED → FORMALISED → SUPPORTED`, side branches `CHALLENGED`, `REFUTED` — *how strongly does evidence support the hypothesis?*

**(v0.2)** These words are reserved vocabulary: they may appear in `epistemic_status` fields and nowhere else in loose senses (KB-001 §6.1 crosswalk governs their relation to EL-* and E-*). v0.1's informal "GROUNDED as a research direction" usage is retired; the intended meaning is now expressed as `PLAUSIBLE` plus explicit motivating TH-* citations.

A correct entry may therefore be:

```yaml
status: STABLE
epistemic_status: SPECULATIVE
```

**(v0.2)** Every hypothesis entry now also declares its **clock type** (CON-035) and, where recurrence is involved, its **level/witness** data (CON-022/CON-034), per INV-R-008/009.

---

## 2. Null hypothesis family

### HYP-000 — Descriptive-null hypothesis
**Statement.** The repeated role of information-theoretic quantities in quantum gravity is entirely a consequence of ordinary quantum mechanics plus the chosen gravitational/holographic formulation. "Information dynamics" adds no independent physical law, constraint, invariant, or prediction.
**Status:** `STABLE` / `PLAUSIBLE` baseline. **Strength:** weakest / default comparator.
**What would support it:** every candidate IDEG bridge is eliminated by an invertible re-description or is already contained in the baseline theory.
**What would weaken it:** a compact information-dynamical principle that independently derives multiple gravitational relations or excludes baseline-allowed states.
**Why mandatory:** without HYP-000, the project can mistake vocabulary for discovery.
**(v0.2)** HYP-000 applies with full force to HYP-009: "quantum systems evolve" is the null against every cross-level claim (KC-007).

---

## 3. Weak-to-strong hypothesis ladder

### HYP-001 — Relational-geometry constraint
**Statement.** In at least one nontrivial class of quantum-gravitational systems, effective geometric observables are constrained by relational information structure not reducible to a single entropy scalar.
\[
\mathcal G = \Phi[\mathcal R_I],
\]
where \(\mathcal R_I\) may include relative entropy, modular data, operator-algebra inclusions, multipartite correlations, or encoding structure.
**Status:** `STABLE` / `PLAUSIBLE` — motivated by TH-005–TH-017, TH-029, TH-031; not yet a universal hypothesis. *(v0.2: status vocabulary corrected; motivation extended with the thermodynamic and algebraic clusters.)*
**Clock:** inherited from the framework (dictionary-level; clock-deferred).
**Framework risk:** strongest evidence is holographic; TH-029 is the main non-holographic anchor.
**Falsifier/downgrade:** no invariant \(\mathcal R_I\) beyond framework-specific dictionaries.

### HYP-002 — Dynamical bridge hypothesis
**Statement.** Changes in a suitable information-relational structure constrain changes in effective gravitational geometry:
\[
\dot{\mathcal G}=\Psi(\mathcal R_I,\dot{\mathcal R}_I;\theta)
\quad\text{or}\quad
\delta \mathcal F_I = 0 \iff \mathcal E_{grav}=0 .
\]
**Motivation:** TH-008, TH-009, TH-010, TH-029.
**Status:** `STABLE` / `PLAUSIBLE`, formalisation required.
**Clock:** must be declared per candidate formalisation (CON-035); the modular/thermal option (TH-032) is the leading internal candidate.
**Alternative explanation:** these relations may be consequences of AdS/CFT plus Einstein gravity with no autonomous information dynamics.
**Falsifier/downgrade:** bridge cannot be stated without importing the full gravitational equations as hidden assumptions.

### HYP-003 — Autonomous information-dynamics hypothesis
**Statement.** There exists a deeper state variable \(X\) and dynamics \(\dot X=F[X]\) such that \(\mathcal G=\Phi[X]\) and gravitational evolution follows without geometry as an independent fundamental variable.
**Status:** `DRAFT` / `SPECULATIVE`.
**Clock (v0.2, now mandatory):** an external background clock is inadmissible here (NC-010) — that would smuggle in exactly the temporal structure geometry is supposed to supply. Admissible: relational or modular/thermal clocks internal to \(X\). This is a *new explicit promotion requirement*.
**Required before promotion:** define \(X\) invariantly; define \(F\) without circular use of the target geometry **or its time function**; recover a known gravitational limit; show nontriviality vs HYP-000.
**Kill condition:** all viable \(F\) require the geometry (including its causal/temporal structure) to be given first.

### HYP-004 — Persistent-structure-as-dynamics hypothesis
**Statement.** Persistent effective physical structures correspond, in an appropriate deeper state space, to dynamically stable structures rather than literal microscopic stasis:
\(X(t)\in\mathcal A\) (invariant set, metastable manifold, code subspace, symmetry orbit, recurrent region) while \(\mathcal C[X(t)]\approx G_*\).
**Status:** `STABLE` / `PLAUSIBLE` generic principle; not yet specifically gravitational.
**Clock:** per-model.
**Scientific content requires:** a gravitationally relevant \(X\), \(\mathcal C\), and invariant \(\mathcal A\).
**Failure mode:** triviality — every stationary quantum system fits, adding no gravity-specific constraint. **(v0.2)** The *sustained-by* requirement (CON-036) is now part of the statement: mere compatibility is HYP-000 territory.

### HYP-009 — Cross-level dynamical persistence (CLDP) (added v0.2; logically between HYP-004 and HYP-005)
**Statement.** For each adjacent pair of abstraction-ladder levels (OL-k−1, OL-k), persistent structures at OL-k are *sustained by* (CON-036) nontrivial dynamics at OL-k−1, witnessed by at least one invariant observable (CON-034) at OL-k−1 — and this pattern continues at the geometric rung: effective geometry (OL-4) is the persistence face of OL-0–OL-2 information dynamics in the same structural sense.
**Decomposition.** (a) *Sub-geometric part:* pattern holds for the rungs below OL-4 — `epistemic_status: GROUNDED` via TH-033/TH-034/TH-035 (established instances with witnesses; census AR-015 to complete and classify sustained-by vs compatible-with). (b) *Geometric part:* pattern holds at OL-3→OL-4 — `epistemic_status: SPECULATIVE`; this is RQ-013 and the actual research content.
**Clock:** level-relative; the OL-4 claim requires an internal clock (as in HYP-003) or a declared external one with scope noted.
**Provenance:** this is the faithful formalization of INT-001's "on every level of persistent reality" (ADR-001); it replaces v0.1's silent narrowing to "a subset of gravitational/Planck structures."
**Promotion criteria (geometric part):** exhibit a model (Track E3) in which an emergent-geometry functional \(\Phi[X]\) is stationary *because of* — counterfactually dependent on — witnessed microdynamics, with the dependence surviving representation changes; then seek the pattern in a controlled gravitational framework.
**Kill conditions:** KC-007 (reduces everywhere to "quantum systems evolve" with no cross-level constraint); or the geometric part fails while sub-geometric instances remain — in which case HYP-009 is downgraded to a documented pattern-with-terminus, itself a publishable negative (SC-005/SC-006).

### HYP-005 — Recurrent/oscillatory persistent-mode hypothesis (geometric-level specialization; rewritten v0.2)
**Statement.** Within HYP-009's geometric part: some persistent gravitational structures correspond to recurrent, periodic, or quasiperiodic modes of the deeper information dynamics, with an OL-4-level invariant witness:
\[
d_{phys}(X(t+T),X(t))<\varepsilon,
\]
\(d_{phys}\) invariant under gauge/phase/encoding redundancy.
**Status:** `STABLE` / `SPECULATIVE`.
**Level/witness ledger (v0.2):** kinematic phase oscillation — established, significance open (TH-035, NC-009); driven many-body recurrence — established with witness (TH-033, template); geometric transient ringing — established, classical, the null comparator (TH-036); geometric *sustaining* recurrence — open, this hypothesis.
**Promotion criteria:** recurrence follows from the candidate dynamics rather than being imposed; survives quotienting by redundancies; explains or predicts a stable feature that fixed-point/metastable alternatives do not; **differs demonstrably from quasinormal ringing** (TH-036).
**Kill condition:** KC-005 applied at OL-4 — no invariant witness exists at the geometric level, or recurrence adds nothing over the alternatives in BH-004/BH-005 comparisons. Killing HYP-005 does not kill HYP-009's sub-geometric part or the broader programme.

### HYP-006 — Black-hole redistribution hypothesis
**Statement.** The physically useful description of unitary black-hole evaporation is primarily **dynamic redistribution/re-encoding/reconstructability of quantum information**, not preservation in a localized terminal storage object.
**Status:** `STABLE` / `PLAUSIBLE` — strongly motivated in controlled models by TH-004, TH-015–TH-017; universal form unproven. *(v0.2: vocabulary corrected.)*
**Consequences:** a stable remnant is not logically required; "where the information is" may be subsystem/algebra/reconstruction-relative; any local-current picture must reproduce nonlocal reconstruction facts.
**Alternative branches:** fuzzball and remnant models preserve information by different mechanisms.

### HYP-007 — Complexity-dynamics bridge
**Statement.** A complexity-like quantity may encode gravitational dynamics not captured by entropy after entanglement saturates: \(\mathcal C(t)\leftrightarrow \mathcal V(t)\) or \(I_{WDW}(t)\).
**Motivation:** TH-019. **Status:** `STABLE` / `PLAUSIBLE`, conjectural underpinnings.
**Risks:** gate-set/cost-function dependence; ambiguity among proposals.
**IDEG question:** can a more invariant relative/conditional complexity retain the gravitational correspondence?

### HYP-008 — Algorithmic-structure bridge
**Statement.** Some aspect of effective geometric regularity or dynamical persistence relates to compressibility/conditional description length of the underlying relational state:
\(L(\mathcal G\mid X)\ll L(\mathcal G)\) or a rate–distortion relation.
**Status:** `DRAFT` / `SPECULATIVE`. **Why included:** connects to AIT/MDL without treating Kolmogorov complexity as directly observable. **(v0.2)** Explicitly flagged as the researcher's comparative-advantage branch (see §8 note); its priority is a standing decision (ADR candidate E), not a settled demotion.
**Kill criteria:** arbitrary encoding dependence; no physically meaningful distortion; nothing beyond ordinary effective-theory compression.

---

## 4. Bridge hypotheses — the likely locus of original contribution

### BH-001 — Relative-information → geometric-response bridge
A distinguishability functional \(D(\rho\Vert\sigma)\) controls a geometric response \(\Delta G\) through a relation stronger than a one-off holographic identity. Sources: TH-008–TH-010, TH-029.
**Target:** identify the abstract axioms actually used: monotonicity, first-law variation, modular flow, locality/algebra inclusion.

### BH-002 — Reconstruction-front dynamics
Time-dependent reconstructable algebra \(\mathcal A_R(t)\); geometric transitions characterized by algebra change rather than a scalar entropy: \(\mathcal A_R(t^-)\subsetneq\mathcal A_R(t^+)\). Motivation: TH-015–TH-017.
**Potential novelty:** replacing "information flow" with algebraic growth/relocation of reconstructability.

### BH-003 — Information-dynamical continuity without a local current
A conservation/consistency law on channels, algebras, or correlations rather than a spacetime vector current: \(\mathfrak I[X(t)]=\text{invariant}\) while subsystem measures vary.
**Value:** formalizes "information does not stop" without the fluid metaphor.

### BH-004 — Stationary geometry from nonstationary relational microdynamics
Toy model with \(X(t)\neq X(0)\), \(\Phi[X(t)]=g_*+O(\epsilon)\), where the microdynamics is witnessed (CON-034) and the stationarity is *sustained-by* rather than merely compatible (CON-036).
**Status:** `STABLE` / `PLAUSIBLE` **(v0.5, owner ruling 2026-08-13:** SPECULATIVE → PLAUSIBLE on the adversarially-corrected AR-010/AR-011 record — replicated in-model support for the sustained-by clause (switch-off geometry change; criterion (b)); the witnessed-stationarity leg remains open pending AR-020. This ruling covers BH-004 only; HYP-009's geometric part stays `SPECULATIVE`.**)**
**Purpose:** convert HYP-009's geometric question into an explicit model. **(v0.2)** \(\Phi\) should preferentially be the mutual-information-graph metric of TH-037 to avoid hand-coding geometry; the model family and success metric are specified in KB-005 Track E3. **This is the programme's first deliverable (ADR-002).**
**Null comparator:** ordinary phase evolution producing no physically meaningful microdynamic change; and stationarity that persists when the dynamics is switched off (compatible-with, not sustained-by).
**(v0.3, corrected v0.4) Evidence note — AR-010 confirmatory + AR-011
adversarial (2026-08-12/13, `ar/AR-010_confirmatory-2026-08-12.md`,
`ar/AR-011_adversarial-2026-08-13.md`; epistemic status unchanged —
promotion is now an owner decision on the adversarially-corrected
record).** Outcome of record after AR-011:
(1) the *sustained-by* clause has in-model support on corrected
grounds — the geometry the dynamics maintains is NOT the geometry the
motionless (dephased) state holds: switch-off moves Φ by 43–90% of
‖D̄‖ per class (floor-free), and criterion (b) — the class-resolved
robustness differential — HOLDS with two-size replication in both
tracks. The v0.3 phrasing "the stationary comparator is far more
fragile" was an instrument artifact (floored denominator) and is
withdrawn; the comparator's absolute response is smaller. No Φ-matched
motionless comparator exists in the family as designed (§4.1 matching
assumption refuted — MI nonlinearity); constructing one, or proving it
impossible, is an AR-020 requirement. Stationary-with-witness regimes
exist (chaotic/scrambling 20/20; T-B DTC ε = 0.03 100/100).
(2) Criterion (a) FAILS on one pair (scrambling|localized) after W3 was
discarded by the preregistered §4.4 null test (the OTOC fires on the
frozen null — not a valid CON-034 witness as instantiated) — witness
scheme to FORMALIZE per spec §5.4 (SC-005; → AR-020). Metastable Ξ
margins are tolerance-robust (AR-011 Attack B).
(3) Φ's partition-dependence is quantified at 9–20% (nonlocal two-site
frames) — same order as ε_Φ = 0.25; Φ is a geometry of the posited
factorization, not of the state alone (TH-037 caveat now quantitative;
standing scope wall).
(4) T-B: switch-off resolves compatible-with for the DTC regime (W5
collapses, Φ persists — MBL holds the pattern without the drive);
rigidity ε_c > 0.20 (bound); r2 comparator prethermal at 200 periods.

### BH-005 — Recurrence as an emergent-stability mechanism
Within a successful BH-004 model, test whether recurrence/limit-cycle/quasiperiodicity — including a driven/Floquet regime modeled on TH-033 — provides robustness unavailable to fixed-point/invariant-subspace alternatives. **Only proceed if BH-004 survives.** This is HYP-005's proving ground.

### BH-006 — Complexity/entropy complementarity
Two information variables: entropy-like (accessible correlations/coarse-graining) and complexity-like (continued microscopic evolution); phase portrait \((S(t),\mathcal C(t))\) where \(S\) saturates while \(\mathcal C\) evolves. Motivation: TH-019 and the interior/complexity literature.
**Value:** a precise expression of "the process keeps going even when a coarse observable looks stationary."

### BH-007 — Clock/phase–geometry seam (added v0.2)
**Statement.** Investigate whether the universal coupling of gravity to internal clock rates (TH-035) and the clock-makes-entropy-well-defined structure of crossed products (TH-031) are two faces of one seam: operationally, effective geometry as the bookkeeping of relative internal-phase/modular-flow rates across subsystems.
**Weakest form (kinematic):** reconstruct metric/redshift data from relative clock-rate assignments — plausibly a re-derivation of standard results (HYP-000 risk explicitly high).
**Stronger form (structural):** show that consistency conditions on a family of internal/modular clocks constrain the effective geometry beyond re-description.
**Clock:** the hypothesis is *about* clocks; CON-035 typing is part of its statement.
**Motivation:** ADR-001's kinematic reading; TH-031/TH-032/TH-035.
**Kill conditions:** the weakest form is exactly equivalent to standard GR kinematics with no invariant surplus (KC-001); or no consistency condition on clock families exists that is not already the Einstein equations by assumption.
**Sequencing:** AR-016 (audit) must precede any formal investment; this bridge does not gate the toy models.

---

## 5. Hypothesis dependency graph

```text
HYP-000  descriptive null ──────────── challenges every other hypothesis (incl. HYP-009 via KC-007)

HYP-001  relational geometry constraint
   └──> HYP-002  dynamical bridge
            └──> HYP-003  autonomous information dynamics  [internal clock now mandatory]

HYP-004  persistent structure is dynamical (single-level)
   └──> HYP-009  cross-level dynamical persistence (CLDP)  [faithful INT-001 form]
            ├── sub-geometric part: GROUNDED (TH-033/034/035; census AR-015)
            └── geometric part: SPECULATIVE ──> HYP-005 recurrent/oscillatory specialization
                                                   └── proving ground: BH-004 → BH-005

HYP-006  black-hole redistribution ──> BH-002, BH-003
HYP-007  complexity dynamics ──> BH-006
HYP-008  algorithmic/MDL bridge  (comparative-advantage branch; priority = ADR candidate E)
BH-007   clock/phase–geometry seam  (from ADR-001 kinematic reading; gated on AR-016)
```

No downstream hypothesis may be treated as supported merely because its parent is supported. **(v0.2)** Conversely, HYP-009's sub-geometric grounding may not be cited as support for its geometric part.

---

## 6. Prediction / discriminant template

Every `HYP-*` promoted to `FORMALISED` must answer:

```text
Hypothesis ID:
Precise statement:
State space / objects:
Dynamics:
Clock type (CON-035):            # v0.2
Level(s) and witness(es) (CON-022/034), if recurrence is involved:   # v0.2
Gauge / equivalence relation:
Framework assumptions:
Baseline/null model:
Quantity that differs from baseline:
Derivation or simulation protocol:
Falsifier:
Known limiting cases:
Primary sources:
Open mathematical gaps:
```

A hypothesis with no baseline difference remains conceptual even if expressed with equations.

---

## 7. Adversarial checklist

For each candidate bridge, an adversarial run must ask:

1. Is this already a known theorem under different notation?
2. Did we hide geometry in the definition of the information variable?
3. **Did we hide time in the dynamics — what clock is assumed, and is it available without the target geometry?** (v0.2)
4. Did we hide the target dynamics in the reconstruction map?
5. Is the result invariant under basis, gauge, code, or subsystem changes?
6. Does the claim survive mixed states and finite-\(N\) corrections?
7. Is it specific to AdS boundary factorization?
8. Can a conventional quantum channel reproduce the same result with no new principle?
9. Are we confusing correlation with causation — specifically, sustained-by with compatible-with (CON-036)? (v0.2 sharpened)
10. Does coarse-graining create the apparent arrow/dynamics?
11. If recurrence is invoked: what level, what witness, and what excludes a fixed point, random recurrence, or quasinormal ringing (TH-036)? (v0.2 sharpened)
12. Could an exactly stationary state satisfy the same observables, making "ongoing dynamics" unidentifiable?
13. What concrete result would make us abandon the hypothesis?

---

## 8. Current hypothesis ranking for research effort (revised v0.2)

**Effort priority, not truth probability.** Revised per ADR-002 (first deliverable = toy-model family) and the comparative-advantage principle: early effort concentrates where (a) the work is bounded and falsifiable-in-parts and (b) the researcher's toolkit (dynamical systems, state-space methods, coarse-graining, MDL) gives leverage, while retaining one verification anchor in the strongest external mathematics.

| Priority | Item | Reason |
|---|---|---|
| **P0** | **BH-004 / Track E3 toy-model family** | first deliverable (ADR-002); directly tests HYP-009's geometric part; bounded; toolkit-aligned |
| **P0** | **AR-015 cross-level census** (HYP-009 sub-geometric) | second deliverable (SC-006); low-risk; establishes witness discipline; feeds the toy models |
| **P0** | AR-003 / BH-001 relative-information → geometric response | strongest external mathematical foothold; the verification anchor |
| **P0** | AR-005 / BH-002 reconstruction-front dynamics | captures redistribution without local-flow assumptions |
| P1 | AR-016 / BH-007 clock/phase–geometry audit | ADR-001 kinematic reading; cheap audit before any formal bet |
| P1 | AR-017 / TH-031–032 algebra & thermal-time verification | modern rigorous home of CAND-002; feeds clock discipline |
| P1 | BH-006 entropy/complexity complementarity | natural handle on post-saturation dynamics |
| P1 | HYP-006 black-hole redistribution generality | strong controlled evidence; test generality |
| P1 | BH-005 / HYP-005 recurrence mechanism | now *reachable through* BH-004 rather than deferred behind five gates; still gated on BH-004 survival |
| P2 | HYP-003 autonomous dynamics | too strong before bridge work; internal-clock requirement added |
| P2 | HYP-008 algorithmic/MDL bridge | high invariance burden; **priority to be re-decided at ADR candidate E after first toy-model results** — not a settled demotion |
| P3 | HYP-005 beyond toy models (gravitational frameworks) | after BH-004/BH-005 outcomes exist |

**(v0.2 note on the v0.1 ranking.)** v0.1 placed all P0 effort on holography-verification territory and deferred the researcher's distinctive branches (recurrence to P3, MDL to P2 with an exit ramp). That allocation optimized evidential footing but minimized both comparative advantage and fidelity to INT-001. The revised table keeps one strong verification anchor (AR-003/BH-001) while making the intuition-testing toy models the lead item.

---

## 9. What would count as a genuinely interesting first paper? (revised v0.2)

Not "information is fundamental." Narrow and formal candidates, now ordered by ADR-002:

1. **The toy-model family paper (first deliverable).** *Stationary emergent geometry from witnessed nonstationary microdynamics:* finite models where an MI-graph metric (TH-037) is stationary while microdynamics is invariantly witnessed; comparison of fixed-point, quasiperiodic, chaotic, metastable, and driven/Floquet classes; identification of when stationarity is sustained-by vs compatible-with; a robustness differential (or its absence) across classes. Honest negative results included by design.
2. **The cross-level census (second deliverable).** Established persistence-through-dynamics instances, each with level, clock, witness, and null comparator; the invariant-witness criterion as an organizing contribution; the geometric rung posed sharply as an open problem.
3. **A reconstruction-algebra formulation of black-hole information redistribution** unifying Page-transition language and exposing what "flow" can and cannot mean.
4. **A theorem/no-go result** on minimal axioms under which an information variation law implies a geometric constraint.
5. **An entropy–complexity two-coordinate dynamical model** showing when entropy is insufficient.
6. **A rate–distortion / MDL formulation of emergent geometry** with explicit representation invariance (if ADR candidate E promotes HYP-008).

The first publishable result should be the smallest one that survives HYP-000.

---

## 10. Changelog v0.1 → v0.2

1. Added HYP-009 (CLDP) — the faithful, level-indexed formalization of INT-001's cross-level claim (ADR-001), with sub-geometric part `GROUNDED` on TH-033/034/035 and geometric part `SPECULATIVE`; added KC-007 linkage.
2. Rewrote HYP-005 as the geometric-level specialization of HYP-009 with a per-level witness ledger and quasinormal-ringing null comparator; unwound the v0.1 "Planck-scale subset, defer to P3" framing.
3. Added BH-007 (clock/phase–geometry seam) from ADR-001's kinematic reading.
4. Added mandatory clock declaration to all hypotheses; made an internal clock a promotion requirement for HYP-003; added checklist item 3 (hidden time) and sharpened items 9 and 11.
5. Extended BH-004 with the TH-037 emergent-metric functional, the sustained-by requirement, and its ADR-002 first-deliverable status; BH-005 gains a driven/Floquet regime.
6. Corrected status-vocabulary misuse (HYP-001, HYP-006: "GROUNDED as a direction" → `PLAUSIBLE` + citations); reserved epistemic vocabulary per KB-001 §6.1; fixed "most strongest" typo by rewrite.
7. Revised §8 priority table per ADR-002 and comparative advantage; recorded the rationale for departing from the v0.1 allocation; HYP-008 demotion converted from default to open decision (ADR candidate E).
8. Revised §9 first-paper list: toy-model family first, census second.
9. Added CON-036 sustained-by/compatible-with discipline to HYP-004, BH-004, and the checklist; extended the discriminant template with clock and level/witness fields.
