# `articles/theory/` — parallel theory stream

This folder is a **parallel theory project** inside the IDEG repo, opened
2026-10-23 at owner direction. It is *not* paper-1 content and it does not
touch the quantum-toy-model line (AR-010..AR-023). It follows the same
substrate discipline (CLAUDE.md): nothing exists until recorded; literature
claims are `verify`-flagged until checked against the primary source;
every mathematical statement is machine-checked where that is possible.

> **The external-facing paper now has its own repository:**
> **https://github.com/olegroshka/brown-radial-tests** (canonical public home;
> clean `paper/` + `figures/` + `code/` layout, the repo the paper itself points
> to). The `paper/`, `latex/figures/`, and `checks/` files here are the
> development history and stay with the stream's records; the new repo is the
> version to cite, submit, and point readers to.

## Contents

| File | Role | Status |
|---|---|---|
| `v2_admissibility_and_weighted_geometry.md` | **Note of record.** Claims K1–K6 with status tags (Komaki–Perelman gradient identity with corrected sign; the scalar-curvature term has no statistical counterpart; shrinkage ⇔ non-parabolic Fisher manifold; Brown's integral = weighted-manifold recurrence test; Komaki's conformal frame; parameter dimension), four geometries named, v1 formalisms as explored options, open questions Q1–Q5, kill conditions, corrections log. | DRAFT (AR-025 DONE) |
| `admissible_spacetime_and_statistical_general_relativity.md` | v1: the LLM-drafted blueprint (Stein inadmissibility, Brown recurrence, Komaki shrinkage priors, Perelman F-functional, horizon-as-truncation, ADM analogy). **SUPERSEDED by v2**; kept as the input record. Do not cite. | SUPERSEDED |
| `checks/lint_admissible_spacetime.py` | Equation-by-equation symbolic lint (sympy) + Monte Carlo risk checks (numpy). Re-derives every checkable displayed equation from scratch; curvature tensors are computed from metric components, not quoted. | runs clean |
| `checks/lint_results_2026-10-23.txt` | Output of record for the lint run (22 checks: 6 FAIL on v1 claims, 12 PASS, 4 INFO). | — |
| `checks/biblio_verification_2026-10-23.md` | Field-by-field verification of the blueprint's 24 references against publisher / Crossref / arXiv records (22 verified, 1 with corrections, 1 unverified). | — |
| `../../ar/AR-024_article-lint-2026-10-23.md` | Evidence packet: verdicts, theorem-level verification against primary sources, the surviving kernel stated correctly, errors, adversarial checklist, proposed KB deltas. | DONE |
| `../../ar/AR-025_blueprint-v2-2026-10-23.md` | Packet for v2: resolution of the scalar-curvature question (negative, Komaki 2015 Thm A1), the Brown-integral reformulation, queued KB deltas and follow-on ARs (Q1 theorem hunt, prior-art search). | DONE |
| `../../ar/AR-026_Q1-brown-weighted-manifold-2026-10-23.md` | Q1 packet: Brown 1971 and Grigor'yan 1999 read in full; theorem-by-theorem dictionary (Brown Thm 4.3.1 = capacity, 5.1.1 = admissible ⟺ parabolic, 6.3.1 = model-manifold test, 6.4.3 = sphere-area test predating Lyons–Sullivan 1984); ball-volume test is a corollary (C24); Q1 closed negative, Q1′ opened. | DONE |
| `../../ar/AR-027_Q3-prior-art-2026-10-23.md` | Q3 packet: prior-art map. K1/K5/K7 not found; K4 known in Dirichlet-form language (Brown, Johnstone 1986, Eaton 1992, Takanashi–McAlinn 2023) but not in geometric language; no cross-citation between the literatures; wording rule for any note. | DONE (targeted scope) |
| `../../ar/AR-028_spec_Q1prime-admissibility-via-weighted-potential-theory.md` | Preregistered plan for Q1′ (T1 doubling/A₂ iff-theorem vs T2 Brown's undecided examples) with gate G0. | G0 EXECUTED → NO-GO |
| `../../ar/AR-028_G0-2026-10-23.md` | Gate record: Lemma K8 (spherical A₂ ⇒ Brown's radial tests exhaustive, proof), numerical companion, an explicit undecided example decided by product heat kernels (inadmissible), prior art Johnstone–Lalley 1984. Stream closed. **§6 correction (same day):** the general "T1-class ⊂ bounded-ratio class" step was unproved; Lemma K9 proves it for product weights; non-product case open. Verdict unchanged. | DONE (corrected) |
| `checks/g0_feasibility.py`, `checks/g0_results_2026-10-23.txt` | Sphere/ray/volume integrals for three weights on R³ and the Crank–Nicolson 1-D heat kernel (control exact to 5 digits). | run of record |
| `checks/g0_doubling_poincare.py`, `checks/g0_doubling_poincare_2026-10-23.txt` | Doubling ratios, Muckenhoupt–Hardy bounds on the scale-invariant Poincaré constant, spherical A₂ ratios and the Lemma-K9 quantity for six 1-D weights (local Simpson sums for short intervals; non-doubling control). | run of record |
| `Co-Dimension-2-Extensions.md` | **Argon draft (2026-10-24), INPUT RECORD.** Theorem 5 (co-dimension-two cylinder weight: doubling + Poincaré with unbounded spherical A₂) — VERIFIED numerically (AR-029 C6); Theorem 6 (ring weight "transient by the volume test") — DEAD as written, the weight is parabolic (AR-029 §0–§2); Prop 7 (Krein–Kasahara proof) — plausible, citations to verify; Prop 3 — DIRECTION only. Do not cite. | INPUT (assessed in AR-029 §6) |
| `math-note.tex` | Argon's proposed isolated note (2026-10-24) incorporating the above. **NOT the note of record**: Theorem 6 reversed, Prop 3 to demote, "[NEW IN V2]" tags violate the wording rule. To be rewritten at step A3. | DRAFT (not of record) |
| `checks/a_gate_ring_weight.py`, `checks/a_gate_ring_weight_2026-10-24_a2.txt`, `_a3.txt` | AR-029 gate numerics: mesh of the ring net, Brown-test silence, the Thomson lower bound per block (Lemma K11), the Poincaré quotient across the wall vs the cylinder control, Theorem 5's Q(r). ASCII; anaconda python; seed 20261024. | runs of record |
| `../../ar/AR-029_seam-gate-A-2026-10-24.md` | Seam gate A1: the ring weight is parabolic ⇒ δ_F admissible (Lemma K11, non-radial Thomson bound); Theorem 5 stands and closes AR-028 G0 §6; Johnstone–Lalley 1984 read in full (the G0 example is an instance of their phenomenon, not their construction); Brown–Hwang 1982 not obtained (Volume 1 not on ScienceDirect); programme sequence A2/A3/B/C/park/handover with gates. | GATE DONE; A2 next |
| `checks/a2_scattered_weight.py`, `checks/a2_scattered_weight_2026-10-24_a4.txt`, `_a6.txt` | AR-029a (A2) numerics for the scattered lattice weight: lattice geometry (no wall), sphere means, ray integrals over 802 directions per block (Brown silent both ways), volume growth, doubling ratios, Lipschitz constant of log w. ASCII; anaconda python; seed 20261024. | runs of record |
| `checks/a2_poincare_eigen.py`, `checks/a2_poincare_eigen_2026-10-24_a4.txt` | AR-029a Poincaré tests as weighted Neumann eigenvalue problems (finite volumes + shift-invert Lanczos; Lebesgue controls 2.467 / 4.333): the Björn 2001 local weight, a single circle at all scales, the lattice on axis-centred balls to 8 spacings (λ₁ρ² ≥ 1.5), and Argon's wall as the positive control (collapses ∝ ρ^{−(α−1)}). | run of record |
| `../../ar/AR-029a_A2-scattered-2026-10-24.md` | **A2 packet.** The scattered co-dimension-two lattice weight on R³: doubling + Poincaré (proof architecture: Björn 2001 Prop 6 READ, Hajłasz–Koskela self-improvement, gluing Lemma K13), both Brown tests silent with explicit bounds, μ(B_r) ≍ r³ ⇒ transient (Grigor'yan Thm 11.1 READ) ⇒ δ_F inadmissible; Lemma K12 (Lipschitz-log weights are comparable to genuine Gaussian marginals — closes the Hess log f* item); Theorem K15 (under D+P Brown's sphere test is exhaustive for parabolicity; the ray test is not exhaustive for transience). **GO (conditional on citation checks) for A as a theorem note.** | DONE; A3 next |
| ~~`paper/`~~ **(MOVED)** | **The paper now lives in its own repository, https://github.com/olegroshka/brown-radial-tests** (Theorem A: sphere test complete under D+P; Theorem B: the lattice prior; Section 5: the zone is two-sided; Appendix A: Komaki/Perelman). Review round 1 applied there (`../../ar/AR-029c_review-round1-triage-2026-10-25.md`): correctness fixes, Theorem 4.1 proof repaired, citations verified, eight figures. The local `paper/` copy was removed to avoid duplication; the figures and numerical scripts remain here because the v2 note and the AR gate packets depend on them. | MOVED |
| `checks/a3_offaxis_eigen3d.py`, `checks/a3_offaxis_eigen3d_2026-10-24_a4.txt` | Full 3-D Neumann eigenvalue test on cubes centred on an off-axis circle, in the bulk and on the axis (the case the axisymmetric reduction cannot reach); cube control π²/4 reproduced. | run of record (bulk/axis cubes were still running at the end of the A3 session) |
| `latex/figures/make_figures_v3.py`, `latex/figures/fig3_lattice_vs_wall.{pdf,png}` | Figure 1 of the paper: the lattice vs the wall in the meridian half-plane; Poincaré constants as Neumann eigenvalues (recomputed from the check scripts). | built |
| `../../ar/AR-029b_A3-paper-2026-10-24.md` | A3 packet: the discarded v3 attempt (self-correction), the paper's contribution as stated, the internal pre-submission checklist (citations to open, Brown–Hwang comparison, LLM credit, venue), provenance of every number, the Lean assessment. | DONE |
| `../../ar/AR-029c_review-round1-triage-2026-10-25.md` | **Review round 1 triage.** Independent verification of an external review of the paper: verdict table, the four Theorem 4.1 proof gaps re-derived (blocking; repairable), the Appendix A errors (fixed), missing predecessors (Björn–Buckley–Keith, Shimizu–Nakano; `verify`), two pushbacks on the review, the corrections applied, and the queued work. | DONE (round 1) |
| `finance_applications_note_2026-10-24.md` | **Direction note, speculative.** How the paper's results read for expected-return estimation (whitened sample means; certainty-equivalent loss = quadratic loss; Jorion / Black–Litterman / Pástor–Stambaugh as δ_F), a factor-subspace corollary to verify (polynomial priors around a K-factor subspace: beatable for K ≥ 2 in the D+P range), the Komaki side for density forecasts, caveats, candidate items F1–F5. Finance sources `verify`. | DIRECTION (not of record) |
| `latex/note.tex`, `latex/references.bib`, `latex/figures/make_figures.py` | v2 typeset note (quantumarticle, two columns, status tags). **SUPERSEDED as the external-facing document by `paper/main.tex`** (owner ruling 2026-10-24: internal lingo had leaked to the reader); kept as the internal record of the first pass; `make_figures.py` still produces the paper's Figure 2. | superseded (internal record) |

**Stream status: PARKED 2026-10-24** (owner ruling: "lets park commit and push it.. and do the handover to coig"; closing note `CLOSING_NOTE_2026-10-24.md`; handover written to the coig repo, `coig2/sessions/2026-10-24_inbound-handover-from-ideg-theory-stream.md`). **Seam programme steps A1–A3 DONE. The external-facing document is `paper/main.tex` (first-principles draft, 15 pp, with acknowledgements).** Owner ruling 2026-10-24: directions A → B → C optional → park → COIG-2 handover (`../../ar/AR-029_seam-gate-A-2026-10-24.md` §7). Library session the same evening (AR-029b §2, §9): Hajłasz–Koskela 2000, Saloff-Coste 1992 and Kasahara 1975 verified at theorem level and cited with theorem numbers; Brown–Hwang 1982 title/authorship confirmed, Volume 1 not reachable. Next: the owner's proof pass and the rest of the checklist (Brown–Hwang Vol. 1 via document supply; citation-index sweep; LLM credit; venue); then PARK (closing note) and HANDOVER to coig; B (AR-030) only if still wanted. The v2 note and `math-note.tex` are internal records only. The 2026-10-23 closure stands as the record of what the first pass concluded.

## How to run the lint

```
PYTHONIOENCODING=utf-8 C:\Users\olegr\anaconda3\python.exe checks\lint_admissible_spacetime.py
```

The repo has no `.venv`; the interpreter on `PATH` belongs to another
project and lacks sympy. Any Python with `sympy>=1.13` and `numpy` works.

## Rules for this stream

1. **New files only** in this stream; the canonical substrate files
   (`substrate/KB-00x`) and existing `ar/` packets are owned by the main
   stream. Proposed KB deltas are *queued* in the session logs and in the
   AR packets, not applied here.
2. **Lint before formalize.** No Lean/Mathlib work on a statement until it
   has survived the sympy lint and its sources are verified.
3. **Four geometries, four names.** "Interior geometry" in the blueprint
   silently denotes (i) the Fisher–Rao metric of the model, (ii) the
   weighted manifold (g, e^{-Φ}dV) and its conformal Einstein frame,
   (iii) the Tweedie–Stein pullback J^T Σ^{-1} J, and (iv) the hyperbolic
   location-scale horn. Name which one you mean.
