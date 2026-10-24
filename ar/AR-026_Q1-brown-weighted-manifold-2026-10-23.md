# AR-026 — Q1: does weighted-manifold potential theory give admissibility criteria beyond Brown (1971)?

```yaml
id: AR-026
title: "Read Brown (1971) and Grigor'yan (1999) in full; decide whether Bakry–Émery / parabolicity theory yields admissibility criteria not already in Brown"
mode: VERIFY + FORMALIZE
parent: v2 K4 (articles/theory/v2_admissibility_and_weighted_geometry.md §0), v2 Q1; RQ-001 information-geometry frame
priority: P1 (owner ruling 2026-10-23: "lets do Q1 open the browser lets get this papers")
inputs: [Brown 1971 full text (49 pp., JSTOR scan via Project Euclid, owner's browser session; read as page images),
         Grigor'yan 1999 Bull. AMS 36 (author's PDF + AMS PDF; text extracted),
         Maruyama–Strawderman 2021 (AR-024), lint checks C23–C24]
question: >
  (a) What exactly does Brown (1971) prove, in weighted-manifold language? (b) Do the parabolicity /
  transience criteria of Grigor'yan (1999) §§3, 5, 7 transfer to the weighted manifold (R^m, flat, f* dx)
  and, if so, do they give admissibility statements not already in Brown §6?
deliverable: this packet; v2 §0 K4 restated in sourced general form, new K7 (priority), Q1 closed, Q1' opened;
  lint C24 (sphere test vs ball test)
promotion_effect: v2 K4 status REFORMULATION -> THEOREM (Brown 1971 Thms 4.3.1, 5.1.1, 6.3.1, 6.4.2–6.4.4)
  with the geometric reading sourced to Grigor'yan Prop 3.1, Thm 5.1, Thm 7.5
kill_effect: Q1 as posed (new sufficient admissibility criteria by transferring volume tests) is CLOSED NEGATIVE;
  the "candidate theorem" route for a paper is dead unless Q1' (below) succeeds
status: DONE (2026-10-23; deltas QUEUED, not applied — parallel-stream rule)
```

## 0. Verdict

**Brown (1971) is weighted-manifold potential theory on (R^m, δ_ij, f* dx), written
thirteen years before the Riemannian parabolicity tests it coincides with were
published for manifolds.** Every transferable sufficient condition for recurrence
in Grigor'yan's survey is already in Brown §6, and the one that is not literally
there (the ball-volume test) is a corollary of Brown's Theorem 6.4.3 by a
two-line Cauchy–Schwarz argument (lint C24). Q1 as posed is therefore **closed,
negative**: no new admissibility criterion comes from transferring known
parabolicity tests. What the reading does establish is a precise dictionary and a
priority observation (K7), and it pins down the one place where geometric methods
might still add something (Q1′).

## 1. Brown (1971), read: the statements that matter (page numbers of the Annals)

Setting (p. 857–858): X ~ N_m(θ, I), loss (δ−θ)ᵀD(δ−θ), generalized prior F with
convolution density f* = p*F, generalized Bayes δ_F = x + ∇f*/f* (1.2.2),
γ_F = δ_F − x. K_F = closed convex hull of supp F.

- **Fundamental equation (1.3.3)–(1.3.4), p. 860:** for finite G_i with
  ĵ_i = (g_i*/f*)^{1/2}, B(G_i, δ_F) − B(G_i, δ_{G_i}) = ∫‖∇ĵ_i‖² f* dx.
  *Geometric reading:* the Bayes-risk difference is the **weighted Dirichlet
  energy** of ĵ_i on the weighted manifold W_F := (R^m, δ, f* dx).
- **Variational problem (1.3.5)–(1.3.6), p. 860–861:** minimize ∫_{|x|>1}|∇j|² f* dx
  over piecewise differentiable j with j ≥ 1 on |x| ≤ 1 and j → 0 at infinity;
  infimum > 0 ⇒ δ_F inadmissible; a minimizing sequence with energy → 0 ⇒
  (heuristically) admissible. *Geometric reading:* this infimum is the **capacity of
  the unit ball** in W_F; cap = 0 is the definition of parabolicity (Grigor'yan
  1999 Thm 5.1(6), §4.3).
- **Euler equation (1.3.9)–(1.3.10), p. 862:** Σ j_ii + Σ (f_i*/f*) j_i = 0, i.e.
  L_F j = 0 with L_F = Δ + ∇log f*·∇, "the generator of the diffusion with local
  variance 2I and local mean ∇f*/f* = δ_F(x) − x"; the exterior Dirichlet problem is
  soluble iff the diffusion is transient; the solution is the hitting probability of
  the unit ball. *Geometric reading:* L_F is the **weighted Laplacian** Δ_μ of W_F
  (μ = f* dx); the diffusion is weighted Brownian motion on W_F.
- **Theorem 4.3.1 (p. 878–880, statement reconstructed from the proof and from
  p. 885):** {Z_t} transient ⟺ inf_{j∈J} ∫|∇j|²f* dx = k₀ > 0; recurrent ⟺ there
  is a sequence in J with energy → 0. **Corollary 4.3.2:** K_F compact ⇒ recurrent.
  **Corollary 4.3.3:** f*(x) ≥ b₁|x|^{2−m+b₂} for |x| > b₀ ⇒ transient.
  **Corollary 4.3.4:** f*(x) ≤ b₁|x|^{2−m−b₂} ⇒ recurrent.
- **Theorem 5.1.1 (p. 884), verbatim structure:** a necessary condition for δ to be
  admissible is that δ = δ_F a.e. for some F with f* < ∞. (A) If {Z_t} is transient
  then δ is inadmissible. (B) If {Z_t} is recurrent and sup_{x∈K} |γ_F(x)| = B < ∞
  then δ is admissible. Theorem 3.3.1: (5.1.1) ⟺ sup_{θ∈K} R(θ, δ) < ∞.
- **Theorem 5.6.1 (p. 893):** Stein's sufficient condition in Brown's form (finite
  measures G_i with G_i({|θ| ≤ 1}) ≥ 1 and B(G_i, δ) − B(G_i, δ_{G_i}) → 0 ⇒ δ
  admissible).
- **§6.1 (p. 896):** Theorem 5.1.1 does *not* contain all known admissibility
  results: proper Bayes rules can violate (5.1.1) (example f* = (4π)^{−m/2}e^{−|x|²/4}).
- **Theorem 6.2.1 (p. 896–897), m = 1:** inadmissible iff ∫_1^∞ dx/f*(x) < ∞ or
  ∫_{−∞}^{−1} dx/f*(x) < ∞ (Feller's test, cited to Itô–McKean).
- **Theorem 6.3.1 (p. 898), spherical F:** ∫_1^∞ (r^{m−1} f*_R(r))^{−1} dr < ∞ ⇒
  inadmissible; = ∞ and γ_F bounded ⇒ admissible. (This is the M–S 2021 quote in
  the variable r.) **Corollary 6.3.2 / 6.4.1:** radial drift γ·r̂ ≥ (2−m+k)/|x| ⇒
  inadmissible; ≤ (2−m)/|x| and bounded ⇒ admissible.
- **Theorem 6.4.2 (p. 899), general F with γ(x) = O(1/|x|):** with f̄(r) the average
  of f* over the sphere |x| = r, ∫_1^∞ (r^{m−1} f̄(r))^{−1} dr < ∞ ⇒ inadmissible,
  = ∞ ⇒ admissible (iff). Remark: f*(x_r) for any point on the sphere may replace f̄.
- **Theorem 6.4.3 (p. 899–900), general F:** γ bounded on K_F and
  ∫_1^∞ (r^{m−1} f̄(r))^{−1} dr = ∞ ⇒ admissible ({Z_t} recurrent). Proof: radial
  test functions j_i(x) = c_i ∫_{|x|}^{i} (r^{m−1}f̄)^{−1} dr with energy c_i → 0.
- **Theorem 6.4.4 (p. 900):** if a set of directions Q of positive measure has
  sup_{φ∈Q} ∫_1^∞ (r^{m−1} f*_R(r, φ))^{−1} dr < ∞ then δ_F is inadmissible.
  Remark (p. 900): there are examples satisfying neither (6.4.6) nor (6.4.7).
- **Theorem 6.5.1–6.5.2 (p. 901–902):** coordinate-wise products; 6.5.2's second
  proof uses the invariant measure f* dx of {Z_t} and ergodicity.
- **Reference list (p. 902):** James & Stein cited as "(1960). Estimation with
  quadratic loss. Proc. Fourth Berkeley Symp. Math. Statist. Prob. 1 361–379" —
  volume and pages confirm SRC-T02's as-given values; the year is given as 1960
  (symposium) where modern citations give 1961 (publication).

## 2. Grigor'yan (1999), read: the matching statements

- **Prop. 3.1 (p. 148):** a model manifold (metric dρ² + σ(ρ)²dθ², S(ρ) = ω_d σ^{d−1})
  is recurrent iff ∫^∞ dr/S(r) = ∞. Footnote 1: neglecting the angular direction,
  this is recurrence of the 1-D diffusion generated by d²/dρ² + (S′/S) d/dρ
  (Feller, Khas'minskii).
- **Thm 5.1 (p. 164 ff.):** equivalent definitions of recurrence, item (6): capacity
  of every (some) precompact set is zero (parabolicity).
- **Thm 7.3 (p. 177), Karp/Varopoulos/Grigor'yan:** complete M with
  ∫^∞ ρ dρ/V(x, ρ) = ∞ is parabolic. **Thm 7.5 (p. 178), Ahlfors–Nevanlinna
  (surfaces), Lyons–Sullivan (1984) and Grigor'yan (1985) (manifolds):**
  ∫^∞ dρ/S(x, ρ) = ∞ ⇒ parabolic; necessary too for model manifolds, not in
  general. **Thm 7.6:** iff via flux of an exhaustion function.
- Weighted manifolds are not treated explicitly in the 1999 survey (the measure is
  the Riemannian volume throughout); the arguments of §7 use only the Dirichlet
  form and volumes of balls, and the weighted versions are standard in the
  author's later monograph — **cite-verify item** (Grigor'yan, *Heat Kernel and
  Analysis on Manifolds*, AMS/IP 2009; not read).

## 3. The dictionary, now sourced on both sides

| Brown 1971 | weighted manifold W_F = (R^m, δ, f* dx) | Grigor'yan 1999 |
|---|---|---|
| ∫‖∇ĵ‖² f* dx (1.3.4) | weighted Dirichlet energy | §2.1, (2.4) |
| inf over J of the energy (1.3.5); Thm 4.3.1 | capacity of the unit ball; cap = 0 ⟺ parabolic | Thm 5.1(6), §4.3 |
| L_F = Δ + ∇log f*·∇ (1.3.10) | weighted Laplacian Δ_μ | §2.1 (unweighted form) |
| {Z_t}, local mean ∇log f*, variance 2I | weighted Brownian motion (time ×2) | §2.2 |
| exterior Dirichlet problem soluble ⟺ transient (p. 862) | hitting probability of the ball is nonconstant ⟺ non-parabolic | §4.5–4.6 |
| Thm 5.1.1: admissible ⟺ recurrent (bounded risk) | admissible ⟺ W_F parabolic | — (statistics only) |
| Thm 6.2.1 (m = 1) | Feller's test | Prop 3.1 footnote |
| Thm 6.3.1 (spherical) | model-manifold test ∫dr/S(r), S = ω r^{m−1} f*(r) | Prop 3.1 (lint C23) |
| Thm 6.4.3 (general, sufficient) | ∫dr/S̄(r) = ∞ ⇒ parabolic, S̄ = ω r^{m−1} f̄(r) | Thm 7.5 (1984/1985) |
| Thm 6.4.2 (iff under γ = O(1/|x|)) | quasi-model manifold: f* varies by a bounded factor on spheres | Thm 7.5 + Prop 3.1 (no exact analogue) |
| Thm 6.4.4 (directional, inadmissibility) | transience from a positive-measure cone of directions | no exact analogue |
| Cor. 4.3.2 (K_F compact ⇒ recurrent); §6.5.2 ergodicity | finite weighted volume ⇒ recurrent | §5 (finite measure) |
| — | ball-volume test ∫ρ dρ/V(ρ) = ∞ ⇒ parabolic | Thm 7.3 — **corollary of Brown 6.4.3** (lint C24) |

## 4. Why the transfer yields nothing new (C24)

By Cauchy–Schwarz on dyadic shells, (2^{k+1} − 2^k)² ≤ ∫_{2^k}^{2^{k+1}} S̄ dρ ·
∫_{2^k}^{2^{k+1}} dρ/S̄, so ∫_{2^k}^{2^{k+1}} dρ/S̄ ≥ 4^k / V(2^{k+1}); summing,
∫^∞ ρ dρ/V = ∞ forces ∫^∞ dρ/S̄ = ∞. Hence the Karp–Varopoulos–Grigor'yan
volume test, transferred to W_F, is implied by Brown's Theorem 6.4.3. The converse
fails (thin cubic shells: sphere integral diverges, ball integral converges), so
Brown's sphere test is strictly stronger. Lint C24 illustrates both numerically.

Curvature route: Ric_f = −∇²log f* ≥ K > 0 (strongly log-concave f*) forces finite
weighted volume, i.e. a proper prior — admissibility is then classical (Brown
§6.1, Cor. 4.3.2). Ric_f ≥ 0 (log-concave f*, inherited from log-concave priors by
Prékopa) has no volume comparison in the N = ∞ case and gives no new test.

## 5. What the reading does establish

- **K4 upgraded to THEOREM:** admissibility (bounded risk) ⟺ parabolicity of W_F
  is Brown's Theorem 5.1.1 read on W_F; the spherical and spherical-average tests
  are Brown's Theorems 6.3.1 / 6.4.2–6.4.3.
- **K7 (priority, new observation):** Brown's Theorem 6.4.3 (1971) is the
  weighted-Euclidean instance of the parabolicity test that Grigor'yan (p. 178)
  attributes to Lyons–Sullivan (1984) and Grigor'yan (1985) for Riemannian
  manifolds; Brown's Theorem 4.3.1 is the capacity characterization of
  parabolicity on W_F. Neither literature cites the other in the sources read
  (Brown's reference list; Grigor'yan's attributions) — to be checked
  systematically under Q3.
- **Q1′ (the surviving open question, narrow):** Brown notes (p. 900) examples where
  neither his sufficient recurrence test (6.4.6) nor his directional transience
  test (6.4.7) applies. Grigor'yan's transience criteria via isoperimetric /
  Faber–Krahn inequalities (§8, §10–11) are of a different type (not radial). Do
  weighted Faber–Krahn inequalities decide admissibility in Brown's undecided
  examples? Prerequisites: the weighted relative Faber–Krahn inequality (holds
  under volume doubling + Poincaré for the weighted measure), an explicit
  undecided example from Brown's remark, and a check against Brown–Hwang (1982)
  and Maruyama–Strawderman (2021). Research-level; not attempted here.

## 6. Sources and access notes

- Brown 1971: obtained through the owner's Chrome session (Project Euclid requires
  a human-verification step on download; the assistant does not complete CAPTCHAs,
  the owner clicked it). JSTOR scan without text layer; pages rendered to PNG and
  read as images. Local copy: owner's Downloads (`admissible-estimators-brown.pdf`);
  working copy in the session scratchpad. **Not committed to the repository.**
- Grigor'yan 1999: author's PDF (Bielefeld) and AMS PDF, byte-level identical
  content not checked; text extracted from the AMS file.
- Stein 1981, Hartigan 1998, James–Stein 1961: not downloaded in this session (no
  longer load-bearing: Stein 1981 via GLX eqs. (10)–(12); Hartigan superseded by
  Komaki 2015 Thm A1 for the E2 question; James–Stein volume/pages corroborated by
  Brown's reference list).

## 7. Proposed KB deltas (QUEUED)

- v2 (stream file, applied): K4 → THEOREM with the §3 table; K7 added; Q1 closed,
  Q1′ opened; references SRC-T03 status "read in full".
- KB-003 (queued): TH-039 wording unchanged; new SRC-T31 Grigor'yan 2009 monograph
  (verify), SRC-T32 Lyons & Sullivan 1984 (J. Diff. Geom. 19, 299–323 — from
  Grigor'yan's attribution; verify), SRC-T33 Brown & Hwang 1982 (verify).
- KB-005 (queued): AR-026 DONE; AR-027 (Q3 systematic prior art) now also covers
  "has anyone identified Brown 1971 with weighted-manifold parabolicity?"; AR-028
  Q1′ PROPOSED (P2, research-level).
