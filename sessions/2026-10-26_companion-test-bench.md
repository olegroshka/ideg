# Session 2026-10-26 — companion guide: the test bench (paper repository, parallel theory stream)

- target: the companion guide of the spun-out paper (https://github.com/olegroshka/brown-radial-tests,
  `companion/explainer.html`), continuing the 2026-10-25 work recorded in `sessions/2026-10-25_AR-029c-review-round1.md`.
- mode: SYNTHESIZE (exposition), with EXPERIMENT-grade numerics on the paper's own priors.
- outcome: the guide gained Section 15, "The test bench": Brown's sphere test, Brown's ray test and the ball probe run
  step by step on the paper's two priors (scattered circles, Thm B, alpha = 4; wall of circles, Prop 5.2, alpha = 2),
  each drawn in one slice through the symmetry axis with its reading; then the verdicts (volume count licensed by
  Theorem A; flux bound across the walls) and the true resistance for comparison. Scorecard table, a "what the bench
  demonstrates" box, a live bench (sphere / ray / axis-centred ball computed in the browser), and a compact scorecard on
  the front page. Sections 15-31 renumbered to 16-32, cross-references updated, finance references re-id'd.

## Owner message (verbatim)
"Ok i brieflly looked at it, it's better now I think / ok the way u described financial example is useful.. almost
sounds like we found extension to the Etos calculus:) / ..but I still think we need to do better in explaining those
tests and how exactly they apply (illustrations how our space time theory passes them exactly draw some balls etc make
it clear..) thats the base line we basically say these two sent here and here a our test now and thats what it
demonstrates hence the advantage..."

## Numbers (run of record: brown-radial-tests `code/companion_bench.py` -> `code/results/companion_bench.txt`)
- Sphere sum from r = 8: levels off at 0.283 (circles) / 0.122 (wall) by r = 512; min fbar on [16, 512] 0.0042 / 0.0197.
- Ray tolls per shell over 721 directions, k = 4..8: min 0.99-1.39 (circles; paper's 802-direction min 0.94-1.92) /
  0.84-0.94 for k >= 5 (wall).
- V(r)/(4/3 pi r^3): 0.019-0.029 (circles) / ~0.035 (wall).
- Ball probe (axis-centred, m = 0 problem, mesh <= 0.5): circles z0 = 96: 1.53, 2.48, 2.66, 2.28 (rho = 8..64);
  wall z0 = 128: 0.98, 0.50, 0.26, 0.17. Paper Table values reproduced at z0 = 256 (0.975, 0.497, 0.256, 0.129).
- True resistance B_8 -> S_{2^K}, K = 5..10 (polar network, radial step 1, 3216 angles, <= 3.3M nodes; step halving
  changes it < 0.5 %): circles 0.167 -> 0.301 (sphere bound 0.162 -> 0.286, ray bound 0.273 -> 1.390); wall
  0.130 -> 0.836 (+0.14 per shell; sphere 0.056 -> 0.124, ray 0.141 -> 0.985). Order sphere <= true <= ray holds.
- Live-bench JS cores agree with the Python runs (sphere sum to 256: 0.2706 / 0.1173; eigenvalues identical to the
  N0 = 32 Python grid; empty ball 4.262 on that grid).

## Verification
Page checked in a browser in light and dark themes and at 390 px (no horizontal overflow, no MathJax or console
errors); live bench exercised for all three instruments on both priors; artifact (version 5) renders and runs.

## Self-corrections before commit (SC-005)
- Wall ray toll first written as "at least about 0.9"; the 721-direction minimum for k = 5 is 0.84 -> corrected.
- Wall sphere-average floor first written as 0.020; it is 0.0197 -> "0.019".
- A CSS edit "fixing" the table-wrapper selector was itself wrong (the selector was fine); caught by inspection, dropped.

## Answered in chat (not in the guide)
- The Ito remark: no new stochastic calculus. Brown (1971) already ran the diffusion with generator
  Delta + grad log f* . grad; the finance link is an algebraic identity (CE loss = quadratic form); the paper's
  contribution is geometric (Theorem A, the scattered prior), not an extension of Ito calculus.

## Repo state
- brown-radial-tests: commit b32c1ae (guide + `code/companion_bench.py` + run of record + README), pushed.
- claude.ai artifact https://claude.ai/artifact/3VJWxzSeuffYBvXpBNMmAP version 5 (private).

Delta list: none (parallel-stream rule; the guide lives in the paper repository).
Open items: paper title choice (offered earlier, not chosen); factor-subspace corollary still held out (unverified).
