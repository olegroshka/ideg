# Session 2026-10-24 (second session of the day) — AR-029a: seam programme step A2, the scattered lattice weight

- target: AR-029a (A2 of the programme of record, AR-029 §7): the scattered co-dimension-two construction with its
  preregistered GO/NO-GO rule
- mode: FORMALIZE + EXPERIMENT + VERIFY
- substrate versions at load: KB-001 v0.3, KB-002 v0.2, KB-003 v0.8, KB-004 v0.11, KB-005 v0.18
- substrate versions at close: unchanged (deltas queued — parallel-stream rule)
- infrastructure: anaconda python (numpy 2.1.3, scipy 1.15.3, sympy 1.13.3, PyMuPDF); web search + fetch for three
  sources (PDFs saved by the fetch tool, text extracted locally with `python -I` from the scratchpad); no browser, no
  login, nothing downloaded by hand

## Owner ruling recorded (verbatim)

"Good and interesting results... Thank you. Let's go A2" → A2 executed as specified in AR-029 §7 (construction, three
conditions, kill rule); no scope change.

## Outcome

1. **Construction of record** (AR-029a §1): per dyadic shell k, N_k = 2^{k+2} latitude circles on L_k = 2^{⌈k/2⌉} layers,
   polar angles exhausting the grid π(n+½)/N_k, spacing ≍ s_k = 2^{k/2} in the meridian half-plane; weight
   w = ((1+d²)/(1+|x|+d²))^{α/2}, α ≥ 4. The counting argument (N_k circles of length 2^k in a shell of volume 8^k) forces
   s_k² ≍ 2^k; α = 4 is the threshold at which a bounded miss distance still costs every ray a constant per block.
2. **Verdict: all three conditions hold** — (i) doubling + Poincaré (proof architecture with Björn 2001 Prop 6 as the local
   input, Hajłasz–Koskela self-improvement, an elementary gluing lemma K13 written out, a bending argument for circles
   and a two-regime argument for small circles; eigenvalue numerics E1–E3 with the wall of AR-029 as positive control E4);
   (ii) both Brown tests silent with explicit bounds (every ray pays ≥ 0.28·r^{α/2−2} per block; f̄ ≥ c); (iii) μ(B_r) ≍ r³.
   Hence W_F transient (Grigor'yan 1999 Thm 11.1, read today) and δ_F inadmissible (Brown 5.1.1 (A)).
   **GO for A as a theorem note, conditional on the citation checks listed in AR-029a §0 item 6.**
3. **Lemma K12** (Lipschitz-log weights are comparable to genuine Gaussian marginals with bounded drift) closes the open
   item "Hess log f* ≥ −I" for every example in the stream at once.
4. **Theorem K15** (under doubling + Poincaré: parabolic ⟺ Brown's sphere test ⟺ volume test; the ray test is not
   exhaustive for transience in m ≥ 3). Elementary given Grigor'yan; it explains why AR-029's wall had to fail D+P.
5. **Sources read today (primary text):** Grigor'yan 1999 Thms 7.3, 7.6, 11.1 + remarks (theorem numbering of AR-028/029
   confirmed; a 2026 arXiv paper's "Thm 16.3" is the fractional analogue); Björn 2001 (Ann. Acad. Sci. Fenn. Math. 26,
   175–188) Prop 6 and Lemma 11 — Argon's Theorem 5 (1) now has a published citation; Björn–Buckley–Keith 2005
   (Proc. AMS 134, 703–705) Remark 4 quoting HKM Cor. 15.35.
6. **Numbers of record** in AR-029a §5; scripts and outputs in `articles/theory/checks/a2_*`.

## Delta list (QUEUED — parallel-stream rule; apply at reconciliation in dependency order)

- v2 §0: + K12, K13, K14, K15; K10 (Theorem 5) citation → Björn 2001 Prop 6 (READ) — reason: AR-029a §2–§4.
- v2 §8 Q1′: "example pending A2" → "A2 DONE: D+P transient weight with both Brown tests silent (K14); under D+P the
  sphere test is exhaustive for parabolicity (K15)" — reason: AR-029a §0.
- v2 §9: "theorem pending A2" → "GO conditional on citation checks (AR-029a §0 item 6)".
- v2 references: + SRC-T58 Björn 2001 (READ), T59 Björn–Buckley–Keith 2005 (READ), T60 Hajłasz–Koskela 2000 (verify),
  T61 Saloff-Coste 1992 (verify), T62 Grigor'yan 1991 (verify), T63 Chanillo–Wheeden (verify); SRC-T47 Grigor'yan 1999
  → Thms 7.3/7.6/11.1 READ.
- AR-029 §0 item 5, §7 row A2: PENDING → DONE (pointer added to the AR-029 status line — APPLIED, stream file);
  §1 last sentence ("to be checked in A2") → resolved by K12.
- articles/theory/README.md: two check rows + packet row + status line — APPLIED (stream file).
- CLAUDE.md "Current state": one bullet for AR-029/AR-029a — APPLIED (currency bullet only; no intent wording).
- KB-005 (queued): AR-029a DONE; A3 next; AR-030 (B), AR-031 (C optional), PARK, HANDOVER unchanged.
- KB-003 (queued): SRC entries above.

## ADR candidates raised

None. INT-001 untouched; static information geometry with an external sample clock; no IDEG dynamical claim.

## Open items

- **A3 (next session):** rewrite `math-note.tex` into the honest isolated note: K8–K15, the three decided examples
  (G0 product weight — transient, not doubling; wall — parabolic, not D+P; lattice — transient, D+P), Theorem 5 with the
  Björn citation, Prop 7 only if its Kasahara/Kotani–Watanabe citations are verified, wording rule, no "[NEW]".
- Owner library items: HKM 1993 Cor. 15.35 (first-hand); Hajłasz–Koskela 2000 theorem numbers; Saloff-Coste 1992 /
  Grigor'yan 1991; Grigor'yan 2009 (weighted form of Thm 11.1); Brown & Hwang 1982 (Purdue III Vol. 1); Kasahara 1975,
  Kotani–Watanabe 1982.
- Optional numerics: a full 3-D off-axis Neumann eigenvalue test (≈ 2.6·10⁵ unknowns) to close the on-axis-only gap;
  the m = 2 analogue.
- Nothing committed; the eleven other-session files untouched; Argon's two files remain INPUT / DRAFT not of record.

## Self-corrections (SC-005)

- None affecting results. Two infrastructure detours (bash heredoc vs apostrophe; WebFetch cannot read PDFs — text
  extracted locally) recorded in AR-029a §8. The two E3/E4 cells pending at first write were filled from the run of
  record the same session.
