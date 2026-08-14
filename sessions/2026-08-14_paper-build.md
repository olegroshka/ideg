# Session 2026-08-14 — Paper build: figures, source verification, LaTeX

- target: paper production (owner-directed: figures + LaTeX plan, then
  "verify the sources and do the latex conversion")
- mode: SYNTHESIZE + VERIFY
- substrate versions at load: KB-003 v0.5 (rest as at 2026-08-13 close)
- substrate versions at close: KB-003 v0.6 (rest unchanged)

## Outcome

1. **Figures 1–6 generated** (`paper/figures/`, PDF + PNG;
   `scripts/make_figures.py`): validated colorblind-safe palette on the
   print surface; ONE fixed class→color identity across the paper
   (survivor class = accent blue; null = neutral gray); every figure
   eyeballed and iterated (label collisions, axis splits, panel-b
   redesign of fig 6).
2. **SRC-059..063 VERIFIED** against primary listings (paper
   bibliography gate; KB-003 → v0.6): SRC-060 upgraded to its published
   reference (J. Phys. Complex. 2, 035008 (2021)); SRC-061 author and
   SRC-063 full 17-author list confirmed; DOIs recorded. Discipline
   note: SRC-044's full author list was initially typed from memory
   into the .bib — caught and verified against the arXiv listing before
   acceptance (it matched; now it is verified rather than recalled).
3. **LaTeX conversion complete** (`paper/latex/main.tex` +
   `references.bib`): hand-converted from draft.md v0.3 (canonical
   source now main.tex; draft.md frozen). Compiles clean under TeX Live
   2026 (0 errors, 0 unresolved citations, 3 minor overfull boxes);
   14 pages; all 6 figures embedded with full captions incl. the
   honesty notes; amendment log as Appendix C table with commit
   hashes; author block with ORCID 0009-0009-3075-9417. SciPost class
   swap deferred to submission (template endpoint returned invalid
   archive; one-line documented swap in the preamble).

## Delta list

- KB-003: SRC-059..063 entries → verified (dated), SRC-060 published
  ref, author fields filled; registry line; changelog; v0.5 → v0.6.
- paper/figures/* + scripts/make_figures.py (committed earlier today).
- paper/latex/{main.tex, references.bib, main.pdf, .gitignore} (new).
- paper/LATEX_PLAN.md steps 1–5 complete except owner gates.
- No other KB changes.

## ADR candidates raised

None.

## Open items (owner gates to submission)

1. Owner proof pass on `paper/latex/main.pdf`.
2. Acknowledgements text (incl. AI-assistance wording), affiliation
   confirmation, funding statement (TODO markers in main.tex).
3. Repo public + submission tag; expand abbreviated hashes in App. C.
4. SciPost class swap (fetch current template at submission).
5. Carried: SRC-036..041/045..048/050..058 verification backlog
   (NOT paper-blocking — the paper cites only verified sources).
