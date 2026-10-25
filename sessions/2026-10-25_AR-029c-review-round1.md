# Session 2026-10-25 — AR-029c: review round 1 on the paper

- target: `articles/theory/paper/main.tex` ("Beyond Brown's radial tests").
- mode: ADVERSARIAL (external review received, independently verified, corrections applied / queued).
- outcome: the review is competent and substantially correct; I re-derived the load-bearing claims. One result
  (Theorem 4.1, the scattered-circle D+P prior — the paper's strongest contribution) is **not established as
  written**: four steps of its D+P proof are false or unjustified. The construction looks repairable and the tools are
  mostly present. Separately, a batch of definite statement-level errors were fixed, and three missing predecessors
  were identified. Full triage with my independent proof checks: `ar/AR-029c_review-round1-triage-2026-10-25.md`.

## Owner message (verbatim)
- "ok now lets go into the first review cycle" + the external review text (table + long form).
- mid-turn: "this is jsut a review on the nete we drafted waht is the probelem?" — answered: no problem, this is normal
  peer review of our own draft; a spurious safety flag had briefly interrupted the previous turn.

## Fixed this round (main.tex; rebuilt clean, 16 pp, 0 overfull boxes)
Abstract "supported near"→"small along"; Thm 2.1(c) bounded-drift qualifier restored; Remark 2.2 priority qualified
(Ahlfors–Nevanlinna predate the surface case); eq. (4) constant made α-dependent (2.62^{-α/2}, ≥0.14 at α=4) with the
Section 6 cross-reference updated; Prop 5.2 "unit tube"→"tube of bounded radius" and the false "touches Σ_{k+1}"
replaced (antipodal poles, not a shared point); Appendix A.1 strictness corrected (superharmonic **not harmonic**; the
half-space harmonic counterexample); A.2 integrability caveat added; "flat cylinder"→"round cylinder, scalar curvature
(d-1)(d-2), parabolic despite positive curvature"; appendix "separate volume/sphere" sentence corrected (both
integrals converge; the volume criterion decides under D+P); the exhaustion open question reworded (Grigor'yan Thm 7.6
answers the existence form via the conformal metric w^{2/(m-2)}δ; the explicit exhaustion is the open part); "forced"
restricted to the ansatz. No proof logic altered; no unverified mathematics added.

## Not done — queued (delta list)
- **Theorem 4.1 proof repair** (the real work): consistent (1+d²)^{α/2}/s^α comparison; bounded-factor (not 1+O(1/s))
  estimates; explicit polar-region covering via the uniform Lemma 4.3; a tube-volume covering lemma; the Lemma 4.3
  Fermi-chart fix (ρ≤R/6 + intermediate scale). Owner to direct approach.
- Bibliography additions, all `verify` at the primary source before committing (no invented metadata):
  Björn–Buckley–Keith 2005/2006 (Lemma 3.3 predecessor); Shimizu–Nakano 2017 (Prop 5.3 kernel); Grigor'yan
  *Heat kernels on weighted manifolds* Cor. 9.9; ref [25] first name (Kosaku vs Kohei) Takanashi.
- Prop 5.3 normalization note (full-line constant 4 vs reflected 8; transience unaffected).
- Prop 5.2 all-ball doubling (sub-mesh / polar / cross-shell cases).
- Brown–Hwang comparison still needs Volume 1 (document supply).
- Consult Brown's 1973 correction when finalizing Brown citations.

## Pushback on the review (recorded)
- Axisymmetric-modes criticism: for axis-centred balls the m≥1 modes are handled analytically (Poincaré constant 1);
  off-axis checks are full 3-D. The valid residual (finitely many balls ≠ uniform constants) is already conceded.
- eq. (4) "0.28" was contained to α=4 in the prose; now explicitly α-dependent.

## Repo state
- Round-1 corrections pushed as 1bba954.
- **Theorem 4.1 repair drafted** (owner: "please go ahead"): proof of Lemma 4.3 (Fermi-chart fix, ρ≤R/6 branch) and
  proof of Theorem 4.1(a) rewritten (correct bounded-factor comparison eq. (5); tube-volume cell mass eq. (6); polar
  circles via the uniform Lemma 4.3; large balls via gluing with σ/32 cells so enlargements are small balls). All four
  R4 gaps addressed. Scratch build clean (16 pp, 0 overfull, no undefined refs). Confidence and residual referee items
  recorded in AR-029c §9 (honest: drafted revision, not refereed). `main.pdf` NOT regenerated — file locked by an open
  viewer; the committed PDF lags the source by one build until the viewer is closed and I rebuild it.
