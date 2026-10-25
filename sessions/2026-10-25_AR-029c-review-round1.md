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

## Owner requests after the repair (same day)
- Acknowledgements rewritten (owner wording): this note was separated out from a broader information-geometry study
  (admissibility / predictive density / curvature), collected separately as possibly useful to others; the work was a
  collaboration with large language models, Claude (Anthropic) via Claude Code and **Gemini (Google)** — named, the
  owner's collaborator in the neighbouring study, from which the cylinder weight (Thm 3.4) and the coherent-circles
  candidate (§5.1) came; their main help was speed (ideas built/tested/discarded quickly). TODO comment removed.
- Bibliography: the amsplain repeated-author dashes removed by **inlining the bibliography** (`thebibliography`
  pasted into main.tex, the three `\bysame` entries written out as "Alexander Grigor'yan" / "Alexander A. Grigor'yan"
  / "Fumiyasu Komaki"); no more bibtex pass; the whole list now fits on one page. `references.bib` kept for provenance.
- Three illustrations added (TikZ, `\usepackage{tikz}`): Fig. 1 walls vs scattered curves on a ball (co-dimension one
  vs two; Poincaré fails vs holds); Fig. 2 the covering behind Thm 4.1(a) (cells of side ≍√|x|, ≤1 circle each, one
  small ball highlighted); Fig. 3 the 2×2 zone map (doubling × Poincaré) with the three examples and the Theorem A
  cell boxed. Rebuilt clean (17 pp, 0 overfull, no undefined refs); all pages checked visually.

## Citation verification (owner: "let get this papers and verify")
- All three verified against primary sources, open access, no library login: Björn–Buckley–Keith (Maynooth MURAL
  record + AMS DOI; abstract confirms 1-D p-admissible = Muckenhoupt A_p) added as [4] and cited in Lemma 3.3;
  Shimizu–Nakano (arXiv 1705.04408 full text; Theorem 1.3 read) added as [24] and cited in Prop 5.3 with the
  kernel-constant wording fixed (4 full-line / 8 reflected); Takanashi first name corrected Kohei → Kosaku [27].
  Shimizu–Nakano cited as the arXiv preprint (no journal-ref on arXiv; the reviewer's Tsukuba J. Math. details not
  confirmed, not asserted). Rebuilt clean (17 pp, no undefined citations). Detail in AR-029c §10.
- Open question to owner (not acted on): whether to credit a partner library (e.g. Oxford) in the acknowledgements.
  This round needed no library (all open access); the earlier library sources (Hajłasz–Koskela, Saloff-Coste,
  Kasahara) were obtained via the OU library, already credited. Awaiting the exact institution name and confirmation
  before amending, to avoid an inaccurate institutional credit.

## Remaining items closed (owner: "check outstanding review items and close them all")
- R5 Prop 5.2 all-ball doubling: replaced "at the relevant scales" with a full case argument (far / straddle /
  sub-mesh, slab-volume computation, uniform across shell boundaries and near Σ's boundary), doubling constant
  ≤ 2^{α+3}. Rebuilt clean (18 pp).
- Brown–Hwang open question reframed: the lattice prior is inadmissible, so no sufficient admissibility condition
  (Brown–Hwang included) can certify it; only the explanatory "which hypothesis fails" remains.
- Brown 1973 correction: confirmed it exists (sugaku.net catalogue listing) but no full text / exact citation found in
  a quick search; NOT added (no verified metadata). Residual retrieval item for submission.
- Full item-by-item closure table in AR-029c §11. Only two items remain, both needing a physical source and neither a
  defect: the specific failing Brown–Hwang hypothesis (Vol. 1) and the Brown 1973 correction retrieval.

## Source retrieval (owner: "none available through my academic ou student credential?")
- Both residuals are reachable. Brown 1973 correction: open access on Project Euclid (no login needed), Ann. Statist.
  1(3) 594–596, DOI 10.1214/aos/1176342433 — READ: it is about finite-time explosion of the diffusion; bounded drift
  (every prior here) excludes it, so all of Brown (1971) holds as stated. Added to the bibliography and cited, with a
  one-line note after Theorem 2.1. Brown–Hwang 1982 Vol. 1: available via the OU library as the Academic Press ebook
  (ProQuest Ebook Central UKI, EBC1901593, Vol. 1, 551 pp) — not read this turn; the "which hypothesis fails" read is
  unblocked and optional. Detail in AR-029c §12. Rebuilt clean (18 pp, no undefined citations); main.pdf locked by the
  viewer at commit time, source verified via -jobname build, PDF lags one build.

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
