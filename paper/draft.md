# Motion-borne geometry: when an information metric needs the dynamics beneath it

**Oleg Roshka**

*Draft v0.1 — 2026-08-13. Target: SciPost Physics. Markdown working
draft; LaTeX conversion at submission prep. Author line and
acknowledgements pending owner confirmation.*

---

## Abstract

A stable emergent structure can relate to its substrate in two ways: it
can be merely *instantiated* — some motionless configuration of the
substrate would carry the same structure — or it can be *actively
maintained*, existing only because the substrate moves. We introduce an
operational test that separates the two, and apply it in a preregistered
numerical study of the mutual-information-graph metric of finite spin
chains, across fixed-point, quasiperiodic, chaotic, metastable,
localized, and driven (discrete-time-crystal) dynamics. The test has
three probes: witnessed motion beneath a stationary metric, response to
switching the dynamics off, and an explicit search for a motionless
state carrying the same time-averaged structure. The outcome is a
single-survivor split. Every class's time-averaged metric can be
reproduced by some stationary state — chaotic classes almost exactly,
consistent with eigenstate thermalization — except the quasiperiodic
class: across 80 runs at two system sizes, no stationary state within a
broad smooth-of-H family comes within the stationarity threshold. The
same class is independently singled out by its response to weak
dephasing, which *pins* its moving metric to the time average — a
negative drift ratio stable over two decades of noise strength — while
destabilizing chaotic-class metrics. Incommensurate coherence-carried
motion is thus the one regime, in this family, whose emergent structure
demonstrably needs its dynamics. The study was preregistered with
committed seed manifests and a dated amendment log; its discipline
caught four failure modes before publication, including the discovery
that the out-of-time-order correlator — the field's default dynamics
diagnostic — fails a basic witness requirement: it fires on frozen
states. We report the corrected instruments, the corrections themselves,
and class-resolved scope walls (including a measured, class-dependent
partition-dependence of the metric).

---

## 1. Introduction

*(to be drafted last, per writing plan — contributions list, positioning
against [SRC-049, SRC-060, SRC-061] (MI-network geometry, static),
[SRC-043, SRC-044] (DTC), [SRC-062, SRC-063] (noise-stabilized
dynamics), [SRC-059] (Zeno/damping mechanism family); non-claims box:
no gravity, no primitive-information assumption, external lab clock,
no firstness claims.)*

## 2. Models, functional, witnesses, and protocol

### 2.1 Model family

All models are open chains of $N$ qubits with $\hbar = 1$ and the
nearest-neighbour coupling setting the unit of energy and time. Every
dynamical statement below is made with respect to an external laboratory
clock; the drive of the Floquet family defines a second, stroboscopic
clock derived from it. Nothing in this study bears on the question of
clocks internal to a system, which we regard as out of scope.

We use three tracks. Track A collects four closed-system classes chosen
to span the qualitative types of quantum motion:

| class | Hamiltonian | initial ensemble | class certificate |
|---|---|---|---|
| (i) fixed point | transverse-field Ising, $H=-\sum_i \sigma^z_i\sigma^z_{i+1} - g\sum_i\sigma^x_i$, $g=1.5$ | ground state (single deterministic run) | gapped, nondegenerate |
| (ii) quasiperiodic | XX chain, $H=\tfrac12\sum_i(\sigma^x_i\sigma^x_{i+1}+\sigma^y_i\sigma^y_{i+1})$ | 20 superpositions of 3 single-magnon modes with pairwise-incommensurate Bohr gaps | free-spectrum reconstruction $<10^{-8}$ |
| (iii) chaotic | mixed-field Ising, $(h_x,h_z)=(0.9045,0.8090)$ | 20 Haar-random product states | $\langle r\rangle = 0.529\text{–}0.542 \in [0.51,0.55]$ |
| (iv) metastable | ferromagnetic Ising, $g=0.05$, weak-disorder dressings $\delta g_i \in [-0.01,0.01]$ | $\lvert\uparrow\cdots\uparrow\rangle$, 20 dressings | quasi-degenerate doublet |

Track C reuses the chaotic and quasiperiodic Hamiltonians as
"scrambling" and "integrable" regimes with N\'eel-anchored product-state
ensembles, and adds a localized regime (XXZ with random fields,
$\Delta=1$, $W=8$; 20–40 disorder realizations;
$\langle r\rangle = 0.38\text{–}0.40 \in [0.36,0.42]$). Track B is a
kicked-Ising discrete time crystal modeled on the established protocol
[SRC-043, SRC-044]: an imperfect global $\pi$-flip ($\varepsilon$ the
imperfection) alternating with disordered Ising interactions, 20
disorder realizations $\times$ 5 initial product states, with two
comparator regimes — no interactions (r1) and no disorder (r2).

The class certificates in the table are *preregistered sanity checks*,
run before any confirmatory analysis at every system size used. One
failed as originally registered: we specified a Poisson level-statistics
window for the integrable class, which is a heuristic for generic
integrable models and is inapplicable to a free chain whose many-body
spectrum is exactly the subset-sums of its single-particle spectrum. The
replacement certificate — reconstruction of the many-body spectrum from
single-particle energies to $10^{-8}$ — is strictly stronger, and the
mis-specification plus its dated repair are part of the study record
(Appendix C). A second certificate finding: the quasiperiodic
incommensurability requirement is *exhaustively unsatisfiable* at
$N=8$ (0 of 56 magnon triples pass), which fixed the usable size range
$(10, 12)$ for class comparisons.

### 2.2 The information metric and its stationarity

From the state (pure or mixed) we compute all one- and two-site reduced
density matrices, the pairwise mutual information
$I_{ij} = S_i + S_j - S_{ij}$, and normalize
$x_{ij} = I_{ij}/(2\ln 2)$. Following the emergent-metric construction
of [SRC-049], link weights are $w_{ij} = -\ln x_{ij}$, regularized by a
floor $x_{\min}=10^{-6}$, and the *metric* $D(t)$ is the matrix of
weighted shortest-path distances on the complete graph over sites. We
emphasize the scope of the word "metric" here: $D$ is the metric
structure of the mutual-information graph on a *posited* site
factorization. It is not a claim about spacetime, and its dependence on
the factorization is measured, not assumed away (§8).

Stationarity is judged on the window $\mathcal{W} = [20, 200]$ (units of
inverse coupling; stroboscopic periods for Track B), sampled every
$\Delta t = 0.5$: with $\bar D$ the window mean and
$\delta\Phi(t) = \lVert D(t)-\bar D\rVert_F / \lVert\bar D\rVert_F$, the
metric is stationary iff $\max_{t\in\mathcal W}\delta\Phi(t) <
\varepsilon_\Phi = 0.25$. The threshold was set by a preregistered
calibration pilot that measured the construction's finite-size
fluctuation floor (the originally registered $0.05$ sat below the noise
floor of every dynamical class — an instrument artifact the pilot
existed to catch; Appendix C, Amendment 3). A cap diagnostic — the same
drift restricted to above-floor links — is reported alongside every
verdict to expose any cap dominance; none of the verdicts below is
cap-dominated.

### 2.3 Witnesses and the null-silence requirement

The claim "the metric is stationary while the state moves" is only as
good as the certificate of motion. We require every *witness of motion*
to satisfy a null-silence condition: **it must vanish identically on a
frozen state.** The null comparator is class (i) — an eigenstate,
whose evolution is a global phase — and the preregistered rule is that
any witness which fires on the null is discarded as a witness,
whatever its other virtues.

The battery: (W1) the participation ratio $\mathrm{PR}_A$ of the binned
Bohr spectral measure $\sum_{m,n}|c_m|^2|c_n|^2\,\delta(\omega -
|E_m-E_n|)$, equal to 1 exactly on the null; (W2) the recurrence
distance $d(t) = 1-|\langle\psi(t_0)|\psi(t)\rangle|^2$, identically
zero on the null, summarized by its window mean; (W4) the off-diagonal
energy coherence $\Xi = \sum_{E_m\neq E_n}|\rho_{mn}|^2$, computed over
energy-*distinct* pairs so that coherence within a degenerate level —
which does not move — does not fire it; and, for Track B, (W5) the
subharmonic Fourier weight of the stroboscopic magnetization at half
the drive frequency, with its rigidity curve $h_{\rm sub}(\varepsilon)$.
All are invariant under global phase and basis relabelings in the
senses catalogued in Appendix D.

We also registered (W3) an out-of-time-order correlator,
$C(r,t)=\tfrac12\langle|[\sigma^z_{i_0+r}(t),\sigma^z_{i_0}]|^2\rangle$,
with saturation value and arrival time as statistics. It failed the
null test — measured, not argued: on the frozen fixed point it rises to
$C\approx 1.11$ by $t=1.5$. The OTOC certifies Heisenberg-*operator*
spreading, which a gapped ground state supports; it does not certify
state motion. Under the preregistered rule its statistics were
discarded from the class-separation criterion, with consequences
reported in §4. We keep it in the outputs as the operator-spreading
diagnostic it actually is.

### 2.4 Comparators and perturbation protocols

Three controls give the sustained-by test its content. The *diagonal
ensemble* $\bar\rho = \sum_n |c_n|^2 |n\rangle\langle n|$ is the
canonical motionless partner of a run: exactly stationary, with the
same time-averaged two-site reduced density matrices. We registered it
as "matched to the time-averaged metric by construction" — which is
false, and measurably so: mutual information is nonlinear in the
(correctly time-averaged) reduced density matrices, and $\Phi[\bar\rho]$
sits 43–90% away from $\bar D$ depending on class. The corrected
comparator methodology — an explicit optimization over stationary
states — is described with its results in §6. The *switch-off test*
dephases the state in the energy eigenbasis mid-window (equivalently:
projects onto $\bar\rho$, since populations are conserved) and asks
whether the metric's behaviour changes. And three *perturbation
protocols* — a local Hamiltonian quench $\lambda\sigma^z$, a local
dephasing channel of rate $\gamma$, and the loss of two non-adjacent
sites — probe robustness through the scale-free log drift ratio
$\log\rho = \log[\max_{t>t_p}\delta\Phi_{\rm pert} /
\max(\max_{t>t_p}\delta\Phi_{\rm unpert}, 10^{-3})]$, with strengths
$(\lambda, \gamma) = (0.1, 0.01)$ fixed by the calibration pilot before
any confirmatory run.

### 2.5 Preregistration protocol and statistics

Every metric, threshold, witness, comparator, and analysis rule above
was fixed in a specification document before implementation code was
written; every run consumed seeds from manifests committed to the
repository before execution; and every post-hoc change is a dated entry
in an amendment log, reproduced in full as Appendix C with commit
hashes. The study ran as: specification → threshold review →
calibration pilot (exploratory, excluded from confirmatory statistics)
→ confirmatory campaign → an adversarial companion analysis tasked
with attacking our own conclusions → a witness-battery reformalization
forced by the null-test failure, itself confirmed on fresh seeds. Class
separation is judged by exact Mann–Whitney AUC $\geq 0.95$ for at least
two witness statistics per class pair at two system sizes (singleton
classes by exact-value exclusion); robustness differences by
$|\Delta\,\overline{\log\rho}| > \ln 1.5$ with disjoint BCa bootstrap
confidence intervals, replicated with consistent direction at two
sizes; disordered ensembles resample at the realization level. Where a
sharp threshold met a finite ensemble, seed sensitivity was measured
and stabilized (n = 40, §4); where it met a third size, the trend was
checked descriptively (N = 14, Appendix B).

## 3. Results I: stationary metrics over witnessed motion

*(next drafting block)*

## 4. Results II: the witness discipline at work

*(next drafting block)*

## 5. Results III: class-resolved robustness and the dephasing sign structure

*(next drafting block)*

## 6. Results IV: the motionless-comparator search — one class survives

*(next drafting block)*

## 7. Results V: the driven regime

*(next drafting block)*

## 8. Scope walls and limitations

*(next drafting block)*

## 9. Discussion and outlook

*(next drafting block)*

## Appendices

*(A: numerics; B: statistics + size trend; C: the amendment log with
commit hashes; D: invariance battery; E: Track-B implementation notes —
assembled from the evidence packets)*
