# Session 2026-08-14/15 — External review response + major revision

- target: paper-1 external pre-submission review (owner-relayed) →
  assessment, decisive computation, major revision
- mode: ADVERSARIAL (received) + EXPERIMENT + SYNTHESIZE
- substrate versions at load: KB-003 v0.6, KB-004 v0.7, KB-005 v0.14
- substrate versions at close: KB-003 v0.7, KB-004 v0.8, KB-005 v0.15

## Outcome

1. **Review assessment:** core criticisms ACCEPTED (time-average
   framing mismatch; smooth-f(H) ≠ all stationary states; rename
   switch-off; temper OTOC; DTC-like; stage separation; self-contained
   numerics; p13 float). Gutter-overlap claim NOT reproduced
   (independent rasterization clean; text-extraction artifact of the
   reviewing tool).
2. **AR-020c (decisive computation):** unrestricted diagonal-population
   search, softmax + analytic gradient (entropy derivatives +
   predecessor-tracked shortest-path subgradients; FD-verified
   1.7e-3), 5 starts, full ensembles, both sizes.
   **Single-survivor claim REFUTED**: every class matchable —
   quasiperiodic 12/20 (median 0.241) at N = 10, **20/20 (median
   0.025) at N = 12**; other classes 20/20 at 0.008–0.066.
   Parameter counting (2^N params vs N(N−1)/2 targets) makes
   unrestricted matchability generic with size. Surviving
   class-resolved, size-robust object: the **naturalness gap** —
   smooth-f(H) ensembles match chaotic at ~0.04 while quasiperiodic
   stays unmatched at ~0.32 (0/80). Fifth major self-correction;
   first externally triggered.
3. **Citations verify-gated:** SRC-054 (Yao et al., PRL 118, 030401
   (2017)) verified with Comment/Reply caution retained; SRC-064
   (Hahn/Luitz/Chalker, PRX 14, 031029 (2024)) added + verified.
   KB-003 → v0.7.
4. **Substrate corrections:** KB-004 → v0.8 (survivor claim refuted at
   unrestricted scope; naturalness gap = discriminator; BH-004 status
   unchanged — grounded on (b) + coherence-removal legs). KB-005 →
   v0.15 (§31).
5. **Major revision executed** (main.tex, 15 pp, 0 errors / 0 overfull
   / 0 cite warnings): question-form title ("Does an emergent
   information metric need its dynamics?"); abstract + §1 + §6 + §9
   rewritten to the non-commutation + complexity-split thesis;
   coherence-removal / drive-removal renames throughout (incl. figure
   titles); OTOC reframed as classification-not-failure with SRC-064;
   DTC-like wording with SRC-054; registered/exploratory/pre-committed
   stages table (§4); self-contained numerics (App A: Floquet operator,
   distributions, Lindblad dephasing, optimizer + convergence);
   amendment log extended with review + AR-020c + revision rows;
   Fig 5 rebuilt as three panels (coherence removal | naturalness gap
   smooth-vs-unrestricted | threshold sensitivity); five-corrections
   count throughout; review acknowledged in Acknowledgements;
   p13 isolation resolved. Build fix of note: quantumarticle
   \maketitle rejects \\ in \title ("missing \item") — single-line
   title.

## Delta list

- KB-003 v0.7, KB-004 v0.8, KB-005 v0.15 (as above).
- scripts/ar020c_unrestricted_probe.py + results
  ar020c_unrestricted_N{10,12}.json (committed).
- paper/latex/main.tex (major revision), references.bib (+SRC054,
  SRC064), paper/figures/fig5, fig6 regenerated.
- Nothing marked STALE; AR-009 spec §8 untouched this session (the
  AR-020c correction is recorded in KB-004/KB-005 and the paper's own
  amendment log; spec comparator entries already carry the AR-020b
  dated corrections — a consolidated spec §8 entry can ride with any
  future spec touch).

## ADR candidates raised

None.

## Open items

1. Owner proof pass of the REVISED build (title change flagged
   prominently — owner picked the previous title; the claim it
   asserted no longer survives, hence question form).
2. Then: retag paper-v1, endorsement outreach (candidates parked),
   arXiv + Quantum submission.
3. Open question recorded in the paper §9: a principled
   stationary-state complexity measure for the naturalness gap; its
   large-N fate.
