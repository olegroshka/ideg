# AR-009 — Track E3 toy-model family specification

```yaml
id: AR-009
title: Toy-model family specification (Track E3, first deliverable)
mode: FORMALIZE
parent: BH-004, HYP-009
priority: P0
inputs: [KB-004 §4 BH-004, KB-005 §7, TH-033, TH-037, CON-034, CON-035, CON-036,
         ar/AR-015_partial-2026-08-11_trackE3-G1.md]
question: >
  What exact models, observables, witnesses, comparators, and pass/fail
  thresholds adjudicate BH-004: stationary emergent geometry from witnessed,
  sustained-by nonstationary microdynamics — and does robustness of
  Φ-stationarity differ by dynamical class?
deliverable: this document, reviewable standalone before any AR-010 code
promotion_effect: AR-010 implementation licensed against this spec
kill_effect: if no well-posed witness/comparator scheme exists, BH-004 returns
  to FORMALIZE with the obstruction recorded
status: DONE (spec drafted 2026-08-11; threshold review completed by owner
  2026-08-11 — see §8 Amendment 1; AR-010 licensing now gated on G0 owner
  review of the substrate only)
```

> **Preregistration rule:** every metric, threshold, and comparison below is
> fixed before AR-010 runs. Post-hoc additions are recorded as amendments in
> §8 with dates and reasons, and analysed separately (exploratory, not
> confirmatory).
>
> **G1 note:** TH-033 and TH-037, the two load-bearing external inputs, were
> primary-source verified 2026-08-11 (AR-015 partial packet). TH-034/TH-035
> are *framing only* in this spec and carry no load.

## 0. Conventions

- All models are chains of qubits (spin-1/2), open boundary conditions,
  ħ = 1, J = 1 sets the unit of energy and time (t in units of 1/J).
- **Clock declaration (CON-035, INV-R-009):** all dynamics below uses an
  **external lab clock** (type 1), admissible for toy models and scope-noted:
  no OL-4 conclusion may inherit this clock; the OL-4 caveat of NC-010
  stands. T-B's drive period T defines a second, stroboscopic clock derived
  from the same external clock.
- "Microstate" X(t) = the pure state |ψ(t)⟩ (or ρ(t) where a channel is
  specified). "Emergent-geometry functional" Φ[X] is defined in §2 only.
- Energy eigenbasis {|n⟩, E_n} always refers to the model's Hamiltonian H
  (for T-B: the Floquet operator U_F and its quasienergies).

## 1. Models

### T-A — Closed finite quantum system
- **Sizes:** N = 10 primary; N = 8, 12 for size-scaling checks. Exact
  diagonalization is tractable to N = 12 dense (dim 4096); N = 14 via
  Krylov only if a specific check demands it (amendment required).
- **Hamiltonian classes** (all standard models; no literature metadata is
  load-bearing — each class carries a preregistered spectral sanity check
  in §6.3 instead of a citation):
  - **(i) fixed point:** transverse-field Ising chain,
    H = −Σᵢ σᶻᵢσᶻᵢ₊₁ − g Σᵢ σˣᵢ with g = 1.5 (gapped, nondegenerate ground
    state). Initial state: the ground state. Dynamics: global phase only.
    This class doubles as the **null comparator** of §4.4.
  - **(ii) quasiperiodic:** XX chain, H = Σᵢ (σˣᵢσˣᵢ₊₁ + σʸᵢσʸᵢ₊₁)/2.
    Initial states: normalized superpositions of m = 3 single-magnon
    eigenstates whose two independent Bohr frequencies have ratio
    verified irrational to tolerance (no rational p/q with q ≤ 50 within
    10⁻³). Motion: quasiperiodic on a 2-torus.
  - **(iii) chaotic:** mixed-field Ising chain,
    H = Σᵢ σᶻᵢσᶻᵢ₊₁ + h_x Σᵢ σˣᵢ + h_z Σᵢ σᶻᵢ, (h_x, h_z) = (0.9045, 0.8090).
    Initial states: Haar-random product states. Sanity check §6.3 (GOE
    level statistics) guards the class label; parameters may be amended
    only via §8 if the check fails.
  - **(iv) metastable / code subspace:** ferromagnetic Ising with weak
    transverse field, H = −Σᵢ σᶻᵢσᶻᵢ₊₁ − g Σᵢ σˣᵢ, g = 0.05: quasi-degenerate
    ground doublet (GHZ-like sector, splitting exp. small in N). Initial
    state: |↑…↑⟩ (superposition of the doublet). Motion: slow coherent
    rotation inside the doublet + small transverse dressing.
- **Ensembles:** 20 initial states per class (class (i): the single ground
  state, 20 trivially identical runs collapse to 1; class (ii): 20 random
  triples of magnon modes meeting the incommensurability test; class (iii):
  20 Haar product states; class (iv): the fixed initial state with 20
  weak-disorder dressings of H, δg_i uniform in [−0.01, 0.01]).

### T-B — Driven / Floquet system
- **Size:** N = 10; disordered, 20 disorder realizations.
- **Drive (period T = t₁ + t₂):** stroboscopic two-part Floquet unitary
  U_F = exp(−i H₂ t₂) · exp(−i H₁ t₁), modeled on the verified TH-033
  template (SRC-043 definition; SRC-044 realization):
  - H₁ = (π/2)(1 − ε) Σᵢ σʸᵢ with t₁ = 1 (imperfect global π-flip;
    ε is the drive perturbation),
  - H₂ = Σᵢ Jᵢ σᶻᵢσᶻᵢ₊₁ + Σᵢ hᵢ σᶻᵢ with t₂ = 1, Jᵢ uniform in [0.05, 0.15]π,
    hᵢ uniform in [0, π] (strong disorder → MBL regime).
- **Regimes:** DTC regime ε ∈ {0.03, 0.06, 0.10}; comparator regimes:
  (r1) no interactions (Jᵢ = 0; fine-tuned, peak splits ∝ ε — not a DTC),
  (r2) no disorder (hᵢ = 0, thermalizing).
- **Subharmonic witness (verified TH-033 form):** height of the Fourier
  peak of the stroboscopic magnetization time series ⟨σᶻᵢ(nT)⟩ at
  ω = ω_drive/2 (period-2T response), site-averaged; plus its **rigidity
  curve** h_sub(ε) — the DTC phase shows a locked peak for ε below a
  critical value (ε_c ≈ 0.11 at the SRC-044 parameters; ours will differ,
  measured not assumed).
- Initial states: random z-product states, 5 per disorder realization.

### T-C — Interacting spin chain with MI-graph geometry (primary arena)
- **Sizes:** N = 12 primary, N = 8, 10 scaling; open BC.
- **Dynamics regimes:**
  - **scrambling:** mixed-field Ising as in T-A(iii);
  - **integrable:** XX chain as in T-A(ii);
  - **localized:** XXZ + random fields,
    H = Σᵢ (σˣᵢσˣᵢ₊₁ + σʸᵢσʸᵢ₊₁ + Δ σᶻᵢσᶻᵢ₊₁) + Σᵢ hᵢ σᶻᵢ, Δ = 1,
    hᵢ uniform in [−W, W], W = 8 (deep localized regime); 20 disorder
    realizations.
- Initial states: Néel state |↑↓↑↓…⟩ (primary) + 5 random product states
  per regime/realization.
- Φ[X] per §2 computed on the natural site factorization (the TH-037
  caveat that the factorization is *posited* is inherited and recorded as
  a scope wall in §7).

## 2. Emergent-geometry functional Φ

Exactly the verified TH-037 (SRC-049 §III.2) construction, adapted to a
chain of single-site factors:

1. From |ψ(t)⟩ (or ρ(t)), compute all single- and two-site reduced density
   matrices; mutual information I_ij(t) = S_i + S_j − S_ij (von Neumann,
   natural log).
2. Normalize x_ij = I_ij / I₀ with I₀ = 2 ln 2 (maximum for a qubit pair).
3. Graph weights (SRC-049 eq. 13 with the suggested choice Φ(x) = −log x):
   w_ij(t) = −ln x_ij(t), **regularized**: x_ij values below x_min = 10⁻⁶
   are set to x_min (weight cap w_max = ln 10⁶ ≈ 13.8); this cap is part of
   the preregistered definition.
4. **Distance matrix** D_ij(t) = weighted shortest path over the complete
   graph on the N sites (SRC-049 eq. 14; Floyd–Warshall).
5. Φ[X(t)] := D(t) (the full distance matrix — no scalar reduction).
   Classical MDS embedding (SRC-049 eqs. 23–25) is computed as a
   **diagnostic only** (dimensionality estimate); no §5 metric depends
   on it.

**Stationarity criterion (preregistered):** on the analysis window
𝒲 = [t_eq, t_end] = [20, 200] (units 1/J; T-B: stroboscopic periods
n ∈ [20, 200]), with samples every Δt = 0.5 (T-B: every period), define the
window mean D̄ and the drift

  δΦ(t) = ‖D(t) − D̄‖_F / ‖D̄‖_F .

Φ is **stationary** on 𝒲 iff max_{t∈𝒲} δΦ(t) < ε_Φ = 0.25 *(amended from
0.05, 2026-08-11, §8 Amendment 3: the pilot measured the construction's
finite-size fluctuation floor at N = 10 — chaotic-class baselines
0.11–0.22 — placing the original value below the noise floor of every
dynamical class; 0.25 sits above that floor and below genuine
Φ-motion, quasiperiodic/integrable 0.32–1.2)*. Report also the
fitted linear drift slope of δΦ(t) with bootstrap CI. The transient
t < t_eq = 20 is excluded by design (equilibration is not the claim under
test; the claim is about the persistent regime).

**Cap diagnostic (reported, never thresholded; added 2026-08-11):** δΦ is
additionally computed restricted to the pair set whose x̄_ij in D̄ exceeds
x_min (the above-cap subgraph). This exposes any cap-dominance of the
stationarity verdict — in late-time scrambled states many distant-pair
weights sit at w_max, which biases the capped δΦ toward stationarity; the
subgraph version is the honesty check on that bias.

## 3. Witnesses (CON-034)

Each witness is stated with the redundancies it provably survives. A witness
"fires" when its class-conditional statistic exceeds the null-comparator
value (class (i)/global-phase evolution) by the §5 margins.

- **W1 — Bohr spectral measure / motion spectrum.**
  A(ω) = Σ_{m≠n} |c_m|²|c_n|² δ(ω − (E_m − E_n)) for |ψ₀⟩ = Σ c_n |n⟩
  (T-B: quasienergies of U_F). Statistic: participation ratio
  PR_A = (Σ_k a_k)² / Σ_k a_k² over binned lines (bin 10⁻³ J).
  *Invariance:* built from H's spectrum and |c_n|²; invariant under global
  phase, under any fixed unitary change of computational basis, and under
  relabeling of subsystems. Silent (PR_A = 1, all weight at ω = 0) iff the
  state is an eigenstate — exactly the null.
- **W2 — Recurrence distance.** d_phys(t) = 1 − |⟨ψ(t_eq)|ψ(t)⟩|²
  on 𝒲; statistics: min over 𝒲 (recurrence depth) and mean.
  *Invariance:* |·|² kills global phase; unitary basis changes preserve
  inner products. This is the CON-022 d(X(t+T), X(t)) object.
- **W3 — OTOC front.** C(r, t) = ½ ⟨|[σᶻ_{i₀+r}(t), σᶻ_{i₀}]|²⟩ with i₀ the
  chain center, r ∈ {1, …, N−i₀−1}, evaluated in the evolving state.
  Statistics: saturation value C_sat(r) = mean over the last quarter of 𝒲,
  and arrival time t*(r) (first crossing of 0.1).
  *Invariance:* global phase, and covariant under the local-operator class —
  the §4.3 battery quantifies robustness to the choice of local operator
  (σᶻ → σˣ, σʸ) and site i₀.
- **W4 — Off-diagonal energy coherence.** Ξ(ρ) = Σ_{m≠n} |ρ_mn|²
  (energy eigenbasis; T-B: Floquet eigenbasis). Ξ > 0 iff the state moves
  nontrivially under H. *Invariance:* spectral decomposition of H is
  representation-independent; Ξ is invariant under global phase and any
  fixed basis change. **W4 is the designated discriminator against the
  stationary-state comparator (§4.1), which has Ξ = 0 identically.**
- **W5 — Subharmonic response (T-B only).** As defined in §1 T-B; the
  verified TH-033/SRC-044 witness. *Invariance:* peak location ω_drive/2 is
  fixed by the drive clock; peak height is invariant under global phase and
  site relabeling (site-averaged).

**Witness-level ledger (collision rule 15):** all witnesses live at the
model's OL-0/OL-1 (state and correlation structure) certifying microdynamics
below the emergent OL-"geometric" functional Φ; the clock is the external
lab clock throughout (§0); no OL-4 assertion is made or implied.

## 4. Mandatory comparators and controls

### 4.1 Stationary-state comparator (KB-004 §7 item 12)
For each dynamical run, construct the **diagonal ensemble**
ρ̄ = Σ_n |c_n|² |n⟩⟨n| — exactly stationary under H, and matched to the run's
long-time-averaged Φ by construction (its MI pattern is the time average's).
Preregistered checks:
1. **Distinguishability:** W4 separates ρ̄ (Ξ = 0) from ρ(t) (Ξ > 0). If for
   some class no witness distinguishes the dynamical state from ρ̄ within
   the §5 margins, the sustained-by claim **fails for that class** (item-12
   failure), recorded as such.
2. **Fair-perturbation comparison:** apply the §5(b) robustness protocols
   identically to ρ(t) and ρ̄. The sustained-by verdict (§5.3) turns on
   whether robustness differs.

### 4.2 Switch-off test (CON-036 operationalization)
"Quench the dynamics and record whether Φ-stationarity degrades":
- **T-A/T-C:** at t_off = 100 (mid-window), dephase the state in the energy
  eigenbasis (ρ → diag part) — this kills all motion (state exactly
  stationary thereafter) while preserving the instantaneous time-averaged
  MI structure. Predicted signature if *sustained-by* holds: the
  subsequent Φ trajectory departs from the dynamical run's under the §5(b)
  perturbations (robustness loss). If Φ-stationarity and robustness are
  unchanged: *compatible-with* verdict for that class.
- **T-B:** at period n_off = 100, remove the drive (evolve under H₂ alone).
  Record both W5 collapse and Φ response. (Honest open question,
  preregistered as such: MBL may hold the MI pattern with the drive off —
  witness collapse with Φ persistence would be a *compatible-with* result
  for T-B, and that is a reportable finding, not a failure of the spec.)

### 4.3 Representation-invariance battery
Applied to every witness statistic and to Φ:
- global phase e^{iα}|ψ⟩ (α random): all outputs must be bit-identical
  within numerical tolerance 10⁻¹⁰;
- fixed random local basis change U = ⊗ᵢ uᵢ applied to state and operators
  consistently: W1/W2/W4 identical; W3/Φ recomputed with transformed
  operator/factorization definitions must agree within 10⁻¹⁰;
- fixed random local basis change applied to the state only (operators
  kept in the computational basis) — *expected* to change W3 and Φ; the
  battery records the magnitude as the measure of factorization-dependence
  (TH-037 caveat made quantitative, reported not thresholded);
- site relabeling (reflection i → N+1−i): Φ distance matrices must map
  accordingly; site-averaged statistics identical.

### 4.4 Null comparator (NC-009 guard)
Class (i): eigenstate under global-phase evolution. Preregistered
requirement: **every** witness is silent (W1: PR_A = 1; W2: d_phys ≡ 0;
W3: C(r, t) time-independent; W4: Ξ = 0) while Φ is exactly stationary.
Any witness that fires on the null is discarded as a CON-034 candidate
(this is the "witness must vanish if the oscillation stops" clause).

## 5. Success / failure metrics (preregistered)

### 5.1 (a) Witness separates dynamical classes
Statistic: for each witness statistic s ∈ {PR_A, min d_phys, C_sat(r_max),
t*(r_max), Ξ} and each pair of T-A classes (and each pair of T-C regimes),
the two-sample AUC over the ensemble (20 runs/class).
**Threshold:** (a) holds iff for every class pair there exist ≥ 2 witness
statistics with AUC ≥ 0.95 (complete or near-complete separation), at both
N = 10 and N = 12 (T-C; N = 8 and 10 for T-A if 12 is infeasible in
budget). Class (i) is a single deterministic state with exact witness
values (PR_A = 1, Ξ = 0, d_phys ≡ 0); pairs involving class (i) use
exact-value separation (the other class's ensemble range excludes the
exact value) instead of rank AUC, which is degenerate for a singleton. Ordinal sanity predictions (preregistered, non-binding on (a)):
PR_A ≈ 1 (i) < PR_A ∈ [2, 12] (ii) ≪ PR_A (iii); class (iv) shows a
single dominant low-frequency line; C_sat larger and t* shorter for
scrambling than integrable; localized shows frozen C(r, t) for r ≳ ξ.

### 5.2 (b) Robustness differential of Φ-stationarity
*(amended 2026-08-11 after owner review — see §8; original fixed-strength
R-measure retained as descriptive only)*

Perturbation protocols (each applied within 𝒲, all classes/regimes):
1. **Hamiltonian quench:** add λ σᶻ_{i₁} at random site i₁, from t_p = 100
   onward; confirmatory λ chosen by the §5.2.1 pilot from the grid there;
2. **Dephasing noise:** local σᶻ dephasing channel, rate γ, from t_p = 100
   (density-matrix evolution; N ≤ 10 for this protocol); confirmatory γ
   chosen by the §5.2.1 pilot;
3. **Subsystem loss:** trace out k = 2 random non-adjacent sites at
   t_p = 100; recompute Φ on the reduced (N−2)-site graph, compared to the
   unperturbed run's Φ restricted to the same sites (discrete protocol —
   no calibration dial; k = 2 fixed).

**Primary effect measure (scale-free):** the log drift ratio
  log ρ = log [ max_{t > t_p} δΦ_pert(t) / max(max_{t > t_p} δΦ_unpert(t), δ_floor) ],
with δ_floor = 10⁻³ (preregistered floor at the numerical/sampling noise
scale; guards the exactly-stationary class (i), whose unperturbed drift is
zero to machine precision).
**Threshold:** (b) holds iff for ≥ 1 protocol, at least one pair of classes
has |mean log ρ difference| > ln 1.5 (≈ 0.405; a ≥ 50% relative difference
in perturbation-induced drift) with disjoint bootstrap 95% CIs
(1000 resamples over the ensemble), replicated at both system sizes.
**Secondary (descriptive only, no threshold):** the original retention
R = 1 − [max_{t > t_p} δΦ(t) − max_{t > t_p} δΦ_unpert(t)]₊ clipped to
[0, 1], reported for continuity with the pre-amendment draft.

### 5.2.1 Calibration pilot (exploratory; runs before confirmatory analysis)
- Grids: λ ∈ {0.02, 0.05, 0.1, 0.2}; γ ∈ {0.003, 0.01, 0.03}.
- Reduced ensemble: 5 runs per class/regime, N = 10 only.
- Outputs: (i) the confirmatory λ and γ (chosen to place typical log ρ in a
  responsive, non-saturated range), logged as a dated §8 entry **before**
  any confirmatory run; (ii) exploratory failure-threshold curves — the
  smallest strength λ*_class (resp. γ*_class) at which the ε_Φ criterion
  first fails — recorded as a candidate alternative robustness instrument
  in the style of the verified SRC-044 rigidity/critical-strength protocol.
- Pilot data are excluded from all confirmatory statistics.
- **Instrument-upgrade clause:** AR-019 (KB-005 §6) may recommend replacing
  or augmenting the log-ratio instrument (e.g., by λ*-style thresholds or a
  fidelity-decay-class analysis). Adoption is a dated §8 amendment, valid
  only before confirmatory runs begin; absent that, this section stands
  as written.

### 5.3 Sustained-by adjudication (CON-036, per class)
*Sustained-by* is affirmed for a class iff **both**:
1. witnesses distinguish the dynamical state from the stationary comparator
   (§4.1 check 1 passes), **and**
2. the dynamical run's robustness R̄ differs from its diagonal-ensemble
   comparator's under ≥ 1 protocol (disjoint 95% CIs), or the switch-off
   test (§4.2) shows Φ-drift increase with disjoint CIs after t_off.
Otherwise the class verdict is *compatible-with* (Φ-stationarity does not
depend on the motion) — recorded as a first-class result.

### 5.4 Outcomes and their KB effects
- (a) and (b) hold → BH-004 supported in-model; BH-005 licensed
  (KB-004 §4); HYP-009 geometric part gains its first model realization.
- (a) holds, (b) null → paper reports a clean null on the novel question
  (robustness differential); BH-004 partially supported (witnessed
  stationarity exists; class-independence of robustness is the finding).
- (a) fails → witness scheme returns to FORMALIZE; recorded negative
  (SC-005).
- All classes *compatible-with* under §5.3 → BH-004's sustained-by clause
  fails in this family; KC-007 pressure on HYP-009 recorded; census
  (AR-015) becomes the lead deliverable per KB-005 §13.

## 6. Analysis plan

### 6.1 Estimators and statistics
Ensembles as in §1 (20 runs per class/regime; disordered models: 20
realizations × 5 initial states, analysed with realization as the
resampling unit). All CIs: nonparametric bootstrap, 1000 resamples, 95%,
BCa where the estimator is a mean. AUCs computed exactly (Mann–Whitney).
No p-values; separation criteria are AUC/CI-based as preregistered above.

### 6.2 Numerics
Exact diagonalization (dense) to N = 12; time evolution via
eigendecomposition (T-A/T-C) and repeated U_F application (T-B);
density-matrix evolution only for protocol 2 (N ≤ 10). Tolerances:
unitarity/trace drift < 10⁻¹⁰ per run (checked). Seeds: all RNG seeded;
seed list fixed in the AR-010 run manifest before execution.
Language: Python 3.12 + NumPy/SciPy (src/ideg); no GPU required.
Compute budget: ≤ 200 CPU-hours total; any overrun → §8 amendment.

### 6.3 Class-label sanity checks (run before confirmatory analysis)
- (iii)/scrambling: mean level-spacing ratio ⟨r⟩ ∈ [0.51, 0.55]
  (GOE ≈ 0.531) in the zero-magnetization sector where applicable;
- (ii)/integrable (XX): free-spectrum reconstruction — many-body energies
  in the Sz = 0 sector equal subset-sums of the single-particle hopping
  spectrum, max abs deviation < 10⁻⁸ *(amended 2026-08-11, §8 Amendment 2:
  the original Poisson window is a generic-integrability heuristic
  inapplicable to a free model's additive spectrum; this certificate is
  strictly stronger)*;
- localized: ⟨r⟩ ∈ [0.36, 0.42] at W = 8;
- T-B DTC regime: subharmonic peak present at ε = 0.03 in ≥ 18/20
  realizations.
A failed check stops confirmatory runs for that class; parameters are
amended via §8, never silently.

### 6.4 Size scaling
Every §5 threshold is evaluated at two sizes (§5.1/5.2). Direction-of-effect
must agree across sizes for a criterion to count as "replicated"; magnitude
scaling is reported descriptively (no extrapolation claims — scope wall §7).

## 7. Non-goals and scope walls
- No claim that T-A/B/C are gravity; no OL-4 conclusions beyond "the
  pattern does/does not have a nontrivial model realization" (collision
  rule 10; KB-005 §7 non-goals).
- The site factorization defining Φ is *posited*, inheriting SRC-049's
  stated caveat; the §4.3 battery measures, and the paper reports,
  factorization-dependence rather than claiming it away.
- The external lab clock is scope-noted (§0); nothing here bears on
  NC-010's OL-4 clock problem.
- MDS embeddings are illustrative diagnostics only.
- TH-034/TH-035 are framing, not load; they remain verification-pending.

## 8. Open items / amendments log
- 2026-08-11: spec drafted (this document).
- **2026-08-11 — Amendment 1 (pre-run; owner review session).** Owner
  reviewed all preregistered thresholds. Rulings: Layer 1 (stationarity:
  ε_Φ = 0.05, window, cap) and Layer 2 (criterion (a): AUC ≥ 0.95, ≥ 2
  statistics per pair, two sizes) accepted unchanged. Layer 3
  (criterion (b)) amended before any run: primary effect measure changed
  from fixed-strength retention R (differential > 0.2) to the scale-free
  log drift ratio (|Δ mean log ρ| > ln 1.5, disjoint CIs); calibration
  pilot §5.2.1 added with preregistered grids; λ*/γ* failure thresholds
  collected as exploratory candidate instrument; R demoted to descriptive.
  Also: cap diagnostic added to §2 (reported only); class-(i)
  exact-value treatment added to §5.1 (statistical wording fix, no
  substance change). Reason: the fixed-strength R measure risked
  criterion (b) returning null by instrument coarseness rather than
  physics (both under- and over-driving failure modes).
- **2026-08-11 — Amendment 2 (pre-run; AR-010 sanity phase).** §6.3
  integrable-class certificate replaced. The preregistered Poisson window
  FAILED as specified for the XX chain (measured ⟨r⟩ = 0.477 in the Sz = 0
  sector at N = 10) — diagnosis: XX is free; its many-body spectrum equals
  subset-sums of single-particle energies (verified to 1.3×10⁻¹⁴), so the
  Poisson heuristic for generic integrable models does not apply. New
  certificate: free-spectrum reconstruction to < 10⁻⁸ (strictly stronger:
  proves integrability rather than inferring its absence of chaos).
  Chaotic (⟨r⟩ = 0.5295, reflection-even sector), localized (⟨r⟩ = 0.382),
  and DTC (20/20 subharmonic) checks passed as preregistered, unchanged.
  No confirmatory run had been executed at amendment time.
- **2026-08-11 — Amendment 3 (pre-confirmatory; §5.2.1 pilot outcomes,
  owner-reviewed).** Calibration pilot complete (7 groups × 5 runs,
  N = 10, manifest-committed seeds; results/AR-010/). Rulings and records:
  1. **ε_Φ: 0.05 → 0.25** (§2). Pilot evidence: baseline max δΦ — fixed
     point 0.000; chaotic 0.114–0.127; scrambling 0.115–0.218; localized
     0.204–0.338; metastable 0.540–0.623; quasiperiodic 0.741–1.211;
     integrable 0.319–1.001. The original 0.05 lay below the −log-weight
     construction's finite-size fluctuation floor (cap diagnostic confirmed
     the chaotic floor is genuine graph-wide fluctuation, not cap noise),
     making stationarity unattainable for every dynamical class at N = 10 —
     an instrument artifact the pilot existed to catch. Under 0.25:
     chaotic/scrambling = stationary-with-witness (the BH-004 candidate
     regime); quasiperiodic/integrable = genuinely moving; localized
     straddles (size-scaling adjudicates); metastable is artifact-dominated
     (near-product state: above x > 10⁻² its MI graph is empty — recorded,
     cap-diagnostic reporting mandatory for this class).
  2. **Confirmatory strengths (the §5.2.1 output): λ = 0.1, γ = 0.01.**
     Owner override of the analysis script's mechanical grid-edge pick
     (λ = 0.2, γ = 0.03): discrimination saturates by γ = 0.01 (chaotic
     +2.2 vs quasiperiodic −0.26 on log ρ) with smaller Trotter error and
     non-degenerate retention; λ = 0.1 resolves the fixed-point comparator.
  3. Pilot findings of record: dephasing response is monotone and
     class-ordered (chaotic/scrambling ≫ localized > integrable >
     metastable > quasiperiodic, the last two *negative* — dephasing
     stabilizes genuinely-oscillating Φ, an early sustained-by signature);
     quench protocol is null for all dynamical classes at every grid λ
     (expectation recorded — its confirmatory role is comparator only);
     W1 (PR_A, 10⁻³ bins) cannot resolve the metastable doublet splitting
     (reads ≈ 1) — W4 (Ξ = 0.50) carries that class's separation, witness
     redundancy intact; exploratory failure thresholds λ*/γ* recorded in
     results/AR-010/pilot_summary.json.
  4. Pilot data remain exploratory and are excluded from confirmatory
     statistics; no confirmatory run had been executed at amendment time.
- **Instrument-upgrade window:** AR-019 (queued in KB-005 §6, advisory,
  non-blocking) may propose a better criterion-(b) instrument by analogy
  (fidelity/Loschmidt-echo decay classes; SRC-044-style critical-strength
  curves). Adoption requires a dated amendment here, valid only before
  confirmatory runs begin.
- Open: G0 owner review of the v0.2 substrate (separate gate; still
  pending) — AR-010 licensing requires it.
- Open: decide whether T-C at N = 14 (Krylov) is worth the budget after
  first N = 12 results (amendment if yes).
