---
id: AR-029a
parent: AR-029 (seam gate A), step A2 of the programme of record (AR-029 §7)
title: "A2 — the scattered co-dimension-two lattice weight: a doubling + Poincaré prior on R³ on which both of Brown's radial tests are silent and the volume test decides transience (δ_F inadmissible); GO/NO-GO for A as a theorem note"
date: 2026-10-24
mode: FORMALIZE + EXPERIMENT + VERIFY
owner_ruling: "Good and interesting results... Thank you. Let's go A2" (2026-10-24)
inputs:
  - AR-029 §7 row A2 (the preregistered construction and kill rule), §1 Lemma K11, §0 item 2 (Theorem 5 stands)
  - articles/theory/Co-Dimension-2-Extensions.md Theorem 5 (Argon; the cylinder weight) — INPUT, assessed in AR-029 §6
  - Brown 1971 Thms 4.3.1, 5.1.1 (A)/(B), 6.4.3, 6.4.4 as read in AR-026 §1 (hypotheses quoted there)
  - Grigor'yan 1999 Thms 7.3, 7.6, 11.1 and the two remarks after 11.1 — READ TODAY from the author's PDF (text extracted)
  - Björn 2001, Ann. Acad. Sci. Fenn. Math. 26, 175–188, Proposition 6 and Lemma 11 — READ TODAY (PDF text extracted)
  - Björn–Buckley–Keith 2005, Proc. AMS 134(3), 703–705, Remark 4 (quoting HKM Corollary 15.35) — READ TODAY
checks:
  - articles/theory/checks/a2_scattered_weight.py  → a2_scattered_weight_2026-10-24_a4.txt, _a6.txt  (D1–D6; seed 20261024)
  - articles/theory/checks/a2_poincare_eigen.py    → a2_poincare_eigen_2026-10-24_a4.txt            (E1–E4)
kill_rule: "GO for a paper iff (i) uniform doubling + Poincaré, (ii) both Brown tests silent, (iii) μ(B_r) ≍ r³ all hold with proof sketches a referee could check; else A is the examples note" (AR-029 §7)
status: EXECUTED 2026-10-24 — verdict in §0: GO (conditional on the citation checks listed in §0 item 6)
---

# AR-029a — A2: the scattered lattice weight

## 0. Verdict

1. **The construction exists and does what A2 asked.** On R³ take the latitude circles Γ = ∪ Γ_{k,i,j} of §1 (one lattice
   of circles per dyadic shell, spacing ≍ s_k = 2^{k/2} in the meridian half-plane, 2^{k+2} circles per shell whose polar
   angles exhaust the grid π(n+½)/2^{k+2}) and the weight w = ((1+d²)/(1+|x|+d²))^{α/2}, d = dist(x,Γ), α ≥ 4. Then:
   (i) μ = w dx is doubling and supports the scale-invariant L² Poincaré inequality on all balls (Proposition K14 (a),
   §3 — proof architecture with two external inputs; numerics E1–E3); (ii) f̄(r) is bounded below and every ray's
   integral ∫dr/(r²w) diverges, so Brown's Theorems 6.4.3 and 6.4.4 are both silent (§2, exact bounds; D2–D3);
   (iii) μ(B_r) ≍ r³ (§2; D4). Hence ∫ r dr/μ(B_r) < ∞ and, by Grigor'yan Thm 11.1 under the relative Faber–Krahn
   inequality that doubling + Poincaré provide, W_F is **transient**; by Brown Thm 5.1.1 (A) δ_F is **inadmissible**.
2. **The weight is a legitimate prior.** Lemma K12 (§2): log w is Lipschitz with constant L = α/2 + o(1) (D6: 1.999 at
   α = 4), so f* := φ*w is a Gaussian marginal with c_L w ≤ f* ≤ C_L w and |∇log f*| ≤ L. Every statement above is
   stable under comparability of weights, so it holds for f* as for w. This disposes of AR-029's open item
   "Hess log f* ≥ −I for every example": the same lemma legitimises Theorem 5's cylinder weight, the wall weight of
   AR-029, and the G0 product weight (all have Lipschitz logarithms).
3. **The hierarchy of tests under doubling + Poincaré is now complete (Theorem K15, §4):** parabolic ⟺ Brown's sphere test
   (6.4.3) fires ⟺ the volume test fires; Brown's ray test (6.4.4) implies transience but is **not** exhaustive for it in
   m ≥ 3 — the lattice weight is the witness. So within the doubling + Poincaré class Brown's own sphere test already
   decides admissibility completely, and the only case the geometric literature adds is the transient one where no cone
   of rays is cheap: exactly A2's weight. Together with AR-029 (the wall: parabolic, not D+P) and AR-028 (the G0
   product: transient, not doubling), Brown's undecided zone is now populated on both sides, inside and outside D+P.
4. **Argon's Theorem 5 (1) acquires a published citation:** Björn 2001, Prop. 6 (a generalisation of Chanillo–Wheeden): for
   x = (x′,x″), x′ ∈ R^k, 2 ≤ k ≤ n, v ∈ A_p, the weight v(x)(1+|x′|)^{γ₀}Π_j(|x′−a_j|/(1+|x′−a_j|))^{γ_j} is p-admissible
   for all γ_j ≥ 0. With k = 2, n = 3, v ≡ 1, m = 0 this is the cylinder weight (1+|x′|)^α ≍ (1+|x′|²)^{α/2}; with
   γ₀ = 0, m = 1 it is the local shape (d/(1+d))^α of A2's weight. Also the HKM Corollary 15.35 statement is confirmed
   second-hand (Björn–Buckley–Keith 2005, Remark 4: |x|^α, α > 0, is p-admissible in R^n, n ≥ 2, for all p > 1, and
   is A_p iff p > 1 + α/n) — HKM itself still to be opened (owner library item).
5. **Numbers of record (§5):** worst sampled ray pays ≥ 0.94 per block at α = 4 (bound 0.28), doubling per block at α = 6;
   f̄ ∈ [0.0039, 0.052]; μ(B_r)/(4πr³/3) ∈ [0.019, 0.029] (period-2 alternation by parity of k); doubling ratios 4–13 at
   scales ≥ s_k and the co-dimension-two values (≤ 94) at tube scale; Neumann λ₁ρ² for the lattice on axis-centred
   balls: 1.55–3.09 from ρ = s_k to 8 s_k across k = 8, 10 (Lebesgue 4.33), h-converged to three digits; local weight
   0.77 (R → ∞); single circle 0.47–2.6 over all R_c and ρ ≥ R_c; wall control collapses (E4, §5).
6. **GO / NO-GO: GO** for A as a short theorem note (K12–K15 with the two AR-029 examples), under the kill rule's own
   terms: (i)–(iii) hold with proof sketches a referee can check, where "check" means verifying the following
   load-bearing external statements, all standard and all still tagged verify until the owner opens them:
   (a) Hajłasz–Koskela 2000 (Mem. AMS 688): weak ⇒ strong Poincaré under doubling, and (1,2) ⇒ (2,2) self-improvement
   (theorem numbers not yet seen); (b) doubling + Poincaré ⇒ relative Faber–Krahn (Grigor'yan 1991 / Saloff-Coste 1992
   via the heat-kernel upper bound; Grigor'yan 1999 remark after Thm 11.1 gives RFK ⟺ doubling + upper bound, citing
   [79, Prop 5.2] and [37, Thm 1.1]); (c) the weighted-manifold form of Thm 11.1 (Grigor'yan 2009 monograph; AR-026
   cite-verify item); (d) Björn 2001 Prop 6 — READ (primary); (e) Brown 5.1.1 (A) — READ (AR-026). Nothing in the
   argument depends on a statement we could not source. **What A2 does not deliver:** an off-axis 3-D eigenvalue test
   (the proof covers off-axis balls through the cell decomposition, the numerics only through D5 and the on-axis
   problems), and the m = 2 case (not attempted; see §6).

## 1. The construction

**Shells and lattice.** For k ≥ 4 let N_k = 2^{k+2}, L_k = 2^{⌈k/2⌉}, M_k = N_k/L_k. Layer i (0 ≤ i < L_k) has radius
r_{k,i} = 2^k + i·2^k/L_k; circle (k,i,j) (0 ≤ j < M_k) is the latitude circle {|x| = r_{k,i}, θ = θ_n}, θ_n = π(n+½)/N_k,
n = jL_k + i. The map (i,j) ↦ n is a bijection onto {0,…,N_k−1}, so the N_k circles of shell k occupy ALL the angles
of the grid π(n+½)/N_k. In the meridian half-plane the circles are a sheared rectangular lattice with radial spacing
2^k/L_k ∈ {s_k, s_k/√2} and angular spacing rπL_k/N_k ∈ (0.79, 2.22)·s_k, s_k := 2^{k/2} (D1). Consecutive layers are
offset by one grid step π/N_k in angle (physical ≤ π/4 at the outer radius), which is what spreads the angular
coverage across the shell's thickness instead of across a single surface — the opposite of AR-029's wall, where all
2^k circles of a block sat on one surface Σ_k at angular spacing π/2^k and radial spacing 1.

**Weight.** w(x) = ((1+d²)/(1+|x|+d²))^{α/2}, d = dist(x,Γ), α ≥ 4. Writing s(r)² = 1 + r: w ≍ (1+d²)^{α/2}/s^α for
d ≤ s/2 (the cylinder weight normalised by the local spacing), and w ∈ [(u²/(1+u²))^{α/2}·(1+O(1/s²)), 1] for d = us,
u ≳ 1. Thus the low-weight set {w ≤ ε} is a union of tubes of radius O(√ε·s) around circles ≍ s apart: for ε small the
tubes are disjoint and thin, and no co-dimension-one surface of small weight exists at any scale (D1: the maximal
distance from a shell point to Γ is 0.96–1.54 s_k; the nearest-neighbour distance between circles is ≥ 0.71 s_k).
Circles near the poles are small (radius ≥ 0.39), the smallest being point-like; every circle of layer i other than
n = i has radius ≥ 1.2 s_k.

**Why these exponents.** A ray at polar angle φ passes within angular distance π/(2N_k) of some θ_n, i.e. within
physical distance ≤ rπ/(2N_k) ≤ π/4 of a circle of shell k at radius r_{k,i} ≤ 2^{k+1}. On r ∈ [r_{k,i}−1, r_{k,i}+1]
one has d² ≤ 1 + π²/16 < 1.62 and w ≤ (2.62/r_{k,i})^{α/2}, so
∫_{r_{k,i}−1}^{r_{k,i}+1} dr/(r²w) ≥ 2(r_{k,i}/2.62)^{α/2}/(r_{k,i}+1)² ≥ 0.28·r_{k,i}^{α/2−2}. For α = 4 every block
contributes ≥ 0.28 to every ray (α = 4 is the threshold at which a bounded miss distance still yields a constant); for
α > 4 the contribution grows like 2^{k(α/2−2)}. Spacing s_k = 2^{k/2} is forced by counting: N_k ≍ 2^k circles of
length ≍ 2^k each must be spread through a shell of volume ≍ 8^k with mutual distance ≍ s, so s² ≍ 8^k/(2^k·2^k) = 2^k.

## 2. Lemma K12 and the elementary parts of Proposition K14

**Lemma K12 (Gaussian-marginal comparison).** Let F ≥ 0 be locally integrable on R^m with log F L-Lipschitz, and let
f* = φ*F (φ the standard Gaussian). Then (a) c_L F ≤ f* ≤ C_L F with c_L = E e^{−L|Z|} > 0, C_L = E e^{L|Z|} < ∞,
Z ~ N(0,I_m); (b) |∇log f*| ≤ L; (c) f* < ∞ everywhere and F is a σ-finite measure, so δ_F = x + ∇log f* is a
generalised Bayes estimator to which Brown's Theorem 5.1.1 applies; (d) the weighted spaces (R^m, F dx) and (R^m, f* dx)
have comparable Dirichlet forms, hence the same capacities up to constants (Brown Thm 4.3.1), the same parabolicity
type, and comparable doubling constants, Poincaré constants, sphere means and ray integrals (so Brown's two tests are
silent for one iff for the other, and the volume test fires for one iff for the other).
*Proof.* e^{−L|z|} ≤ F(x+z)/F(x) ≤ e^{L|z|}; integrate against φ for (a); ∇f* = φ*(F∇log F) gives (b); (d) is
∫|∇u|²F ≍ ∫|∇u|²f* for every test function. ∎  For m = 3: C_2 = 73.8, c_2 = 0.085 (sympy, chi₃ integral).
*Application.* For A2's weight, ∇log w = (α/2)[2d∇d/(1+d²) − (∇|x| + 2d∇d)/(1+|x|+d²)], |∇d| ≤ 1 a.e., so
L ≤ (α/2)(1 + 1.618) analytically and L = α/2 + o(1) in practice (D6: 1.9987 at α = 4, 2.9981 at α = 6; the second
term is O(1/|x|)). The same computation gives Lipschitz logarithms for Theorem 5's weight ((α/2)·2d/(1+d²) ≤ α/2),
AR-029's wall weight (≤ α), and the G0 weight (1+|t|)^{−1}log(e+|t|) (≤ 1). *Remark.* Theorem 5's weight is even a
Gaussian marginal exactly: E|y+Z|⁴ = |y|⁴ + 8|y|² + 8 for y, Z ∈ R² (sympy), i.e. (1+|y|²)² ≍ φ*|θ′|⁴.

**Proposition K14 (the lattice weight), parts (b)–(c).** (b) *Silence of 6.4.4:* shown in §1 for every direction φ,
with the explicit bound 0.28·r^{α/2−2} per block (D3 gives ≥ 0.94 at α = 4 over 802 sampled directions per block,
including the worst-case midpoints between consecutive θ_n, the pole and the equator). Hence ∫_1^∞ dr/(r²w(rφ)) = ∞
for EVERY φ, and no set of directions of positive measure has uniformly bounded ray integrals. *Silence of 6.4.3:* on
each sphere |x| = r the set of θ with d ≥ s/4 has θ-measure fraction ≥ c₀ > 0 (lattice geometry: the tubes of radius
s/4 around circles ≥ 0.71 s apart cover a bounded fraction of any sphere), and there w ≥ ((s/4)²/(1+r+s²/16))^{α/2}
≥ (1/17)^{α/2}, so f̄(r) ≥ c₀17^{−α/2} and ∫dr/(r²f̄) < ∞ (D2: f̄ ∈ [0.0039, 0.052] at α = 4). (c) *Volume:*
w ≤ 1 gives μ(B_r) ≤ (4π/3)r³; the same fraction argument on shells gives μ(B_r) ≥ c r³ (D4: 0.019–0.029 times the
Lebesgue volume). Hence ∫^∞ r dr/μ(B_r) < ∞. ∎ (modulo (a))

## 3. Proposition K14 (a): doubling + Poincaré — the proof architecture

Write D+P for "μ is doubling and ∫_B|u−u_B|²dμ ≤ C ρ²∫_B|∇u|²dμ on every ball of radius ρ" (the (2,2) strong form;
this is what the Neumann eigenvalue measures and what Grigor'yan's chain needs). Three external inputs:

- **[B01]** Björn 2001, Prop. 6 (read): for x′ ∈ R^k, 2 ≤ k ≤ n, the weights (1+|x′|)^{γ₀}Π_j(|x′−a_j|/(1+|x′−a_j|))^{γ_j}
  are p-admissible on R^n (doubling + weak (1,p)-Poincaré). We use k = 2, n = 3, p = 2.
- **[HK00]** Hajłasz–Koskela 2000: under doubling, weak (1,p)-Poincaré ⇒ strong (p,p)-Poincaré on balls (self-improvement
  in the exponent and removal of the dilation). Verify theorem numbers.
- **[BL]** bi-Lipschitz invariance: if Φ is bi-Lipschitz with constant Λ and μ′ = Φ_*μ, then D+P for μ with constant C
  gives D+P for μ′ with a constant depending on (C, Λ, doubling constant) — balls map to sets sandwiched between balls
  of comparable radii, so one obtains weak Poincaré for μ′ and then [HK00]. Elementary.

**Lemma K13 (gluing).** Let μ = w dx on R^n and s₀ > 0. Suppose (G1) μ(B(x,ρ)) ≍ ν(B(x,ρ)) for all x and all ρ ≥ s₀,
where ν is a D+P measure (here: Lebesgue), and (G2) the strong Poincaré inequality holds for μ on all balls of radius
≤ 2s₀ with a uniform constant, and μ is doubling at those scales. Then μ is D+P on all balls.
*Proof.* Doubling: (G2) below s₀, (G1) above. Poincaré on B = B(x₀,ρ), ρ ≥ 2s₀: tile 2B by cubes Q_j of side s₀; let
B_j ⊃ Q_j be the ball of radius s₀ and ū_j the μ-mean on Q_j. For any constant m,
∫_B|u−m|²dμ ≤ 2Σ_j∫_{Q_j}|u−ū_j|²dμ + 2Σ_j μ(Q_j)|ū_j−m|². The first sum is ≤ 2C s₀²Σ_j∫_{B_j}|∇u|²dμ ≤ C′ρ²∫_{2B}|∇u|²dμ
by (G2) and bounded overlap. For the second take m the μ(Q_j)-weighted mean of the ū_j; by (G1) μ(Q_j) ≍ s₀^n, so the
sum is ≍ s₀^n Σ_j|ū_j−m|² ≤ C s₀^n (ρ/s₀)² Σ_{j∼j′}|ū_j−ū_{j′}|² (discrete Poincaré on the cell graph of a digital
ball of radius ρ/s₀, constant ≍ (ρ/s₀)²: elementary, via monotone lattice paths), and for adjacent cells
|ū_j−ū_{j′}|² ≤ 2(μ(Q_j)^{−1}+μ(Q_{j′})^{−1})∫_{B_{jj′}}|u−u_{B_{jj′}}|²dμ ≤ C s₀^{2−n}∫_{B_{jj′}}|∇u|²dμ with
B_{jj′} the ball of radius 2s₀ containing both ((G2)). Summing: ≤ C ρ²∫_{2B}|∇u|²dμ. This is the weak (1-dilation) strong
form; [HK00] removes the dilation. ∎

**Proof of K14 (a).** Fix a shell k and s = s_k. Apply K13 with s₀ = s/8 and ν = Lebesgue.
(G1): every ball of radius ≥ s/8 has μ(B) ≍ |B| — the pattern (lattice of spacing ≍ s, weight (d/s)-profile
W(u) = (u²/(1+u²))^{α/2}) is the same in every shell up to the two parities and the O(1/s) distortion at shell
boundaries, so cell masses are ≍ s³ uniformly (D5: ratios 4–13 at ρ ≥ s/4, Lebesgue 8).
(G2): a ball of radius ρ ≤ s/4 meets at most one circle (two circles are ≥ 0.71 s apart). If it meets none and
dist(B,Γ) ≥ ρ, then w varies on B by a factor ≤ (W(3u)/W(u)) ≤ 9^{α/2}, so μ ≍ Lebesgue on B. Otherwise B ⊂ B(y,3ρ)
with y ∈ Γ on a circle of radius R_c, and it suffices to prove the strong Poincaré inequality for the one-circle weight
w_{R_c}(x) = (1+dist(x,C_{R_c})²)^{α/2} on balls of radius ≤ 3ρ ≤ s (the factor (1+|x|+d²)^{−α/2} varies by ≤ (1+O(1/s))
on such a ball). This is **Lemma L′**: w_R is D+P on R³ with constants independent of R ≥ 0. *Proof of L′.* Scales
ρ ≤ R: bend the cylinder of radius ρ around C_R to a straight one — a bi-Lipschitz map with constant ≤ 1 + ρ/R ≤ 2
that carries dist(·,C_R) to dist(·,line) up to the same factor; the straight weight is [B01] with γ₀ = α (k = 2, n = 3),
strong form by [HK00], transfer by [BL]. Scales ρ ≥ R: rescale x ↦ x/R; the weight becomes (ε²+d_{C₁}²)^{α/2}R^α,
ε = 1/R ≤ 1; on balls of radius ≤ 1 this is the bent-line case again; at scales ≥ 1 within B(c,33) the measure is
Lebesgue-comparable (the ε-tube carries mass ≤ ε² and the rest has weight between c_α and 33^α), so K13 with
s₀ = 1 and ν = Lebesgue gives D+P on balls of radius 1–16 around the circle; beyond 16 R the weight is pointwise
comparable to the point weight (1+|x−c|²)^{α/2} outside B(c,2R) and K13 with s₀ = 8R and ν = that point weight
([B01] with k = n = 3) finishes. E2 is the numerical companion (λ₁ρ² ∈ [0.47, 2.6] for R_c ∈ {1,4,16}, ρ/R_c ∈ {1,…,8}).
∎

**What is proved, what is cited, what is numerical.** Cited: [B01] (read), [HK00] (verify numbers), [BL] (folklore).
Proved here: K12, K13, L′ modulo the citations, (b), (c), K15. Numerical: E1 (the [B01] weight, λ₁R² → 0.770),
E2 (L′), E3 (the lattice on axis-centred balls to 8 s_k; the m ≥ 1 azimuthal modes satisfy Poincaré with constant 1
on axis-centred balls for ANY weight, so E3 is the complete spectral statement for those balls), E4 (the method
detects AR-029's wall). Off-axis balls are covered by the proof (cells) and by D5 (doubling at an off-axis circle
centre and at a bulk point), not by an eigenvalue computation.

## 4. Theorem K15 (the hierarchy under doubling + Poincaré) — and transience of A2's weight

**Theorem K15.** Let W_F = (R^m, δ, f* dx), m ≥ 2, with f* dx doubling and supporting the scale-invariant L² Poincaré
inequality on all balls. Then: (1) W_F is parabolic ⟺ ∫^∞ r dr/μ(B_r) = ∞ ⟺ ∫^∞ dr/(r^{m−1}f̄(r)) = ∞ (Brown 6.4.3 fires);
(2) if Brown 6.4.4 fires then W_F is transient; the converse fails for m = 3: A2's weight is transient with 6.4.4 silent.
Consequently, for doubling + Poincaré weights with bounded drift, δ_F is admissible iff Brown's sphere test fires, and the
volume test adds decidable cases only on the inadmissible side.
*Proof.* First ⟺: Grigor'yan 1999 Thm 11.1 (read: under the relative Faber–Krahn inequality (11.2), (11.1)
∫^∞ r dr/V(x,r) < ∞ is equivalent to non-parabolicity; his remark after the proof: (11.2) ⟺ doubling + the heat-kernel
upper bound (11.4), citing [79, Prop. 5.2], [37, Thm 1.1]) together with the standard fact that doubling + Poincaré give
the two-sided Gaussian heat-kernel bounds (Grigor'yan 1991, Saloff-Coste 1992 — verify), hence (11.4). Second ⟺:
"⇐" is Brown 6.4.3 (needs bounded drift only for the statistical conclusion, not for recurrence; the recurrence half is
Grigor'yan Thm 7.5's sphere test, unconditional). "⇒": with V(r) = μ(B_r), V′(r) = ω_m r^{m−1}f̄(r), Cauchy–Schwarz on
[R,2R] gives ∫_R^{2R}dr/V′ ≥ R²/V(2R), while ∫_R^{2R} r dr/V ≤ 2R²/V(R); summing over R = 2^j, divergence of
∫ r dr/V forces divergence of ∫ dr/V′ (checked numerically for V = r³: the dyadic sums are 0.125 and 0.5). (2): the
first claim is Brown 6.4.4; the witness is Proposition K14. ∎
*Remark.* (1) is three lines once Grigor'yan is in hand; it is the exact form of AR-026 C24 ("the ball-volume test is a
corollary of the sphere test") read in reverse under D+P, and it says why AR-029's wall could not have been a D+P
example: a D+P parabolic weight always trips Brown's sphere test. Wording of record (AR-027 rule): "not found in the
literature we searched"; the combination is elementary.

**Transience and inadmissibility of A2's weight.** By K14 (a) and Lemma K12, f* = φ*w is D+P with bounded drift and
μ_{f*}(B_r) ≍ r³, so ∫ r dr/μ(B_r) < ∞ and W_F is transient by K15 (1); Brown 5.1.1 (A): δ_F is inadmissible. Both of
Brown's tests are silent by K14 (b). This is the statement A2 was asked to deliver.

## 5. Numbers of record (seed 20261024; anaconda python; numpy 2.1.3, scipy 1.15.3)

| check | α = 4 | α = 6 | reading |
|---|---|---|---|
| D1 radial spacing / s_k; angular / s_k; NN / s_k; max dist(shell pt, Γ)/s_k | 1.00 or 0.71; 0.79–2.22; ≥ 0.707; 0.96–1.54 | same (geometry) | lattice, no wall |
| D2 f̄(r) at layer / between / mid-shell, k = 4..11 | 0.0039–0.0176 / 0.033–0.054 / 0.008–0.028 | 0.0004–0.0032 / 0.007–0.013 / 0.001–0.007 | bounded below: 6.4.3 silent |
| D3 min I_k over 802 directions, k = 4..11 | 1.39, 1.10, 1.12, 1.83, 1.79, 1.92, 0.94, 1.91 | 17, 28, 54, 181, 357, 715, 767, 2857 | ≥ 0.28 bound; α = 6 doubles: 6.4.4 silent for every ray |
| D3 I_k(pole), I_k(equator) | 1.85–1.95, 2.80–2.92 | 26→2857, 42→4374 | poles covered by the small circles |
| D4 μ(B_r)/(4πr³/3), r = 2^k, k = 5..11 | 0.064, 0.032, 0.021, 0.028, 0.019, 0.029, 0.019 | 0.037, 0.010, 0.0042, 0.0067, 0.0036, 0.0072, 0.0037 | ≍ r³, period-2 alternation |
| D5 doubling ratio, k = 8, on circle / bulk / axis, ρ = 1, 4, s, 4s, 8s | 31/7.3/6.6; 93/4.8/5.2; 7.2/9.0/12.5; 8.2/8.1/7.9; 9.0/8.9/8.9 | 69/7.0/6.1; 323/4.0/5.4; 7.0/9.3/15.4; 8.3/8.2/7.9; 9.8/9.7/9.7 | bounded; tube-scale values are the co-dim-2 power constants |
| D6 sup \|∇log w\| , k = 6, 8, 10 | 1.985, 1.996, 1.999 | 2.977, 2.994, 2.998 | L = α/2 (Lemma K12) |
| E1 λ₁R² for (1+\|y\|²)^{α/2} on [−R,R]², R = 2..64 (Lebesgue 2.467) | 1.011, 0.831, 0.785, 0.774, 0.771, 0.770 | — | [B01] weight: bounded below |
| E1 same, valley on the edge | 1.754 → 1.716 | — | bounded below |
| E2 λ₁ρ² single circle, R_c ∈ {1,4,16}, ρ/R_c = 1,2,4,8 (m=0; Lebesgue 4.33) | 2.58,1.45,1.67,2.17; 1.09,0.53,1.49,2.15; 0.94,0.47,1.50,2.15 | — | L′: uniform in R_c |
| E3 λ₁ρ² lattice, axis-centred ball at 1.5·2^k, ρ/s_k = 1,2,4,8 (m=0; Lebesgue 4.26–4.33) | k=8: 1.546, 2.686, 2.930, 2.820; k=10: 1.601, 2.712, 3.088, 3.015 (4.1·10⁵ cells, 224 s) | — | bounded below; no large-scale failure |
| E3 h-convergence at ρ = 2s_k, h = 1, ½, ¼ | k=8: 2.6857, 2.6858, 2.6955; k=10: 2.7017, 2.7118 | — | converged |
| E4 wall control (AR-029 ring weight, α = 2), ball at z₀ = 256, ρ = 8, 16, 32, 64 | λ₁ρ² = 0.975, 0.497, 0.256, 0.129; λ₁ρ²·ρ^{α−1} = 7.80, 7.96, 8.20, 8.27 | — | halves per doubling, ∝ ρ^{−(α−1)}: the method sees a wall (AR-029 C5a) |

## 6. What A2 did not do; open items

- **m = 2.** In the plane the co-dimension-two valleys are points; the same counting gives spacing 2^{k/2}, but the ray
  test's threshold becomes α/2 ≥ 1 + (growth exponent needed for transience in two dimensions), and transience needs
  μ(B_r) ≫ r² log r, so the weight must grow. Not attempted; one session if wanted.
- **Non-axisymmetric variants** ("orientations varied" in the spec) were not needed: the axisymmetric lattice already
  has no coherent co-dimension-one structure (D1, E3). Axisymmetry bought the exact 2-D reduction used in E2–E4.
- **A full 3-D off-axis eigenvalue test** (cube of side 4 s_k around an off-axis circle, h = 1, ≈ 2.6·10⁵ unknowns) is
  feasible on the workstation and would close the only numerical gap left by the on-axis reduction; not run.
- **Citations to verify (owner library):** HKM 1993 Cor. 15.35 (opened second-hand only); Hajłasz–Koskela 2000 theorem
  numbers for the two self-improvement steps; Saloff-Coste 1992 / Grigor'yan 1991 for D+P ⇒ Gaussian bounds; Grigor'yan
  2009 for the weighted-manifold form of Thm 11.1; Brown–Hwang 1982 for the comparison paragraph of the note (still not
  obtained — Volume 1 of Purdue III is not on ScienceDirect, AR-029 §5).
- **Theorem-numbering correction:** the volume-test iff is Grigor'yan 1999 **Thm 11.1** in the author's PDF (verified
  today, text extracted); a 2026 arXiv paper cites the same result as "Thm 16.3", which in the PDF is the α-process
  (fractional) analogue — our AR-028/029 citation stands.

## 7. Proposed deltas (QUEUED — parallel-stream rule)

- v2 §0: + K12 (Gaussian-marginal comparison), K13 (gluing), K14 (lattice weight; transient; both tests silent),
  K15 (D+P hierarchy); K10's Theorem 5 (1) now cites Björn 2001 Prop 6 (READ). §8 Q1′: "inclusion fails in m ≥ 3;
  example pending A2" → "A2 DONE: the lattice weight is a D+P transient weight with both Brown tests silent (K14);
  under D+P Brown's sphere test is exhaustive for parabolicity (K15)". §9: "theorem pending A2" → "GO (conditional on
  citation checks, AR-029a §0 item 6)".
- v2 references: + SRC-T58 Björn 2001 (READ), T59 Björn–Buckley–Keith 2005 (READ), T60 Hajłasz–Koskela 2000 (verify),
  T61 Saloff-Coste 1992 (verify), T62 Grigor'yan 1991 (verify), T63 Chanillo–Wheeden (as cited by Björn; verify);
  SRC-T47 Grigor'yan 1999 → Thms 7.3, 7.6, 11.1 READ (text).
- AR-029 §0 item 5 / §7 row A2: PENDING → DONE (GO conditional); open item "Hess log f* ≥ −I" → CLOSED by Lemma K12.
- AR-029 §1 (Lemma K11 application, last sentence): "to be checked in A2" → "resolved by Lemma K12 (AR-029a §2)".
- README (stream file): rows for this packet and the two scripts; status line.
- KB-005 (queued): AR-029a DONE; A3 (rewrite of math-note.tex) is next; B = AR-030, C = AR-031 unchanged.
- KB-003 (queued, at reconciliation): SRC entries above.

## 8. Self-corrections (SC-005)

- None affecting results. Infrastructure: a bash heredoc write of the script failed on an apostrophe in a docstring (file
  written with the editor tool instead); WebFetch cannot read PDFs (binary), so the three sources were saved and their
  text extracted locally with PyMuPDF, run with `python -I` from the scratchpad as untrusted downloads.
- The E3 rows for k = 10, ρ = 8 s_k and the E4 control were pending when this packet was first written and were filled
  in from the run of record the same session (see §5).
