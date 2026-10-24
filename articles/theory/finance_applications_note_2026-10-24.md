# Further applications to finance research — direction note (2026-10-24)

- Status: **DIRECTION NOTE, SPECULATIVE.** Nothing here is a result of record. Written in answer to the owner's
  question "how these contribution might apply to finances?" after the paper (`paper/main.tex`) was parked.
- Source of record for every theorem cited below: `paper/main.tex` (Theorem A = Thm 3.1, Theorem B = Thm 4.1,
  Lemma 2.3, Theorem 3.4, Propositions 5.2–5.3, Appendix A). Finance references in §6 are **`verify`** (metadata
  from memory, not checked against the primary source) unless marked otherwise.
- Wording rule (AR-027): any novelty claim in this note is "not found in the literature we searched"; no citation
  sweep of the finance literature has been done.

## 1. Where the paper's problem lives in finance

The paper's object is the estimation of a normal mean vector from one noisy observation. The finance instance is the
estimation of **expected returns** of m assets from sample means, the input that mean–variance optimisation is most
sensitive to (Michaud 1989, "error maximisation").

- **Model.** With T observations and known covariance Σ, the vector of sample means is X ~ N(μ, Σ/T). Whitening by
  Σ^{-1/2} (and rescaling by √T) gives the paper's X ~ N(θ, I_m).
- **Loss.** For a mean–variance investor with risk aversion γ who plugs an estimate μ̂ into w = Σ^{-1}μ/γ, the
  expected certainty-equivalent loss is (1/2γ)(μ̂ − μ)ᵀΣ^{-1}(μ̂ − μ) (Kan–Zhou 2007, `verify`). After whitening this
  is quadratic loss |δ − θ|². So, with Σ known, **"admissible under quadratic loss" = "no other estimate gives a
  better plug-in portfolio for every true vector of expected returns"**, and Brown's criterion applies verbatim.
- **The estimators in use are generalized Bayes rules δ_F.** Jorion's Bayes–Stein shrinkage toward the
  minimum-variance return (Jorion 1986), Black–Litterman (a Gaussian prior around model-implied returns,
  Black–Litterman 1992), priors centred on a pricing model with dispersion σ_α (Pástor–Stambaugh 2000), and the flat
  prior behind OLS alphas are all of the form δ_F(x) = x + ∇ log f*(x) for a prior F on (whitened) expected returns.
  Each has an admissibility verdict given by the recurrence of the weighted Brownian motion of (R^m, f* dx).

## 2. What each result of the paper says in this setting

| Paper | Finance reading | Confidence |
|---|---|---|
| Theorem A (sphere test complete under D+P) | For a prior whose blur is doubling and has no walls, one radial integral decides whether the shrinkage rule can be beaten. Radial priors around a target (zero alphas, a model-implied vector) are decided by Brown's Thm 6.3.1 already: decay at least like the point-charge potential \|θ\|^{2−m} ⇒ admissible; slower decay (toward the flat prior) ⇒ beatable. No geometric criterion can add admissible cases in this class. | direct corollary |
| Theorem B (lattice prior) | A prior assembled from many local pieces (mixtures over regimes, clusters of similar assets, pockets of excluded parameter values) can pass every radial diagnostic and still yield a beatable rule; the verdict then depends on the prior mass of large balls, not on rays or sphere averages. | lesson, no finance example built |
| Prop. 5.2 (the wall) | Bimodal / regime-switching priors have bottlenecks, which break the Poincaré condition. There the volume heuristic can point the wrong way and the bottleneck pushes toward admissibility. | lesson |
| Lemma 2.3 (landscapes are priors) | Priors specified as penalties −log w with bounded slope (ridge-like, factor-like) are genuine priors with the same verdict; one may reason on the penalty directly. | direct |
| Section 6 (eigenvalue certificate) | A computable check for walls in a given low-dimensional prior (reuse `checks/a2_poincare_eigen.py` with the prior's weight). | tool |
| Appendix A (Komaki) | For density forecasts of returns (Bayesian portfolio choice, risk measures, pricing under parameter uncertainty), a prior whose predictive density beats the Jeffreys one exists iff the Fisher manifold of the return model is non-parabolic. Normal with unknown mean and variance: hyperbolic plane, so already for one asset. Known covariance: threshold three assets (Komaki 2001, George–Liang–Xu 2006, both `verify`). The improvement term is the prior-dependent part of Perelman's weighted scalar curvature. | direct, asymptotic |

## 3. A corollary to check: priors concentrated near a factor subspace

Derived in conversation on 2026-10-24; **not in the paper, not checked to the paper's standard.** Every step is
listed so that it can be verified or killed.

Setting. Shrinking expected returns (or alphas) toward a K-factor pricing model means a prior concentrated near the
K-dimensional subspace L ⊂ R^m spanned by the factor loadings (K = 0: a point, "all alphas zero"; K = 1: the CAPM
line; K ≥ 2: a multi-factor model with unknown premia). Take the improper prior with polynomial profile in the
distance to L,

    w(θ) = (1 + dist(θ, L)²)^{γ/2},   k := m − K = co-dimension of L.

Steps.

1. **D+P range.** Writing θ = (θ', θ'') with θ' ∈ R^k normal to L, w ≍ (1 + |θ'|)^γ, a Muckenhoupt A₂ weight on
   R^k exactly when −k < γ < k (`verify`: standard, average of w times average of 1/w over balls). A_p weights are
   p-admissible, i.e. doubling + weak (1,p)-Poincaré (Heinonen–Kilpeläinen–Martio 1993, Ch. 15; book not held, see
   AR-029b §2), and the weak form self-improves to the paper's (1) (Hajłasz–Koskela 2000, Thms 5.1, 9.7, READ). So
   for −k < γ < k the prior is D+P and Theorem A applies. (The paper's Theorem 3.4 covers γ ≥ 0 via Björn 2001
   Prop. 6; the negative range is the new step.)
2. **Lipschitz log, bounded drift.** |∇ log w| ≤ |γ| everywhere, so Lemma 2.3 applies and Brown's admissibility
   direction (bounded drift) is available.
3. **Volume growth.** μ(B_r) ≍ r^{m−k} · ∫_{|θ'|<r}(1+|θ'|)^γ dθ' ≍ r^{m−k} · r^{k+γ} = r^{m+γ} (uses γ > −k).
4. **Volume test (Theorem A).** Recurrent ⇔ ∫^∞ r dr / r^{m+γ} = ∞ ⇔ m + γ ≤ 2 ⇔ γ ≤ 2 − m.
5. **Combine with step 1.** γ > −k = K − m and γ ≤ 2 − m are compatible only if K − m < 2 − m, i.e. **K < 2**.

Conclusion, if the steps hold:

- **K ≥ 2 (multi-factor subspace):** every polynomial-profile prior in the D+P range gives a transient weight, hence
  a **beatable** plug-in rule, whatever the tail exponent.
- **K = 1 (one-factor line):** admissible iff γ ∈ (1 − m, 2 − m]; the endpoint γ = 2 − m is the "harmonic prior
  around the line".
- **K = 0 (a point):** γ ∈ (−m, m), admissible iff γ ≤ 2 − m: Stein's harmonic prior, consistent with Brown's
  Thm 6.3.1 (radial case), which is the sanity check.

Cross-check (product structure). The weighted Brownian motion for w = v(θ') is the product of a plain K-dimensional
Brownian motion along L and the transverse diffusion with weight (1+|θ'|)^γ on R^k; return densities multiply,
t^{−K/2} · t^{−(k+γ)/2} = t^{−(m+γ)/2}, and ∫^∞ t^{−(m+γ)/2} dt = ∞ iff m + γ ≤ 2. Same answer, no D+P needed for
this direction (it is the Johnstone–Lalley product reading, Section 5.2 of the paper).

Outside the range (γ ≤ −k): the transverse weight is integrable, the transverse diffusion is positive recurrent, and
the product is recurrent iff K ≤ 2. Not D+P; Theorem A silent; the product argument decides. Not pursued.

To verify before use: step 1 (A₂ range and p-admissibility of A_p weights at the stated source), the constants in
step 3 near L (the weight is ≍ 1 within distance 1 of L, harmless), and whether any of the finance priors in §1 are of
this form in whitened coordinates (Pástor–Stambaugh's are proper Gaussian around the model, hence always admissible;
the improper limit σ_α → ∞ is the flat prior).

## 4. What does not transfer

- Known covariance, Gaussian, i.i.d. noise. With estimated Σ the plug-in problem is different (Kan–Zhou 2007 treat
  it); whether Brown's recurrence criterion has an analogue with unknown Σ is an open literature question for this
  stream (Stein-type results with estimated covariance exist; not searched).
- Admissibility is a weak criterion: it certifies that no rule dominates, not that the gain is material. The beatable
  James–Stein rule is excellent in practice; "inadmissible" is a sanity flag, not a selection rule.
- Komaki's results are N → ∞ asymptotics at order N^{-2}; finance samples are short.
- Time variation, non-Gaussian tails, transaction costs: outside the model.

## 5. Candidate research items (proposals only; not AR-numbered, not preregistered)

- **F1. Classify the standard shrinkage estimators of expected returns by Brown's tests.** Write Jorion 1986,
  Black–Litterman 1992, Pástor–Stambaugh 2000, OLS, and factor-shrinkage rules as δ_F in whitened coordinates;
  apply Brown's Thm 6.3.1 / sphere / ray tests. Expected outcome: all radial or Gaussian, hence decided; the paper's
  novelty bites only for factor-structured and mixture priors. Cheap; one session.
- **F2. Prove or kill the factor-subspace corollary (§3).** Analytical steps as listed; numerical companion with the
  eigenvalue certificate for w = (1 + dist(θ, L)²)^{γ/2}, K = 0, 1, 2, m = 3, 4, on balls to 8 spacings.
- **F3. Regime and mixture priors.** Which regime-switching priors on expected returns break the Poincaré condition
  (walls)? Eigenvalue certificate on two-regime priors in m = 2, 3; relate the wall depth to the verdict.
- **F4. Density forecasts of returns via Komaki's criterion.** Fisher manifold of the multivariate normal family with
  unknown (μ, Σ) (known to be non-parabolic? `verify`); which priors are superharmonic there; link to Bayesian
  portfolio choice under parameter uncertainty (Barberis 2000; Kandel–Stambaugh 1996; both `verify`).
- **F5. Unknown covariance.** Literature search: Stein-type admissibility results for the mean with estimated
  covariance; whether a weighted-manifold reading exists. Gap, not a plan.

## 6. Sources

Read in the stream (theorem level): Brown 1971; Grigor'yan 1999; Saloff-Coste 1992; Hajłasz–Koskela 2000; Björn
2001; Kasahara 1975; Johnstone–Lalley 1984; Komaki 2006, 2015 (see `paper/references.bib`).

`verify` (finance; metadata from memory):

- P. Jorion, "Bayes–Stein estimation for portfolio analysis", J. Financial and Quantitative Analysis 21 (1986).
- F. Black and R. Litterman, "Global portfolio optimization", Financial Analysts Journal 48 (1992).
- R. Kan and G. Zhou, "Optimal portfolio choice with parameter uncertainty", J. Financial and Quantitative Analysis
  42 (2007).
- R. O. Michaud, "The Markowitz optimization enigma: is 'optimized' optimal?", Financial Analysts Journal 45 (1989).
- Ľ. Pástor and R. F. Stambaugh, "Comparing asset pricing models: an investment perspective", J. Financial Economics
  56 (2000).
- N. Barberis, "Investing for the long run when returns are predictable", J. Finance 55 (2000).
- S. Kandel and R. F. Stambaugh, "On the predictability of stock returns: an asset-allocation perspective",
  J. Finance 51 (1996).
- F. Komaki, "A shrinkage predictive distribution for multivariate normal observables", Biometrika 88 (2001).
- E. I. George, F. Liang and X. Xu, "Improved minimax predictive densities under Kullback–Leibler loss",
  Ann. Statist. 34 (2006).
- J. Heinonen, T. Kilpeläinen and O. Martio, *Nonlinear potential theory of degenerate elliptic equations*,
  Oxford, 1993 (Ch. 15, A_p weights are p-admissible; not held, AR-029b §2).
