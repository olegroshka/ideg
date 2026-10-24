# AR-024 — Lint and source verification of the "Admissible Interior Geometry / Statistical GR" blueprint

```yaml
id: AR-024
title: "Which equations and theorem citations of the admissible-spacetime blueprint are correct, which are errors, which are analogies — and what survives as a registrable kernel?"
mode: VERIFY + ADVERSARIAL
parent: RQ-001 (non-metaphorical bridge candidate); placement between HYP-001 and HYP-002 (KB-004 §2); attacks per KB-004 §7
priority: P1 (owner-directed 2026-10-23; opens the parallel theory stream, see articles/theory/README.md)
inputs: [articles/theory/admissible_spacetime_and_statistical_general_relativity.md,
         KB-002 CON-017/CON-018/CON-035, KB-001 NC-010, KB-004 §7,
         KB-003 SRC-036 (Jacobson), SRC-041 (Connes–Rovelli) — cross-referenced, not re-verified here]
question: >
  The blueprint claims that curved Lorentzian geometry is the "unique statistically admissible
  interior state space" of a bounded observer, via Stein (1956) / Brown (1971) / Komaki (2006) /
  Perelman (2002). Equation by equation and citation by citation: what is a theorem, what is an
  error, what is an analogy, and what is the correctly stated kernel?
deliverable: this packet; articles/theory/checks/lint_admissible_spacetime.py (+ lint_results_2026-10-23.txt);
  articles/theory/checks/biblio_verification_2026-10-23.md (24 records); SRC-T01..T24 candidates (§8)
promotion_effect: licenses (i) a HYP candidate "statistical-admissibility bridge" in KB-004 with the
  CORRECTED kernel of §4 and SPECULATIVE status; (ii) new SRC entries in KB-003 (table §8); (iii) a
  KB-002 collision note on "interior geometry" (§7)
kill_effect: none for the programme (the blueprint was never a KB object). Inside the blueprint: Formalism 3
  is killed as a derivation; the "d ≥ 3 coincidence" is killed as stated (§5 E14); the "identical to
  Perelman's F" claim is killed as stated and replaced by §4 K1
status: DONE (2026-10-23; substrate deltas QUEUED, not applied — parallel-stream rule, owner ruling 2026-10-23)
```

## 0. Verdict (summary)

**The blueprint contains one genuine, now source-verified kernel, wrapped in
six machine-detected equation errors, several invented or misattributed
theorem statements, and two analogies presented as derivations.** It is not
ready for formalization (Lean) and must not be cited as-is. The kernel is
worth registering as a hypothesis candidate once restated as in §4.

1. **Kernel confirmed (with a sign correction).** For a prior
   f = e^{-Φ} π_J on a d-dimensional model manifold with Fisher metric g,
   Komaki (2006) eqs. (3)–(5) give the O(N^{-2}) Kullback–Leibler risk
   *reduction* over the Jeffreys prior as
   (1/(2N²))·(2Δ_gΦ − |∇Φ|²_g), and Perelman (2002) Remark 1.3 defines the
   weighted scalar curvature R^m = R + 2Δf − |∇f|². Hence
   **Risk(π_J) − Risk(f) = (R^m_Φ − R)/(2N²) + o(N^{-2})**. The blueprint
   writes this term with the opposite sign (lint C10) and adds an unsourced
   "K_curv ∝ R" baseline. Komaki's Section-3 conformal metric
   g̃ = (h/π_J)^{2/(d−2)} g (d ≥ 3) is literally the blueprint's "Einstein
   frame" (Theorems 4–6), and the Stein-prior case of that metric is the
   flat cylinder S^{d−1} × R (Komaki Example 1) — the "horizon" r = 0 sits
   at infinite g̃-distance. No prior work linking Komaki's functional to
   Perelman's F or Bakry–Émery geometry was found (standard web search;
   not a systematic survey).
2. **Six equation errors** (sympy, from scratch; §2): the Weyl-count
   formula, the Einstein-frame kinetic coefficient, the "Schwarzschild"
   radial metric, the risk-term sign, the Hamiltonian-constraint
   identification, the momentum-constraint sign. Eleven displayed
   equations pass.
3. **Theorem statements**: Brown (1971) is misstated (the quotable theorem
   is an integral transience criterion, not "u = ∇ ln ψ with ψ
   superharmonic"); the "Brown–Komaki admissibility condition
   R + 2ΔΦ − |∇Φ|² = 2ρ_info" appears in neither source; the
   Efron–Morris multi-centre force law is invented. Stein (1956),
   James–Stein (1961), Stein (1981), George–Liang–Xu (2006), Komaki
   (2006), Perelman (2002) are correctly described at the level of what
   they prove, with the sign/attribution caveats in §3.
4. **Headline coincidence does not stand as stated.** Stein's threshold is
   on the number of jointly estimated parameters, not on spatial dimension
   (three particles in one spatial dimension already trigger it; lint A1).
   The d ≥ 3 ↔ Weyl-curvature pairing needs the unstated assumption "one
   particle, position only".
5. **Clock and geometry audit (KB-004 §7 items 2–3):** the Lorentzian
   signature is asserted, not derived; the clock is the observation count
   N (external, NC-010); four distinct geometries are called "the interior
   geometry". The owner's horn visual makes the clock explicit (§7).
6. **Bibliography:** 22/24 records verified against publisher or Crossref
   records; Bakry–Émery verified with orthographic corrections; James &
   Stein (1961) confirmed only via the 1992 Springer reprint record.

## 1. Method and scope

- **Equation lint.** Every displayed equation that is mechanically checkable
  was re-derived in `articles/theory/checks/lint_admissible_spacetime.py`
  (sympy 1.13.3; curvature tensors computed from metric components with a
  convention check on S²; numpy Monte Carlo for risk claims, seed
  20261023, 4·10⁵ samples). Output of record:
  `articles/theory/checks/lint_results_2026-10-23.txt` — **20 checks:
  6 FAIL, 11 PASS, 3 INFO.**
- **Primary sources read in full or in the relevant sections**
  (arXiv text extracted with pypdf): Komaki 2006 (all 12 pp.), George–
  Liang–Xu 2006 (§§1–2), Perelman 2002 (§1 and Remark 1.3), Maruyama &
  Strawderman 2021 (review restating Brown 1971 Thm 3.6.1).
- **Not accessible from this environment:** Project Euclid returned HTTP
  403 to both scripted and server-side fetches, so Stein (1981) and Brown
  (1971) full texts were **not** read; their statements are taken from
  expert restatements (GLX 2006 eqs. (10)–(12); M–S 2021 eqs. (1.2)–(1.4))
  and are flagged accordingly in §3.
- **Metadata verification** (24 records) delegated to a subagent under the
  rule "every field from a fetched record, nothing from memory"; report in
  `articles/theory/checks/biblio_verification_2026-10-23.md`.
- **Prior-art check** (KB-004 §7 item 1): three standard-mode web searches
  (Komaki + Perelman/Ricci/Bakry–Émery; Stein's paradox + gravity;
  superharmonic prior + scalar curvature). Scope caveat as in AR-021 §1:
  this is a spot check, not a systematic survey.
- **Out of scope:** Part V tracks 2–4 (Λ from capacity, quantum Stein,
  Buchert) were classified (§5) but not checked beyond the formulas they
  quote; the Part VI toy model was not run.

## 2. Equation lint (machine-checked)

| id | location in blueprint | claim | result | note |
|---|---|---|---|---|
| C1 | Part II §2.1 | N_Weyl(d) = (d+1)d(d−1)(d−2)/12, N(3) = 10 | **FAIL** | formula gives 2 at d = 3; correct count D(D+1)(D+2)(D−3)/12 with D = d+1 (= 10 at d = 3). Qualitative claim (0 at d = 2, > 0 for d ≥ 3) survives. |
| C5 | Part II §2.2 | E‖X‖² = ‖θ‖² + d | PASS | |
| C6 | Part II §2.2 | dR = dW + (d−1)/(2R) dt | PASS | d = 2..5 |
| C7 | Part II §2.2 | Φ_Green ∝ r^{2−d} harmonic (d ≥ 3), ln r (d = 2) | PASS | |
| C8 | Formalism 1 §1.2 (implicit) | 2ΔΦ − |∇Φ|² = −4Δ√ψ/√ψ, ψ = e^{−Φ} | PASS | the real kernel identity; Komaki's own relation below his Theorem 2 |
| C10 | Formalism 1 §1.2 | Risk = d/2N + (1/2N²)[K_curv + 2ΔΦ − |∇Φ|²] | **FAIL** | Komaki eq. (3) gives the Φ-part as **−**(1/2N²)(2ΔΦ − |∇Φ|²); eq. (3) and eqs. (4)–(5) checked mutually consistent; blueprint = minus Komaki |
| C9 | Formalism 1 §1.3 | ∫(R + 2ΔΦ − |∇Φ|²)e^{−Φ} = ∫(R + |∇Φ|²)e^{−Φ} | PASS | divergence identity verified n = 3, 4; the integrand is Perelman's R^m (Remark 1.3) |
| C2 | Formalism 1 §1.4 | Einstein-frame kinetic coefficient (d−1)/(d−2) | **FAIL** | derived 1/(d−2) (Riemann tensor of e^{2ω}δ computed, ω = −Φ/(d−2), n = 3, 4); exponent −2/(d−2) and "singular at d = 2" correct |
| C11 | Formalism 2 §2.3 | g_int = σ^{-2}[δ − 2σ²∇∇Φ + σ⁴(∇∇Φ)²] | PASS | |
| C12 | Formalism 2 §2.4 | JS-map Jacobian: radial 1 + r_S²/r², tangential 1 − r_S²/r² | PASS | at r = r_S the **tangential** eigenvalue vanishes, radial = 2; Part VI step 4 says the radial one vanishes — internal inconsistency |
| C3 | Formalism 2 §2.4 | g_rr ∝ (1 − r_S/r)^{−1} from Y = (1 − r_S/r)x | **FAIL** | Y_r = r − r_S, dY_r/dr = 1, g_rr = 1/σ² flat; Schwarzschild form asserted |
| C13 | Formalism 3 §3.2 | K_ij = ∇_i∇_jΦ (stationary, N = 1, β = −∇Φ) | PASS | |
| C14 | Formalism 3 §3.2 | ADM R + K² − K_ijK^ij ↔ Komaki R + 2ΔΦ − |∇Φ|² | **FAIL** | Φ = a r²/2 on a flat slice: 6a² vs 6a − a²r²; no identity relates a quadratic-in-Hessian form to a linear-in-ΔΦ one |
| C15 | Formalism 3 §3.2 | ∫(K² − K_ijK^ij) = ∫Ric(∇Φ,∇Φ) | PASS | Bochner/Reilly, verified as a pure divergence in the flat case; correct but does not rescue C14 |
| C16 | Formalism 3 §3.2 | ∇_j(∇^i∇^jΦ − h^{ij}ΔΦ) = **−**R^{ij}∇_jΦ | **FAIL** | sign is **+** in the convention where S² has Ric = +g (checked on S² with generic f) |
| C20 | Formalism 2 §2.2 | Tweedie E[θ|X] = X + Σ∇ln m | PASS | |
| C21 | Formalism 2 §2.2 | Stein's identity | PASS | |
| C4 | Part II §2.1, Part VI | JS dominates MLE for d ≥ 3; JS⁺ dominates JS | INFO | reproduced; R(JS, θ=0) = 2 for all d ≥ 3; d = 1 formula meaningless (E[1/X²] = ∞); per-step gap bounded ≤ d − 2, so "cumulative risk diverges" is strict domination, not instability |
| A1 | Part II headline | threshold is "spatial d ≥ 3" | INFO | three 1-D particles (parameter dim 3): R(JS) = 1.996 < 3 |
| C22 | owner's horn visual | Fisher metric of N(μ,σ²) hyperbolic | INFO | g = diag(1/σ², 2/σ²), K = −1/2; pasted formula omits the 2 (K = −1); location family alone is flat (K = 0) |

## 3. Theorem-level verification against sources

| source | what it actually states (exact location) | blueprint's use | verdict |
|---|---|---|---|
| Komaki 2006, Thm 1 (p. 3–4) | If a Green function exists on (M, g), the prior π_G = G(ξ,·)π_J asymptotically dominates π_J. Proof assumes d ≥ 2. | "Komaki's Riemannian shrinkage theory" | consistent |
| Komaki 2006, eq. (3) (p. 4) | Risk(p_f) = d/2N + (1/2N²)g^{ij}(∂_i log(f/π_J) + ½T_i)(∂_j log(f/π_J) + ½T_j) + (1/N²)∇^e_i{g^{ij}(∂_j log(f/π_J) + ½T_j)} + **terms independent of f** + o(N^{-2}) | risk written with +[2ΔΦ − |∇Φ|²] and K_curv ∝ R | **sign reversed** (C10); the f-independent terms are **not** identified with scalar curvature anywhere in the paper |
| Komaki 2006, eqs. (4)–(5) (p. 4–5) | Risk(π_J) − Risk(f) = (1/2N²)|∇ log(f/π_J)|² − (1/N²)(π_J/f)Δ(f/π_J) + o(N^{-2}); domination if Δ(f/π_J) ≤ 0, ∂ log(f/π_J) ≠ 0 | — | this is the kernel (§4 K1) |
| Komaki 2006, Thm 2 (p. 6) | p_f asymptotically dominates p_{π_J} **iff** (f/π_J)^{1/2} is a nonconstant positive superharmonic function on (M, g); relation ½|∇log ψ|² − Δψ/ψ = −2Δ√ψ/√ψ stated | — | matches C8 |
| Komaki 2006, Thm 3 (p. 6) | complete simply connected (M, g) with negative curvature (d ≥ 3) ⇒ shrinkage priors exist (via Aomoto's Green-function theorem) | not used | relevant: the recurrence/transience theme is Komaki's own (Green function ⇔ non-parabolic ⇔ transient BM) |
| Komaki 2006, §3, Thms 4–6 (p. 7–8) | For d > 2 and a vague prior h: g̃_ij = {h/π_J}^{2/(d−2)} g_ij; domination over h governed by Green function / superharmonicity on (M, g̃) | "conformal transformation to the Einstein frame, requires d ≥ 3, exponent −2/(d−2)" | **verified**: same map with h/π_J = e^{−Φ}. Komaki computes no curvature of g̃ and no action |
| Komaki 2006, Ex. 1 (p. 8–9) | Normal model: Fisher manifold ≅ Euclidean R^d; d ≤ 2 no Green function — "corresponds to the relation discussed by Brown [6] between the recurrence properties of Brownian motion on R^d and the existence of shrinkage estimators"; Green prior = Stein's prior ‖μ‖^{−(d−2)}; GLX exact-domination iff √f superharmonic; conformal image under the Green prior is the cylinder S^{d−1} × R embedded by μ ↦ (μ/‖μ‖, ½ log‖μ‖²); **no Green function on (M, g̃)**, "seems related to the admissibility of the shrinkage predictive distribution" | Brown connection; d ≥ 3 | consistent; the cylinder fact is new to the blueprint and bears on the horizon picture (§4 K3) |
| Komaki 2006, Ex. 2 (p. 9–10) | location-scale model: g = (a/σ²)(dμ² + dσ²) after rescaling μ; H²(−1/a); Jeffreys π_J ∝ 1/σ² left-invariant; right-invariant π_R ∝ 1/σ, π_R/π_J ∝ σ harmonic | — | grounds the owner's horn visual (§7) |
| GLX 2006, eqs. (10)–(12) (p. 3–4) | Brown's representation μ̂_π = x + ∇ log m_π; Stein's unbiased risk reduction U = ‖∇log m‖² − 2∇²m/m = −4∇²√m/√m; ∇²√m ≤ 0 sufficient for minimaxity | "Tweedie's formula (Efron 2011)"; Stein identity | consistent; attribution: the representation is Brown (1971) per GLX, Efron (2011) supplied the name |
| GLX 2006, abstract + §2 | Bayes predictive density minimax if marginal or √marginal superharmonic; p̂_U inadmissible for p ≥ 3 (Komaki 2001); admissible p = 1 (Liang–Barron) | — | consistent |
| Stein 1981 | **full text not accessed** (Project Euclid 403); statement taken from GLX eqs. (11)–(12) and Komaki's citation [26] | "Stein's identity", "superharmonic" | VERIFY-PENDING at the primary level |
| Brown 1971, Thm 3.6.1 as quoted by Maruyama–Strawderman 2021 (p. 1–2) | Π spherically symmetric, m_Π(‖x‖²): if ∫_1^∞ dt /(t^{d/2} m_Π(t)) < ∞ then δ_Π inadmissible; if infinite and sup_μ E‖∇ log m_Π‖² < ∞ then admissible | "Brown's Theorem: δ = X + u admissible iff u = ∇ ln ψ generates a recurrent diffusion, ψ superharmonic (Δψ ≤ 0)" | **misstated**: the superharmonic clause is Stein's sufficient condition, not Brown's criterion; the recurrence language is Brown's framing (title) and the quotable theorem is the integral test. Full text not accessed |
| Perelman 2002, §1.1 (p. 5) | F = ∫(R + |∇f|²)e^{−f}dV; δF at fixed dm = e^{−f}dV has L² gradient −(R_ij + ∇_i∇_jf); gradient flow (g_ij)_t = −2(R_ij + ∇_i∇_jf) is Ricci flow modified by a diffeomorphism | Bakry–Émery flow, "Ric + ∇∇Φ = 0 at the fixed point" | consistent |
| Perelman 2002, Remark 1.3 (p. 6) | R^m_ij = R_ij + ∇_i∇_jf, **R^m = 2Δf − |∇f|² + R**; note g^{ij}R^m_ij = R + Δf ≠ R^m | integrand "R + 2ΔΦ − |∇Φ|²" | the blueprint's integrand **is** Perelman's weighted scalar curvature R^m; F = ∫R^m dm |
| Stein 1956; James–Stein 1961 | risk d − (d−2)² E[1/‖X‖²] < d, admissibility iff d ≤ 2 — standard; metadata verified / reprint-only | Part II §2.1 | consistent (C4) |
| Baranchik 1964; Efron–Morris 1973 | JS⁺ dominates JS (Baranchik); EB interpretation (E–M) — not read, metadata verified | "JS itself inadmissible" | consistent at the level stated |
| Buchert 2000 | Q_D = (2/3)(⟨θ²⟩ − ⟨θ⟩²) − 2⟨σ²⟩ — standard; not re-derived | Part V.4 | formula as commonly quoted; the Stein identification is speculation |

## 4. The surviving kernel, stated correctly (candidate hypothesis content)

**K1 (Komaki–Perelman identity; theorem-level, assembled here from sourced parts).**
Let (M, g) be a d-dimensional regular model manifold with Fisher metric,
π_J the Jeffreys prior, and f = e^{−Φ}π_J a smooth prior. Then, with
R^m_Φ := R + 2Δ_gΦ − |∇Φ|²_g (Perelman's weighted scalar curvature of
(M, g, e^{−Φ}dV)),

  Risk_N(π_J) − Risk_N(f) = (R^m_Φ − R)/(2N²) + o(N^{−2})  [Komaki (4)–(5) + Perelman Rmk 1.3],

and p_f asymptotically dominates p_{π_J} iff e^{−Φ/2} is a nonconstant
positive superharmonic function (Komaki Thm 2), i.e. iff R^m_Φ − R ≥ 0
with strict inequality somewhere. Integrating the risk reduction against
the prior measure dm = e^{−Φ}dV:

  ∫(Risk(π_J) − Risk(f)) dm = (1/2N²) ∫|∇Φ|² dm = (1/2N²)·[F(g, Φ) − ∫R dm].

So Perelman's F equals ∫R dm plus 2N² times the Bayes-integrated
O(N^{−2}) risk reduction of f over Jeffreys. **Not** "the integrated risk
equals F" (sign), and the R term has no statistical counterpart in Komaki
(2006). Clock: none — this is a fixed-N statement.

**K2 (Komaki's conformal frame = the blueprint's Einstein frame; sourced).**
Komaki's g̃ = (h/π_J)^{2/(d−2)} g, d ≥ 3, with h = e^{−Φ}π_J is
g̃ = e^{−2Φ/(d−2)} g. Under it, ∫R^m dm = ∫[R̃ − (1/(d−2))|∇̃Φ|²_g̃] dṼ
(lint C2; coefficient corrected from (d−1)/(d−2)). Komaki uses g̃ only to
state domination over h via superharmonicity on (M, g̃); the curvature
reading is new here and carries no claim beyond the identity.

**K3 (Stein prior geometry; sourced).** For the flat normal model, the
Green prior is Stein's harmonic prior ‖μ‖^{−(d−2)}; its Komaki frame is
the flat cylinder S^{d−1} × R, with r → 0 at infinite g̃-distance, and no
Green function exists on it (Komaki Ex. 1). Any "horizon" statement about
‖X‖² = d − 2 must be made in a named geometry (§7): in the Komaki frame
there is no horizon, the origin is a cusp at infinity; in the Tweedie–Stein
pullback the positive-part boundary degenerates the **angular** metric
only (C12).

**K4 (dimension; sourced).** Transience/recurrence and existence of
shrinkage priors are governed by the dimension of the *jointly estimated
parameter vector* (Komaki Ex. 1 citing Brown; lint A1), not by spatial
dimension.

What would make this a bridge (RQ-001) rather than a dictionary: a
derivation in which (a) the τ-evolution of Φ is Bayesian updating rather
than a postulated Ricci flow, (b) a Lorentzian structure arises from
something other than an asserted sign, and (c) the R term in K1 acquires a
statistical meaning. None of the three exists yet.

## 5. Errors, unsupported steps, misattributions (by location)

- **E1** Part II §2.1 — Weyl-count formula wrong (C1).
- **E2** Formalism 1 §1.2 — sign of the Φ-dependent risk term reversed (C10); "K_curv ∝ scalar curvature R" unsourced. Lead: the f-independent O(N^{−2}) term is tied to the *mean mixture (α = −1) curvature* in Komaki (1996) / Hartigan (1998) as restated in later work (verify), i.e. an embedding-curvature quantity, not the Levi-Civita scalar curvature.
- **E3** Formalism 1 §1.3 — "mathematically identical to Perelman's F": holds for the Φ-dependent part as risk **reduction**; fails as stated (sign and R term). Correct form: §4 K1.
- **E4** Formalism 1 §1.4 — kinetic coefficient (d−1)/(d−2) → 1/(d−2) (C2); otherwise the Einstein-frame step is the standard conformal computation.
- **E5** Formalism 2 §2.4 — "g_rr ∝ (1 − r_S/r)^{−1}" does not follow (C3); the argument silently switches Φ from (M/2) ln r² to −r_S/r mid-paragraph.
- **E6** Formalism 2 §2.4 vs Part VI step 4 — radial vs tangential eigenvalue contradiction (C12).
- **E7** Formalism 3 §3.1 — Lorentzian signature **asserted** ("information gain enters with opposite sign"); clock = update index/observation count, an external clock (NC-010); nothing is derived.
- **E8** Formalism 3 §3.2 — "Brown's (1971) and Komaki's (2006) admissibility condition R + 2ΔΦ − |∇Φ|² = 2ρ_info" appears in neither source; ρ_info undefined.
- **E9** Formalism 3 §3.2 — Hamiltonian-constraint identification is an analogy (C14); the Bochner step (C15) is correct and irrelevant to it.
- **E10** Formalism 3 §3.2 — momentum-constraint sign (C16).
- **E11** Part II §2.2 — Brown's theorem misstated (superharmonic ψ is Stein's sufficient condition; Brown's criterion is the integral/recurrence test; §3).
- **E12** Part V.1 — "Efron–Morris" pairwise force law (d−2)G m_b/‖X_a − X_b‖^{d−1} is invented; empirical-Bayes James–Stein shrinks every X_a toward the grand mean by a common factor set by the total sum of squares.
- **E13** Part VI — "flat observer's cumulative KL risk diverges linearly … dynamically unstable": the per-step gap is bounded (≤ d − 2); the content is strict domination (C4).
- **E14** Part II headline — parameter dimension vs spatial dimension (A1): the "exact dimensional threshold" coincidence requires the unstated assumption of one particle with position-only coordinates.
- **E15** Formalism 2 §2.2 — Tweedie formula attributed to Efron (2011); the representation is Brown's (1971) per GLX eq. (10); Efron supplied the name (minor).
- **E16** Part I table and Abstract — "Statistical General Relativity" is used as if an established field name; it is not (no hits; the four cited pillars are distinct programmes, cf. TH-029/TH-032 scope walls).

Classification of Part V tracks (not checked beyond quoted formulas):
V.1 invented law (E12); V.2 Λ from a capacity constraint — *direction*,
consistent with Perelman's normalized λ/shrinker structure but not derived;
V.3 quantum Stein on Kähler manifolds — speculative, a shrinkage-on-Kähler
literature exists (Choi–Mullhaupt, found in the prior-art search; verify
before citing); V.4 Buchert variance = Stein bias — speculation.

## 6. Adversarial checklist (KB-004 §7)

1. *Known theorem under other notation?* Partly: K1 is Komaki (2006) plus Perelman's Remark 1.3 read together; the union was not found in the literature (spot check). The Einstein-frame step is textbook conformal rescaling. Nothing in the blueprint beyond K1–K3 is a theorem.
2. *Geometry hidden in the information variable?* Yes, three times: Σ^{−1} chosen as the base metric of the pullback; Fisher metric chosen as "spatial metric"; curvature of the prior (Bakry–Émery) and curvature of the model (Fisher) conflated (§7).
3. *Clock hidden in the dynamics?* Yes: τ is the observation count; the Ricci-flow τ of Formalism 1 and the Bayesian-update τ of Formalism 3 are different flows identified by name. The horn visual exposes this (§7). Status under NC-010: external clock, inadmissible for HYP-003-type claims.
4. *Target dynamics hidden in the reconstruction map?* Yes: Einstein-type equations appear only after postulating that the risk functional is to be extremized by Ricci flow at fixed measure (Perelman's theorem supplies the flow once the functional and the variational rule are chosen by hand).
5. *Invariance?* The shrinkage point θ_0 is a choice (the blueprint concedes this in V.1); JS⁺ truncation is coordinate-independent about θ_0 only.
6. *Mixed states / finite N?* Asymptotic in N throughout; Komaki warns (§4, p. 8) that asymptotic domination need not imply finite-sample domination.
7. *AdS-specific?* No.
8. *Conventional explanation?* Entirely: standard decision theory and differential geometry; no new principle enters.
9. *Sustained-by vs compatible-with?* The headline ("gravity is the geometric manifestation of admissibility") asserts identity from a threshold coincidence that does not survive E14.
10. *Coarse-graining creates the arrow?* The only arrow is N increasing.
11. *Recurrence invoked:* OL-level unspecified; the recurrence is of a *fictitious* diffusion in parameter space (Brown's criterion), not of a physical process — collision rule 15–18 territory.
12. *Stationary state unidentifiable?* Not applicable yet (no dynamics derived).
13. *Abandon if:* no formulation exists in which the Φ-flow is derivable from updating rather than postulated (§4 closing paragraph).

## 7. The horn visual (owner's side exchange, 2026-10-23) — assessment

Useful, in a precise way: it is a correct picture of **one** geometry, the
Fisher manifold of the Gaussian location-scale family, which is hyperbolic
(lint C22: g = diag(1/σ², 2/σ²), K = −1/2; Komaki Ex. 2 gives the general
location-scale case H²(−1/a); the pasted line element omits the factor 2).
The pseudosphere/cusp embeds a horocyclic strip of it: thin throat = σ → ∞
(zero precision), flare = high precision, axial coordinate u = −ln σ ∼
½ ln N. Two consequences for this programme:

- **It makes the clock explicit.** The horn's axis is the observation
  count. That is the NC-010 question answered in the open: the blueprint's
  "time" is an external sample clock, not a relational or modular one.
- **It separates the geometries.** The blueprint's Stein setting
  (σ known) lives on the *flat* location family; its curvature is the
  prior's (Bakry–Émery), or the pullback's. The horn's curvature is the
  model's (Fisher). Komaki's cylinder (K3) is a fourth object. The curved
  spine / anisotropic cross-section refinement is a legitimate
  visualization of a non-geodesic reference trajectory and unequal Fisher
  eigenvalues, but its labels ("tidal force", "frame dragging") are
  metaphors with no derivation behind them yet (collision rules 1–4).

Recommendation: keep the horn as the stream's picture of the *location-
scale* Fisher geometry, and require every later statement to name which of
the four geometries it is about.

## 8. Proposed KB deltas (QUEUED — not applied; main stream owns the files)

- **KB-002 §collision rules:** add a rule — "interior geometry / emergent
  metric in statistical-admissibility arguments must name one of: Fisher–
  Rao metric of the model; weighted manifold (g, e^{−Φ}dV) and its Komaki
  conformal frame; estimator-pullback metric; location-scale hyperbolic
  geometry" — reason: §7, lint C22.
- **KB-003 §TH:** new entry TH-039 "Komaki–Perelman identity: shrinkage-
  prior KL risk reduction equals (R^m_Φ − R)/(2N²)" — evidence class E3
  (theorem-level, assembled from sourced parts, machine-checked), sources
  SRC-T04, T06, T11; scope wall: fixed-N, no clock, no Lorentzian content.
- **KB-003 §SRC:** add the verified records below (provisional ids
  SRC-T01..T24 to avoid colliding with the main stream's numbering; map to
  SRC-069+ at reconciliation). Verification status per
  `articles/theory/checks/biblio_verification_2026-10-23.md`:
  T01 Stein 1956 (VERIFIED, Crossref 10.1525/9780520313880-018);
  T02 James & Stein 1961 (**UNVERIFIED** original; reprint 10.1007/978-1-4612-0919-5_30);
  T03 Brown 1971 (VERIFIED, 10.1214/aoms/1177693318; statement via M–S 2021);
  T04 Komaki 2006 (VERIFIED, 10.1214/009053606000000010; read in full);
  T05 Amari & Nagaoka 2000 (VERIFIED, 10.1090/mmono/191);
  T06 Perelman 2002 (VERIFIED, arXiv math/0211159; §1 read);
  T07 Jacobson 1995 = existing SRC-036 (metadata now VERIFIED, 10.1103/PhysRevLett.75.1260);
  T08 Connes & Rovelli 1994 = existing SRC-041 (metadata now VERIFIED, 10.1088/0264-9381/11/12/007);
  T09 Chirco et al. 2014 (VERIFIED, 10.1103/PhysRevD.90.044044);
  T10 Stein 1981 (VERIFIED metadata, 10.1214/aos/1176345632; statement via GLX);
  T11 George, Liang & Xu 2006 (VERIFIED, 10.1214/009053606000000155; §§1–2 read);
  T12 Baranchik 1964 (VERIFIED, Stanford TR "CHE ONR 51", PURL hq883mw7116);
  T13 Efron & Morris 1973 (VERIFIED, 10.1080/01621459.1973.10481350);
  T14 Efron 2011 (VERIFIED, 10.1198/jasa.2011.tm11181);
  T15 Komaki 1996 (VERIFIED, 10.1093/biomet/83.2.299);
  T16 Liang & Barron 2004 (VERIFIED, 10.1109/tit.2004.836922);
  T17 Buchert 2000 (VERIFIED, 10.1023/A:1001800617177);
  T18 Bakry & Émery 1985 (VERIFIED-WITH-CORRECTIONS: "Émery", "Séminaire de probabilités XIX", 10.1007/BFb0075847);
  T19 Hartigan 1998 (VERIFIED, 10.1214/aos/1024691462);
  T20 Padmanabhan 2010 = SRC-037 lineage (VERIFIED, 10.1088/0034-4885/73/4/046901);
  T21 Verlinde 2011 = SRC-038 lineage (VERIFIED, 10.1007/JHEP04(2011)029);
  T22 Hu & Verdaguer 2008 (VERIFIED, 10.12942/lrr-2008-3);
  T23 Caticha 2015 (VERIFIED, 10.3390/e17096110);
  T24 Ruppeiner 1995 (VERIFIED, 10.1103/RevModPhys.67.605; erratum RMP 68, 313);
  plus T25 Maruyama & Strawderman 2021, arXiv:2110.01945 (read; metadata from arXiv header only — verify).
- **KB-004 §2:** new HYP-010 candidate "Statistical-admissibility bridge"
  — statement = §4 K1–K4 with the §4 closing requirements as promotion
  conditions; epistemic status SPECULATIVE; clock: none at K1 level,
  external (sample count) in every dynamical extension so far; falsifier:
  §6 item 13.
- **KB-005 §6:** register AR-024 DONE; propose AR-025 "corrected blueprint
  v2 (new file) + HYP-010 registration packet" (P1), AR-026 "Part VI toy
  model with corrected expectations: bounded gap, angular degeneration,
  named geometry" (P2), AR-027 "Lean pilot on the C8/C9/K1 identities"
  (P3, only after AR-025).
- **KB-001:** no change; INT-001 untouched. No ADR candidate: the bridge
  candidate sits inside RQ-001 as written.

## 9. Open items

- Primary full texts of Stein (1981) and Brown (1971): obtain via a browser
  session or library access; until then §3 marks them VERIFY-PENDING at the
  statement level.
- James & Stein (1961) original record: Project Euclid blocked; verify from
  the Berkeley Symposium volume.
- E2 lead: confirm from Komaki (1996) / Hartigan (1998) what the
  f-independent O(N^{−2}) term is (mean mixture curvature?) and whether any
  Levi-Civita curvature appears.
- Prior-art: systematic search (not a spot check) for "superharmonic prior"
  × "Bakry–Émery / Perelman / weighted scalar curvature" and for Kähler
  shrinkage priors (Choi–Mullhaupt) before any novelty language.
- The owner's question "can we set up and search through Lean proofs":
  deferred by ruling; environment has no elan/Lean/Mathlib; Mathlib lacks
  Stein/Brown/Komaki/Perelman objects, so a pilot would formalize C8/C9
  class identities only.

### Addendum 2026-10-23 (AR-025)

- Open item "E2 lead" **resolved negatively**: Komaki (2015) Thm A1 eq. (29)
  gives the prior-independent O(N^{−2}) terms explicitly (Efron curvature,
  mixture embedding curvature, skewness, fourth moment); they are nonzero at
  d = 1 where R ≡ 0. See `articles/theory/v2_admissibility_and_weighted_geometry.md` §3.
- Lint extended to 21 checks with C23 (Brown's integral = weighted-manifold
  recurrence test; m ≡ 1 reproduces d ≥ 3). Counts in §1–§2 above refer to the
  20-check run; the file of record now holds 21.
- §8 HYP-010 wording superseded by v2 §0 K1–K6 (AR-025 §3).

## 10. Ops notes and self-corrections (SC-005)

- The shell tool truncates very long heredocs (the first attempt to write
  the 250-line lint script died with "unexpected EOF"); scripts of that
  size are written with the file tool.
- Two empty placeholder shell calls were emitted by mistake while
  assembling a path; no effect on any file.
- `python` on PATH is another project's venv; sympy came from the anaconda
  interpreter (recorded in memory). Console is cp1252: a Unicode print
  crashed the first lint run; the script is now ASCII-only and run with
  PYTHONIOENCODING=utf-8.
- No canonical substrate file, no existing `ar/` packet, and none of the
  eleven files modified by the other session were touched.
