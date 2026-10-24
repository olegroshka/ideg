# Closing note — the admissibility / weighted-geometry stream (PARKED 2026-10-24)

Owner ruling (2026-10-24): "lets park commit and push it.. and do the handover to coig". This note is the PARK step of
the seam programme (AR-029 §7). It says what survived, what did not, what was not tried, and where the material goes.

## What survived (the paper)

`paper/main.tex` (first-principles draft, 15 pp, builds clean) is the external-facing document. Its content:

1. **Theorem A (3.1).** For a doubling + Poincaré marginal, recurrence ⟺ Brown's sphere test ⟺ the ball-volume test.
   Brown's 1971 sphere test is complete for admissibility in that class; geometric criteria can only add decidable
   cases on the inadmissible side. (Grigor'yan 1999 Thm 11.1 + Saloff-Coste 1992 Thms 3.1/4.2 + Cauchy–Schwarz.)
2. **Theorem B (4.1).** The lattice prior on R³ (circles at dyadic scale 2^k, spacing 2^{k/2}, exponent α ≥ 4): doubling
   + Poincaré (Björn 2001 Prop. 6; Hajłasz–Koskela 2000 Thms 5.1 and 9.7; gluing Lemma 4.2; one-circle Lemma 4.3), both
   of Brown's tests silent along every ray, volume ≍ r³, hence transient and δ_F inadmissible.
3. **Two-sidedness (§5).** Coherent circles form a wall: recurrent (flux bound, Lemma 5.1), admissible, Poincaré fails
   ∝ ρ^{α−1}. The log-product prior: transient by product kernels (Kasahara 1975 Thm 2(iii), α = 1), an instance of the
   Johnstone–Lalley phenomenon.
4. **Lemma 2.3.** Lipschitz-log weights are, up to constants, Gaussian marginals with bounded drift.
5. **Remark 2.2.** Brown's Thm 6.4.3 is the sphere-area parabolicity test, thirteen years before Lyons–Sullivan; the two
   literatures do not cite each other in what we read.
6. **Appendix A.** Komaki's shrinkage-prior criterion is the same dichotomy on the Fisher manifold; the risk-reduction
   identity through Perelman's weighted scalar curvature; the scalar curvature has no risk counterpart.

Sources read at theorem level: Brown 1971; Grigor'yan 1999 (Thms 7.3, 7.5, 7.6, 11.1); Johnstone–Lalley 1984; Björn
2001; Björn–Buckley–Keith 2005; Hajłasz–Koskela 2000; Saloff-Coste 1992; Kasahara 1975; Komaki 2006, 2015.

## What did not survive

- The v1 blueprint's physics (horizons, Einstein frame, spacetime, dynamics): killed by lint and sources (AR-024/025).
- The "scalar curvature in the risk" conjecture: refuted by Komaki 2015 Thm A1 (Prop. A.2).
- The doubling/A₂ iff route (AR-028): Lemma K8/K9 make Brown's tests exhaustive for product weights; the volume route is
  not a new criterion there.
- The coherent ring construction as a transient example (Argon's Theorem 6): reversed — it is recurrent (AR-029).
- The v2 note and `math-note.tex` as external documents: superseded (internal lingo); kept as internal records.

## What was not tried

- m = 2 analogue of Theorem B; a characterisation of the undecided zone without doubling + Poincaré; the comparison
  with Brown–Hwang 1982 (Volume 1 not reachable through the OU library; document supply pending).
- Direction B (Gauss-equation reorganisation of Komaki 2015 Thm A1, AR-030) and C (log-concave priors via
  Bakry–Émery comparison, AR-031): optional, not started.
- Lean: nothing formalised. Assessment in `../../ar/AR-029b_A3-paper-2026-10-24.md` §5 and the session log: the
  elementary pieces (Lemma 2.3, Corollary 2.5, Lemma 3.2, inequality (4), the discrete part of Lemma 4.2) are
  formalisable against axiomatised externals; the load-bearing theorems (Brown, Grigor'yan, Björn, Hajłasz–Koskela)
  are not in Mathlib. Lean is not installed on the workstation; a dedicated session (AR-032) is the right unit.

## Open owner items before submission

Checklist in `../../ar/AR-029b_A3-paper-2026-10-24.md` §2: Brown–Hwang Vol. 1; Grigor'yan 1991 / Sturm 1996 (see-also
only); citation-index sweep on Brown 1971 and Johnstone–Lalley 1984 before any novelty wording beyond the present
hedges; name of the second language-model assistant in the acknowledgements; venue and arXiv classes; proof pass on
Lemmas 4.2–4.3 (sketch level).

## Where the material goes

- **ideg:** this folder is the record; nothing here touches the IDEG dynamical programme (no ADR candidates).
- **coig (COIG-2):** handover written to `coig2/sessions/2026-10-24_inbound-handover-from-ideg-theory-stream.md`
  (parabolicity type of the accessible manifold as a candidate invariant with a theorem attached; monotonicity along
  the Blackwell preorder as the KC-201 test; the "admissible" collision rule; prior-art items for AR-201; SRC entries
  for KB-203). KB files there are not edited; deltas are queued per COIG-2's own rules.

Stream status: PARKED. Reopen only for the checklist items, the Lean session, or directions B/C by owner ruling.
