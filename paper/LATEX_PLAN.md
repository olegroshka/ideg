# LaTeX conversion plan (SciPost Physics)

Status: PLAN (2026-08-14). Source of truth for content: `paper/draft.md`
v0.3 + `paper/figures/*.pdf`. Owner gates marked ⛔.

## 1. Template and layout

- **Class:** `SciPost.cls` (fetch the current bundle from
  scipost.org/submissions; verify class date at conversion time — do not
  vendor an old copy from memory).
- Structure map: draft.md §§1–9 → `\section`; appendices A–E →
  `\appendix`; the §2.1 class table → `table` env (booktabs, no vertical
  rules); the Appendix C amendment log → `longtable`/`table*` with a
  `\texttt{}` commit column.
- Figures: `paper/figures/fig{1..6}_*.pdf` via `\includegraphics`
  (vector; fonttype 42 already set). Widths: figs 1, 3, 5, 6 full-width
  (`\textwidth`); figs 2, 4 single-column-ish (`0.7\textwidth` floats).
- Math: draft.md already uses LaTeX math throughout — conversion is
  mostly `pandoc draft.md -o main.tex` + hand-cleanup of tables,
  figure envs, and the abstract block. Budget one pass for
  pandoc-artifacts (smart quotes, unicode arrows → `$\to$`, − → `-`).

## 2. Bibliography (the one hard gate)

⛔ **No reference enters the .bib file until its metadata is verified
against the primary source.** Current state: SRC-043, SRC-044, SRC-049
verified (2026-08-11); **SRC-059..063 are `verify`-flagged** — two have
explicitly unconfirmed author fields (SRC-061, SRC-063). Plan:
1. One verification session (AR-002-series scope): fetch each of
   SRC-059..063 from arXiv/publisher, confirm authors/title/journal/
   year/DOI, update KB-003 flags.
2. Generate `references.bib` from the verified KB-003 entries only;
   citation keys = SRC ids (`\cite{SRC049}`) for traceability, mapped to
   human-readable keys at the end if desired.
3. The draft cites nothing else from memory; any additional
   contextual citations a referee-facing intro wants (ETH, MBL, OTOC
   originals) get new SRC entries through the same verify gate first.

## 3. Statements and metadata

- ⛔ Author line + affiliation + ORCID (owner).
- ⛔ Acknowledgements: wording for AI-assisted research infrastructure
  (owner drafts or approves; SciPost expects transparency).
- Data/code availability: repository public at submission; cite the
  commit hash of the submission tag; the amendment log (App. C) links
  to it. ⛔ Owner flips the repo to public.
- Funding statement (owner).

## 4. Figure captions (to write during conversion)

Each caption carries what the outline assigns it, including the honesty
notes: Fig 2 (representative runs; ensemble verdicts in text), Fig 3
(final n = 40 fresh-seed battery; null lines; W3 panel = the discarded
witness), Fig 4 (the † localized confirmatory point uses the 5-state
realization ensemble; sprint curves are Néel-primary — caption
explains), Fig 5 (paired N = 10/12 dots; 0/80 stress result), Fig 6
(ε_c interpolated at h = 1/2; r2 inset = 2000-period persistence).

## 5. Order of work (estimate: one session + owner passes)

1. SRC-059..063 verification (~30–45 min, web) → KB-003 v0.6.
2. `main.tex` skeleton from template + pandoc body pass (~1 h).
3. Tables, figures, captions, cross-refs (~1 h).
4. `references.bib` from verified entries (~15 min).
5. Compile, proof pass on PDF (line breaks, math, overfull boxes).
6. ⛔ Owner read-through of the compiled PDF → corrections → tag
   `paper-v1` → arXiv + SciPost submission checklist.

## 6. Not in scope of conversion

No content changes ride along with the conversion: any text edit
during LaTeX work happens in draft.md first (single source of truth
until `main.tex` exists, then main.tex takes over and draft.md is
frozen with a pointer note).
