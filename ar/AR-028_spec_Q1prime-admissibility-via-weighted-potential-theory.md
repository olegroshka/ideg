# AR-028 (spec, PROPOSED) — Q1′: a new admissibility criterion from weighted potential theory?

```yaml
id: AR-028
title: "Can non-radial potential theory on W_F = (R^m, δ, f* dx) decide admissibility of generalized Bayes estimators beyond Brown (1971) §6?"
mode: FORMALIZE (+ VERIFY inputs; + EXPERIMENT numerics)
parent: v2 K4 (THEOREM), AR-026 §5 Q1′, AR-027 wording rule
priority: P2 — owner decision pending (2026-10-23: "ok so what do we need for Q1?")
inputs: [Brown 1971 (read), Grigor'yan 1999 (read: Thm 11.1 + remarks, §14 (D)/(P)), Komaki/Perelman side NOT involved]
question: see T1 / T2 below — the owner must pick one
deliverable: a theorem with a proof that is a chain of cited results, plus one example not decidable by Brown §6, plus numerics
promotion_effect: if T1 or T2 succeeds, the stream has a genuine contribution; v2 §9 upgrades from "note" to "paper"
kill_effect: feasibility gate G0 (below) fails → close Q1′ and the stream
status: G0 EXECUTED 2026-10-23 — verdict NO-GO (see ar/AR-028_G0-2026-10-23.md); T1 adds nothing for product weights (Lemmas K8 + K9; the first record's general claim was unproved and is withdrawn, G0 §6), non-product case open with no candidate; T2's product sub-case is Johnstone–Lalley 1984; stream CLOSED
```

> **Outcome (2026-10-23):** the G0 conjecture is TRUE under a spherical A₂
> condition (Lemma K8, two-line proof via Fubini + Chebyshev + Brown Thms
> 6.4.3/6.4.4), and doubling + Poincaré imply that condition for product weights
> (Lemma K9, added in the same-day correction, G0 §6). T1 therefore adds no
> decidable case for product weights; for non-product weights the conjecture is
> open and no candidate was found. The undecided zone has unbounded spherical A₂
> ratio; its product sub-class is decided by product heat kernels (Johnstone &
> Lalley 1984, prior art); an explicit logarithmic example (not doubling) was
> decided (inadmissible) numerically and heuristically. No further work.

## 0. Two candidate theorems

**T1 — "doubling makes the volume test exact" (packaging theorem, likely true).**
Let δ_F have bounded risk (Brown Thm 3.3.1: sup_{K_F}|∇log f*| < ∞) and let μ = f* dx
satisfy volume doubling and a scale-invariant L² Poincaré inequality on Euclidean
balls — in particular whenever f* is a Muckenhoupt A₂ weight (Fabes–Kenig–
Serapioni 1982 give both properties). Then

  δ_F admissible ⟺ ∫_1^∞ r dr / μ(B(0, r)) = ∞.

Proof chain (all links are published theorems; the chain is what would be new):
(i) Brown Thm 5.1.1 + 4.3.1: admissible ⟺ the Dirichlet form ∫|∇j|² f* dx is
recurrent; (ii) doubling + Poincaré ⟹ parabolic Harnack ⟹ two-sided Gaussian
heat-kernel bounds p_t(x,x) ≍ 1/μ(B(x,√t)) for the weighted operator
(1/f*) div(f*∇·) (Grigor'yan 1991 / Saloff-Coste 1992 on manifolds; Sturm 1996
"Analysis on local Dirichlet spaces III" for strongly local Dirichlet forms);
(iii) with such bounds, transience ⟺ ∫^∞ p_t(x,x) dt < ∞ ⟺ ∫^∞ r dr/μ(B(x,r)) < ∞
(the argument of Grigor'yan 1999 Thm 11.1, which states exactly this under the
relative Faber–Krahn inequality and notes that RFK ⟺ doubling + heat-kernel upper
bound). Sanity: f* ≡ 1 gives Stein's d ≤ 2; f* ~ |x|^{−a} (A₂ iff −m < a < m)
gives admissible iff a ≥ m − 2, Brown's Cor. 6.3.2 boundary; Stein's harmonic
prior (a = m − 2) admissible.

**T2 — Brown's undecided examples (genuinely open, hard).** Brown (p. 900) notes
f* for which neither his recurrence test (6.4.6, spherical average) nor his
transience test (6.4.7, cone of rays) applies: every ray sees f* ≲ r^{2−m} most of
the time while the spherical average is much larger, i.e. a "rotating cap" of large
f* that each ray meets rarely. Such weights have unbounded local contrast, so they
violate doubling: T1's hypotheses exclude them by construction. Deciding them
needs capacity estimates for non-doubling weights (Sturm 1994 "sharp estimates for
capacities", §4 of Grigor'yan's survey, or bespoke test functions) — no standard
toolkit guarantees an answer.

## 1. The feasibility gate G0 (one session, decides go / no-go for T1)

T1 is only worth proving if it decides cases Brown §6 leaves open. Conjecture
(status: unproven, suggested by the examples worked in AR-028 planning): under
volume doubling, the convergence of Brown's ray integrals ∫dr/(r^{m−1} f*(r, φ))
on a positive-measure cone and of his spherical-average integral
∫dr/(r^{m−1} f̄(r)) always agree with the convergence of ∫ r dr/μ(B_r), so that
Theorems 6.4.3 and 6.4.4 together are already exhaustive on doubling weights.
If this conjecture is **true**, T1 is pure repackaging → stop. If **false** (a
doubling, bounded-drift f* exists on which both Brown tests are silent), T1 has
content → proceed. G0 = settle the conjecture, by proof or by an explicit
Gaussian-convolution counterexample f* = φ*F (it must be a genuine marginal with
bounded log-gradient, e.g. F a weighted lattice measure).

## 2. Inputs still needed (access)

- Fabes, Kenig & Serapioni (1982), Comm. PDE 7, 77–116 — A₂ ⟹ doubling + weighted
  Poincaré + Harnack. Paywalled (Taylor & Francis); OU library.
- Sturm (1995, 1996), Analysis on local Dirichlet spaces II (Osaka J. Math. 32,
  275–312) and III (J. Math. Pures Appl. 75, 273–297) — parabolic Harnack for
  strongly local Dirichlet forms. Library.
- Grigor'yan & Saloff-Coste (2005), Ann. Inst. Fourier 55, 825–890 — stability of
  Harnack inequalities. Open access (numdam / AIF).
- Brown & Hwang (1982), Statistical Decision Theory and Related Topics III — the
  standard non-radial sufficient condition; T1 must be compared with it. Library.
- Maruyama & Strawderman (2020–2023) admissibility papers — arXiv.
- All metadata above from memory → VERIFY before use (AR-027 rule).

## 3. Work plan and effort

| step | mode | effort | output |
|---|---|---|---|
| G0 feasibility (§1) | FORMALIZE + numerics | 1 session | conjecture proved (stop) or counterexample (go) |
| inputs verified (§2) | VERIFY | 1 session + library access | exact statements with hypotheses |
| T1 proof as citation chain; hypothesis matching (domains, intrinsic metric = Euclidean for A₂) | FORMALIZE | 1 session | theorem + proof |
| examples + numerics: capacity of the unit ball in W_F computed by solving the weighted Dirichlet problem on annuli (Johnstone's k_n), m = 2, 3 | EXPERIMENT | 1 session | figures, consistency with Brown's radial cases |
| prior-art sweep for T1 (Scholar: admissibility × Harnack / doubling / Muckenhoupt) — spot check 2026-10-23 found nothing | VERIFY | owner, 1 hour | novelty verdict |
| T2 | research | open-ended, months | no guarantee |

## 4. Honest assessment (recorded 2026-10-23)

- T1 is a clean theorem with classical hypotheses, probably true, and probably
  cheap. Its value hinges entirely on G0: if doubling weights are always decided
  by Brown's one-sided tests, T1 adds a nicer statement and nothing decidable.
- T2 is the only route to a result Brown could not have written down, and the
  only one with real risk.
- Neither involves gravity, Komaki, or Perelman: Q1′ is a project in admissibility
  theory, a field with strong active specialists (Maruyama, Strawderman,
  Fourdrinier, the Eaton–Hobert line). The contribution, if any, is the import of
  Harnack/capacity technology they do not currently use (AR-027: no hits).

## 5. Go / no-go

- GO on T1 only after G0 comes back "counterexample exists".
- GO on T2 only as a deliberate research commitment, not as a side stream.
- Otherwise: close Q1′, record the stream as a closed negative (v2 §10 condition 2).
