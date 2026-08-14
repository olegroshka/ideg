---
id: KB-003
title: "IDEG Theory Landscape and Canonical Bibliography"
status: DRAFT
owner: shared
last_reviewed: 2026-08-14
version: 0.6
research_layer: R2
epistemic_status: MIXED
sources:
  - "Primary literature registry SRC-001..SRC-063 below; SRC-001..035 metadata checked 2026-08-11; SRC-042..044 + SRC-049 verified 2026-08-11 (AR-015 partial, Track E3 G1); SRC-059..063 verified 2026-08-14 (paper-1 bibliography gate); SRC-036..041, 045..048, 050..051 metadata VERIFICATION PENDING (AR-017/AR-016/AR-015/AR-002d); SRC-052..058 added 2026-08-12 (AR-019 survey) — VERIFICATION PENDING"
depends_on: [KB-001, KB-002]
referenced_by: [KB-004, KB-005]
changelog:
  - "0.1: initial landscape, sections A–N, TH-001..028, SRC-001..035 (Sol/ChatGPT, 2026-08-11)"
  - "0.2: review revision (Claude, 2026-08-11) — see §Q"
  - "0.3: Track E3 G1 verification reconciled (Claude, 2026-08-11) — SRC-042..044, SRC-049 verified; TH-033 no-go scope condition added; TH-037 equation locations added; see ar/AR-015_partial-2026-08-11_trackE3-G1.md"
  - "0.4: AR-019 robustness-instrument survey sources added (Claude, 2026-08-12) — SRC-052..058, all flagged verify; see §S and ar/AR-019_note-2026-08-12_robustness-instruments.md"
  - "0.5: AR-021 dephasing-stabilization literature-check sources added (Claude, 2026-08-13) — SRC-059..063, all flagged verify; mechanism known (Zeno/damping family), object not found in survey scope; see ar/AR-021_note-2026-08-13_dephasing-stabilization-lit.md"
  - "0.6: SRC-059..063 metadata VERIFIED against primary listings (Claude, 2026-08-14, paper-1 bibliography gate) — SRC-060 upgraded to its published ref (J. Phys. Complex. 2, 035008 (2021)); SRC-061 author and SRC-063 full author list confirmed; DOIs recorded"
---

# Theory Landscape and Canonical Bibliography

> **SSOT rule:** this file owns external-theory claims (`TH-*`) and bibliography entries (`SRC-*`). Other IDEG files cite `TH-*` / `SRC-*` rather than duplicating literature summaries.

## 1. Reading rule

The literature is organized by **what relation it establishes between information and gravity** (and, in §O, between persistence and dynamics), not by chronology or personality.

For each cluster distinguish: (1) what is actually established/proposed; (2) the mathematical object used; (3) the framework scope; (4) what the result does **not** imply; (5) relevance to IDEG.

The programme must resist a common failure mode: collecting papers containing the words *information*, *entanglement*, *geometry*, and *gravity* and treating them as evidence for one unified ontology.

**v0.2 metadata rule:** entries SRC-036..051 were added from the 2026-08-11 review session; their bibliographic metadata is recorded to the best of current knowledge but is **verification-pending** and must be primary-source-checked (per §N governance) before any becomes load-bearing in a formal argument.

---

# A. Black-hole thermodynamics and the information problem

## TH-001 — Horizon area behaves as entropy in black-hole thermodynamics
Bekenstein proposed black-hole entropy proportional to horizon area; Hawking's semiclassical calculation fixed the temperature and coefficient:
\[
S_{BH}=\frac{k_B c^3 A}{4G\hbar}.
\]
**Evidence class:** E3 within semiclassical black-hole thermodynamics. **Information object:** thermodynamic/generalized entropy. **Geometry object:** horizon area. **Sources:** SRC-002, SRC-003.
**Does not imply:** that spacetime is made of information; that an entropy current generates curvature; that evaporation ends in a remnant.
**IDEG relevance:** earliest robust area↔entropy seam.

## TH-002 — Semiclassical Hawking radiation drives mass loss
Hawking's calculation predicts approximately thermal radiation and mass loss. Extrapolation toward the Planck regime is not controlled.
**Evidence class:** E3 semiclassically; Planck-scale endpoint outside the derivation's reliable regime. **Source:** SRC-003.
**Does not imply:** a specific Planck-mass stable endpoint.

## TH-003 — Unitary evaporation motivates the Page curve
Page's analysis shows how information can emerge in radiation if the process is unitary; fine-grained radiation entropy rises then falls.
**Evidence class:** E2/E3 depending on model assumptions. **Source:** SRC-004.
**IDEG relevance:** turns "information loss" into a time-dependent quantitative target.

## TH-004 — Old black holes can act as information mirrors in scrambling models
Hayden–Preskill: assuming unitary rapidly mixing dynamics and access to prior radiation, information newly thrown into an old black hole becomes rapidly recoverable from subsequent radiation.
**Evidence class:** E2 in the quantum-information model. **Information object:** decoupling/recoverability. **Source:** SRC-005.
**Does not imply:** a literal local information current across the horizon.
**IDEG relevance:** *recoverability dynamics* is more precise than a vague "flow."

---

# B. Entanglement ↔ geometry in holography

## TH-005 — Ryu–Takayanagi: boundary entanglement entropy ↔ bulk extremal area
\[
S(A)=\frac{\mathrm{Area}(\gamma_A)}{4G_N}
\]
at leading order for static holographic states. **Evidence class:** E3 within AdS/CFT. **Source:** SRC-006.
**Does not imply:** full spacetime dynamics from entropy alone.

## TH-006 — HRT extends the relation covariantly
Covariant extremal-surface prescription for time-dependent states. **Evidence class:** E3 within holography. **Source:** SRC-007.
**IDEG relevance:** moves the seam toward time dependence, though still as a duality dictionary.

## TH-007 — Entanglement is linked to bulk connectivity
Van Raamsdonk: reducing boundary entanglement corresponds to bulk regions pulling apart. **Evidence class:** E1/E2 conceptual + holographic examples. **Source:** SRC-008.
**Does not imply:** pairwise entanglement is a universal spacetime metric.

---

# C. Entanglement/thermodynamic constraints ↔ gravitational equations

## TH-029 — The Einstein equation as a thermodynamic equation of state (added v0.2)
Jacobson (1995) derived the full nonlinear Einstein equations from the Clausius relation \(\delta Q = T\,dS\) applied to all local Rindler horizons, with \(S\propto A\) and Unruh temperature — geometry as the equation of state of underlying degrees of freedom.
**Evidence class:** E3 as a derivation under its stated assumptions (local equilibrium, area-entropy proportionality). **Information object:** horizon entropy/heat flux. **Geometry object:** Einstein equations. **Source:** SRC-036.
**Does not imply:** identification of the underlying degrees of freedom; uniqueness of the thermodynamic interpretation.
**IDEG relevance:** the historical root of "gravity as thermodynamics of something deeper"; direct ancestor of TH-009; a *dynamical* seam that predates and is independent of holography — important as a non-AdS anchor (RQ-012). **(v0.1 omission, restored.)**

## TH-030 — Entropic/thermodynamic-gravity programmes (added v0.2)
Verlinde proposed gravity as an entropic force arising from information associated with material bodies' positions; Padmanabhan developed a broad thermodynamic reformulation of gravitational dynamics (equipartition, surface degrees of freedom).
**Evidence class:** E1 programmes with contested elements; heuristic derivations reproduce Newtonian/Einstein limits under assumptions. **Sources:** SRC-037, SRC-038.
**Does not imply:** established microscopic mechanism; several specific claims are disputed.
**IDEG relevance:** landscape completeness for the "gravity from information/thermodynamics" family; cautionary examples of the relabelling risk (KC-001) the programme must avoid.

## TH-008 — Entanglement first-law constraints imply linearized Einstein equations in holographic CFTs
Lashkari–McDermott–Van Raamsdonk and Faulkner et al.: the first law of entanglement for boundary balls, with the holographic dictionary, implies linearized gravitational equations around AdS: \(\delta S = \delta\langle H_{mod}\rangle\) ↔ linearized bulk Einstein equations.
**Evidence class:** E3 within the holographic setup. **Sources:** SRC-011, SRC-012.
**IDEG relevance:** information-theoretic consistency constraining **dynamics**, not merely static area.
**Does not imply:** an autonomous information law generating arbitrary 3+1 gravity.

## TH-009 — Entanglement equilibrium can imply the semiclassical Einstein equation locally
Jacobson (2016): stationarity/maximality of vacuum entanglement for small geodesic balls is equivalent at first order to Einstein dynamics; nonconformal matter requires an additional conjectural ingredient.
**Evidence class:** E2/E3 under assumptions. **Source:** SRC-013.
**IDEG relevance:** Einstein dynamics as an equilibrium/variation condition on entanglement plus geometry; the modern entanglement-native descendant of TH-029.

## TH-010 — Relative entropy has a bulk dual and supports reconstruction
JLMS: boundary relative entropy equals bulk relative entropy to leading order; boundary modular flow relates to bulk modular flow in the wedge.
**Evidence class:** E3 within holography. **Source:** SRC-014.
**IDEG relevance:** distinguishability and modular structure as candidate fundamental research variables.

---

# D. Quantum error correction, encoding, and reconstructability

## TH-011 — Bulk locality can be understood through quantum-error-correction structure
Almheiri–Dong–Harlow. **Evidence class:** E2/E3 structural interpretation with controlled code models. **Source:** SRC-009.

## TH-012 — Tensor-network codes explicitly realize holographic encoding features
HaPPY code: exactly solvable tensor-network QEC model reproducing RT-like entropy relations and redundant reconstruction. **Evidence class:** E2 toy model. **Source:** SRC-010. Related: Swingle's identification of MERA entanglement-renormalization networks with emergent holographic geometry (SRC-051).
**Does not imply:** literal tensor-network microstructure of the universe.

## TH-013 — The strong QEC interpretation is currently debated at finite N
Terashima (2026) argues entanglement-wedge reconstruction should be separated from the stronger shared-logical-operator QEC claim at finite \(N\). **Evidence class:** E1 current critical proposal / active debate. **Source:** SRC-029.
Related: non-isometric codes show gravitational encoding may differ materially from textbook isometric QEC (SRC-030).
**IDEG relevance:** do not build the ontology on "spacetime = QEC" as settled fact.

---

# E. Generalized entropy, QES, islands, and replica wormholes

## TH-014 — Quantum extremal surfaces generalize holographic entropy
Engelhardt–Wall: extremize \(S_{gen}=\frac{A}{4G\hbar}+S_{bulk}+\cdots\). **Evidence class:** E3 within semiclassical holographic gravity. **Source:** SRC-015.

## TH-015 — The Page transition as a change in entanglement wedge
Penington: an evaporating AdS black hole undergoes a QES transition near the Page time; interior information becomes reconstructable from radiation. **Evidence class:** E3 in the controlled setup. **Source:** SRC-016.
**IDEG relevance:** central example of **changing reconstructability without a terminal remnant**.

## TH-016 — Island formulas reproduce the unitary Page curve in controlled models
AMMZ and subsequent work. **Evidence class:** E3 in the studied models. **Source:** SRC-017.

## TH-017 — Replica wormholes provide a gravitational-path-integral mechanism for the island rule
**Evidence class:** E3 in controlled low-dimensional/semiclassical models. **Sources:** SRC-018, SRC-019.
**Does not imply:** a completed microscopic description of astrophysical 3+1 Hawking quanta.

---

# F. Entanglement, wormholes, and complexity

## TH-018 — ER=EPR is a conjectured entanglement/geometry relation
Maldacena–Susskind. **Evidence class:** E1/E2 conjectural programme. **Source:** SRC-020.
**Does not imply:** every entangled pair is connected by a classical traversable wormhole.

## TH-019 — Holographic complexity may be dual to bulk geometric/action quantities
Complexity=volume/action: \(\mathcal C \sim I_{WDW}/(\pi\hbar)\) up to prescription details. **Evidence class:** E1/E2 conjectural duality with nontrivial checks. **Sources:** SRC-021 and related literature.
**IDEG relevance:** complexity can keep growing after entanglement saturates — natural candidate for "persistent hidden dynamics." **Guardrail:** definition/cost-function dependence.

---

# G. Soft charges / asymptotic information

## TH-020 — Soft hair adds exact gravitational charges and correlations
Hawking–Perry–Strominger. **Evidence class:** E1/E2. **Source:** SRC-022.
**Does not imply:** by itself, a complete solution of the information paradox.

---

# H. String microstates / fuzzballs

## TH-021 — Fuzzball/microstate programmes replace the featureless interior with information-bearing microstructure
**Evidence class:** E2/E3 for constructed families; generality open. **Sources:** SRC-023, SRC-024.
**IDEG relevance:** "dynamics throughout" rather than "information waits in a relic," via very different machinery from islands.

---

# I. Planck stars, white-hole remnants, and remnant proposals

## TH-022 — Planck stars are a specific LQG-inspired bounce scenario
**Evidence class:** E1 proposal. **Source:** SRC-025.

## TH-023 — Black-to-white-hole tunnelling can yield a long-lived remnant in specific models
**Evidence class:** E1/E2 model proposal. **Source:** SRC-026.

## TH-024 — Remnants remain possible but controversial, not a generic quantum-gravity prediction
Reviews catalogue motivations and objections; status: viable class with unresolved consistency and phenomenology. **Evidence class:** E1 landscape/review. **Sources:** SRC-027, SRC-028.

## TH-025 — Planckian relics remain an active 2026 phenomenological hypothesis
LQG-inspired primordial-black-hole studies assume quasi-stable relics and derive constraints; the relic is a model assumption, not an accepted endpoint. **Evidence class:** E1 model + E4 conditional constraints. **Source:** SRC-033.

---

# J. Historical provenance of the triggering X post

## TH-026 — Markov's maximon/minimon programme is real historical work
**Evidence class:** E1 historical theoretical proposal. **Source:** SRC-031.

## TH-027 — Planck-mass stable-particle remnants were explicitly proposed in the 1980s
Aharonov–Casher–Nussinov. **Evidence class:** E1 proposal. **Source:** SRC-032.

## TH-028 — No canonical "Yukawa / Markov / Hawking theorem" was identified
No standard joint result stating evaporation necessarily halts at Planck mass or that particles are Planck-remnant bound states. Separately grounded: Yukawa's elementary-domain ideas (SRC-035); Markov's maximons (SRC-031); Hawking's semiclassical radiation (SRC-003); later remnant proposals (SRC-032, SRC-027, SRC-028).
**Status:** provenance correction. `AR-001` owns deeper historical verification if needed.

---

# M. Algebraic structure, modular time, and the problem of time (added v0.2)

## TH-031 — Crossed products render gravitational entropy algebraically well-defined
Witten and Chandrasekaran–Longo–Penington–Witten showed that including an observer's degrees of freedom (a clock) converts the Type III von Neumann algebras of QFT subregions into Type II algebras with a well-defined trace, giving a mathematically rigorous definition of (generalized) entropy in gravitational settings, including de Sitter.
**Evidence class:** E3 within perturbative gravity / large-\(N\) settings studied. **Information object:** algebraic entropy on Type II factors. **Geometry object:** subregions/horizons with observer worldlines. **Sources:** SRC-039, SRC-040 (metadata verification pending).
**Does not imply:** a full nonperturbative theory; observer-dependence questions remain active.
**IDEG relevance:** *very high.* (i) The modern rigorous home of CAND-002 (operator-algebra dynamics). (ii) Structurally striking for IDEG: a **clock is the ingredient that makes entropy well-defined** — a formal junction of CON-035 (clock) and CON-024 (generalized entropy), directly relevant to RQ-014 and NC-010. **(v0.1 omission, restored.)**

## TH-032 — Thermal time hypothesis: equilibrium states define their own flow
Connes–Rovelli: in generally covariant theories, a state's modular automorphism group can be taken to *define* physical time; an equilibrium (KMS) state does not lack dynamics — it singles one out.
**Evidence class:** E1/E2 structural proposal with exact mathematical content (Tomita–Takesaki theory). **Source:** SRC-041 (verification pending).
**IDEG relevance:** near-formalization of INT-001's "persistence and ongoing dynamics as two faces of one structure"; candidate clock type 3 in CON-035; connects to TH-010/TH-031 through modular theory.

---

# O. Cross-level persistence-through-dynamics exemplars (added v0.2)

> These entries ground OBS-004 / HYP-009. They are **not** gravity results; scope walls apply (collision rule 10). Their role is to establish that (a) the persistence-through-dynamics pattern has E2–E4 instances at several OL levels and (b) the invariant-witness bar (CON-034) is passable.

## TH-033 — Time crystals: equilibrium no-go, driven realization
Watanabe–Oshikawa proved the absence of time-crystalline order in ground/equilibrium states (no-go), for Hamiltonians with not-too-long-range interactions (scope condition per the source's own statement). Else–Bauer–Nayak defined Floquet (discrete) time crystals (TTSB-1/2 definitions; subharmonic response at half the drive frequency; MBL load-bearing for stability); experiments (trapped ions, NV centers; later a quantum processor) observed the phase — the trapped-ion observation (10 ¹⁷¹Yb⁺ spins, period-2T response, rigidity up to a critical drive perturbation) is verified.
**Evidence class:** E3 (no-go theorem) + E4 (driven realization). **Sources:** SRC-042, SRC-043, SRC-044 (verified 2026-08-11, AR-015 partial; NV-center and processor companions remain unverified leads).
**Does not imply:** anything about gravity; driven systems import an external drive/clock.
**IDEG relevance:** the **witness template**. The subharmonic response is an invariant, measured order parameter — a persistent structure whose defining feature is an oscillation *not removable by representation choice*. This falsifies "oscillation is always a gauge artifact" as a universal claim and calibrates KC-005: the kill test is per-level witness existence. The no-go/realization *pair* also shows exactly what an invariant oscillation costs (here: driving + many-body stabilization).

## TH-034 — Hadronic mass is dominantly dynamical
Ab initio lattice QCD reproduces light hadron masses; the overwhelming majority of the proton's mass arises from gluon-field and quark kinetic energy, not Higgs-generated rest masses.
**Evidence class:** E3/E4. **Source:** SRC-045 (verification pending).
**IDEG relevance:** the strongest everyday exemplar of CON-036's *sustained-by* sense: a maximally persistent structure whose defining bulk property (mass) **is** ongoing internal dynamics. Null comparator: this is standard QFT; the exemplar's role is structural, not evidential for gravity claims.

## TH-035 — Internal quantum clocks exist and couple to gravity; interpretations partly contested
Every massive system carries Compton-frequency phase evolution (CON-033); zitterbewegung has been quantum-simulated (SRC-048). Atom-interferometry experiments have been interpreted as measuring gravitational redshift at the Compton frequency (Müller–Peters–Chu) and as realizing a "Compton clock" linking time directly to mass (Lan et al.); the redshift interpretation was seriously disputed (Wolf et al.), and the debate is part of the record.
**Evidence class:** E4 for phase evolution and interferometric phenomenology; **contested (E1/E4 mix)** for the redshift-at-Compton-frequency interpretation. **Sources:** SRC-046, SRC-047, SRC-048 (verification pending).
**Does not imply:** that internal phase is load-bearing for emergent geometry (NC-009); a global phase is unobservable — witnesses are relative phases/energy differences.
**IDEG relevance:** the reading-1 seam. Gravity couples *universally* to internal clock rates (gravitational time dilation); operationally, geometry does bookkeeping of relative phase accumulation along worldlines. Whether that is kinematic decoration or constraint is AR-016's question.

## TH-036 — Quasinormal ringing: perturbed geometry itself oscillates transiently
Perturbed black holes relax through damped characteristic oscillations (quasinormal modes), observed in gravitational-wave ringdown.
**Evidence class:** E3 theory / E4 observation (standard GR + LIGO-Virgo ringdown consistency). **Source:** covered by standard literature; a canonical review to be selected in AR-015 (SRC slot reserved).
**IDEG relevance:** the only currently established sense in which *geometry* oscillates — transient, decaying, and fully within classical GR. Serves as the null comparator for any stronger geometric-oscillation claim: HYP-005-class claims must differ from "QNM ringing exists."

---

# P. Emergent-space constructions from entanglement data (added v0.2)

## TH-037 — Emergent spatial geometry from mutual-information structure
Cao–Carroll–Michalakis construct an emergent spatial metric from the entanglement structure of a Hilbert-space state (mutual-information graph → distances), with redundancy/robustness analysis. Verified construction (SRC-049 §III): redundancy-constrained states with entropy from a pairwise-MI cut function (eq. 9); graph weights w(p,q) = ℓ·Φ(I(A_p:A_q)/I₀) with suggested Φ(x) = −log x (eq. 13); distance = weighted shortest path (eq. 14); classical MDS embedding (eqs. 23–25). Author-stated caveats: the factorization is posited, not derived; embeddings unique only up to isometry; area-law/short-range-entangled regime; framework has no dynamics/time (§VI).
**Evidence class:** E2 explicit construction in a controlled setting. **Source:** SRC-049 (verified 2026-08-11, AR-015 partial).
**IDEG relevance:** a concrete, implementable \(\Phi: X \mapsto \mathcal G\) for CAND-003 and for the Track E3 toy models — lets BH-004 use an off-the-shelf emergent-geometry functional instead of inventing one.

## TH-038 — Causal sets: discrete order as the primitive of geometry
Bombelli–Lee–Meyer–Sorkin: spacetime as a locally finite partial order; geometry from order + number.
**Evidence class:** E1/E2 programme. **Source:** SRC-050 (verification pending).
**IDEG relevance:** landscape completeness (a non-information-theoretic discreteness route); watch-level unless a bridge hypothesis needs it.

---

# K. What the current landscape says about the initiating intuition

## K.1 "Information dynamics does not stop" — weakest defensible reading
Compatible with modern unitary pictures: state evolution → scrambling → correlation/re-encoding → changing reconstructability (TH-004, TH-015–TH-017). Does **not** require a stable Planck remnant.

## K.2 "Stable structure is maintained by ongoing microscopic dynamics" — established below gravity, open at gravity (revised v0.2)
v0.1 called this "plausible but generic." §O sharpens it: at several levels it is **established physics with invariant witnesses** (TH-033, TH-034, TH-035), not merely a generic possibility. What remains open is precisely the geometric rung (RQ-013), for which quasinormal ringing (TH-036) is the transient null comparator and complexity growth (TH-019) the conjectural candidate. IDEG's job is the rung, not the ladder.

## K.3 "Geometry is information" — too strong
Existing results establish several **bridges**, not one identity: entropy ↔ extremal area (TH-005/006); entanglement variations ↔ linearized Einstein dynamics (TH-008/009); thermodynamics ↔ Einstein equations (TH-029/030); relative entropy ↔ bulk relative entropy (TH-010); encoding/reconstructability ↔ wedges (TH-011–017); clock ↔ well-defined entropy (TH-031); conjectural complexity ↔ volume/action (TH-019). The research opportunity: test whether these are manifestations of a common structure.

## K.4 "Everything oscillates" — level-indexed status (revised v0.2)
Not established as a universal claim, and NC-004/NC-009 stand. But the v0.1 flat verdict is replaced by a per-level ledger: kinematic phase oscillation — universally true, significance open (TH-035); driven many-body oscillation — realized with invariant witness (TH-033); geometric oscillation — only transient QNM ringing established (TH-036); recurrent *emergent-geometry-sustaining* modes — open, researched as HYP-005 within HYP-009. The scientifically useful question: *at which levels does an invariant witness exist, and does the pattern continue at OL-4?*

---

# L. Seam matrix — first-pass synthesis (extended v0.2)

| Seam | Information object | Geometric/gravity object | Dynamics? | Scope | IDEG priority |
|---|---|---|---|---|---|
| Bekenstein–Hawking | thermodynamic entropy | horizon area | indirect | semiclassical BH | medium |
| **Jacobson 1995 (v0.2)** | horizon entropy / Clausius relation | full Einstein equations | **yes, derivation** | local Rindler / semiclassical | **very high** |
| Entropic-gravity programmes (v0.2) | positional information / equipartition | Newton/Einstein limits | heuristic | contested | low-medium (landscape) |
| RT/HRT | entanglement entropy | extremal-surface area | mainly dictionary | holography | high |
| Entanglement first law | \(\delta S\), modular energy | linearized Einstein equations | **yes, constraint** | holographic CFT | **very high** |
| Entanglement equilibrium | local vacuum entanglement stationarity | Einstein equation | **yes, constraint** | local semiclassical | **very high** |
| JLMS | relative entropy / modular flow | bulk relative entropy / wedge | relational dynamics | holography | **very high** |
| **Crossed product / Type II (v0.2)** | algebraic entropy | observer+subregion | **structural: clock ⇒ entropy** | perturbative gravity / dS | **very high** |
| **Thermal time (v0.2)** | modular automorphism group | covariant "time" | **state defines flow** | general covariant QM | high |
| QES/islands | generalized entropy | QES + reconstruction region | **yes, phase transition** | semiclassical/holographic | **very high** |
| Hayden–Preskill | recoverability/decoupling | BH/radiation partition | **yes** | scrambling model | high |
| QEC/tensor networks | encoding/redundancy | bulk locality/geometry | partly | holographic toy models | high |
| **MI-graph geometry (v0.2)** | mutual-information structure | emergent spatial metric | kinematic construction | controlled Hilbert-space setting | high (toy-model tooling) |
| ER=EPR | entanglement | wormhole connectivity | conjectural | holography/QG | medium |
| complexity=action | circuit complexity | WDW action | **yes, growth** | holographic conjecture | high |
| fuzzballs | microstate information | horizon-scale structure | **yes** | string theory | medium |
| Planck stars/remnants | internal quantum state | endpoint geometry | **yes** | LQG-inspired | medium |
| soft hair | asymptotic charges | horizon/asymptotic structure | yes | asymptotic gravity | medium |
| **Internal clocks (v0.2)** | phase / proper time along worldline | metric via time dilation | **kinematic coupling, universal** | measured; significance contested | high (AR-016) |
| **Time crystals (v0.2, template only)** | subharmonic order parameter | — (non-gravitational) | **yes, witnessed** | driven many-body | template for CON-034 |

**First-pass inference (revised):** the most promising formal seam remains **state distinguishability / modular structure / entanglement constraints / reconstruction**, now reinforced by the crossed-product results in which a *clock* is the enabling ingredient — suggesting the invariant IDEG should chase may live at the junction of modular structure and time reference, with complexity as a separate candidate for continued dynamics beyond entropy saturation. Provisional; to be attacked by `AR-012`.

---

# N. Bibliography governance

1. `SRC-*` entries are leads until metadata and the load-bearing claim have been checked against the primary source. **v0.2 entries SRC-036..051 are explicitly verification-pending.**
2. For any paper used in a formal argument, record the exact theorem/equation/section in the corresponding `AR-*` evidence artifact.
3. Reviews map a field; they do not adjudicate technical claims.
4. Current papers (`SRC-029`, `SRC-033`, `SRC-034`) remain current-watch until independently checked.
5. Historical Yukawa/Markov claims are provenance, not evidence.
6. **(v0.2)** SRC-034 does not meet this file's own metadata standard (no authors/title recorded); it is retained as watchlist-only and barred from formal use until completed.

---

# M2. Canonical source registry / bibliography

> SRC-001..035 metadata checked 2026-08-11 (v0.1). SRC-036..051 added v0.2 from review session; **metadata verification pending** (assign to AR-015/AR-016/AR-017 as parented below).

### SRC-001 — Shared Substrate method
Roshka, Oleg. **Shared Substrate: A Discipline for Sustained Human–AI Coupling on Complex Problems.** Draft v0.2, 2026. SSRN DOI: 10.2139/ssrn.7218019. Repo: https://github.com/olegroshka/shared-substrate

### SRC-002 — Black-hole entropy
Bekenstein, J. D. **Black Holes and Entropy.** *Phys. Rev. D* 7, 2333–2346 (1973). https://doi.org/10.1103/PhysRevD.7.2333

### SRC-003 — Hawking radiation
Hawking, S. W. **Particle Creation by Black Holes.** *Commun. Math. Phys.* 43, 199–220 (1975). https://doi.org/10.1007/BF02345020

### SRC-004 — Page information curve
Page, D. N. **Information in Black Hole Radiation.** *Phys. Rev. Lett.* 71 (1993). https://arxiv.org/abs/hep-th/9306083

### SRC-005 — Hayden–Preskill
Hayden, P.; Preskill, J. **Black Holes as Mirrors.** *JHEP* 09 (2007) 120. https://arxiv.org/abs/0708.4025

### SRC-006 — Ryu–Takayanagi
Ryu, S.; Takayanagi, T. **Holographic Derivation of Entanglement Entropy from AdS/CFT.** *Phys. Rev. Lett.* 96, 181602 (2006). https://arxiv.org/abs/hep-th/0603001

### SRC-007 — HRT
Hubeny, V. E.; Rangamani, M.; Takayanagi, T. **A Covariant Holographic Entanglement Entropy Proposal.** *JHEP* 07 (2007) 062. https://arxiv.org/abs/0705.0016

### SRC-008 — Entanglement and connectivity
Van Raamsdonk, M. **Building up Spacetime with Quantum Entanglement.** *Gen. Rel. Grav.* 42, 2323–2329 (2010). https://arxiv.org/abs/1005.3035

### SRC-009 — Holographic QEC
Almheiri, A.; Dong, X.; Harlow, D. **Bulk Locality and Quantum Error Correction in AdS/CFT.** *JHEP* 04 (2015) 163. https://arxiv.org/abs/1411.7041

### SRC-010 — HaPPY code
Pastawski, F.; Yoshida, B.; Harlow, D.; Preskill, J. **Holographic Quantum Error-Correcting Codes.** *JHEP* 06 (2015) 149. https://arxiv.org/abs/1503.06237

### SRC-011 — Entanglement thermodynamics → gravity
Lashkari, N.; McDermott, M. B.; Van Raamsdonk, M. **Gravitational Dynamics From Entanglement "Thermodynamics".** *JHEP* 04 (2014) 195. https://arxiv.org/abs/1308.3716

### SRC-012 — Gravitation from entanglement
Faulkner, T.; Guica, M.; Hartman, T.; Myers, R. C.; Van Raamsdonk, M. **Gravitation from Entanglement in Holographic CFTs.** *JHEP* 03 (2014) 051. https://arxiv.org/abs/1312.7856

### SRC-013 — Entanglement equilibrium
Jacobson, T. **Entanglement Equilibrium and the Einstein Equation.** *Phys. Rev. Lett.* 116, 201101 (2016). https://arxiv.org/abs/1505.04753

### SRC-014 — JLMS
Jafferis, D. L.; Lewkowycz, A.; Maldacena, J.; Suh, S. J. **Relative Entropy Equals Bulk Relative Entropy.** *JHEP* 06 (2016) 004. https://arxiv.org/abs/1512.06431

### SRC-015 — Quantum extremal surfaces
Engelhardt, N.; Wall, A. C. **Quantum Extremal Surfaces.** *JHEP* 01 (2015) 073. https://arxiv.org/abs/1408.3203

### SRC-016 — Entanglement wedge and information paradox
Penington, G. **Entanglement Wedge Reconstruction and the Information Paradox.** *JHEP* 09 (2020) 002. https://arxiv.org/abs/1905.08255

### SRC-017 — Page curve from semiclassical geometry
Almheiri, A.; Mahajan, R.; Maldacena, J.; Zhao, Y. **The Page Curve of Hawking Radiation from Semiclassical Geometry.** *JHEP* 03 (2020) 149. https://arxiv.org/abs/1908.10996

### SRC-018 — Replica wormholes and radiation entropy
Almheiri, A.; Hartman, T.; Maldacena, J.; Shaghoulian, E.; Tajdini, A. **Replica Wormholes and the Entropy of Hawking Radiation.** *JHEP* 05 (2020) 013. https://arxiv.org/abs/1911.12333

### SRC-019 — Replica wormholes and the interior
Penington, G.; Shenker, S. H.; Stanford, D.; Yang, Z. **Replica Wormholes and the Black Hole Interior.** *JHEP* 03 (2022) 205. https://arxiv.org/abs/1911.11977

### SRC-020 — ER=EPR
Maldacena, J.; Susskind, L. **Cool Horizons for Entangled Black Holes.** *Fortsch. Phys.* 61, 781–811 (2013). https://arxiv.org/abs/1306.0533

### SRC-021 — Complexity=action
Brown, A. R.; Roberts, D. A.; Susskind, L.; Swingle, B.; Zhao, Y. **Complexity Equals Action.** *Phys. Rev. Lett.* 116, 191301 (2016). https://arxiv.org/abs/1509.07876

### SRC-022 — Soft hair
Hawking, S. W.; Perry, M. J.; Strominger, A. **Soft Hair on Black Holes.** *Phys. Rev. Lett.* 116, 231301 (2016). https://arxiv.org/abs/1601.00921

### SRC-023 — Fuzzball review / information paradox
Mathur, S. D. **Fuzzballs and the Information Paradox: A Summary and Conjectures.** arXiv:0810.4525 (2008).

### SRC-024 — Modern fuzzball / microstate review
Bena, I.; Martinec, E. J.; Mathur, S. D.; Warner, N. P. **Fuzzballs and Microstate Geometries.** arXiv:2204.13113 (2022).

### SRC-025 — Planck stars
Rovelli, C.; Vidotto, F. **Planck Stars.** *Int. J. Mod. Phys. D* 23, 1442026 (2014). https://arxiv.org/abs/1401.6562

### SRC-026 — White-hole remnants
Bianchi, E.; Christodoulou, M.; D'Ambrosio, F.; Haggard, H. M.; Rovelli, C. **White Holes as Remnants.** *Class. Quantum Grav.* 35, 225003 (2018). https://arxiv.org/abs/1802.04264

### SRC-027 — Remnants review 2014/2015
Chen, P.; Ong, Y. C.; Yeom, D. **Black Hole Remnants and the Information Loss Paradox.** *Phys. Rep.* 603, 1–45 (2015). https://arxiv.org/abs/1412.8366

### SRC-028 — Remnants review 2024
Ong, Y. C. **The Case For Black Hole Remnants: A Review.** arXiv:2412.00322 (2024).

### SRC-029 — Current critique of strong holographic QEC interpretation
Terashima, S. **Entanglement Wedge Reconstruction without Holographic Quantum Error Correction.** arXiv:2607.08684 (2026).

### SRC-030 — Non-isometric gravitational QEC
Kar, A. **Non-Isometric Quantum Error Correction in Gravity.** arXiv:2210.13476 (2022).

### SRC-031 — Markov maximon/minimon historical source
Markov, M. A. **The Maximon and Minimon…** *JETP Letters* 45, 141–144 (1987). Archive index: https://www.inr.ac.ru/a/r/m/m.htm

### SRC-032 — Planck-mass stable-particle remnant proposal
Aharonov, Y.; Casher, A.; Nussinov, S. **The Unitarity Puzzle and Planck Mass Stable Particles.** *Phys. Lett. B* 191, 51–55 (1987). https://doi.org/10.1016/0370-2693(87)91320-7

### SRC-033 — 2026 Planckian-remnant phenomenology
Dierckx, A.; Clesse, S.; Vidotto, F. **Signatures of Loop Quantum Gravity in Primordial Black Hole Cosmologies.** arXiv:2605.28953 (2026).

### SRC-034 — 2026 relic gravitational-wave phenomenology [WATCHLIST — metadata incomplete; barred from formal use]
*Phys. Rev. D* work on primordial-black-hole relics and induced gravitational waves; relics as a conditional hypothesis. DOI record checked 2026-08-11: https://doi.org/10.1103/fwhr-syl2 . Authors/title to be completed before any citation.

### SRC-035 — Yukawa extended-particle / elementary-domain historical context
Katayama, Y.; Yukawa, H. **Field Theory of Elementary Domains and Particles. I.** *Prog. Theor. Phys. Suppl.* 41, 1–21 (1968). https://doi.org/10.1143/PTPS.41.1

---

### SRC-036 — Einstein equation of state (v0.2; verify)
Jacobson, T. **Thermodynamics of Spacetime: The Einstein Equation of State.** *Phys. Rev. Lett.* 75, 1260 (1995). https://arxiv.org/abs/gr-qc/9504004

### SRC-037 — Entropic gravity (v0.2; verify)
Verlinde, E. **On the Origin of Gravity and the Laws of Newton.** *JHEP* 04 (2011) 029. https://arxiv.org/abs/1001.0785

### SRC-038 — Thermodynamic aspects of gravity (v0.2; verify)
Padmanabhan, T. **Thermodynamical Aspects of Gravity: New Insights.** *Rep. Prog. Phys.* 73, 046901 (2010). https://arxiv.org/abs/0911.5004

### SRC-039 — Gravity and the crossed product (v0.2; verify)
Witten, E. **Gravity and the Crossed Product.** *JHEP* (2022). https://arxiv.org/abs/2112.12828

### SRC-040 — Algebra of observables for de Sitter (v0.2; verify)
Chandrasekaran, V.; Longo, R.; Penington, G.; Witten, E. **An Algebra of Observables for de Sitter Space.** *JHEP* 02 (2023) 082. https://arxiv.org/abs/2206.10780

### SRC-041 — Thermal time hypothesis (v0.2; verify)
Connes, A.; Rovelli, C. **Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in Generally Covariant Quantum Theories.** *Class. Quantum Grav.* 11, 2899 (1994). https://arxiv.org/abs/gr-qc/9406019

### SRC-042 — Time-crystal no-go (verified 2026-08-11, AR-015 partial)
Watanabe, H.; Oshikawa, M. **Absence of Quantum Time Crystals.** *Phys. Rev. Lett.* 114, 251603 (2015). https://arxiv.org/abs/1410.2143 . DOI: 10.1103/PhysRevLett.114.251603

### SRC-043 — Floquet time crystals (verified 2026-08-11, AR-015 partial)
Else, D. V.; Bauer, B.; Nayak, C. **Floquet Time Crystals.** *Phys. Rev. Lett.* 117, 090402 (2016). https://arxiv.org/abs/1603.08001 . DOI: 10.1103/PhysRevLett.117.090402

### SRC-044 — Discrete time crystal observation (verified 2026-08-11, AR-015 partial)
Zhang, J.; Hess, P. W.; Kyprianidis, A.; et al. **Observation of a Discrete Time Crystal.** *Nature* 543, 217–220 (2017). https://arxiv.org/abs/1609.08684 . DOI: 10.1038/nature21413 . (Companions still unverified leads: Choi, S. et al., *Nature* 543, 221 (2017); later processor realization: Mi, X. et al., *Nature* 601, 531 (2022) — add SRC entries if load-bearing.)

### SRC-045 — Ab initio hadron masses (v0.2; verify)
Dürr, S. et al. (BMW Collaboration). **Ab Initio Determination of Light Hadron Masses.** *Science* 322, 1224–1227 (2008). DOI: 10.1126/science.1163233

### SRC-046 — Compton clock / matter-wave redshift claims (v0.2; verify)
Lan, S.-Y.; Kuan, P.-C.; Estey, B.; English, D.; Brown, J. M.; Hohensee, M. A.; Müller, H. **A Clock Directly Linking Time to a Particle's Mass.** *Science* 339, 554 (2013). Prior claim: Müller, H.; Peters, A.; Chu, S. **A Precision Measurement of the Gravitational Redshift by the Interference of Matter Waves.** *Nature* 463, 926 (2010).

### SRC-047 — Critique of the matter-wave redshift interpretation (v0.2; verify)
Wolf, P. et al. **Atom Gravimeters and Gravitational Redshift.** *Nature* 467, E1 (2010). (Record as the contested-interpretation counterpart to SRC-046.)

### SRC-048 — Zitterbewegung quantum simulation (v0.2; verify)
Gerritsma, R. et al. **Quantum Simulation of the Dirac Equation.** *Nature* 463, 68 (2010). https://arxiv.org/abs/0909.0674

### SRC-049 — Space from Hilbert space (verified 2026-08-11, AR-015 partial)
Cao, C.; Carroll, S. M.; Michalakis, S. **Space from Hilbert Space: Recovering Geometry from Bulk Entanglement.** *Phys. Rev. D* 95, 024031 (2017). https://arxiv.org/abs/1606.08444 . DOI: 10.1103/PhysRevD.95.024031

### SRC-050 — Causal sets (v0.2; verify)
Bombelli, L.; Lee, J.; Meyer, D.; Sorkin, R. D. **Space-Time as a Causal Set.** *Phys. Rev. Lett.* 59, 521 (1987).

### SRC-051 — Entanglement renormalization and holography (v0.2; verify)
Swingle, B. **Entanglement Renormalization and Holography.** *Phys. Rev. D* 86, 065007 (2012). https://arxiv.org/abs/0905.1317

### SRC-052 — Fidelity/Loschmidt-echo decay review (v0.4, AR-019; verify)
Gorin, T.; Prosen, T.; Seligman, T. H.; Žnidarič, M. **Dynamics of Loschmidt Echoes and Fidelity Decay.** *Phys. Rep.* 435, 33–156 (2006). https://arxiv.org/abs/quant-ph/0607050 . DOI: 10.1016/j.physrep.2006.09.003 . (Methodology-analogy source for AR-009 criterion (b): decay-regime taxonomy — perturbative/Gaussian, Fermi-golden-rule, perturbation-independent. Not load-bearing for any physics claim.)

### SRC-053 — Perturbation-independent decoherence-rate regime (v0.4, AR-019; verify)
Jalabert, R. A.; Pastawski, H. M. **Environment-Independent Decoherence Rate in Classically Chaotic Systems.** *Phys. Rev. Lett.* 86, 2490 (2001). (Origin of the Lyapunov/saturated fidelity-decay regime; methodology analogy only.)

### SRC-054 — DTC rigidity and criticality theory (v0.4, AR-019; verify)
Yao, N. Y.; Potter, A. C.; Potirniche, I.-D.; Vishwanath, A. **Discrete Time Crystals: Rigidity, Criticality, and Realizations.** *Phys. Rev. Lett.* 118, 030401 (2017). https://arxiv.org/abs/1608.02589 . (Phase-diagram/melting companion to the verified SRC-044 protocol. Caution of record: a 2021 Comment, arXiv:2109.00551, disputed aspects of the phase diagram; Reply arXiv:2109.07485 — verify pass must record what was conceded.)

### SRC-055 — Finite-size drift of the MBL critical disorder (v0.4, AR-019; verify)
Šuntajs, J.; Bonča, J.; Prosen, T.; Vidmar, L. **Quantum Chaos Challenges Many-Body Localization.** *Phys. Rev. E* 102, 062144 (2020). (arXiv ID unconfirmed recollection: 1905.06345 — check. Methodology analogy: threshold-location estimators drift with system size.)

### SRC-056 — Avalanche instability of localization thresholds (v0.4, AR-019; verify)
De Roeck, W.; Huveneers, F. **Stability and Instability Towards Delocalization in Many-Body Localization Systems.** *Phys. Rev. B* 95, 155129 (2017). (arXiv ID unconfirmed recollection: 1608.01815 — check.)

### SRC-057 — Regression-based dose–response guidance (v0.4, AR-019; verify)
OECD. **Current Approaches in the Statistical Analysis of Ecotoxicity Data: A Guidance to Application.** OECD Series on Testing and Assessment No. 54 (2006). DOI: 10.1787/9789264085275-en . (NOEC-vs-ECx methodology; NOEC is the structural analog of λ*-style grid thresholds.)

### SRC-058 — Dissent in the NOEC/ECx debate (v0.4, AR-019; verify)
Green, J. W. (author initials unconfirmed — check). **The Drive to Ban the NOEC/LOEC in Favor of ECx Is Misguided and Misinformed.** *Integr. Environ. Assess. Manag.* 9, 12–16 (2013). DOI: 10.1002/ieam.1367 . (Recorded so the AR-019 methodology analogy carries its own adversarial counterpart.)

### SRC-059 — Canonical quantum Zeno review (v0.5, AR-021; **verified 2026-08-14**, arXiv listing)
Facchi, P.; Pascazio, S. **Quantum Zeno dynamics: mathematical and physical aspects.** *J. Phys. A: Math. Theor.* 41, 493001 (2008), Topical Review. arXiv:0903.3297. DOI: 10.1088/1751-8113/41/49/493001. (Canonical home of the strong-coupling limit of dephasing-suppressed dynamics; the AR-010 quasiperiodic effect sits in the WEAK-coupling damping regime — cited for the mechanism family, not the regime.)

### SRC-060 — MI-network response to decoherence attacks (v0.5, AR-021; **verified 2026-08-14**, arXiv listing — PUBLISHED)
Sundar, B.; Walschaers, M.; Parigi, V.; Carr, L. D. **Response of quantum spin networks to attacks.** *J. Phys. Complex.* 2, 035008 (2021). arXiv:2012.10474. DOI: 10.1088/2632-072X/abf5c2. (Closest prior object: emergent mutual-information networks under decoherence — but STATIC ground states under projective attacks; no dynamics, no dephasing channel, no dynamical classes. Scope checked at abstract/summary level 2026-08-13.)

### SRC-061 — MI emergent-distance metricity (v0.5, AR-021; **verified 2026-08-14**, arXiv listing)
Leighton-Trudel, Beau. **Emergent Distance and Metricity of Mutual Information in 1D Quantum Chains.** arXiv:2507.09749 [cond-mat.stat-mech] (2025), preprint. DOI: 10.48550/arXiv.2507.09749. (SRC-049 lineage; stationary phase diagnostic — no temporal dynamics or noise response. Scope checked at abstract/summary level 2026-08-13.)

### SRC-062 — Noise-stabilized discrete time crystals (v0.5, AR-021; **verified 2026-08-14**, arXiv listing)
Shinjo, K.; Seki, K.; Yunoki, S. **Noise-stabilized discrete time crystals on digital quantum processors.** arXiv:2510.13577 (2025; v2 2026-03-31), preprint. DOI: 10.48550/arXiv.2510.13577. (Nearest live work in spirit: structured noise SUSTAINS subharmonic oscillations — noise stabilizing MOTION; the AR-010 effect is noise stabilizing geometric STATIONARITY over motion — same family, different object and direction.)

### SRC-063 — Noise-induced quantum synchronization (v0.5, AR-021; **verified 2026-08-14** via publisher listing + PMC/INSPIRE mirrors)
Tao, Z.; Schmolke, F.; Hu, C.-K.; Huang, W.; Zhou, Y.; Zhang, J.; Chu, J.; Zhang, L.; Sun, X.; Guo, Z.; Niu, J.; Weng, W.; Liu, S.; Zhong, Y.; Tan, D.; Yu, D.; Lutz, E. **Noise-induced quantum synchronization with entangled oscillations.** *Nat. Commun.* 16, 8457 (2025). DOI: 10.1038/s41467-025-63196-6. (Adjacent noise-stabilized-dynamics literature; recorded for the AR-021 framing verdict.)

---

# Q. Changelog v0.1 → v0.2

1. Added §C TH-029 (Jacobson 1995 equation of state) and TH-030 (entropic/thermodynamic-gravity programmes) — restoring the thermodynamic-gravity lineage dropped between the drafting session's proposed structure (TL-15) and the v0.1 delivery.
2. Added §M (algebraic structure and time): TH-031 (crossed products / Type II / algebraic generalized entropy), TH-032 (thermal time hypothesis).
3. Added §O (cross-level persistence exemplars): TH-033 (time crystals: no-go + driven realization — the CON-034 witness template), TH-034 (dynamical hadron mass), TH-035 (internal clocks and gravity coupling, contested parts recorded), TH-036 (quasinormal ringing as geometric-oscillation null comparator).
4. Added §P: TH-037 (Cao–Carroll–Michalakis emergent metric — toy-model tooling), TH-038 (causal sets, watch-level; restores dropped TL-13).
5. Extended TH-012 with Swingle/MERA pointer.
6. Rewrote K.2 (established-below-gravity, open-at-gravity) and K.4 (per-level oscillation ledger).
7. Extended seam matrix with Jacobson-1995, entropic gravity, crossed product, thermal time, MI-graph geometry, internal clocks, time crystals; revised first-pass inference (modular structure × clock junction).
8. Added SRC-036..051 (all flagged verification-pending); governance rule 6 barring incomplete SRC-034 from formal use.
9. Reserved an SRC slot for a canonical quasinormal-mode review (AR-015 to select).

---

# R. Changelog v0.2 → v0.3

1. SRC-042, SRC-043, SRC-044, SRC-049 verified against primary records (arXiv/ar5iv/nature.com, 2026-08-11); `verify` flags dropped; DOIs added; SRC-044 page range completed (217–220). Evidence: `ar/AR-015_partial-2026-08-11_trackE3-G1.md`.
2. TH-033: added the no-go's scope condition (not-too-long-range interactions) and the verified TTSB-definition/witness content; companion sources (Choi, Mi) remain unverified leads.
3. TH-037: added verified equation locations (SRC-049 eqs. 9, 13, 14, 23–25) and author-stated caveats.
4. Effect: Track E3's G1 scope (KB-005 §4) is cleared; TH-033/TH-037 may be cited as load-bearing by AR-009/AR-010.

---

# S. Changelog v0.3 → v0.4

1. Added SRC-052..058 (AR-019 robustness-instrument survey, 2026-08-12), all flagged `verify`: fidelity/Loschmidt-echo decay (SRC-052, SRC-053), DTC rigidity theory with Comment/Reply caution (SRC-054), MBL threshold finite-size fragility (SRC-055, SRC-056), dose–response NOEC/ECx methodology with recorded dissent (SRC-057, SRC-058). All are methodology-analogy sources for AR-009 criterion (b); none is load-bearing for a physics claim. Evidence: `ar/AR-019_note-2026-08-12_robustness-instruments.md`.
2. No TH-* changes.
