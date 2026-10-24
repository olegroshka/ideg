# Admissibility, shrinkage priors, and weighted Riemannian geometry
## v2 of the "admissible interior geometry" blueprint — research note of record

```yaml
id: THEORY-V2
supersedes: articles/theory/admissible_spacetime_and_statistical_general_relativity.md (v1; LLM-drafted options, kept as input record only)
basis: ar/AR-024_article-lint-2026-10-23.md (lint + source verification), ar/AR-025_blueprint-v2-2026-10-23.md, ar/AR-026_Q1-brown-weighted-manifold-2026-10-23.md (Brown 1971 + Grigor'yan 1999 read in full)
machine_checks: articles/theory/checks/lint_admissible_spacetime.py -> lint_results_2026-10-23.txt (22 checks: 6 FAIL on v1 claims, 12 PASS, 4 INFO); checks/g0_feasibility.py and checks/g0_doubling_poincare.py -> *_2026-10-23.txt
typeset_version: articles/theory/latex/note.tex (quantumarticle, two columns, figures/make_figures.py) — builds clean; same claims, same status tags
status: DRAFT research note; every claim carries a status tag; no gravitational claim is made
owner_frame (2026-10-23): "connect information-geometry ideas" — shrinkage/admissibility on one side, weighted Riemannian geometry and Ricci-flow functionals on the other; "Stein–Einstein" is shorthand, not a thesis
date: 2026-10-23
```

**Status tags used below.** `THEOREM (source)` — stated and proved in the cited
source, read by us; `IDENTITY (check)` — elementary identity, machine-verified in
the named lint check; `REFORMULATION` — a sourced statement rewritten in the
other field's language, with the rewriting machine-checked; `NEGATIVE (source)` —
a v1 claim refuted from a source; `DIRECTION` — a question, not a claim;
`DEAD` — a v1 claim that failed and is not carried forward.

---

## 0. Claims of record

**K1 — Komaki's shrinkage risk reduction is the Φ-dependent part of Perelman's weighted scalar curvature.**
Let (M, g) be a d-dimensional regular model manifold with Fisher metric g, π_J the
Jeffreys prior, and f = e^{−Φ} π_J a smooth prior; write u = √(f/π_J) = e^{−Φ/2}.
Komaki (2006) eqs. (4)–(5) give

  Risk_N(π_J) − Risk_N(f) = (1/N²)·(½|∇Φ|² + ΔΦ − |∇Φ|²) + o(N^{−2}) = (1/(2N²))·(2Δ_gΦ − |∇Φ|²_g) + o(N^{−2}),

and Perelman (2002) Remark 1.3 defines R^m := R + 2Δf − |∇f|² for the smooth metric
measure space (M, g, e^{−f}dV). Hence, with f ≡ Φ,

  **Risk_N(π_J) − Risk_N(e^{−Φ}π_J) = (R^m_Φ − R)/(2N²) + o(N^{−2}),  and  R^m_Φ − R = −4Δu/u.**

Domination holds iff u is a nonconstant positive superharmonic function (Komaki Thm 2),
i.e. iff R^m_Φ ≥ R with strict inequality somewhere.
*Status:* IDENTITY (C8, C9, C10) assembled from THEOREM (Komaki 2006 Thms 1–2,
eqs. (3)–(5)) and a definition (Perelman Rmk 1.3). v1 had the sign reversed (C10).
*Prior art (AR-027):* not found in the literature searched (Komaki × Perelman /
Ricci flow / Bakry–Émery / weighted scalar curvature, standard and extended
search). Permitted wording: "we have not found this identity stated".

**K2 — The scalar-curvature potential has no statistical counterpart.**
Komaki (2015) Theorem A1, eq. (29), writes the full O(N^{−2}) Kullback–Leibler risk
of a Bayesian predictive density. In the conventional setting (data and target
share the model) its prior-independent part is a fixed combination of: the Efron
(e-embedding) curvature E(v^{(e)ik}v^{(e)jl})g_{kl}g_{ij}; the mixture embedding
curvature E(v^{(m)}_{ij}v^{(m)}_{kl}) contracted two ways (norm and squared mean
curvature); the skewness norm T_{ijk}T^{ijk}; a fourth-moment contraction Q; and a
mixed moment E(∂_i l ∂_j l v^{(m)}_{kl}). These are generally nonzero for d = 1
(Efron's statistical curvature of a one-parameter curved family), where the
Riemannian scalar curvature of (M, g) vanishes identically. Therefore the
prior-independent term is **not** proportional to R, and Perelman's F is **not** the
integrated predictive risk. Only the gradient part of F is statistical:

  ∫(Risk(π_J) − Risk(f)) e^{−Φ}dV = (1/(2N²)) ∫|∇Φ|² e^{−Φ}dV = (1/(2N²))·[F(g, Φ) − ∫R e^{−Φ}dV].

*Status:* NEGATIVE (Komaki 2015 Thm A1; d = 1 argument). Kills v1 §1.2 "K_curv ∝ R"
and v1 §1.3 "mathematically identical to Perelman's F".
*Corollary:* the operator governing shrinkage domination is −4Δ_g acting on u, i.e.
Perelman's Schrödinger operator −4Δ + R **with the potential removed**. Perelman's
λ(g) (lowest eigenvalue of −4Δ + R; verify the section before citing) has no
statistical reading here.

**K3 — Existence of shrinkage priors ⇔ non-parabolicity of the Fisher manifold.**
Komaki (2006) Thm 1: if a Green function exists on (M, g), the prior G(ξ,·)π_J
asymptotically dominates π_J; Thm 2 gives the iff in terms of superharmonic u;
Komaki cites the classical equivalence "Green function exists ⇔ a nonconstant
positive superharmonic function exists" (= non-parabolic ⇔ Brownian motion on
(M, g) transient). Thm 3: complete, simply connected, negative curvature (d ≥ 3)
⇒ Green function exists (Aomoto 1966). Flat normal model: Green function exists
iff d ≥ 3; the Green prior is Stein's harmonic prior ‖μ‖^{−(d−2)} (Komaki Ex. 1).
*Status:* THEOREM (Komaki 2006). This is where curvature legitimately enters:
through sign conditions on sectional curvature that decide transience, **not**
through R in the risk.

**K4 — Brown's admissibility criterion is the recurrence test of a weighted manifold.**
For a spherically symmetric prior with marginal m(‖x‖²), Brown (1971) Thm 3.6.1
(as quoted by Maruyama–Strawderman 2021, eq. (1.3)) states: the generalized Bayes
estimator δ_m = x + ∇log m is inadmissible iff ∫_1^∞ dt /(t^{d/2} m(t)) < ∞
(admissible when the integral diverges and the risk is bounded). On the smooth
metric measure space (R^d, flat g, m dx) the weighted area of the sphere of radius
r is S(r) = ω_{d−1} r^{d−1} m(r²), and the substitution t = r² maps dr/S(r) to
dt/(2t^{d/2}m(t)) exactly (C23). So Brown's integral is the rotationally symmetric
recurrence/parabolicity test ∫^∞ dr/S(r) = ∞ for the **weighted Brownian motion**
with generator Δ + ∇log m·∇, which is precisely Brown's diffusion. With m ≡ 1 the
integral is finite iff d ≥ 3: Stein (1956) is the unweighted case.
*Status (upgraded 2026-10-23, AR-026):* **THEOREM**, on both sides, read in full.
General form: let W_F = (R^m, δ_ij, f* dx) with f* = p*F the marginal of a
generalized prior F. Brown's energy ∫‖∇j‖² f* dx (1.3.4) is the weighted Dirichlet
energy of W_F; his Theorem 4.3.1 says the diffusion with drift ∇log f* is
transient iff the infimum of that energy over j = 1 on the unit ball, j → 0 at
infinity, is positive — i.e. iff the unit ball has positive capacity in W_F, which
is non-parabolicity (Grigor'yan Thm 5.1(6)). **Brown Theorem 5.1.1:** δ_F with
bounded risk is admissible iff that diffusion is recurrent, and transience implies
inadmissibility unconditionally. **Brown Theorem 6.3.1** (spherical F) is the
model-manifold test of Grigor'yan Prop. 3.1 (C23); **Brown Theorem 6.4.3** (any F,
bounded risk): ∫_1^∞ dr/(r^{m−1} f̄(r)) = ∞ with f̄ the spherical average of f* ⇒
admissible — the weighted-Euclidean instance of Grigor'yan Thm 7.5; **Theorem
6.4.2** gives the iff under |∇log f*| ≤ k/|x|; **Theorem 6.4.4** a directional
transience (inadmissibility) test. The ball-volume test (Grigor'yan Thm 7.3) is a
corollary of 6.4.3 by dyadic Cauchy–Schwarz and strictly weaker (C24).
*Consistency check:* a proper prior has finite weighted volume, a reversible
diffusion with finite symmetric measure is recurrent, and proper Bayes rules with
finite Bayes risk are admissible — Brown Cor. 4.3.2 and his §6.5.2 ergodic
argument say exactly this on the statistical side.
*Prior art (AR-027):* the **analytic** form of K4 — admissibility ⟺ recurrence of
the Dirichlet form ∫|∇j|² f* dx — is established in statistics: Brown 1971;
Srinivasan 1981; Johnstone 1984 and 1986 ("Dirichlet principles", the
minimum-energy formulation, for birth–death chains); Eaton 1992, Hobert–Robert
1999, Eaton–Hobert–Jones–Lai 2008 (symmetric Markov chains on the parameter
space); Takanashi–McAlinn 2023 (Lévy models, KL loss, Fukushima's Dirichlet-form
theory). The **geometric** translation — parabolicity of a weighted manifold,
Grigor'yan's sphere-area and volume tests, Lyons–Sullivan — was not found in any
of these, and none of them cites that literature. K4 is therefore **known
mathematics in another language**; only the translation is ours.

**K5 — Komaki's conformal frame is v1's "Einstein frame".**
For d ≥ 3 and a vague prior h, Komaki (2006) §3 introduces g̃ = (h/π_J)^{2/(d−2)} g
and proves (Thms 4–6) that domination over h is governed by Green functions /
superharmonicity on (M, g̃). With h/π_J = e^{−Φ} this is g̃ = e^{−2Φ/(d−2)} g, the
textbook rescaling that takes ∫(R + |∇Φ|²)e^{−Φ}dV to ∫[R̃ − (1/(d−2))|∇̃Φ|²] dṼ
(C2; v1's coefficient (d−1)/(d−2) was wrong). For the Stein prior the frame is the
flat cylinder S^{d−1} × R via μ ↦ (μ/‖μ‖, ½ log‖μ‖²), with no Green function
(Komaki Ex. 1): the origin sits at infinite g̃-distance.
*Status:* THEOREM (Komaki) + IDENTITY (C2, C9). Meaning in statistics: **changing
the vague prior is a conformal change of the Fisher metric.** The "dilaton
gravity" form of the rescaled functional is a name for a Euclidean, static,
Riemannian functional and carries no further content (see §7).
*Prior art (AR-027):* the Einstein-frame reading of Komaki's frame was not found
(remark-level; trivial once seen).

**K6 — The dimension in Stein's theorem is the number of jointly estimated parameters.**
Three one-dimensional particles already trigger inadmissibility (A1). Any "d ≥ 3"
statement about *spatial* dimension presupposes a one-particle, position-only
model. *Status:* THEOREM (Stein; Brown) + check (A1). v1's "exact dimensional
threshold" coincidence with Weyl curvature is DEAD as stated.

**K7 — Priority observation (added 2026-10-23, AR-026).**
Brown (1971) is weighted-manifold potential theory on W_F = (R^m, δ, f* dx) written
before that theory existed under that name: his Theorem 4.3.1 is the capacity
characterization of parabolicity, and his Theorem 6.4.3 is the sphere-area
parabolicity test that Grigor'yan (1999, p. 178) attributes, for Riemannian
manifolds, to Lyons–Sullivan (1984) and Grigor'yan (1985). In the sources read,
neither literature cites the other. *Status:* OBSERVATION (sourced on both sides;
systematic cross-citation check pending under Q3). This is the stream's one
genuinely new sentence so far; it is historical, not mathematical.
*Prior art (AR-027):* not found; Grigor'yan 1999 cites no statistics, Johnstone
2019 and Takanashi–McAlinn 2023 cite no geometric parabolicity literature. A
citation-index sweep (not possible from this environment) is still required
before the word "first" is used anywhere.

**K8 — Spherical A₂ makes Brown's radial tests exhaustive (added 2026-10-23, AR-028 G0).**
With f̄(r) the sphere mean of f* and A(r) the sphere mean of 1/f*, suppose
Q(r) = f̄(r)A(r) ≤ C for r ≥ 1. Then ∫_1^∞ dr/(r^{m−1}f̄(r)) = ∞ gives admissibility
(bounded risk; Brown Thm 6.4.3) and < ∞ gives inadmissibility (Brown Thm 6.4.4,
because by Fubini the direction-averaged ray integral is ≤ C·∫dr/(r^{m−1}f̄) < ∞, so
Chebyshev yields a half-sphere of directions with uniformly bounded ray integrals).
*Status:* corollary of Brown's theorems, proof in AR-028 G0 §1; numerically
illustrated (g0_feasibility.py). *Consequence:* Brown's undecided examples have
Q(r) → ∞. Whether a volume-type iff theorem on the doubling + Poincaré class (the
T1 of AR-028) can decide such a case reduces to whether that class contains weights
with unbounded Q: for product weights it does not (K9); in general this is OPEN
(AR-028 G0 §6, correction of 2026-10-23 — the first record claimed the general
inclusion without proof). One such example, the product prior
(1+|θ₁|)^{−1} log(e+|θ₁|) dθ₁ ⊗ dθ₂dθ₃ on R³, is transient (1-D kernel
p_t(0,0) ≍ 4/log²t, product Green integral ≍ (1/π)∫dt/(t log²t) < ∞) hence
inadmissible, with both Brown tests silent — an instance of the Johnstone–Lalley
(1984) product-diffusion phenomenon, which answered Brown's "immunity" question.
*Prior art:* the lemma itself not found (AR-027 scope); too small to carry a paper.

**K9 — Doubling + Poincaré force A₂ on centred intervals (added 2026-10-23, AR-028 G0 §6).**
Let w > 0 on R, μ = w dt, ν = dt/w. If μ is doubling (μ(2I) ≤ Dμ(I)) and satisfies
the scale-invariant L² Poincaré inequality on all intervals (constant C|I|²), then
μ([−r,r])·ν([−r,r]) ≤ 32 C D³ r² for all r. *Proof:* two-region test function on
[−2r, 2r] (0 on [−2r,−r], 1 on [r,2r], energy-minimising between, energy
1/ν([−r,r])); variance ≥ ½·min of the two side masses ≥ μ([−r,r])/(2D³) by
doubling. Both hypotheses are necessary: (1+|t|)² is doubling but not Poincaré
(the valley at 0 is a bottleneck), Q ∝ r; (1+|t|)^{−2} is Poincaré but not
doubling, Q ∝ r. *Consequence:* for product weights w(x₁) on R^m, m ≥ 3, with w
doubling + Poincaré, the spherical ratio is bounded, K8 applies, and δ_F is in
fact always inadmissible by Brown Thm 6.4.4 — the volume criterion (T1) adds
nothing there. The log-example of K8 is NOT doubling (ratio ∝ log r), so it lies
outside T1's class, as recorded. Non-product case: OPEN, no candidate found.
*Status:* elementary; machine-illustrated (checks/g0_doubling_poincare.py).

---

## 1. Setup and notation

- Model {p(x|θ): θ ∈ Θ ⊂ R^d}, Fisher metric g_{ij} = E[∂_i log p ∂_j log p],
  Jeffreys prior π_J ∝ |g|^{1/2}, Laplace–Beltrami Δ_g. Skewness T_{ijk} and the
  α-connections as in Komaki (2006) §2.
- Prior ratio ψ = f/π_J = e^{−Φ}; u = √ψ = e^{−Φ/2}. Smooth metric measure space
  (M, g, dm), dm = ψ dV = e^{−Φ}dV. Weighted Laplacian Δ_Φ = Δ − ∇Φ·∇
  (= Δ + ∇log ψ·∇), self-adjoint on L²(dm); generator of the diffusion with drift
  −∇Φ (Brown's diffusion in the flat case, up to a factor 2 convention).
- Bakry–Émery Ricci tensor Ric_Φ = Ric + ∇∇Φ = Perelman's R^m_{ij}; weighted scalar
  curvature R^m = R + 2ΔΦ − |∇Φ|² (Perelman Rmk 1.3; note g^{ij}R^m_{ij} = R + ΔΦ ≠ R^m).
- Perelman's F(g, Φ) = ∫(R + |∇Φ|²)e^{−Φ}dV = ∫R^m dm = ∫(Ru² + 4|∇u|²)dV; its
  L²-gradient at fixed dm is −(Ric + ∇∇Φ) (Perelman §1.1).
- Parabolic / non-parabolic (M, g, dm): weighted Brownian motion recurrent /
  transient ⇔ no / some Green function ⇔ no / some nonconstant positive
  superharmonic function.

Komaki (2006) eq. (3), general curved model, with the sign as in the source:

  Risk_N(f) = d/(2N) + (1/(2N²)) g^{ij}(∂_i log ψ + ½T_i)(∂_j log ψ + ½T_j)
              + (1/N²) ∇^{(e)}_i{g^{ij}(∂_j log ψ + ½T_j)} + [prior-independent terms] + o(N^{−2}).

The difference of two priors removes the T-terms and the prior-independent terms
(eqs. (4)–(5)), which is why K1 is clean and K2 is about what K1 cannot see.

---

## 2. Dictionary (statistics ↔ weighted Riemannian geometry), with status

| statistics | geometry | status |
|---|---|---|
| model manifold with Fisher metric (M, g) | Riemannian manifold | definition (Amari–Nagaoka) |
| prior f = e^{−Φ}π_J | smooth metric measure space (M, g, e^{−Φ}dV) | definition |
| u = √(f/π_J) | Perelman's u = e^{−f/2} | definition |
| O(N^{−2}) risk reduction over Jeffreys | (R^m_Φ − R)/(2N²) = −2Δu/(N²u) | IDENTITY K1 |
| asymptotic domination over Jeffreys (Komaki Thm 2) | u nonconstant positive superharmonic on (M, g) | THEOREM |
| existence of shrinkage priors (Komaki Thm 1) | (M, g) non-parabolic (Green function) | THEOREM K3 |
| negative sectional curvature ⇒ shrinkage priors exist (Komaki Thm 3) | Aomoto's Green-function theorem | THEOREM |
| Brown Thm 5.1.1: admissibility of δ_F (bounded risk) | parabolicity of W_F = (R^m, flat, f* dx) | THEOREM K4 |
| Brown Thm 4.3.1: infimum of ∫‖∇j‖²f* over j = 1 on the ball, j → 0 | capacity of the unit ball in W_F (Grigor'yan Thm 5.1(6)) | THEOREM K4 |
| Brown Thm 6.3.1 (spherical F) | model-manifold test ∫dr/S(r) (Grigor'yan Prop 3.1) | THEOREM (C23) |
| Brown Thm 6.4.3 (any F): ∫dr/(r^{m−1} f̄(r)) = ∞ ⇒ admissible | sphere-area parabolicity test (Grigor'yan Thm 7.5, 1984/85) | THEOREM; K7 priority |
| — | ball-volume test ∫ρ dρ/V(ρ) = ∞ ⇒ parabolic (Grigor'yan Thm 7.3) | corollary of Brown 6.4.3 (C24) |
| MLE admissible iff d ≤ 2 | Brownian motion on R^d recurrent iff d ≤ 2 | THEOREM (Brown; f* ≡ 1 in K4) |
| Brown's representation δ = x + ∇log m; Tweedie | drift of the weighted diffusion | THEOREM (Brown 1971, per GLX eq. (10)) |
| proper prior ⇒ (finite-risk) proper Bayes admissible | finite weighted volume ⇒ recurrent | consistency check (classical both sides) |
| change of vague prior h (Komaki §3) | conformal change g̃ = (h/π_J)^{2/(d−2)}g | THEOREM K5 |
| Stein prior ‖μ‖^{−(d−2)} in Komaki's frame | flat cylinder S^{d−1} × R, origin at infinity | THEOREM (Komaki Ex. 1) |
| prior-independent O(N^{−2}) risk (Jeffreys baseline) | Efron curvature, m-embedding curvature, skewness, 4th moment — **not** R | NEGATIVE K2 |
| Perelman's R-potential, λ(g) | — | no counterpart (K2) |
| Bakry–Émery Ricci tensor Ric + ∇∇Φ | curvature of the weighted manifold; CD(K, ∞) controls heat kernel / Green function of Δ_Φ | DIRECTION Q1 |
| Ricci flow ∂_t g = −2(Ric + ∇∇Φ) | gradient flow of F at fixed measure | THEOREM (Perelman) with **no statistical process behind it** (§7) |
| Lorentzian signature, lapse, shift, horizon | — | DEAD (v1 Formalism 3; §6) |

---

## 3. The scalar-curvature question, resolved

v1 needed the prior-independent O(N^{−2}) term of the Jeffreys predictive risk to be
"directly proportional to the scalar curvature R" so that the integrated risk would
be Perelman's F. Komaki (2006) leaves that term unspecified ("terms independent of
f"). Komaki (2015) Theorem A1, eq. (29), specifies it. In the conventional setting
the surviving prior-independent terms are

  + (1/2N²)·E(v^{(e)ik}v^{(e)jl}) g_{kl} g_{ij}   (Efron curvature of the model)
  − (1/2N²)·E(v^{(m)}_{ij}v^{(m)}_{kl}) g^{ij}g^{kl}   (squared mixture mean curvature)
  − (1/3N²)·T_{ijk}T^{ijk}   (skewness)
  + (3/4N²)·Q_{ijkl} g^{ij}g^{kl}   (fourth moment)
  − (1/N²)·E(∂_i l ∂_j l v^{(m)}_{kl}) g^{ik}g^{jl}
  + (1/4N²)·E(v^{(m)}_{ij}v^{(m)}_{kl}) g^{ik}g^{jl}   (squared norm of the m-embedding curvature),

all built from moments of log-likelihood derivatives and the α-embedding curvatures
(Komaki's v^{(e)}, v^{(m)} are "vectors orthogonal to the model manifold"). None is a
Levi-Civita curvature invariant, and the decisive observation is dimensional: for a
one-parameter curved exponential family these terms are generically nonzero
(Efron 1975), while every intrinsic curvature of a one-dimensional Riemannian
manifold vanishes. So no rewriting can make the prior-independent term "the scalar
curvature" — at most R could hide inside a reorganization that leaves a d = 1
remainder, which is not the v1 claim.

Consequences carried into v2: K1 is exact for the *difference* of priors; the
integrated identity relates risk reduction to F **minus** its curvature term; the
geometric content of shrinkage is potential theory of Δ_g (K3) and of Δ_Φ (K4), not
curvature-as-risk.

---

## 4. Four geometries, four names (and the horn)

The word "interior geometry" in v1 denoted four different objects. v2 names them:

1. **Fisher–Rao metric g of the model.** Flat for the normal location family (the
   Stein setting: σ known); hyperbolic H²(−1/a) for location-scale families
   (Komaki Ex. 2); for N(μ, σ²): g = diag(1/σ², 2/σ²), K = −1/2 (C22).
2. **Weighted manifold (M, g, e^{−Φ}dV)** carrying the prior; its curvature is
   Bakry–Émery's Ric + ∇∇Φ and Perelman's R^m. This is where K1–K4 live.
3. **Komaki's conformal frame g̃ = (h/π_J)^{2/(d−2)}g** (K5).
4. **Estimator pullback g_int = J^T Σ^{−1} J** of v1 Formalism 2 (C11): a legitimate
   Riemannian object on the data space, defined by a choice of base metric Σ^{−1};
   for the James–Stein map its tangential eigenvalue vanishes at ‖x‖² = (d−2)σ²
   and its radial eigenvalue is 2 there (C12). No Schwarzschild form arises (C3).

**The horn (owner's picture).** The pseudosphere / hyperbolic cusp is a correct
picture of geometry 1 for a location-scale family: thin throat = σ → ∞ (zero
precision), flare = high precision, axial coordinate u = −ln σ ≈ ½ ln N. Two
lessons it teaches cleanly: (i) the horn's axis is the observation count, an
**external clock** (NC-010); (ii) the horn's curvature is the model's, whereas the
curvature in K1–K4 is the prior's. The curved-spine / anisotropic refinement is a
legitimate visualization of a non-geodesic reference path and unequal Fisher
eigenvalues; its physical labels have no derivation and are not carried forward.
Komaki's cylinder (K5) is a fifth picture: the Stein prior's frame has constant
cross-section and an infinitely long throat at the origin.

---

## 5. What "horizon" can mean here

- In geometry 4, the positive-part boundary ‖x‖ = σ√(d−2) is where the James–Stein
  map stops being injective and the **angular** pullback metric degenerates; inside,
  the positive-part map is constant (zero Jacobian). This is a statement about an
  estimator, not about causal structure. (C12)
- In geometry 3 for the Stein prior there is no horizon: the origin is a cusp at
  infinite distance and the manifold is a flat cylinder. (Komaki Ex. 1)
- In geometry 2 the natural "boundary" statements are about parabolicity (K3, K4),
  i.e. whether the weighted diffusion escapes to infinity — again not a horizon.

v1's "information horizon ≅ Schwarzschild horizon" is DEAD (C3, E5, E6).

---

## 6. The three v1 formalisms, recorded as explored options

| v1 option | what it proposed | what survived | status |
|---|---|---|---|
| Formalism 1 — variational risk-action (Komaki ↔ Perelman) | integrated KL risk = F; Bakry–Émery flow; Einstein frame | K1 (sign corrected), K2 (negative), K5 (frame) | kernel of v2 |
| Formalism 2 — Tweedie–Stein pullback metric; horizon | g_int = J^TΣ^{−1}J; horizon at ‖x‖² = d−2; Schwarzschild g_rr | geometry 4 as a well-defined construction; angular degeneration (C12) | construction kept, interpretation DEAD (C3; E5, E6) |
| Formalism 3 — ADM split from updating; Brown recurrence as Hamiltonian constraint | Lorentzian signature from "information gain enters with opposite sign"; K_ij = ∇∇Φ; constraint identification; momentum constraint | K_ij = ∇∇Φ is a correct trivial identity (C13); the Bochner step is correct (C15) | DEAD: signature asserted (E7); clock external; "Brown–Komaki condition = 2ρ_info" invented (E8); constraint identification is an analogy (C14); sign error (C16) |

Also DEAD from v1 Part V: the "Efron–Morris" pairwise force law (E12); from Part II:
the d ≥ 3 spatial coincidence (K6) and the Weyl-count formula (C1); from Part VI:
"flat observer's risk diverges" (C4: bounded per-step gap, strict domination).

---

## 7. Why there is no dynamics yet (structural note, carried as an open problem)

Perelman's remark in §1.1: in F_m the measure m is a *gauge* — different m give the
same flow up to diffeomorphism — and the flowing object is the metric g. In
statistics the situation is reversed: the Fisher metric g is fixed by the model,
and all content sits in the measure (the prior, then the posterior). Bayesian
updating moves the measure at fixed g: f_N ∝ f · L_N, so ∂_N log f_N is the
log-likelihood increment, not a Ricci-type flow; the only N-dependence of the
metric is the homothety g → N g. Hence the Bakry–Émery / Ricci flow of v1
Formalism 1 has **no statistical process generating it** as the framework stands,
and the "τ" of v1 Formalism 3 (update index) is unrelated to Perelman's flow
parameter. Any future dynamical claim must supply a mechanism that changes g, and
must declare its clock (CON-035). Until then the stream's content is static:
identities and potential theory on (M, g, dm).

---

## 8. Open questions, ranked

- **Q1 — CLOSED NEGATIVE (AR-026, 2026-10-23).** Brown (1971) read in full: every
  transferable sufficient recurrence test is already in his §6 (Thms 6.3.1, 6.4.2,
  6.4.3), the ball-volume test is a corollary of 6.4.3 (C24), and the curvature
  route (Ric_f ≥ K > 0 ⇒ finite measure ⇒ proper prior) reduces to the classical
  proper-Bayes case. No new admissibility criterion arises from transferring known
  parabolicity tests. Outcome: K4 upgraded to THEOREM, K7 recorded.
- **Q1′ — CLOSED (AR-028 G0, 2026-10-23; corrected the same day).** Lemma K8: on
  weights with bounded spherical A₂ ratio, Brown's two radial tests are
  exhaustive. Lemma K9: doubling + Poincaré force that bound for product weights,
  so a doubling / Faber–Krahn iff theorem (T1) adds no decidable case there; for
  non-product weights the inclusion is OPEN (the first record claimed it in
  general without proof — withdrawn). Brown's undecided examples have unbounded
  spherical A₂ ratio; the explicit one below is not doubling. The product
  sub-class is decided by product heat kernels — Johnstone & Lalley (1984) — and an
  explicit logarithmic example was decided (inadmissible) that way. The non-product
  undecided zone stays open and is not pursued. **Stream closed as a documented
  negative.**
- **Q2 (VERIFY).** Komaki Thm 6 uses negative curvature of the conformal frame
  (M, g̃) as a sufficient condition. Is there a statistical reading of Ric(g̃) or of
  Ric_Φ in the frame? (Likely only through Q1.)
- **Q3 — CLOSED at targeted-search scope (AR-027, 2026-10-23).** K1, K5, K7 not
  found; K4 known in Dirichlet-form language (Brown 1971; Johnstone 1986; Eaton
  1992; Takanashi–McAlinn 2023) but not in geometric language; the two
  literatures do not cite each other in the sources read. Remaining gap: a
  citation-index sweep on Brown 1971 and Komaki 2006, which needs Scholar /
  MathSciNet access. Until then the permitted wording is "not found in the
  literature we searched", never "new" or "first".
- **Q4 (EXPERIMENT, low).** The v1 Part VI toy model with corrected expectations
  (bounded gap, angular degeneration, named geometry) — only if a figure is needed
  for a note.
- **Q5 (FORMALIZE, lowest).** Lean pilot on the elementary identities C8/C9/C23,
  after Q3.

---

## 9. What a publication could and could not claim (assessment of record)

- **Could** (as a short note in an information-geometry venue; Q3 passed at
  targeted scope, citation sweep still owed): the dictionary of §2; K1 with its
  sign; K2 as the reason the dictionary stops at the gradient term; K4 as the
  geometric translation of the known Dirichlet-form formulation (Brown 1971,
  Johnstone 1986, Eaton 1992, Takanashi–McAlinn 2023 cited as the existing
  analytic form); K5 as a reading of Komaki's frame; K7 as a historical remark.
  Framed as "two literatures that already touch, with the contact points made
  explicit", consistent with the no-firstness rule of this programme.
- **Could not:** any gravitational claim; any dynamical claim (§7); any use of the
  words "horizon", "Einstein frame", "spacetime" except as names of functional
  forms with the fence of §7; any novelty wording before Q3.
- **Would upgrade the note to a paper:** nothing on the table. Q1 and Q1′ are
  closed (K8 shows the volume route is repackaging; the product route is
  Johnstone–Lalley 1984). The honest product is the dictionary, K7 and K8 as
  remarks — and the owner's assessment of record (2026-10-23): "no novelty, nothing
  to contribute". The stream is closed; this file is the record. A typeset
  version with figures, same claims and tags, is
  `articles/theory/latex/note.tex` (built with the IDEG paper's class).

---

## 10. Kill conditions for this stream

1. Q3 finds K1/K4 stated in the weighted-manifold or shrinkage literature → the
   stream reduces to a reading note; no publication. *Outcome 2026-10-23:* K4's
   analytic content is stated (Dirichlet-form recurrence), its geometric
   translation is not; K1 not found. Condition not triggered, but the note's
   claims shrink to translation + K1 + K7.
2. Q1 yielded no theorem (closed 2026-10-23). Q1′'s gate session yielded Lemmas
   K8–K9, which show the volume route adds nothing for product weights (general
   case open, no candidate), and found the product route to be prior art →
   **condition triggered: stream stopped (2026-10-23).**
3. Any attempt to reintroduce dynamics without a mechanism that moves g and a
   declared clock is refused at the substrate level (NC-010, HYP-003 clock rule).

---

## 11. Corrections log, v1 → v2

| v1 location | v1 statement | v2 disposition | evidence |
|---|---|---|---|
| Part II §2.1 | N_Weyl = (d+1)d(d−1)(d−2)/12, N(3) = 10 | removed; count formula was wrong | C1 |
| Part II §2.2 | Brown: u = ∇ln ψ admissible iff recurrent, ψ superharmonic | replaced by Brown Thm 3.6.1 (integral test) and K4 | M–S 2021 eq. (1.3); C23 |
| Part II headline | gravity turns on at the Stein threshold d ≥ 3 | removed; parameter dimension (K6) | A1 |
| Formalism 1 §1.2 | Risk = d/2N + (1/2N²)[K_curv + 2ΔΦ − |∇Φ|²], K_curv ∝ R | sign corrected (K1); K_curv ∝ R refuted (K2) | Komaki 2006 eq. (3); Komaki 2015 Thm A1 |
| Formalism 1 §1.3 | integrated risk ≡ Perelman's F | replaced by K1's integrated form (F minus curvature term) | C9, C10 |
| Formalism 1 §1.4 | coefficient (d−1)/(d−2) | 1/(d−2) | C2 |
| Formalism 2 §2.4 | g_rr ∝ (1 − r_S/r)^{−1}; horizon ≅ Schwarzschild | removed (§5) | C3, C12 |
| Formalism 3 §3.1 | Lorentzian signature from information gain | removed; clock external (§7) | — |
| Formalism 3 §3.2 | "Brown–Komaki condition = 2ρ_info"; Hamiltonian/momentum constraint identification | removed | C14, C16 |
| Part V.1 | Efron–Morris pairwise force law | removed | E12 |
| Part VI | flat observer's risk diverges; radial eigenvalue vanishes at horizon | corrected (bounded gap; tangential eigenvalue) | C4, C12 |
| Part I table / Abstract | "Statistical General Relativity" as a field | removed | E16 |
| AR-028 G0 §1 (first version) and K8 consequence | "T1's doubling + Poincaré class has bounded spherical A₂ ratio" asserted without proof | proved for product weights (K9); open in general; verdict unchanged | checks/g0_doubling_poincare.py |

---

## References (provisional stream ids; metadata status per `checks/biblio_verification_2026-10-23.md`)

- SRC-T01 Stein, C. (1956). Inadmissibility of the usual estimator for the mean of a multivariate normal distribution. *Proc. Third Berkeley Symp.* 1, 197–206. [VERIFIED (Crossref)]
- SRC-T02 James, W.; Stein, C. (1961). Estimation with quadratic loss. *Proc. Fourth Berkeley Symp.* 1, 361–379. [original UNVERIFIED; 1992 reprint record only]
- SRC-T03 Brown, L. D. (1971). Admissible estimators, recurrent diffusions, and insoluble boundary value problems. *Ann. Math. Statist.* 42(3), 855–903. DOI 10.1214/aoms/1177693318. [VERIFIED; **read in full 2026-10-23** (AR-026): Thms 4.3.1, 5.1.1, 5.6.1, 6.2.1, 6.3.1, 6.4.2–6.4.4, 6.5.1–6.5.2, Cors 4.3.2–4.3.4]
- SRC-T04 Komaki, F. (2006). Shrinkage priors for Bayesian prediction. *Ann. Statist.* 34(2), 808–819. DOI 10.1214/009053606000000010. arXiv:math/0607021. [VERIFIED; read in full]
- SRC-T06 Perelman, G. (2002). The entropy formula for the Ricci flow and its geometric applications. arXiv:math/0211159. [VERIFIED; §1 read]
- SRC-T10 Stein, C. M. (1981). Estimation of the mean of a multivariate normal distribution. *Ann. Statist.* 9(6), 1135–1151. DOI 10.1214/aos/1176345632. [metadata VERIFIED; statement via SRC-T11 eqs. (10)–(12)]
- SRC-T11 George, E. I.; Liang, F.; Xu, X. (2006). Improved minimax predictive densities under Kullback–Leibler loss. *Ann. Statist.* 34(1), 78–91. DOI 10.1214/009053606000000155. arXiv:math/0605432. [VERIFIED; §§1–2 read]
- SRC-T15 Komaki, F. (1996). On asymptotic properties of predictive distributions. *Biometrika* 83(2), 299–313. [metadata VERIFIED; not read]
- SRC-T19 Hartigan, J. A. (1998). The maximum likelihood prior. *Ann. Statist.* 26(6), 2083–2103. [metadata VERIFIED; not read]
- SRC-T25 Maruyama, Y.; Strawderman, W. E. (2021). A review of Brown 1971 (in)admissibility results under scale mixtures of Gaussian priors. arXiv:2110.01945. [read; metadata from arXiv header — verify]
- SRC-T26 Komaki, F. (2015). Asymptotic properties of Bayesian predictive densities when the distributions of data and target variables are different. *Bayesian Analysis* 10(1), 31–51 (per search; DOI 10.1214/14-BA886 — verify). arXiv:1503.07643. [Theorem A1 read]
- SRC-T27 Grigor'yan, A. (1999). Analytic and geometric background of recurrence and non-explosion of the Brownian motion on Riemannian manifolds. *Bull. Amer. Math. Soc.* 36(2), 135–249. DOI 10.1090/S0273-0979-99-00776-4. [VERIFIED from the AMS PDF header; **read** (AR-026): Prop. 3.1 + footnote 1 (p. 148), Thm 5.1 (§5), Thms 7.3, 7.5, 7.6 (pp. 177–178) with their attributions]
- SRC-T31 Grigor'yan, A. (2009). *Heat Kernel and Analysis on Manifolds.* AMS/IP Studies in Advanced Mathematics 47. [from memory — VERIFY; needed only for the weighted-manifold form of Thms 7.3/7.5, which Brown 1971 supplies independently for W_F]
- SRC-T32 Lyons, T.; Sullivan, D. (1984). Function theory, random paths and covering spaces. *J. Differential Geom.* 19, 299–323. [as attributed by Grigor'yan 1999 p. 178; VERIFY]
- SRC-T33 Brown, L. D.; Hwang, J. T. (1982). A unified admissibility proof. In *Statistical Decision Theory and Related Topics III*, vol. 1, 205–230. Academic Press. [from memory via Maruyama–Strawderman 2021 — VERIFY]
- SRC-T34 Eaton, M. L. (1992). A statistical diptych: admissible inferences — recurrence of symmetric Markov chains. *Ann. Statist.* 20(3), 1147–1179. DOI 10.1214/aos/1176348764. [metadata from Project Euclid listing via search; not read]
- SRC-T35 Hobert, J. P.; Robert, C. P. (1999). Eaton's Markov chain, its conjugate partner and P-admissibility. *Ann. Statist.* 27(1), 361–373. [from search; VERIFY]
- SRC-T36 Eaton, M. L.; Hobert, J. P.; Jones, G. L.; Lai, W.-L. (2008). Evaluation of formal posterior distributions via Markov chain arguments. *Ann. Statist.* 36(5), 2423–2452. DOI 10.1214/07-AOS542. arXiv:math/0701938. [read: abstract, §1, Thm 5.1]
- SRC-T37 Johnstone, I. (1984). Admissibility, difference equations and recurrence in estimating a Poisson mean. *Ann. Statist.* 12, 1173–1198. [from Johnstone 2019's reference list; VERIFY]
- SRC-T38 Johnstone, I. (1986). Admissible estimation, Dirichlet principles and recurrence of birth–death chains on Z^p_+. *Probab. Theory Related Fields* 71, 231–269. [pages per Johnstone 2019's reference list; a secondary list gives 213–269 — VERIFY]
- SRC-T39 Johnstone, I. M. (2019). Larry Brown's work on admissibility. *Statist. Sci.* 34(4), 657–668. DOI 10.1214/19-STS744. [read (NSF PAR copy)]
- SRC-T40 Srinivasan, C. (1981). Admissible generalized Bayes estimators and exterior boundary value problems. *Sankhyā Ser. A* 43, 1–25. [from Johnstone 2019's reference list; VERIFY]
- SRC-T41 Takanashi, K.; McAlinn, K. (2023). Inadmissibility and transience. arXiv:2310.17891. [read: abstract, §1, §4, Thm 2.4, App. A, references; publication venue unknown]
- SRC-T42 Evans, S. N.; Stark, P. B. (1996). Shrinkage estimators, Skorokhod's problem and stochastic integration by parts. *Ann. Statist.* 24(2), 809–815. DOI 10.1214/aos/1032894466. [metadata from search; not read]
- SRC-T43 Sturm, K.-T. (1994). Analysis on local Dirichlet spaces I: Recurrence, conservativeness and L^p-Liouville properties. *J. Reine Angew. Math.* 456, 173–196. [from secondary listings; VERIFY — the citation for Grigor'yan-type volume criteria on strongly local Dirichlet forms, hence on W_F]
- SRC-T44 Fukushima, M.; Oshima, Y.; Takeda, M. *Dirichlet Forms and Symmetric Markov Processes.* de Gruyter (1994; 2nd ed. 2010). [as cited by T36/T41; VERIFY]
- SRC-T45 Johnstone, I. M.; Lalley, S. P. (1984). On independent statistical decision problems and products of diffusions. *Z. Wahrsch. verw. Gebiete* 68, 29–47. DOI 10.1007/BF00535171. [metadata from Springer DOI listing via search; content known only through Johnstone 2019 p. 663; not accessed]
- SRC-T46 Berger, J. O.; Strawderman, W. E. (1996); SRC-T47 Berger, Strawderman & Tang (2005). [named by Johnstone 2019 as concrete uses of Brown's §6 criteria; titles and venues NOT recorded — VERIFY before any use]
- SRC-T28 Okudo, M.; Komaki, F. (2019). Bayes extended estimators for curved exponential families. arXiv:1906.07514. [eq. (13) read; verify]
- SRC-T29 Efron, B. (1975). Defining the curvature of a statistical problem (with applications to second order efficiency). *Ann. Statist.* 3, 1189–1242. [from memory via Komaki 2015's reference list — VERIFY]
- SRC-T30 Aomoto, K. (1966). L'analyse harmonique sur les espaces riemanniens, à courbure riemannienne négative. I. *J. Fac. Sci. Univ. Tokyo Sect. I* 13, 85–105. [as listed in Komaki 2006 ref. [4] — VERIFY]
- Context references of v1 (Jacobson, Connes–Rovelli, Chirco et al., Padmanabhan, Verlinde, Hu–Verdaguer, Caticha, Ruppeiner, Amari–Nagaoka, Buchert, Bakry–Émery, Efron–Morris, Efron 2011, Baranchik, Liang–Barron): metadata VERIFIED (see report); not load-bearing for v2.
