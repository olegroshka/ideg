---
id: KB-002
title: "IDEG Provisional Ontology and Conceptual Firewall"
status: DRAFT
owner: shared
last_reviewed: 2026-08-11
version: 0.2
research_layer: R1
epistemic_status: PROVISIONAL
sources:
  - "https://arxiv.org/abs/hep-th/0603001 (accessed 2026-08-11)"
  - "https://arxiv.org/abs/1512.06431 (accessed 2026-08-11)"
  - "https://arxiv.org/abs/1908.10996 (accessed 2026-08-11)"
depends_on: [KB-001]
referenced_by: [KB-003, KB-004, KB-005]
changelog:
  - "0.1: initial ontology (Sol/ChatGPT, 2026-08-11)"
  - "0.2: review revision (Claude, 2026-08-11) — see §9"
---

# Provisional Ontology and Conceptual Firewall

> **Ontology status: PROVISIONAL.**
> This file exists to prevent semantic drift while the research is young. It is not a claim that the listed objects are fundamental. If the research discovers a better ontology, changing this file is expected — but the change must be explicit because downstream hypotheses depend on it.

## 1. Why this file is load-bearing

The initiating intuition uses words that are dangerously overloaded: **information, flow, dynamics, geometry, emergence, stability, oscillation** — and, added in v0.2 with equal force, **time**.

A research programme can appear coherent while silently changing the meaning of one of these terms between paragraphs. This file is the semantic firewall that prevents that failure.

The most important early rules are:

\[
\boxed{\text{information} \neq \text{entropy} \neq \text{complexity} \neq \text{correlation}}
\]

\[
\boxed{\text{dynamics} \neq \text{flow} \neq \text{transfer} \neq \text{reconstruction}}
\]

and (v0.2):

\[
\boxed{\text{"evolves in } t\text{"} \Rightarrow \text{a clock has been chosen — say which}}.
\]

---

## 2. Candidate abstraction ladder

This ladder is deliberately labelled `OL-*` rather than "fundamental levels." It is a working decomposition for reasoning.

| Layer | Working content | Typical representation | Main risk |
|---|---|---|---|
| OL-0 | quantum states / operator algebras / amplitudes | Hilbert spaces, density operators, algebras | assuming a preferred subsystem factorization |
| OL-1 | relations and information functionals | entropy, mutual/relative information, channels, correlations | collapsing distinct measures into "information" |
| OL-2 | transformations | unitary/channel evolution, modular flow, scrambling, coarse-graining | calling every change "flow" |
| OL-3 | effective subsystems / fields | QFT degrees of freedom, code subspaces, effective observables | confusing encoding with ontology |
| OL-4 | causal/geometric structure | metric, areas, extremal surfaces, causal wedges, curvature | importing geometry before deriving it |
| OL-5 | semiclassical/macroscopic phenomena | horizons, radiation, thermodynamics, observables | extrapolating beyond framework scope |

**Research question (RQ-001 form):** can OL-4 be derived or constrained from OL-0–OL-2 in a way that is more than a representation change?

**Cross-level question (RQ-013 form, added v0.2):** for each adjacent pair (OL-k−1, OL-k), which persistent OL-k structures possess an invariant witness (CON-034) of sustaining dynamics at OL-k−1? Established instances exist for the lower rungs (KB-003 §O); the OL-3→OL-4 rung is the open one.

---

## 3. Core concepts

### CON-001 — Physical quantum state
A mathematical object representing the state of a quantum system: vector/ray \(|\psi\rangle\), density operator \(\rho\), state on an operator algebra, or path-integral preparation.
**Not equivalent to:** "information." A state may determine many information measures but is richer than any one scalar.
**Research relevance:** the most conservative substrate for information dynamics is the state/algebra itself rather than an entropy scalar.

### CON-002 — Information (programme-level placeholder)
A deliberately non-primitive umbrella term for **distinguishability, uncertainty, correlation, encoding, recoverability, description length, or computational resources**, depending on context.
**Rule:** every scientific use of "information" must resolve to a more specific `CON-*` object.
**Forbidden:** equations containing a bare scalar \(I\) unless its operational definition is given.

### CON-003 — Shannon entropy
\[
H(X)=-\sum_x p(x)\log p(x).
\]
Uncertainty in a classical random variable relative to a specified distribution.
**Not equivalent to:** von Neumann entropy, algorithmic complexity, or physical "amount of reality."

### CON-004 — von Neumann entropy
\[
S(\rho)=-\operatorname{Tr}(\rho\log\rho).
\]
For a subsystem of a pure bipartite state, quantifies entanglement entropy across that bipartition.
**Research relevance:** central to Page curves, generalized entropy, holographic entropy relations.

### CON-005 — Mutual information
\[
I(A:B)=S(A)+S(B)-S(AB).
\]
Total correlation between specified subsystems.
**Caution:** depends on subsystem structure; not automatically a metric on emergent space.

### CON-006 — Relative entropy
\[
S(\rho\Vert\sigma)=\operatorname{Tr}\rho(\log\rho-\log\sigma).
\]
Operationally related to distinguishability; central to JLMS and entanglement-first-law arguments.
**Research relevance:** stronger candidate than raw entropy for geometry constraints — comparative and monotone.

### CON-007 — Entanglement entropy
Von Neumann entropy of a reduced state.
**Framework dependence:** UV-divergent in QFT without regulation; holographic formulas relate suitable entanglement entropy to extremal surfaces under specific assumptions.

### CON-008 — Algorithmic information / Kolmogorov complexity
\[
K_U(x)=\min_{p:U(p)=x}|p|.
\]
Invariant across universal description languages only up to an additive constant; uncomputable in general.
**Major guardrail:** physical conclusions cannot depend on an arbitrary encoding choice. Any use must specify representation class, invariance target, and approximation/MDL surrogate.

### CON-009 — Circuit / state complexity
Minimum gate count, cost, or path length to prepare/transform a state relative to a specified gate set/reference/cost function.
**Not equivalent to:** Kolmogorov complexity.
**Research relevance:** conjectured complexity=volume/action relations; naturally carries continued growth after entropy saturation.

### CON-010 — Information dynamics
Time dependence of a specified information-bearing structure: state evolution \(\rho(t)\); channel composition; changing correlations; entanglement growth; modular flow; scrambling; complexity growth; evolution of reconstructable operator algebras.
Intentionally broader than "information flow."
**(v0.2)** Every instance must declare its clock (CON-035).

### CON-011 — Information transfer
Operational: information encoded in an input system can be recovered from an output system with specified fidelity under a channel/protocol. **Requires:** source, target, encoding, channel, decoding criterion. **Example:** Hayden–Preskill recoverability.

### CON-012 — Information flow / information current
Stronger than transfer: directional propagation through an intermediate structure, in the most literal formulation a continuity equation.
**Status:** unresolved candidate, not assumed primitive.
**Research question:** does gravity require a local information current, or is relational re-encoding/reconstructability the correct invariant description?

### CON-013 — Scrambling
Delocalization of initially accessible information across many degrees of freedom such that small-subsystem access is lost while the global unitary state retains it.
**Not equivalent to:** information destruction.

### CON-014 — Encoding / re-encoding
A map from logical/relational information to physical degrees of freedom, or between representations/subsystems.
**Research relevance:** central to holographic reconstruction and to evaporation redistributing *where* information is encoded without a final storage remnant.

### CON-015 — Reconstructability
Existence of an operator/recovery map allowing information about one description ("bulk/interior/logical") to be recovered from another subsystem ("boundary/radiation").
**Critical distinction:** reconstructability can change with time even if no classical local trajectory of an "information particle" exists.

### CON-016 — Locality
A structural condition on which observables/degrees of freedom can influence or commute with which others at spacelike separation, theory-dependent.
**Research relevance:** emergent locality may be a derived property of encoding/correlation structure.

### CON-017 — Geometry
At minimum, relational structure supplying distance, area, causal separation, connectivity, curvature, or metric data.
**Rule:** "geometry emerges" is incomplete unless it states which geometric observables are reconstructed and from what data.

### CON-018 — Emergent geometry
Effective geometric structure not primitive in the deeper description, reconstructed or approximated from other degrees of freedom.
1. **EG-1 kinematic reconstruction:** a geometric quantity is calculated from non-geometric data.
2. **EG-2 dynamical constraint:** evolution/consistency of the non-geometric data enforces gravitational equations.
3. **EG-3 generative sufficiency:** an autonomous deeper dynamics generates the effective geometry.
The programme must not confuse EG-1 with EG-3.

### CON-019 — Gravitational dynamics
Evolution/constraints on geometric and matter degrees of freedom, e.g.
\[
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G\,T_{\mu\nu},
\]
or quantum/semiclassical generalizations. The programme does not assume Einstein gravity at the deepest level.

### CON-020 — Stationary effective state
A state or observable configuration invariant under the relevant effective time evolution, possibly up to phase, gauge, or symmetry.
**Not equivalent to:** absence of microscopic dynamics. A pure energy eigenstate evolves by a global phase; stationary expectation values coexist with nontrivial phase evolution.

### CON-021 — Persistent structure
A pattern identifiable over a timescale much longer than its microscopic update time.
Candidate realizations: fixed point modulo gauge/phase; invariant subspace; metastable state; decoherence-free or code subspace; periodic orbit / limit cycle; quasiperiodic orbit; attractor in an effective coarse-grained description; topologically protected sector; **(v0.2)** Floquet-stabilized (driven) order.
**Research relevance:** the broad container for "something keeps moving underneath stability."

### CON-022 — Recurrence / oscillation (level-indexed; revised v0.2)
A dynamical property in which the state or selected observables return exactly or approximately after a time interval:
\[
X(t+T)=X(t) \quad\text{or}\quad d(X(t+T),X(t))<\varepsilon .
\]
**v0.2 rule:** every recurrence/oscillation claim is indexed by (a) the abstraction level OL-k at which it is asserted, (b) the clock used (CON-035), and (c) its invariant witness (CON-034) or the explicit absence of one. Unindexed oscillation talk is EL-0 at best.
**Known level instances (see KB-003 §O):** quantum phase/Compton clocks (OL-0; witness contested at the *significance* level, not the existence level); Floquet time-crystal subharmonic response (OL-2/3; witness established); quasinormal ringing of perturbed black holes (OL-5; witness established but transient). The OL-4 (geometric) instance is the open question.

### CON-023 — Coarse-graining
\[
\mathcal C:\mathcal S_{micro}\rightarrow\mathcal S_{eff}.
\]
A map from a detailed description to a reduced effective description discarding or averaging microscopic distinctions.
**Research relevance:** apparent entropy increase or stable macroscopic geometry may coexist with reversible microscopic dynamics because the effective description is coarse-grained.

### CON-024 — Generalized entropy
\[
S_{\mathrm{gen}}(X)=\frac{\mathrm{Area}(X)}{4G_N\hbar}+S_{\mathrm{bulk}}+\cdots
\]
Framework-dependent renormalized definition. Joins geometric area and quantum entropy in the QES/island framework. **(v0.2)** An algebraically well-defined version now exists in crossed-product constructions (KB-003 TH-031).

### CON-025 — Quantum extremal surface (QES)
A codimension-two surface extremizing generalized entropy, generalizing classical extremal-surface prescriptions by including bulk quantum entropy.

### CON-026 — Entanglement wedge
The bulk region associated, in holographic reconstruction, with a boundary region, bounded by the relevant extremal/QES surface.
**Research relevance:** a precise formulation of "where" information is reconstructable that differs from naive local storage.

### CON-027 — Island
A gravitational region included in the entropy/reconstruction domain of a non-gravitating radiation region:
\[
S(R)=\min_I\operatorname*{ext}_I\left[\frac{A(\partial I)}{4G_N\hbar}+S_{\mathrm{bulk}}(R\cup I)\right].
\]
**Guardrail:** an island is not a classical chunk of spacetime physically flying into the radiation.

### CON-028 — Page curve / Page time
For unitary evaporation, fine-grained radiation entropy rises then falls; the Page time is the turnover regime.
**Research relevance:** a clean information-dynamical diagnostic of evaporation.

### CON-029 — Black-hole remnant
A long-lived or stable object after evaporation, often near Planck mass, potentially with large interior capacity.
**Status:** proposal class, not consensus endpoint. **Key issues:** capacity, degeneracy, production rates, stability, entropy bounds.

### CON-030 — Planck star / black-to-white-hole transition
LQG-inspired proposals in which quantum-gravitational effects replace the singularity and may produce a bounce/transition, potentially with a long-lived white-hole-like remnant.
**Not equivalent to:** a generic statement of all quantum gravity.

### CON-031 — Fuzzball / microstate geometry
String-theory programme representing black-hole microstates as horizon-scale quantum/stringy structures or smooth microstate geometries rather than a featureless interior.
**Research relevance:** endpoint-independent way of making information-bearing structure dynamical throughout.

### CON-032 — Modular flow
Evolution generated by a modular Hamiltonian associated with a state and algebra/subregion; not ordinary physical time evolution in general.
**Research relevance:** candidate relational dynamics tightly connected to wedge reconstruction, relative entropy, and — via the thermal-time hypothesis (TH-032) — to CON-035.

### CON-033 — Internal clock / phase dynamics (added v0.2)
The universal phase evolution of quantum systems: a stationary state of energy \(E\) evolves as \(e^{-iEt/\hbar}\); a system of mass \(m\) carries the Compton angular frequency
\[
\omega_C=\frac{mc^2}{\hbar},
\]
de Broglie's "internal clock." Related phenomena: zitterbewegung of Dirac-type systems (simulated experimentally); mass–frequency equivalence underlying modern metrology.
**Status:** established (E3/E4) as kinematics.
**Guardrails:** (i) a single global phase is unobservable — only *relative* phases and energy differences are witnesses (CON-034); (ii) NC-009: universality here does not establish geometric significance. The research question is whether gravity's coupling to these clocks (TH-035) is load-bearing for emergent geometry.

### CON-034 — Invariant oscillation witness (added v0.2)
An observable or order parameter certifying that a claimed oscillation/recurrence at level OL-k is physical rather than representational: it must be invariant under phase/gauge/frame/encoding redundancies at that level and must change (or vanish) if the oscillation stops.
**Template:** the subharmonic response of a discrete time crystal — period-doubling of an observable relative to the drive, robust to perturbations, measured (TH-033). Other candidates: relative-phase interference fringes; recurrence of an invariant state-space distance \(d_{phys}(X(t+T),X(t))\); spectral gap structure (energy *differences*); OTOC revival structure.
**Rule:** KC-005 kills oscillation claims *at a level* exactly when no CON-034 object exists at that level.

### CON-035 — Clock / time reference (added v0.2)
The parameter with respect to which a dynamical claim is stated. Admissible types:
1. **external/background clock** (laboratory time; background spacetime \(t\)) — forbidden as a *fundamental* ingredient of HYP-003-class claims (NC-010);
2. **relational clock** — a physical subsystem whose configuration parametrizes the rest (Page–Wootters-style constructions);
3. **modular/thermal clock** — flow defined by the state itself via its modular automorphism group (TH-032); notable because an *equilibrium* state then *defines* a dynamics — persistence and flow as two faces of one structure, directly relevant to INT-001;
4. **emergent/coarse-grained clock** — a monotone functional of the deeper dynamics.
**Rule (INV-R-009):** every `HYP-*`/`BH-*` and every toy model declares its clock type; "clock-deferred" is admissible only at EL-0/EL-1.

### CON-036 — Cross-level dynamical persistence (CLDP) (added v0.2)
The structural pattern asserted by HYP-009: for adjacent levels (OL-k−1, OL-k), a persistent OL-k structure is *sustained by* nontrivial OL-k−1 dynamics, witnessed by at least one CON-034 object at OL-k−1, such that suppressing the dynamics (counterfactually or experimentally) degrades or destroys the OL-k structure.
**Distinguish:** *sustained-by* (counterfactual dependence; strong) vs *compatible-with* (mere coexistence; weak — this is only CON-020/OBS-003). The census (AR-015) classifies known instances by which of these actually holds, with null comparators.

---

## 4. Semantic collision rules

Mandatory until explicitly superseded.

1. **Information ≠ entropy.** Use the specific measure.
2. **Entropy ≠ ignorance universally.** State whether classical, reduced-state, generalized, coarse-grained, algebraic.
3. **Dynamics ≠ flow.** A state can change without a local current interpretation.
4. **Transfer ≠ reconstruction.** Operational recovery and geometric propagation are different claims.
5. **Scrambling ≠ destruction.**
6. **Stable ≠ static.** Persistence may be dynamical.
7. **Dynamic ≠ oscillatory.** Recurrence is an additional, level-indexed, witness-requiring hypothesis.
8. **Emergent ≠ fundamental.**
9. **Geometric dual ≠ causal mechanism.**
10. **Toy model ≠ universe.** Preserve framework scope.
11. **Area/entropy relation ≠ full spacetime emergence.**
12. **Complexity ≠ Kolmogorov complexity.** State gate set/cost or description language.
13. **Boundary encoding ≠ ordinary memory storage.**
14. **Island ≠ remnant.**
15. **(v0.2) Oscillation without a level is not a claim.** Every oscillation statement names its OL-k, clock, and witness (or witness-gap).
16. **(v0.2) Universality ≠ significance.** That all massive systems carry Compton clocks (CON-033) does not itself elevate any hypothesis (NC-009).
17. **(v0.2) "Evolves" without a clock is not dynamics.** Name the clock type (CON-035).
18. **(v0.2) Sustained-by ≠ compatible-with.** CLDP claims require the counterfactual-dependence sense (CON-036).

---

## 5. Candidate mathematical state spaces for the programme

Compare, do not prematurely choose.

### CAND-001 — Density-operator dynamics
\(\rho(t)=U(t)\rho(0)U^\dagger(t)\) or \(\rho(t+\Delta t)=\mathcal E_{\Delta t}[\rho(t)]\).
Pros: conservative, operational. Cons: geometry relation may require subsystem/algebra structure not contained in \(\rho\) alone.

### CAND-002 — Operator-algebra dynamics
Algebras and their inclusion/reconstruction relations as primary.
Pros: naturally handles gauge/gravity factorization subtleties and reconstructability; **(v0.2)** now has a rigorous gravitational instantiation via crossed-product/Type II constructions in which an observer's clock is what renders entropy well-defined (TH-031) — a direct formal meeting point of CON-035 and CON-024. Cons: technically demanding; "where information is" becomes algebra-relative.

### CAND-003 — Correlation / entanglement structure
Graph/hypergraph weighted by mutual information, entanglement measures, or correlations.
Pros: intuitive route to emergent distance/connectivity; **(v0.2)** an explicit construction exists (Cao–Carroll–Michalakis, TH-037) and supplies a ready-made \(\Phi[X]\) for toy models (Track E3). Cons: non-uniqueness; pairwise measures can discard multipartite structure.

### CAND-004 — Information geometry
Metric from distinguishability (quantum Fisher/Bures-type).
Pros: geometry built from operational distinguishability. Cons: not automatically physical spacetime geometry.

### CAND-005 — Tensor-network / code structure
Encoding map plus network geometry.
Pros: emergence/redundancy explicit and computable. Cons: danger of baking desired geometry into the architecture.

### CAND-006 — Complexity geometry
State complexity or operator growth as the dynamical quantity.
Pros: captures continued growth after entanglement saturation. Cons: definition-dependent; dualities conjectural.

### CAND-007 — Algorithmic/MDL structure
Description length or conditional complexity of states/relations/coarse-grained models.
Pros: connects emergence to compressible regularity and the researcher's AIT/MDL toolkit. Cons: uncomputability, representation dependence, no established universal gravity map.

---

## 6. Candidate meanings of "information does not stop"

The initiating phrase (INT-001) tested against precise alternatives:

### P-1 — Unitary persistence
Global quantum evolution continues; information is not fundamentally erased. Weakest reading; largely standard unitary QM.

### P-2 — Continuous redistribution
Correlations and recoverability migrate among subsystems: \(I(A:B;t),\ S(A;t),\ F_{\mathrm{recover}}(t)\).

### P-3 — Persistent nontrivial microscopic evolution under stationary macroscopic observables
There exists \(\mathcal C\) with \(\mathcal C[X(t)]\approx\text{const}\) while \(X(t)\neq X(0)\) microscopically.

### P-3b — Witnessed persistence-through-dynamics (added v0.2)
P-3 strengthened by CON-034/CON-036: the microscopic dynamics is certified by an invariant witness and the macroscopic persistence *counterfactually depends* on it. Established instances exist below the geometric level (KB-003 §O). This is the reading selected by ADR-001 for the lower rungs.

### P-4 — Autonomous relational dynamics generates effective geometry
\(\dot X = F[X]\), \(g_{\mu\nu}=\Phi[X(t)]\) — strong research hypothesis; clock must be declared (CON-035).

### P-5 — Persistent geometry corresponds to recurrent information modes
\(X(t+T)\simeq X(t)\) or motion on a stable invariant set yields stationary coarse-grained geometry. The specific recurrence branch at the geometric level; must earn a CON-034 witness there.

---

## 7. Ontology change protocol

A nontrivial ontology change should record: concept ID affected; old definition; new definition; reason/evidence; hypotheses impacted; whether prior results remain interpretable; whether a new concept should be added instead of overwriting.
If a definition change invalidates a `HYP-*`, KB-004 must be marked `STALE` until reconciled.

---

## 8. Immediate semantic tests for every future draft

Before accepting a paragraph/equation, ask:

1. What exact `CON-*` does "information" mean here?
2. Is the statement kinematic or dynamical?
3. Is it about transfer, encoding, or reconstructability?
4. What subsystem/algebra factorization is assumed?
5. Is geometry input or output?
6. Is the result framework-specific?
7. Does "stable" mean fixed, invariant modulo symmetry, metastable, or recurrent — and is the sustained-by or compatible-with sense meant (CON-036)?
8. If "oscillation" appears: what level (OL-k), what clock (CON-035), what invariant witness (CON-034)?
9. If algorithmic complexity appears, what encoding and approximation are used?
10. **What clock does the dynamics use, and did we hide time in the dynamics?** (v0.2)
11. What observation/derivation could show the statement is wrong?

If these cannot be answered, the statement remains EL-0.

---

## 9. Changelog v0.1 → v0.2

1. Added CON-033 (internal clock / phase dynamics), CON-034 (invariant oscillation witness, time-crystal template), CON-035 (clock / time reference — problem-of-time firewall), CON-036 (cross-level dynamical persistence; sustained-by vs compatible-with).
2. Revised CON-022 to level-indexed recurrence with mandatory level/clock/witness triple; recorded known level instances.
3. Extended CON-010 (clock declaration), CON-021 (Floquet-stabilized order), CON-024 (algebraic generalized entropy pointer), CON-032 (thermal-time link), CAND-002 (crossed-product instantiation), CAND-003 (Cao–Carroll–Michalakis construction as toy-model \(\Phi\)).
4. Added semantic collision rules 15–18 (level indexing; universality ≠ significance; clock naming; sustained-by ≠ compatible-with) and the boxed clock rule in §1.
5. Added P-3b to §6 and marked it as the ADR-001-selected reading for sub-geometric rungs.
6. Added clock question to §8 checklist.
