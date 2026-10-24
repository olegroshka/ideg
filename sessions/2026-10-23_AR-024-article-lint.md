# Session 2026-10-23 — AR-024: lint + source verification of the admissible-spacetime blueprint

- target: AR-024 (new; parallel theory stream)
- mode: VERIFY + ADVERSARIAL
- substrate versions at load: KB-001 v0.3, KB-002 v0.2, KB-003 v0.8, KB-004 v0.11, KB-005 v0.18
- substrate versions at close: unchanged (deltas queued, not applied — see rulings)
- infrastructure notes: new folder `articles/theory/checks/` (lint script, results, bibliography report);
  `articles/theory/README.md` (stream index); sympy 1.13.3 via the anaconda interpreter (no project
  venv; `python` on PATH is another project's); Project Euclid returns 403 to all scripted fetches.

## Owner rulings recorded this session

1. Session target = "lint + verify the article first"; Lean/Mathlib setup and a
   prior-art-only search were offered and declined for now.
2. The eleven files with uncommitted "12 → q12" edits belong to another
   session's stream: **leave them**. This stream creates new files only and is
   treated as a **parallel theory project**.
3. The horn visual (pseudosphere / Picard cusp; curved spine, anisotropic
   cross-section) was supplied mid-session as the owner's mental image and
   folded into the lint as check C22 and packet §7.

## Outcome

1. **Equation lint:** 20 machine checks, **6 FAIL** (Weyl-count formula;
   Einstein-frame kinetic coefficient (d−1)/(d−2) → 1/(d−2); "Schwarzschild"
   g_rr; sign of the Φ-dependent risk term vs Komaki eq. (3); Hamiltonian-
   constraint identification; momentum-constraint sign), 11 PASS, 3 INFO.
2. **Kernel confirmed and corrected:** Risk(π_J) − Risk(e^{−Φ}π_J) =
   (R^m_Φ − R)/(2N²) + o(N^{−2}) with R^m Perelman's weighted scalar
   curvature (Komaki 2006 eqs. (4)–(5) + Perelman 2002 Remark 1.3). Komaki's
   §3 conformal metric is exactly the blueprint's Einstein frame. The
   Stein-prior frame is a flat cylinder with the origin at infinity (Komaki
   Ex. 1) — "horizon" claims must name their geometry.
3. **Theorem statements:** Brown (1971) misstated; "Brown–Komaki condition
   = 2ρ_info" invented; Efron–Morris force law invented; the d ≥ 3 ↔ Weyl
   coincidence depends on an unstated one-particle assumption (parameter
   dimension, not spatial dimension, governs Stein's threshold).
4. **Clock/geometry audit:** Lorentzian signature asserted; clock = sample
   count (external, NC-010); four geometries under one name — the horn
   visual exposes both points cleanly.
5. **Bibliography:** 24 records checked by a subagent against publisher /
   Crossref records: 22 VERIFIED, 1 VERIFIED-WITH-CORRECTIONS (Bakry–Émery),
   1 UNVERIFIED (James & Stein 1961 original). Report in
   `articles/theory/checks/biblio_verification_2026-10-23.md`.
6. **Prior art (spot check):** no Komaki–Perelman / Bakry–Émery link and no
   Stein-paradox–gravity proposal found in standard web searches.
7. **Lean:** deferred. Not installed; Mathlib lacks the needed objects; the
   blueprint is not yet a trustworthy statement to formalize.

## Delta list (QUEUED — parallel-stream rule; apply in dependency order at reconciliation)

- KB-002 §collision rules: (none) → rule "name the geometry" (Fisher–Rao /
  weighted+Komaki frame / estimator pullback / location-scale hyperbolic) —
  reason: AR-024 §7, lint C22.
- KB-003 §TH: (none) → TH-039 Komaki–Perelman identity, E3, scope-walled
  (fixed N, no clock, no Lorentzian content) — reason: AR-024 §4 K1.
- KB-003 §SRC: (none) → SRC-T01..T25 per AR-024 §8 (renumber to SRC-069+ at
  reconciliation); SRC-036, SRC-041 metadata → VERIFIED — reason: biblio report.
- KB-004 §2: (none) → HYP-010 candidate "Statistical-admissibility bridge",
  SPECULATIVE, statement = AR-024 §4 K1–K4, falsifier = §6 item 13 —
  reason: AR-024 verdict.
- KB-005 §6: (none) → AR-024 DONE; AR-025/026/027 PROPOSED as in AR-024 §8 —
  reason: this session.
- CLAUDE.md "Current state": + one bullet for the parallel theory stream
  (applied — CLAUDE.md is not among the other session's files).

## ADR candidates raised

None. INT-001 and KB-001 §3–4 untouched; the bridge candidate sits inside
RQ-001 as written.

## Open items

- Primary full texts of Stein (1981) and Brown (1971) (Project Euclid 403
  here); James & Stein (1961) original record.
- E2 lead: identify Komaki's f-independent O(N^{−2}) term (mean mixture
  curvature per Komaki 1996 / Hartigan 1998?) — needed before any "R term"
  reading of K1.
- Systematic prior-art search before novelty language (Choi–Mullhaupt
  Kähler shrinkage priors surfaced; verify).
- Owner decisions pending: (a) register HYP-010 via the main stream or keep
  in-stream; (b) corrected blueprint v2 as a new file (recommended) vs
  editing the input in place; (c) whether a Lean pilot on the C8/C9/K1
  identities is wanted at all.
- The other session's eleven "q12" files remain as found.

## Addendum — AR-025 (same session, later the same day)

- **Owner rulings:** "yes absolutely let's do v2"; "do not take Stein–Einstein
  literally — we connect information-geometry ideas"; the three v1 formalisms are
  LLM-drafted options already explored.
- **Decisive question settled from the source:** Komaki (2015) Thm A1 eq. (29)
  lists the prior-independent O(N^{-2}) terms (Efron curvature, mixture embedding
  curvature, skewness, fourth moment); nonzero at d = 1 where R ≡ 0 ⇒ Perelman's
  R-term has no statistical counterpart; the Komaki–Perelman identity holds for
  the gradient term only.
- **New dictionary entry (machine-checked, C23):** Brown's admissibility integral
  ∫_1^∞ dt/(t^{d/2}m(t)) is the rotationally symmetric recurrence test of the
  weighted manifold (R^d, flat, m dx); m ≡ 1 gives Stein's d ≥ 3. Lint now
  21 checks (6 FAIL on v1 claims, 12 PASS, 3 INFO).
- **Deliverables:** `articles/theory/v2_admissibility_and_weighted_geometry.md`
  (note of record, K1–K6 with status tags, four geometries named, formalisms as
  options, structural "no dynamics" note, open questions Q1–Q5, kill conditions,
  corrections log); `ar/AR-025_blueprint-v2-2026-10-23.md`.
- **Deltas (QUEUED, add to the list above):** KB-004 HYP-010 content := v2 K1–K6;
  KB-003 TH-039 := K1 + K2, SRC-T25..T30 (verify flags per v2); KB-005 AR-025
  DONE, AR-026 (Q1), AR-027 (Q3 prior art), AR-028 (Q4), AR-029 (Q5) PROPOSED.
- **Open:** Brown 1971 and Grigor'yan 1999 full texts (Project Euclid 403 here;
  AMS page not read) — Q1 blocked until obtained; systematic prior-art search
  (Q3) blocks any note.

## Addendum — AR-026 (Q1, same session; owner: "lets do Q1 open the browser")

- **Access:** Grigor'yan 1999 via the author's page and the AMS PDF (curl). Brown
  1971 via the owner's Chrome tab on Project Euclid: a Cloudflare human check
  appeared on the download; the owner clicked it (assistant does not complete
  CAPTCHAs); the Save-As dialog was completed by the owner
  (`Downloads/admissible-estimators-brown.pdf`). JSTOR scan without text layer:
  pages rendered to PNG with PyMuPDF and read as images (the PDF reader tool
  refused the file). Not committed to the repo.
- **Outcome:** Q1 CLOSED NEGATIVE for new criteria. Brown's Thm 4.3.1 = capacity
  characterization of parabolicity of W_F = (R^m, flat, f* dx); Thm 5.1.1 =
  admissible ⟺ recurrent (bounded risk); Thm 6.3.1 = Grigor'yan Prop 3.1; Thm
  6.4.3 = Grigor'yan Thm 7.5 (Brown 1971 precedes Lyons–Sullivan 1984); ball-volume
  test (Thm 7.3) is a corollary of 6.4.3 (lint C24; converse fails). K4 → THEOREM;
  K7 (priority observation) added; Q1′ (Faber–Krahn in Brown's undecided examples)
  opened, research-level. Lint now 22 checks (6 FAIL on v1 claims, 12 PASS, 4 INFO).
- **Deliverables:** `ar/AR-026_Q1-brown-weighted-manifold-2026-10-23.md`; v2 §0 K4/K7,
  §2 table, §8 Q1/Q1′, §9–§10, references T03/T27 updated, T31–T33 added (verify).
- **Deltas (QUEUED, add):** KB-003 SRC-T31..T33 (verify); KB-005 AR-026 DONE, AR-027
  (Q3) scope extended to cross-citation check Brown ↔ weighted-manifold literature,
  AR-028 := Q1′ PROPOSED (P2).
- **Open:** Stein 1981 / Hartigan 1998 / James–Stein 1961 downloads not done (no
  longer load-bearing); browser tab left open pending the owner's call.

## Addendum — AR-027 (Q3, same session; owner: "close the tab, lets do Q3")

- Browser tab closed (group auto-removed). 14 targeted searches (one extended),
  four full texts fetched and grepped (Takanashi–McAlinn 2023; Eaton et al.
  2008; Johnstone 2019; Grigor'yan 1999 reference list).
- **Outcome:** K1, K5, K7 NOT FOUND. K4's analytic content (admissibility ⟺
  recurrence of the Dirichlet form) is KNOWN: Brown 1971; Srinivasan 1981;
  Johnstone 1984/1986 ("Dirichlet principles"); Eaton 1992 → Hobert–Robert 1999 →
  Eaton–Hobert–Jones–Lai 2008; Takanashi–McAlinn 2023. Its geometric translation
  (weighted-manifold parabolicity, sphere-area / volume tests, Lyons–Sullivan)
  NOT FOUND; the two literatures do not cite each other in the sources read.
  Sturm 1994 identified as the citation for Grigor'yan-type volume tests on
  strongly local Dirichlet forms (covers W_F).
- **Wording rule for any note:** "not found in the literature we searched",
  never "new"/"first", until a citation-index sweep (Scholar / MathSciNet) is
  run on Brown 1971 and Komaki 2006 — not possible from this environment.
- **Deliverables:** `ar/AR-027_Q3-prior-art-2026-10-23.md`; v2 prior-art
  annotations on K1/K4/K5/K7, §8 Q3 closed, §9–§10 adjusted, SRC-T34..T44.
- **Deltas (QUEUED, add):** KB-003 SRC-T34..T44 (verify flags per v2); KB-005
  AR-027 DONE; next candidates: AR-028 (Q1′, P2), citation sweep (owner-run,
  needs library access), decision on writing the note.

## Addendum — AR-028 spec + G0 gate (same session; owner: "ok lets go with your recommendation")

- Owner's assessment of record on the note: "no novelty … nothing to contribute".
  Agreed; recorded in v2 §9.
- AR-028 spec written (T1 doubling/A₂ iff-theorem vs T2 Brown's undecided examples;
  gate G0). G0 executed: **Lemma K8** — bounded spherical A₂ ratio ⇒ Brown's Thms
  6.4.3/6.4.4 are exhaustive (Fubini + Chebyshev); hence T1 is repackaging →
  **NO-GO**. Undecided zone ⇔ unbounded spherical A₂ ratio. Explicit example
  (1+|θ₁|)^{−1}log(e+|θ₁|) ⊗ flat on R³: both Brown tests silent; 1-D heat kernel
  p_t(0,0) ≍ 4/log²t (Crank–Nicolson; control (4π)^{−1/2} exact), product Green
  integral converges ⇒ transient ⇒ inadmissible. Prior art: Johnstone & Lalley
  1984 (product diffusions; Brown's immunity question) — the example is an instance.
- Self-correction: a scaling heuristic giving p_t ~ log²t/t was wrong; the numerics
  and the null-recurrent equilibration heuristic agree on 4/log²t. The first Part A
  run had a quadrature artefact (uniform angular grid missing the equatorial peak);
  replaced by exact 1-D cumulative integrals on a log grid.
- Deliverables: `ar/AR-028_spec_…md` (status updated), `ar/AR-028_G0-2026-10-23.md`,
  `articles/theory/checks/g0_feasibility.py` + `g0_results_2026-10-23.txt`, v2 K8 /
  Q1′ closed / §9–§10 / SRC-T45..T47.
- **Stream status: CLOSED as a documented negative.** Deltas (QUEUED): KB-005
  AR-028 DONE NO-GO; no further ARs. Nothing committed; the eleven other-session
  files untouched.

## Self-corrections (SC-005)

- Heredoc length limit hit once (script rewritten via the file tool); two
  empty placeholder shell calls emitted by mistake (no effect); first lint
  run crashed on a Unicode print under cp1252 (script made ASCII-only).

---

## Addendum 6 — LaTeX note of record + G0 correction (same day)

**Owner request:** "draft this note in latex, make it short and make a good
presentation and read"; "use same style ideg is using two columns etc"; "maybe
lets use some visuals like this [horn image] given they are well grounded".

**Done.**
- `articles/theory/latex/note.tex` (+ `references.bib`, `figures/make_figures.py`,
  `figures/fig1_geometries.pdf`, `figures/fig2_undecided.pdf`): the v2 note typeset
  in the paper's class (quantumarticle, two columns, same preamble as
  `paper/latex/main.tex`), with status tags, Lemmas K8–K9 and proofs, dictionary
  table, weights table, and two figures. Builds clean (pdflatex, bibtex, no
  errors, no overfull boxes). Figures: (1) pseudosphere = Fisher–Rao geometry of a
  location–scale family (the owner's horn, grounded version), Komaki's cylinder
  frame of the Stein prior, James–Stein pullback eigenvalues (C12); (2) Brown's
  tests / doubling ratio / spherical A₂ ratio on the undecided example and four
  comparison weights. Palette validated with the dataviz validator; every number
  recomputed from the check scripts.
- **G0 correction (AR-028 G0 §6).** While typesetting, the step "T1's doubling +
  Poincaré class has bounded spherical A₂ ratio" was found to be asserted without
  proof in the first G0 record. Numerical check
  (`checks/g0_doubling_poincare.py`): (1+|t|)² is doubling but not Poincaré and has
  Q ∝ r; (1+|t|)^{−2} is Poincaré but not doubling, Q ∝ r; the §3 example and
  (1+|t|)^{−1} are NOT doubling (ratio ∝ log r). New **Lemma K9**: doubling +
  Poincaré (1-D) ⇒ μ([−r,r])ν([−r,r]) ≤ 32CD³r² (two-region test function); hence
  for product weights w(x₁) on R^m, m ≥ 3, Q is bounded, K8 applies and δ_F is
  inadmissible by Brown 6.4.4 — the volume criterion adds nothing. Non-product
  case OPEN, no candidate. Verdict NO-GO unchanged; the reason corrected.
  Self-correction recorded: a draft of this correction briefly read "GO on T1"
  from a first numerical run whose doubling test had float cancellation; fixed
  and withdrawn within the same hour before anything was written to the records.
- Records amended: AR-028 G0 (status + §1 + new §6), AR-028 spec (status +
  outcome), v2 (header, K8 consequence, new K9, Q1′, §9 pointer, §10, §11 row),
  README (rows + status), CLAUDE.md bullet.

**Deltas (QUEUED, parallel-stream rule unchanged):** KB-005 — AR-028 G0 corrected
same day (K9); typeset note of record exists; nothing else changes.

**Stream status: CLOSED as a documented negative (unchanged).** Nothing committed;
the eleven other-session files untouched.
