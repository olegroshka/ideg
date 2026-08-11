---
id: KB-001
title: "IDEG Research Charter — Information Dynamics and Emergent Geometry"
status: DRAFT
owner: shared
last_reviewed: 2026-08-11
version: 0.3
research_layer: R0
epistemic_status: NOT_APPLICABLE
sources:
  - "https://github.com/olegroshka/shared-substrate (accessed 2026-08-11)"
  - "https://doi.org/10.2139/ssrn.7218019 (accessed 2026-08-11)"
depends_on: []
referenced_by: [KB-002, KB-003, KB-004, KB-005]
changelog:
  - "0.1: initial substrate (drafted with Sol/ChatGPT, 2026-08-11)"
  - "0.2: review revision (drafted with Claude, 2026-08-11) — see §15"
  - "0.3: mechanical fix at G0 owner review (2026-08-11): SC-002 pointer §§N–O → §§C, M, O; applied under KB-005 §12 mechanical-fix rule, no intent change — see §16"
---

# IDEG Research Charter

> **Working title:** *Information Dynamics and Emergent Geometry (IDEG)*
> **Status:** research-initiation substrate; the title, ontology, and hypotheses are provisional.
> **Centroid rule:** this file owns the enduring research intent and scope. It must not be silently rewritten to match whatever later mathematics happens to work. The originating intuition is preserved **verbatim** in §3.0 (INT-001); all decompositions and reformulations elsewhere are interpretations of that record and must remain traceable to it.

## 1. Purpose

This research programme investigates whether the repeated appearance of information-theoretic structure in gravitational physics is merely a useful description of known dynamics, or evidence for a deeper relation in which effective geometry and gravitation are constrained by — or emerge from — an underlying dynamical relational/information structure.

The programme deliberately begins **below** the claim that "reality is information" and below the claim that "everything oscillates." Those may be philosophical or later physical interpretations, but they are not admissible starting assumptions.

The immediate research targets are:

> **RQ-001 — Primary research question.**
> Can gravitational or spacetime dynamics be related to a precisely defined information-dynamical structure by a non-metaphorical mathematical bridge that either (a) derives or constrains known gravitational behaviour, or (b) produces a discriminating consequence not already contained in the underlying quantum/gravitational framework?

> **RQ-013 — Cross-level persistence question (added v0.2).**
> Established physics exhibits, at several distinct levels of description, persistent structures that are sustained by — not merely compatible with — nontrivial underlying dynamics, sometimes with an invariant clock-like or recurrent character (see KB-003 §O). Does this *persistence-through-dynamics* pattern continue at the level of effective geometry and gravitation, in a form that constrains or predicts something, or does it terminate below that level?

A useful schematic target remains

\[
\mathcal I(t) \longleftrightarrow \mathcal G(t),
\]

where \(\mathcal I\) is not yet assumed to be a scalar "amount of information," and \(\mathcal G\) is not yet assumed to be the metric alone. Both sides may be relational, algebraic, geometric, or coarse-grained structures.

---

## 2. Research object

The research object is **the relation between dynamical information structure and emergent/effective gravitational geometry**, studied as the top rung of a cross-level pattern: persistent structures sustained by underlying dynamics, examined level by level with explicit invariance controls.

Black holes are an important stress test because they make entropy, information recovery, horizons, locality, and quantum gravity collide sharply. They are **not** the entire research object.

Candidate physical arenas include:

- black-hole formation and evaporation;
- holographic entanglement and bulk reconstruction;
- gravitational equations derived from entanglement or thermodynamic constraints;
- quantum extremal surfaces and islands;
- scrambling and information recoverability;
- complexity/geometry proposals;
- operator-algebraic formulations (modular/thermal time, crossed products);
- internal-clock/phase structure of massive systems and its coupling to gravity;
- established non-gravitational exemplars of persistence-through-dynamics (hadronic mass, driven time crystals) **as structural templates only**;
- non-holographic and asymptotically flat quantum gravity;
- Planck-scale endpoint proposals only as one branch of the landscape;
- eventually, cosmological or weak-field settings if a formal bridge survives the earlier stages.

---

## 3. Initial motivating observations

### 3.0 INT-001 — Originating intuition, verbatim (primary source; added v0.2)

The programme was triggered by an X post claiming a "Yukawa/Markov/Hawking" result that Hawking evaporation halts at the Planck mass leaving stable remnants (provenance audited in KB-003 TH-026–TH-028: no such joint result exists). The researcher's response to that post, recorded verbatim as the primary source of the programme's intent:

> "Well.. why do I think that information flow doesn't really stop it's dynamic in nature.. yes there is some oscillating process o[n] every level of persever[ed] reality including black holes.. extremely hard to observe I guess with the level of our tech ...but what the advanced information gravity theories currently say on this?"

Three features of INT-001 that any faithful decomposition must preserve:

1. the claim is about **every level** of persistent reality, not only black holes or the Planck scale;
2. the intuition asserts a **real physical process** ("extremely hard to observe... with the level of our tech"), not a metaphor or representation choice;
3. "oscillating" and "dynamic" are both present; their relation is left open by the source and must be resolved by explicit decision (ADR-001, §13), not by silent paraphrase.

Additional context: the researcher has prior (unrecorded) conversation threads on (a) information as potentially more fundamental than the spacetime description and (b) an algorithmic-information/MDL toolkit. These inform HYP-008 and the ontological deferrals but have no primary-source record inside this substrate; if they become load-bearing, they must be reconstructed and recorded first.

### OBS-001 — Information and geometry repeatedly meet in controlled theory

Established and semi-established frameworks contain nontrivial relations among: horizon area and entropy; boundary entanglement entropy and bulk extremal-surface area; relative entropy and bulk relative entropy; entanglement first laws and linearized gravitational equations; entanglement wedges and reconstructability of bulk information; generalized entropy, quantum extremal surfaces, islands, and Page curves; scrambling and recoverability in unitary quantum systems; thermodynamic derivations of the Einstein equations.

These are not all the same statement. Their recurrence motivates asking whether a deeper common structure exists.

### OBS-002 — Black-hole evaporation need not be represented as "information stored until the end"

Modern unitary pictures make it natural to describe evaporation through **scrambling, correlation, re-encoding, and changing reconstructability**. In island calculations, a region that semiclassically looks like an interior can enter the entanglement wedge of radiation. That is conceptually different from a literal local packet of information crossing a horizon.

### OBS-003 — A macroscopic steady object need not imply microscopic stasis

A stationary or persistent effective structure can coexist with nontrivial underlying unitary evolution, phase evolution, scrambling, recurrence, or motion within an invariant subspace. "Stable" and "static" must be kept distinct.

### OBS-004 — Persistence-through-dynamics is already established physics at several levels (added v0.2)

This is not merely a possibility (OBS-003) but an observed pattern with concrete instances: quantum phase evolution and internal Compton clocks of massive systems; the dominantly dynamical origin of hadronic mass in QCD; driven (Floquet) time crystals, whose defining subharmonic response is an **invariant, measured order parameter** and therefore not removable by representation choice; thermal/modular time, where an equilibrium state *defines* a flow rather than lacking one. See KB-003 §O for the audited claims. OBS-004 grounds the lower rungs of RQ-013 in E2–E4 physics; it does **not** by itself establish anything about the geometric rung (see NC-009).

---

## 4. Originating intuition — decomposed

INT-001 bundles several logically distinct claims. It is decomposed into:

1. **Weak dynamical claim:** physical quantum information participates in continuous state evolution and relational change.
2. **Redistribution claim:** in black-hole evaporation, information can become encoded/reconstructable in radiation rather than remaining localized in a terminal object.
3. **Geometry claim:** some effective geometric structure may be determined or constrained by information relations.
4. **Dynamics claim:** changes in information structure may constrain or generate changes in effective geometry.
5. **Persistence claim:** persistent macroscopic structures may correspond to invariant, metastable, attractor-like, recurrent, or otherwise dynamically stable structures in the deeper description.
6. **Cross-level claim (restated v0.2):** the persistence-through-dynamics pattern holds **at every level** of the abstraction ladder, each level exhibiting at least one invariant witness (clock, recurrence, or activity observable) of the sustaining dynamics at the level below; the open scientific question is whether the pattern continues at the geometric level. (This is the level-indexed reading of "oscillating process on every level"; researched as HYP-009 in KB-004.)
7. **Ontological claim:** information dynamics is more primitive than spacetime/matter.

Claims 5–7 are progressively stronger. **No later work may use the weak claims as if they establish the strong ones.** Note the v0.2 change: claim 6 is no longer "a subset of persistent structures may be periodic" (a demotion that entered v0.1 without decision); it is the cross-level claim actually present in INT-001, with periodicity per level subject to the invariant-witness requirement (CON-034).

---

## 5. Explicit non-claims

### NC-001 — No primitive-information assumption
We do **not** assume that "information" is a substance or the ultimate ontology.

### NC-002 — No entropy equivalence
We do **not** equate Shannon entropy, von Neumann entropy, entanglement entropy, relative entropy, mutual information, algorithmic complexity, or circuit complexity.

### NC-003 — No local-current assumption
We do **not** assume that information has a local conserved current
\[
\partial_t \rho_I + \nabla \cdot J_I = 0.
\]
Entanglement and reconstructability are intrinsically nonlocal in many quantum settings; the correct primitive may be relational rather than current-like.

### NC-004 — No universal-oscillation assumption
Dynamics does not imply periodicity. Oscillation, recurrence, fixed points, metastability, chaotic mixing, and monotonic coarse-grained evolution are different possibilities. Periodicity claims are admissible only level-by-level with an invariant witness (CON-034).

### NC-005 — No remnant assumption
We do **not** assume Hawking evaporation stops at the Planck mass. Planckian remnants are a live class of proposals, not a settled prediction of quantum gravity.

### NC-006 — No universal extrapolation from AdS/CFT
A result proved in AdS/CFT, JT gravity, a tensor-network code, or an ensemble-averaged model cannot silently be promoted to a universal statement about 3+1-dimensional asymptotically flat gravity.

### NC-007 — No "reconstruction = transport" shortcut
If an operator becomes reconstructable from radiation, this does not by itself establish a literal local trajectory of a conserved information fluid.

### NC-008 — No metaphysics by vocabulary
Using words such as "emergent," "encoded," or "information" does not itself establish ontological priority.

### NC-009 — No significance-by-universality (added v0.2)
The universal quantum phase evolution of massive systems (Compton/de Broglie clocks) is established physics and makes a *kinematic* reading of "everything oscillates" almost trivially true. Its truth at the kinematic level is **not** evidence for the structural claim (persistent structures = recurrent modes of a deeper dynamics) or the ontological claim, and does not by itself establish that phase structure is load-bearing for geometry. The interesting question is whether gravity's universal coupling to internal clocks (KB-003 TH-035) is constraint or decoration; that question must be argued, not assumed.

### NC-010 — No hidden clock (added v0.2)
Any statement of the form "\(X(t)\) evolves" or "\(\dot X = F[X]\)" implicitly assumes a time parameter. In quantum gravity, time is not available for free (Hamiltonian constraint; problem of time). We do **not** assume an external clock; every dynamical claim must state its clock (external, relational, modular/thermal, or emergent) or be marked clock-deferred. See CON-035.

---

## 6. Epistemic levels

| Level | Name | Typical statement | Oracle / check |
|---|---|---|---|
| EL-0 | Conceptual | "Perhaps persistence is dynamic rather than static." | semantic coherence; counterexamples |
| EL-1 | Mathematical object | "Use mutual information / relative entropy / a channel / an algebra." | definitions; dimensional and algebraic consistency |
| EL-2 | Framework result | "In framework F, quantity X equals/constrains geometry Y." | primary-source derivation; reproduction |
| EL-3 | Bridge principle | "A class of information dynamics determines a class of effective geometries." | theorem, derivation, or explicit countermodel |
| EL-4 | Physical model | "The bridge predicts behaviour Z for black holes/cosmology." | simulation, consistency with known limits |
| EL-5 | Empirical consequence | "Observable O differs from baseline by Δ." | data / experiment / observation |

**Guardrail:** a claim at EL-2 does not automatically justify EL-3 or EL-4.

### 6.1 Status-system crosswalk (added v0.2)

The substrate uses four labelling systems for different questions. They are related but not interchangeable; the approximate correspondence, to prevent drift:

| Question | System | Values | Rough alignment |
|---|---|---|---|
| At what abstraction level is the claim stated? | EL-0..EL-5 | see above | — |
| How strong is the evidence *within its scope*? | E0..E4 | KB-001 §7 | E2 ≈ demonstrated at EL-2 in a toy model; E3 ≈ derived at EL-2/EL-3 in a mature framework |
| How strongly do we hold *our* hypothesis? | SPECULATIVE → PLAUSIBLE → GROUNDED → FORMALISED → SUPPORTED (+CHALLENGED, REFUTED) | KB-004 §1 | FORMALISED requires an EL-3 statement with falsifier; SUPPORTED requires ≥E2 evidence for that statement |
| Is the artefact itself well-recorded? | MISSING → DRAFT → STABLE → STALE → DEPRECATED | KB-004 §1 | orthogonal to all of the above |

Only KB-004 §1 vocabulary may appear in a `HYP-*` `epistemic_status` field. Informal uses of these words in prose ("grounded as a direction") are prohibited (v0.1 defect, fixed).

---

## 7. Evidence-strength classes

| Class | Meaning |
|---|---|
| E0 | analogy, heuristic, or philosophical suggestion |
| E1 | explicit theoretical proposal with a defined mechanism |
| E2 | mathematically demonstrated in a toy/controlled model |
| E3 | derived in a mature theoretical framework under explicit assumptions |
| E4 | empirically constrained or observationally supported |

The same idea can have different evidence classes in different scopes. Example: an island formula can be E3 in a controlled semiclassical/holographic model but not thereby E3 as a universal statement about astrophysical black holes.

---

## 8. Research invariants

### INV-R-001 — Preserve null explanations
Every novel hypothesis must be compared against the strongest explanation in which the same phenomenon follows from standard quantum dynamics plus the existing gravitational framework.

### INV-R-002 — Separate kinematics from dynamics
A static mapping such as \(S \leftrightarrow A\) is not yet a dynamical law. The programme must distinguish information/geometry correspondence from information-driven geometric evolution.

### INV-R-003 — Preserve framework scope
Every theory result must record where it is valid: AdS/CFT, semiclassical gravity, JT gravity, string microstates, LQG-inspired models, asymptotically flat settings, condensed-matter/Floquet systems, etc.

### INV-R-004 — Preserve provenance
The desired provenance chain is \(\text{HYP-*} \rightarrow \text{TH-*} \rightarrow \text{SRC-*}\), with agentic investigations contributing evidence through `AR-*` records rather than directly rewriting canonical claims. **(v0.2)** The chain now begins one level higher: interpretive claims about the programme's own intent trace to INT-001.

### INV-R-005 — Ontology remains provisional
The ontology in KB-002 is a working semantic firewall, not a declaration of what fundamentally exists.

### INV-R-006 — Prefer the weakest nontrivial claim
When several formulations fit the same intuition, formalize the weakest version that would still represent genuine scientific content.

### INV-R-007 — Novelty requires extra constraint
A re-description is valuable but not yet a new physical principle. A candidate bridge becomes scientifically stronger if it: derives a known gravitational law from fewer/different assumptions; unifies results previously requiring unrelated constructions; excludes physically possible states allowed by the baseline theory; predicts a new relation or observable; or yields a computationally useful invariant not implicit in the original formalism.

### INV-R-008 — Level and witness discipline (added v0.2)
Every persistence or oscillation claim must state (a) the abstraction-ladder level(s) at which it is asserted (KB-002 §2) and (b) the invariant witness (CON-034) that makes it representation-independent at that level, or explicitly record that no witness is yet identified.

### INV-R-009 — Clock discipline (added v0.2)
Every dynamical claim must state its clock (NC-010, CON-035). "Did we hide time in the dynamics?" joins "did we hide geometry in the information variable?" as a mandatory adversarial question (KB-004 §7).

---

## 9. Success criteria

The programme does **not** need to establish a "theory of everything" to succeed.

### SC-001 — Semantic success
A stable distinction among state, entropy, correlation, complexity, transfer, flow, reconstructability, geometry, emergence, persistence, and recurrence.

### SC-002 — Landscape success
A verified map of the strongest existing information↔gravity relations, including assumptions and non-implications — now explicitly including the thermodynamic-gravity lineage, algebraic/modular formulations, and the cross-level persistence exemplars (KB-003 §§C, M, O).

### SC-003 — Synthesis success
Identification of a recurring mathematical structure across multiple frameworks that is not merely shared terminology.

### SC-004 — Formal success
At least one bridge hypothesis stated with explicit mathematical objects, assumptions, clock, and falsifiers.

### SC-005 — Research success
At least one of: proof/derivation of a nontrivial bridge; explicit no-go result showing why a tempting bridge cannot work; toy model demonstrating a discriminating dynamical effect; principled reduction of the hypothesis space; new measurable consequence. A rigorous negative result is a successful outcome.

### SC-006 — Census success (added v0.2)
A literature-verified cross-level census of persistence-through-dynamics instances, each with its invariant witness and its null comparator, terminating in a sharply posed statement of the open geometric rung. This is a standalone publishable outcome even if all stronger hypotheses die.

---

## 10. Kill / downgrade criteria

### KC-001 — Pure relabelling
Every proposed information-dynamical law is exactly equivalent to ordinary quantum evolution plus an invertible change of variables and adds no constraint, compression, explanatory unification, or prediction.

### KC-002 — Measure dependence destroys physical content
The claimed geometry relation depends arbitrarily on representation/encoding choices with no invariant formulation.

### KC-003 — Local-flow requirement is inconsistent
If the hypothesis requires a conventional local information current but controlled quantum-gravity models exhibit essential nonlocal reconstructability incompatible with such a current, that formulation is rejected.

### KC-004 — Holographic overreach
If the bridge only exists because of special AdS boundary structure and cannot be reformulated meaningfully outside that setting, any universal version is rejected.

### KC-005 — Level-indexed witness failure (revised v0.2)
The recurrence/oscillation component is killed **at a given level k** if no invariant witness (CON-034) exists at that level — i.e., if every candidate oscillation at level k is removable by phase/gauge/frame/representation choice or contributes no invariant consequence. Killing at one level does not kill other levels: driven time crystals demonstrate that the witness bar is passable at at least one physical level (KB-003 TH-033), while the geometric level remains open. The **global** oscillatory hypothesis (all levels) dies only if the geometric-level witness search fails *and* no cross-level pattern with explanatory content survives; the broader dynamical programme may survive either way.

### KC-006 — No common structure
If the candidate bridges across RT/JLMS/entanglement-equilibrium/islands/complexity/thermodynamic-gravity are mathematically unrelated beyond loose analogy, the "single deep information principle" hypothesis is downgraded.

### KC-007 — Cross-level triviality (added v0.2)
If the cross-level persistence pattern (HYP-009) reduces at every level to "quantum systems evolve," with no level exhibiting a witness that constrains, predicts, or excludes anything at the level above it, HYP-009 is downgraded to a pedagogical organizing device and removed from the hypothesis space.

---

## 11. Scope boundaries for initiation

### In scope now
- quantum information notions used in gravity;
- black-hole information and evaporation;
- holographic entropy/reconstruction; information-to-Einstein-equation derivations; generalized entropy/QES/islands; scrambling and recoverability;
- thermodynamic derivations of gravitational dynamics (Jacobson 1995 lineage) and entropic-gravity programmes as landscape entries;
- operator-algebraic structure: modular flow, thermal time, crossed products, algebraic generalized entropy;
- internal-clock/phase structure of matter and its measured coupling to gravity (with contested interpretations recorded as contested);
- non-gravitational persistence-through-dynamics exemplars (QCD mass, time crystals) as structural templates with explicit scope walls;
- complexity/geometry as a candidate dynamical seam;
- endpoint alternatives: complete evaporation, remnants, black-to-white-hole transitions, fuzzball/microstate pictures;
- mathematical candidates for dynamical relational structures;
- algorithmic-information ideas only with explicit representation-dependence controls.

### Deferred
- claims that consciousness or observers are necessary to the dynamics;
- cosmological natural selection; simulation hypotheses;
- generic "it from bit" metaphysics without a mathematical bridge (this includes the ontological reading of INT-001; see ADR-001);
- phenomenology of specific remnant dark-matter models unless required by a surviving hypothesis;
- experimental proposals before a model reaches EL-4.

---

## 12. Initial research questions

- **RQ-002:** What is the weakest information object capable of supporting a geometry bridge: entropy scalar, correlation matrix, operator algebra, channel, tensor network, information metric, complexity measure, or something else?
- **RQ-003:** Is "flow" the wrong primitive? Would evolution, redistribution, re-encoding, modular flow, or changing reconstructability be more invariant?
- **RQ-004:** Which existing information↔geometry relations are kinematic, and which genuinely constrain dynamics?
- **RQ-005:** Can the entanglement-first-law / relative-entropy route be abstracted beyond holographic CFTs?
- **RQ-006:** Is there a common mathematical skeleton behind RT/HRT, JLMS, entanglement equilibrium, islands, complexity proposals, and the thermodynamic-gravity derivations?
- **RQ-007:** Can a persistent physical structure be represented as an invariant set, fixed point modulo phase, limit cycle, quasiperiodic orbit, metastable code subspace, or attractor in a meaningful information state space?
- **RQ-008:** Does the oscillatory idea survive, level by level, after gauge, phase, and representation redundancies are removed — i.e., which levels possess an invariant witness (CON-034)?
- **RQ-009:** Does algorithmic complexity add anything physically invariant beyond entropy/circuit complexity in gravitational dynamics?
- **RQ-010:** What would make an information-dynamical theory empirically distinguishable from standard quantum gravity descriptions?
- **RQ-011:** How much of the black-hole "information flow" story is literal transfer versus changed subsystem reconstruction?
- **RQ-012:** Can any surviving bridge be formulated for asymptotically flat 3+1-dimensional gravity?
- **RQ-013:** (§1) Does the persistence-through-dynamics pattern continue at the geometric level?
- **RQ-014:** (added v0.2) What clock does each candidate information dynamics use, and can modular/thermal time supply a clock that is internal to the information structure rather than imported from a background spacetime?

---

## 13. Decisions of record (added v0.2)

### ADR-001 — Intended reading of the oscillation intuition
**Decision (2026-08-11):** INT-001 is to be read as a **mix of the kinematic and structural readings, asserted across all levels of persistent structure**, with the geometric level as the open research target:
- *Kinematic reading (in scope):* real, universal phase/clock dynamics of quantum systems, with the research question being whether that structure is load-bearing for geometry (NC-009 guards against significance-by-universality).
- *Structural reading (in scope):* persistent structures correspond to dynamically sustained — including recurrent/limit-cycle — modes of an underlying dynamics, level by level, subject to the invariant-witness requirement.
- *Ontological reading (deferred):* oscillation/information as the primitive substrate remains excluded from admissible starting assumptions (NC-001, NC-008) and deferred per §11.

**Context:** v0.1 silently encoded only a demoted structural reading ("a subset of persistent structures"), scoped only to gravitational/Planck structures; that reformulation entered in the first drafting session without an explicit decision. This ADR restores the source intent and the scope, with the invariance discipline retained.

### ADR-002 — First deliverable
**Decision (2026-08-11):** The programme's first deliverable is a **small family of computational toy models** (Track E3 in KB-005, serving BH-004/HYP-009): finite, fully understandable systems in which a coarse-grained "geometric" functional is (approximately) stationary while the microstate is provably nonstationary, comparing dynamical classes (fixed point, quasiperiodic, chaotic, metastable, driven/Floquet) and asking whether an invariant witness distinguishes them **and** whether the emergent functional's robustness differs by class. The cross-level census (AR-015, SC-006) is the second deliverable and may proceed in parallel at low intensity. Rationale: bounded, falsifiable-in-parts, aligned with the researcher's dynamical-systems/state-space/MDL toolkit, and valuable independently of community reception. The heavy holographic verification programme (Phase B) is scoped to what these deliverables and the P0/P1 bridges actually cite (KB-005 Gate G2 revision).

Future ADRs use IDs ADR-003+ and live here; KB-005 §15 holds the open ADR candidates.

---

## 14. Research posture

\[
\boxed{\text{question} \rightarrow \text{concepts} \rightarrow \text{verified theory} \rightarrow \text{hypotheses} \rightarrow \text{formal tests}}
\]

not

\[
\boxed{\text{intuition} \rightarrow \text{search for supporting quotations}}.
\]

The project should become **more precise and potentially less grand** as it matures. A shrinking hypothesis that survives pressure is progress. **(v0.2 addendum)** The converse discipline also applies: the project must not become *smaller than its own question* by silently discarding the parts of INT-001 that are hardest to formalize. Narrowing is legitimate only through recorded decisions (ADRs), never through paraphrase.

## 14a. Dependency map

- `KB-001` (this charter) owns intent (INT-001), scope, non-claims, decisions of record, and success/kill criteria.
- `KB-002` owns terminology and the provisional ontology.
- `KB-003` owns established/contested theory claims and the canonical bibliography (`SRC-*`).
- `KB-004` owns our hypotheses (`HYP-*`, `BH-*`) and their falsifiers.
- `KB-005` owns execution, agentic research protocol, research gates, and the `AR-*` backlog.

No other file should restate the full charter; cite `KB-001` by stable ID. The namespace `OQ-*` is **reserved but unused** in v0.2; open questions are tracked as `RQ-*` here and as `AR-*` operations in KB-005 (v0.1 dangling reference, fixed).

---

## 15. Changelog v0.1 → v0.2

1. Added §3.0 INT-001: verbatim originating intuition as immutable primary source; recorded existence of unrecorded prior-session context.
2. Added OBS-004 (persistence-through-dynamics as established physics at several levels).
3. Restated decomposition claim 6 as the level-indexed cross-level claim actually present in INT-001 (v0.1's "subset may be periodic" demotion reversed; invariance discipline retained via CON-034/INV-R-008).
4. Added NC-009 (no significance-by-universality), NC-010 (no hidden clock).
5. Added INV-R-008 (level/witness discipline), INV-R-009 (clock discipline); extended INV-R-004 provenance to intent.
6. Revised KC-005 to a per-level witness test; added KC-007 (cross-level triviality).
7. Added RQ-013 (cross-level persistence), RQ-014 (clock question); extended RQ-006/RQ-008.
8. Added §6.1 status-system crosswalk; prohibited informal status vocabulary.
9. Added SC-006 (census success); extended SC-002 scope.
10. Added §13 Decisions of record: ADR-001 (reading of INT-001), ADR-002 (first deliverable = toy-model family).
11. Scope: added thermodynamic-gravity lineage, algebraic/modular structure, internal clocks, and non-gravitational exemplars; clarified that the ontological reading is deferred by decision.
12. Fixed dangling `OQ-*` reference (namespace reserved, unused).

---

## 16. Changelog v0.2 → v0.3

1. SC-002: corrected the section pointer "KB-003 §§N–O" → "KB-003 §§C, M, O" (§N is bibliography governance; the cited content lives in §C thermodynamic-gravity, §M algebraic/modular, §O persistence exemplars). Mechanical fix authorized at G0 owner review 2026-08-11 under the KB-005 §12 mechanical-fix rule; INT-001 and §§3–4 untouched.
