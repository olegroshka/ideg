# Motion-borne geometry: when an information metric needs the dynamics beneath it

**Oleg Roshka**

*Draft v0.3 — 2026-08-14. Target: SciPost Physics. All sections and
appendices drafted; Markdown working draft, LaTeX conversion at
submission prep. Pending: figures (6, inventory in paper/OUTLINE.md),
owner pass on the full text, author line / acknowledgements / data
statement, SRC-059..063 metadata verification before the reference
list is finalized.*

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

A stable emergent structure can stand in two different relations to the
substrate that carries it. It can be *merely instantiated*: some
motionless configuration of the substrate would carry the same
structure, and the observed dynamics is incidental to it. Or it can be
*actively maintained*: the structure exists only because the substrate
moves, and no frozen configuration reproduces it. The distinction is
easy to state and surprisingly hard to test — most diagnostics of
"underlying dynamics" do not actually certify that anything is moving,
and most claims of "the dynamics sustains the structure" are never
confronted with a serious search for a motionless impostor.

This paper builds that test and runs it, in the most controlled setting
we could construct: finite spin chains, where the emergent structure is
the mutual-information-graph metric of Refs. [SRC-049, SRC-060,
SRC-061] — pairwise mutual information converted to link weights and
shortest-path distances on a posited site factorization — and the
substrate dynamics ranges over fixed-point, quasiperiodic, chaotic,
metastable, localized, and driven (discrete-time-crystal [SRC-043,
SRC-044]) classes. Prior work on such information-metric structures has
been static: ground-state network robustness under projective attacks
[SRC-060], metricity as a phase diagnostic [SRC-061]. Our object is the
*time dependence* of the structure over a moving state, and its need —
or lack of need — for that motion.

The test has three probes. A *witness battery* certifies that the state
moves while the metric does not, under a requirement we treat as
non-negotiable: a witness of motion must vanish identically on a frozen
state. A *switch-off response* measures what happens to the metric when
the motion is killed in place. And a *motionless-comparator search*
optimizes explicitly over stationary states for one that carries the
same time-averaged metric. The three probes are preregistered — every
metric, threshold, and analysis rule fixed before code was written,
every run seeded from committed manifests, every post-hoc change a
dated amendment (Appendix C) — because a study of this shape has one
dominant failure mode, self-deception through flexible metric choice,
and we preferred to make our mistakes in public.

The mistakes were made, caught, and are reported as results. Four
times, the discipline fired: a registered class certificate was
mis-specified (Poisson statistics for a free chain); the
out-of-time-order correlator — the field's default dynamics diagnostic
— failed the null test, firing on a frozen ground state, and was
discarded by its own preregistered clause; an early robustness
comparison was exposed by our adversarial re-analysis as a
floored-denominator artifact; and a narrow first version of the
comparator search over-claimed unmatchability for two classes that a
hardened search then matched. What survives this gauntlet is
correspondingly compact:

1. **An operational test** of instantiated-vs-maintained emergent
   structure (witnesses with null-silence, switch-off, comparator
   search), portable to any system with a computable structural
   functional.
2. **A single-survivor measurement.** Every class's time-averaged
   metric is carried by some stationary state — chaotic classes almost
   exactly, consistent with eigenstate thermalization — except the
   quasiperiodic class: 0 of 80 runs matchable at two system sizes,
   robustly across mode numbers and optimizer strength.
3. **A sign structure.** Weak dephasing *stabilizes* the moving metrics
   of coherence-carried classes (negative log drift ratio, flat over
   two decades of noise strength) while destabilizing chaotic-class
   metrics — the same class singled out by the comparator search is
   singled out by noise. The mechanism is standard decoherence damping
   [SRC-059]; the class-resolved geometric reading appears, within the
   scope of our survey [SRC-060–SRC-063], to be unreported.
4. **A methods record.** The null-silence filter and the fresh-seed,
   power-stabilized adjudication of sharp statistical criteria — with
   the OTOC's failure and the seed-lottery episode as measured
   exhibits, and the complete dated amendment log as Appendix C.
5. **A driven-phase case study** in which the sustained-by question
   resolves *negatively* despite maximal appearances: the
   discrete-time-crystal metric survives removal of its drive
   unchanged — localization, not the subharmonic motion, holds it.

**What this paper does not claim.** The metric is an
information-theoretic construct on a posited factorization; its
factorization dependence is measured (§8) and it is not spacetime
geometry — no claim here touches gravity or holography. No mechanism
is claimed as new physics. No assumption is made that information is
ontologically primitive. All dynamics is stated against an external
laboratory clock. We make no priority claims about preregistration in
computational physics; the artifact is offered, not its firstness. The
model family is small ($N \leq 14$) and the conclusions are in-model.

Section 2 defines the family, functional, witnesses, and protocol;
Sections 3–7 report results; Section 8 states the scope walls;
Section 9 discusses what the test opens up.

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

The baseline campaign establishes the phenomenon the rest of the paper
interrogates: metrics that do not move over states that demonstrably do.

At the calibrated threshold $\varepsilon_\Phi = 0.25$, the chaotic and
scrambling ensembles are metric-stationary in every run (20/20 at each
size; max window drift $0.09$–$0.21$) while their motion witnesses read
near maximum: $\Xi \geq 0.96$, recurrence mean $\approx 1 - 1/D$, and
Bohr participation ratios in the hundreds to thousands. The driven
track is the sharpest instance: at drive imperfection
$\varepsilon = 0.03$, all 100 runs are metric-stationary while the
subharmonic witness reads $0.939$ — a locked period-doubled
magnetization response over a frozen mutual-information metric. At the
other extreme, the quasiperiodic and metastable classes have genuinely
moving metrics (max drift $0.53$–$1.61$; no run stationary), the
integrable regime likewise ($0.35$–$0.64$), and the fixed point is
stationary to machine precision ($2\times10^{-13}$) with every witness
silent — the null behaving as a null. The localized regime straddles
the threshold (80/100 stationary at $N=12$, drift $0.14$–$0.34$) and is
treated as a boundary case throughout.

Two honesty notes frame everything that follows. First, for the chaotic
classes, metric stationarity over motion is *expected*: the metric is
built from two-site observables, and the equilibration of local
observables in quenched chaotic systems is standard physics. The
existence table is the setup, not the result. Second, none of these
verdicts is an artifact of the weight floor in the metric construction:
the above-floor drift diagnostic tracks the full-graph drift in every
class, and the mean graphs have no floor-dominated links.

## 4. Results II: the witness discipline at work

This section reports the study's methodological core: what the
preregistered witness requirements did when the data pushed back. We
present it as a dual record — the original registration failed; the
owner-ratified repair passed on fresh seeds — because both halves are
results.

**The OTOC is not a witness of motion.** The null-silence requirement
(§2.3) demands that a witness vanish on the frozen class-(i) state. The
out-of-time-order correlator fails: on the gapped ground state it
reaches the arrival threshold at $t^*=1.5$ and saturates at
$C \approx 1.11$. Nothing is wrong with the OTOC as physics — it
certifies operator spreading, which a frozen state supports — but that
is precisely why it cannot certify that a *state* is moving. The
preregistered discard clause executed, removing both OTOC statistics
from the class-separation criterion.

**The discard had teeth.** With the OTOC gone, the original battery
left exactly one class pair under-witnessed: scrambling vs. localized
separated on $\Xi$ alone (AUC $0.985$/$0.990$ at the two sizes), with
the Bohr participation ratio degrading with size ($0.89 \to 0.56$) and
the registered recurrence statistic — the window *minimum* — landing at
$0.71$/$0.945$. Criterion (a), as originally registered, therefore
**fails**. The counterfactual is recorded: had the OTOC been retained,
its arrival time separates that pair at AUC $1.0$ (localized fronts
never arrive; scrambling fronts arrive at $t \approx 2$). The failure
is single-cause, and it is a finding about witness design: the natural
scrambling/localization discriminator is not null-silent, and the
null-silent battery we registered was one statistic short.

**The repair, and what fresh seeds taught us.** The reformalized
battery replaces the recurrence minimum — structurally uninformative
for slow classes, since a slowly rotating state revisits its reference
— with the recurrence *mean*, which is null-silent by construction and
class-resolving in practice. On the data that motivated the redesign,
all 18 pair-size checks passed; we labeled that table validation, not
confirmation, and re-adjudicated on fresh committed seeds. At the
registered ensemble size ($n=20$) the fresh seeds **failed** a
different pair — scrambling vs. integrable at $N=10$, all three
statistics between $0.85$ and $0.93$ — while passing at $N=12$. The
diagnosis is statistical, not physical: a sharp AUC threshold of
$0.95$ estimated from 20-vs-20 samples carries a standard error of
$0.05$–$0.08$, so near-threshold verdicts are seed-lotteries. Doubling
the ensembles ($n=40$, fresh seeds again) stabilized every margin:
**all 18 pair-size checks pass**, the previously marginal pair at
$0.952$–$0.979$, and the repaired pair at $0.987$–$0.992$ (the Bohr
ratio for scrambling vs. localized remains honestly weak, $0.59$ at
$N=12$ — two statistics carry the pair, as the criterion requires). A
descriptive third size ($N=14$, computed from eigenbasis coefficients
alone) confirms the monotone trend: all three statistics
$\geq 0.976$.

The two methodological claims we take from this: null-silence is a
nontrivial filter that the field's default dynamics diagnostic fails;
and sharp-threshold criteria on small ensembles must be fresh-seeded
and, near the threshold, power-stabilized — our original-seed
validation table would have over-claimed.

## 5. Results III: class-resolved robustness and the dephasing sign structure

The robustness criterion asks whether metric stationarity responds to
perturbation differently in different dynamical classes. Under local
dephasing at the calibrated rate $\gamma = 0.01$, it does, with a sign
structure that is the study's most striking single measurement.

The mean log drift ratios, replicated at two sizes with disjoint
confidence intervals and consistent direction: chaotic and scrambling
$+2.1$ to $+2.2$ (noise strongly destabilizes their stationary
metrics), localized $+1.5$, integrable $+0.75$ — and the
coherence-carried classes *negative*: metastable $-0.09$/$-0.11$,
quasiperiodic $-0.27$. Weak dephasing makes the quasiperiodic metric
*more* stationary than its own unperturbed dynamics: the noise damps
the coherences whose beating carries the metric's oscillation, pinning
$D(t)$ to its time average. Every pairwise contrast required by the
registered criterion clears the $\ln 1.5$ threshold in both tracks at
both sizes; the class ordering
(chaotic $\approx$ scrambling $>$ localized $>$ integrable $>$
metastable $\gtrsim$ quasiperiodic, the last two negative) is the
pilot's ordering, confirmed at scale.

A descriptive strength sweep shows the sign structure is a regime, not
a point: across two decades $\gamma \in [10^{-3}, 10^{-1}]$ the
quasiperiodic response is flat at $\approx -0.25$, the metastable
response strengthens monotonically ($-0.02 \to -0.22$), the
chaotic-class response rises and saturates ($+0.9 \to +2.5$), and the
ordering never reorders. The mechanism is standard open-system physics
— decoherence damping of coherence-carried oscillations, the weak-rate
side of the Zeno family [SRC-059] — and we claim none of it as new. The
class-resolved *geometric* reading — noise as a stabilizer of moving
information metrics and a destabilizer of chaotic ones, with the sign
tracking the dynamical class — is, to the extent of our survey
[SRC-060–SRC-063], unreported; we state this conditionally and note
the survey was not systematic.

The other two protocols are clean nulls at the registered strengths:
the local quench leaves every dynamical class's drift ratio at
$|\overline{\log\rho}| \leq 0.07$, and two-site loss reads
$0.07$–$0.25$ everywhere. (The fixed point's large quench ratio,
$+4.4$, is floor-referenced — its unperturbed drift is exactly zero —
and carries no class information; instrument note in Appendix B.)
All robustness statements are statements at the calibrated strengths
and, per the sweep, within the probed regime — not strength-independent
class properties.

## 6. Results IV: the motionless-comparator search — one class survives

The sharpest form of the sustained-by question is: *does there exist a
motionless state carrying the same time-averaged metric?* If yes, the
dynamics is optional for the structure; if no, the structure is
motion-borne. This section reports the search, including the two
corrections our own audits forced.

**The canonical comparator is not matched.** The diagonal ensemble
$\bar\rho$ — the motionless state with the run's exact time-averaged
two-site reduced density matrices — was registered as metric-matched by
construction. It is not: mutual information is nonlinear in the reduced
density matrices, and $\Phi[\bar\rho]$ sits $43$–$90\%$ of
$\lVert\bar D\rVert$ away from the run mean, depending on class.
Relatedly, our first robustness comparison against $\bar\rho$ produced
a large "the comparator is more fragile" differential that an
adversarial re-analysis exposed as a floored-denominator artifact (the
comparator has no baseline drift to compare against; its absolute
perturbed response is in fact *smaller*). Both corrections are dated in
the study record; what survives them is stronger than what they
replaced.

**The switch-off measurement.** Dephasing the state mid-window — which
projects exactly onto $\bar\rho$ — moves the metric by $43$–$90\%$ of
$\lVert\bar D\rVert$ (chaotic $0.54$, scrambling $0.52$, integrable
$0.85$, metastable $0.90$, localized $0.90$, quasiperiodic $0.43$).
Killing the motion does not freeze the metric in place; it changes the
metric. For the metric-stationary classes this registers as a drift
increase with disjoint confidence intervals.

**The optimization search, hardened.** We then searched explicitly for
*any* motionless match: stationarity means $[\sigma, H]=0$, so we
optimized over populations on the energy eigenbasis — three natural
families (thermal at both temperature signs, depolarized diagonal
ensemble, Gaussian microcanonical) and a general smooth-$f(H)$ family
(log-populations parameterized by up to 24 Chebyshev coefficients,
multi-start optimization), over full ensembles at both criterion sizes.
A first, narrower version of this search (families only, one run per
class) wrongly suggested the metastable and integrable classes were
unmatchable; the hardened search corrected this before drafting, and
the correction is part of the record.

The final result is a single-survivor split. Matchable within
$\varepsilon_\Phi$: chaotic and scrambling in every run, almost exactly
(median miss $0.035$–$0.046$ — a Gaussian microcanonical window
reproduces the time-averaged metric of a chaotic state, as eigenstate
thermalization would suggest); metastable in every run
($0.09$–$0.13$); integrable in every run ($0.16$–$0.17$); localized as
a boundary case (3–6 of 20 runs, median $\approx 0.27$). Unmatched:
**the quasiperiodic class, in 0 of 80 runs across both sizes** (median
miss $0.31$; the single closest run reaches $0.264$, still above
threshold), robustly across mode numbers $m = 3, 4, 5$ (medians
$0.31$–$0.33$) and insensitive to enriching the optimizer. The claim is
bounded by its search space — stationary states that are smooth
functions of $H$ — and is not an impossibility theorem; within that
space, it is unambiguous.

Two independent instruments therefore single out the same class. The
quasiperiodic metric is the only one that no searched motionless state
can carry, and the only one that weak noise *stabilizes*. Incommensurate
coherence-carried motion is, in this family, the regime whose emergent
structure needs its dynamics: motion-borne in the operational sense
this paper defines. Conversely, the chaotic classes' stationary metrics
are compatible-with their motion — a thermal-window state carries the
same structure — while their *robustness signature* still
distinguishes them (§5): the two probes answer different questions, and
both answers are class-resolved.

## 7. Results V: the driven regime

The discrete-time-crystal track supplies the study's cleanest
stationary-with-witness regime and its most instructive
compatible-with verdict.

At $\varepsilon = 0.03$, deep in the rigid phase, all 100 runs are
metric-stationary while the subharmonic witness reads $0.939$: a
period-doubled magnetization response, locked across 20 disorder
realizations, above a mutual-information metric that does not move.
Stationarity degrades with drive imperfection (88/100 at
$\varepsilon = 0.06$, 52/100 at $0.10$), tracking the witness. The
rigidity curve is measured over its full range: the subharmonic weight
holds above $0.65$ through $\varepsilon = 0.20$, crosses $1/2$ at
$\varepsilon_c \approx 0.23$ at our drive parameters, and collapses by
$\varepsilon \approx 0.45$ — a complete critical-strength measurement
for this realization of the [SRC-043, SRC-044] protocol.

The switch-off test resolves the sustained-by question for this regime,
and resolves it *against* the drive: removing the kicks at mid-window
collapses the witness ($0.95 \to 0.00$) while the metric's
stationarity persists and slightly improves (mean post-window drift
$0.110 \to 0.086$). The frozen-in disorder, not the drive, holds this
metric — the witnessed subharmonic motion is compatible with the
stationary structure, not required by it. We registered this as an
open question with exactly this outcome listed as reportable, and
report it accordingly. Consistently, the perturbation protocols at the
calibrated strengths barely move the DTC metric
($\overline{\log\rho} = 0.01$–$0.19$).

The comparator regimes behave asymmetrically, and honestly. Without
interactions (r1), the subharmonic peak is destroyed at
$\varepsilon = 0.03$ ($0.13$) — the fine-tuned control fails as
expected, certifying that interactions produce the rigidity. Without
disorder (r2), however, the clean interacting drive does *not*
thermalize on any horizon we probed: its subharmonic response persists
undiminished ($0.89$–$0.90$) to 2000 periods. At small $\varepsilon$
the r2 regime is not a usable thermalizing control, and the
discriminating comparator burden falls entirely on r1 — a
comparator-scope finding we report rather than bury.

## 8. Scope walls and limitations

**The metric belongs to the factorization.** Everything here is
computed on the natural site partition, and the dependence on that
choice is not small and not uniform: under fixed nonlocal two-site
frame changes, the metric moves by a class-dependent amount — mean
relative change $0.11$ (chaotic), $0.15$ (scrambling), $0.20$
(localized), $0.22$ (integrable), $0.42$ (quasiperiodic), $0.53$
(metastable, maximum observed $0.82$). The coherence-carried classes —
including the survivor class of §6 — have the most frame-dependent
metrics. This does not undermine the within-frame comparisons (every
matchability and robustness statement compares objects in the same
partition, which transforms both sides together), but it bounds the
interpretation: these are properties of the metric-on-a-factorization,
not of the state alone. Notably, strictly local (single-site) frame
changes leave the metric invariant to machine precision — the
dependence lives entirely at the partition level, which is where the
construction's own authors located their caveat [SRC-049].

**Finite size, finite family, finite search.** Criterion verdicts are
established at $N \in \{10, 12\}$ with a descriptive $N=14$ point; the
quasiperiodic construction is exhaustively unsatisfiable at $N=8$
(0/56 candidate mode triples), which is a warning about small-size
instantiations of incommensurability generally. The stationarity
threshold $\varepsilon_\Phi = 0.25$ is calibrated to this
construction's finite-size noise floor and has no significance beyond
it. The comparator search spans stationary states that are smooth
functions of $H$; fine-tuned non-smooth populations are outside it,
and the unmatchability result is bounded accordingly. The localized
regime straddles the stationarity threshold (80/100) and we have kept
it out of every headline count. Robustness statements hold at the
calibrated strengths and within the swept regime
($\gamma \in [10^{-3}, 10^{-1}]$). All clocks are external laboratory
clocks; nothing here addresses systems that must supply their own.

## 9. Discussion and outlook

What the study delivers is not a mechanism but an instrument: the
instantiated-vs-maintained distinction, usually a rhetorical flourish,
is here an executable measurement with three independent probes — and
its first execution returned a sharp, doubly-corroborated answer. In
this family, thermalizing motion builds structures a motionless
thermal state could carry; incommensurate coherent motion builds one
that nothing motionless we searched can carry, and that noise defends
rather than destroys.

The result points directly at a next question: is there a form of
robustness that *recurrent* or quasiperiodic dynamics provides and
fixed points cannot? The two signatures reported here — unmatchability
and noise-stabilization, coinciding in one class — are exactly the
evidence such a mechanism would leave, and the driven track supplies a
controlled arena in which to look for it (with the caution of §7: the
most spectacular witnessed motion in this study turned out *not* to
sustain its metric).

The test template itself is not specific to spin chains. Any system
with a computable structural functional over a dynamical substrate
admits the same three probes: certify the motion with null-silent
witnesses, switch the dynamics off, and search honestly for a
motionless impostor. Candidate applications suggest themselves wherever
stable emergent structure rides on flux — resting-state functional
connectivity over neural dynamics, metabolic network structure over
flux-carrying steady states, stability of ecological or market
structure over turnover — and we offer the template for these settings
as a proposal only: nothing beyond spin chains has been demonstrated
here. The distinction the test operationalizes — structure that merely
exists versus structure that is actively kept in existence — is, of
course, much older than physics; we make no attempt to engage that
literature here.

On the methods side, we draw two conclusions we believe generalize.
Null tests for witnesses are cheap and merciless — the OTOC episode
suggests that diagnostics certifying "dynamics" deserve routine
auditing against frozen states. And preregistration with committed
seeds changed the outcome of this study at least four times; the
amendment log (Appendix C) is our answer to the question of what such
discipline buys in a purely computational setting.

The obvious open front is scale and covariance: whether any version of
this question can be asked of structures that deserve the word
"geometry" with fewer scare quotes — partition-covariant functionals,
larger systems, internally clocked dynamics — remains exactly as open
as it was, and none of the present results shortens that road. What
they do establish is that the road's first step is measurable: there
exist, already in twelve qubits, emergent structures that demonstrably
need their dynamics.

## Appendix A: Numerics

Exact diagonalization throughout (dense to $N=14$, dimension 16384);
pure-state evolution via eigendecomposition, density-matrix evolution
for the dephasing protocol via Trotter splitting of the unitary and the
exact per-step damping mask (step $0.5$), $N \leq 10$. State-norm drift
across all unitary runs $< 4\times10^{-15}$; trace drift of dephased
runs recorded per run at the same scale. Python 3.11 / NumPy 2.3 /
SciPy 1.15; every random draw seeded from committed manifests; total
compute across pilot, confirmatory, adversarial, and hardening
campaigns of order a machine-day on a 24-core workstation. The $N=14$
witness point uses the identity
$|\langle\psi(t_0)|\psi(t)\rangle|^2 = |\sum_n p_n e^{-iE_n(t-t_0)}|^2$,
so recurrence statistics require only eigenbasis coefficients. The
comparator search precomputes per-eigenstate two-site reduced density
matrices, making each candidate stationary state's metric a
population-weighted sum evaluable in milliseconds at any dimension.

## Appendix B: Statistics

Class separation: exact Mann–Whitney AUC, symmetrized
$\max(A, 1-A)$ since direction is not registered; threshold $0.95$;
$\geq 2$ statistics per pair; two sizes; singleton classes (the fixed
point) by exact-value exclusion (the ensemble range must exclude the
deterministic value). Robustness: mean log drift ratio per class, BCa
bootstrap (1000 resamples, 95%), disjoint intervals plus
$|\Delta| > \ln 1.5$, replicated with consistent direction; disordered
ensembles resampled at the realization level. Seed sensitivity: at
$n=20$-vs-20 the AUC standard error near $A \approx 0.9$ is
$0.05$–$0.08$, so verdicts within one standard error of threshold are
lotteries — measured directly here when fresh seeds flipped a
marginal pair (§4); $n = 40$ halves the standard error and stabilized
every margin. Size trend for the marginal pair (AUC at
$N = 10 \to 12 \to 14$): Bohr ratio $0.979 \to 0.979 \to 1.000$;
recurrence mean $0.952 \to 0.975 \to 0.976$; energy coherence
$0.956 \to 0.975 \to 0.976$. Instrument notes: the log-ratio floor
($10^{-3}$) makes exactly-stationary objects read
$\log\rho \approx \log(\delta\Phi_{\rm pert}/10^{-3})$ — class-(i)
quench values are floor-referenced and excluded from class inference;
the metric's $-\ln x$ weight cap amplifies machine-epsilon mutual-
information jitter by up to $x_{\min}^{-1}=10^6$, setting an
irreducible $\sim 10^{-9}$ numerical floor on metric-space identity
checks for near-product states.

## Appendix C: The amendment log

The complete dated record of every post-registration change, each with
its reason and repository commit; no entry alters data already taken.

| date | entry | commit |
|---|---|---|
| 08-11 | Spec registered; threshold review (Amendment 1): criterion-(b) instrument → log drift ratio + calibration pilot | 24aa\*/7e40\* |
| 08-11 | Amendment 2 (pre-run): integrable certificate Poisson → free-spectrum reconstruction (mis-specification measured: free chain) | 8393\* |
| 08-11 | Amendment 3 (pilot, owner-ruled): $\varepsilon_\Phi\ 0.05 \to 0.25$ (below measured noise floor); confirmatory strengths $\lambda=0.1$, $\gamma=0.01$ | 5db69ba |
| 08-12 | Instrument survey: KEEP log-ratio (no change; dated entry) | 27ada59 |
| 08-12 | Confirmatory manifest committed pre-execution; survey window closed at first run | b91ad54 |
| 08-12 | Addendum 1: quasiperiodic construction unsatisfiable at $N=8$ (0/56, exhaustive) → criterion sizes (10, 12) | a76db0e |
| 08-12/13 | Confirmatory executed: W3 fires on null → discarded; (a) fails as registered; (b) holds; verdicts of record | fbe324f |
| 08-13 | Adversarial companion: fragility-direction retraction (floored denominator); comparator matching assumption refuted | 33fdd62 |
| 08-13 | Amendment 4 (owner-ratified): battery → {PR$_A$, $\overline{d}$, $\Xi$}; W3 descriptive; fresh-seed re-adjudication required | 9030c0e |
| 08-13 | Fresh seeds $n=20$: FAIL on a different, threshold-marginal pair (seed lottery measured) | 40144d5* |
| 08-13 | Amendment 5 (owner-ratified): $n = 40$, final verdict accepted either way → (a) HOLDS 18/18 | 3e7c0a7 |
| 08-13 | Hardened comparator search corrects family-only over-claim: single-survivor result | 67dda68 |
| 08-13 | Descriptive hardening sweep: $\varepsilon_c$, 2000-period comparator, $\gamma$-grid, partition distribution, $N=14$ | 9ce17de |

(\*abbreviated hashes to be expanded at submission; repository public
from submission date.)

## Appendix D: Invariance battery

Every witness statistic and the metric were checked under: global
phase; consistent local basis change (state, Hamiltonian, and operators
together); local basis change of the state alone; and site reflection.
Witness statistics and mutual-information matrices are identical within
$10^{-10}$ in all mandatory items across every class and size (the
participation ratio judged relative to its own magnitude, which reaches
$10^5$–$10^6$ at $N=12$). Metric-space deviations carry the
cap-amplified numerical floor described in Appendix B and are reported,
not thresholded. The state-only local change leaves the metric
invariant to machine precision — single-site entropies are local-frame
invariant — which localizes all factorization dependence at the
partition level; the partition probe of §8 (fixed random entangling
two-site frames on three disjoint pairs, 24–72 samples per class) is
the quantitative version.

## Appendix E: Driven-track implementation notes

Disorder realizations and initial states are seed-paired across drive
strengths and comparator regimes (identical couplings and fields at
equal seed), so rigidity curves and regime contrasts are paired
comparisons. The subharmonic weight is computed on an even number of
stroboscopic periods so the period-doubled line is the exact Nyquist
bin. Switch-off evolves under the interaction Hamiltonian alone in lab
time, sampled at the same period boundaries (drive removed, clock
kept). The dephasing protocol applies the exact per-period damping mask
with the rate stated in lab-time units ($T_{\rm period} = 2$).

## Acknowledgements and record

*(Author line, acknowledgements — including the role of AI-assisted
research infrastructure in this study — and data/code availability
statement pending owner confirmation. The repository, including the
specification, manifests, amendment log, evidence packets, session
logs, and all run outputs, becomes public at submission.)*
