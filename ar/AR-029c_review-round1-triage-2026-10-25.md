# AR-029c — Review round 1: triage and response (2026-10-25)

- target: the paper `articles/theory/paper/main.tex` ("Beyond Brown's radial tests", draft 24 Oct 2026).
- mode: ADVERSARIAL (external review received; independently verified; corrections applied / queued).
- provenance of the review: an owner-commissioned external review (multi-source literature + proof check), delivered
  2026-10-25, text in the owner's message; a copy of the reviewer's long form was referenced at
  `C:/Users/olegr/Documents/Codex/2026-10-24/.../novelty-and-proof-review.md`. **This is an external review**, not an
  internal owner-run audit, so the no-fictional-review-history memory does not forbid recording it here; but per that
  memory the *paper itself* still carries no review-history framing.
- what this packet is: my independent check of every finding (I re-derived the load-bearing ones), a severity triage,
  the list of corrections applied this round, and the work that remains. The reviewer's claims were not taken on faith.

## 0. Verdict

The review is competent and substantially correct. I verified its key mathematical claims.

- **One result is not established as written:** Theorem 4.1 (the scattered-circle doubling+Poincaré prior), the
  paper's strongest contribution. Four steps of its D+P proof have false or unjustified estimates. The construction
  looks repairable and the needed tools are mostly present, but the current proof is a sketch in the load-bearing places.
- **Several definite errors** in statements (Appendix A strictness and "flat cylinder", Theorem 2.1(c) hypotheses,
  the "separates volume/sphere" phrasing, Prop 5.2 geometry, eq. (4) constant) — all fixed this round.
- **Missing predecessors** narrow the novelty: Björn–Buckley–Keith (one-dimensional A_p, for Lemma 3.3),
  Shimizu–Nakano 2017 (the log-product kernel, for Prop 5.3), and the observation that Grigor'yan Thm 7.6 already
  answers the existence form of the exhaustion question. These are scholarly, not fatal.
- **Two places where the review slightly overreaches**, noted below (the axisymmetric-modes criticism; the eq. (4)
  constant was contained to α=4 in the prose).

The paper's own framing already matches much of this (Theorem A is presented as a corollary; novelty is stated only as
"not found in the literature we searched", AR-027). Nothing here reverses a result; the headline theorem needs a
complete proof.

## 1. Triage table

| # | Finding | My verdict | Severity | Disposition |
|---|---|---|---|---|
| R1 | Thm 3.1 (sphere complete under D+P) is a corollary of Saloff-Coste/Grigor'yan + a dyadic Cauchy–Schwarz | CONFIRMED (paper already frames it so) | low | keep as corollary; wording already modest |
| R2 | Lemma 3.3 (1-D D+P ⇒ A₂) is a special case of Björn–Buckley–Keith; cite directly | CONFIRMED | medium (priority) | **cite** (verify metadata); soften novelty |
| R3 | Thm 3.4 cylinder weight = Björn 2001 Prop 6 + elementary calc | CONFIRMED (paper attributes it) | low | no change |
| R4 | **Thm 4.1 D+P proof incomplete** (four gaps, below) | CONFIRMED | **blocking** | **repair drafted** (§9); residual referee items listed |
| R5 | Prop 5.2 (coherent circles) mechanism standard; geometry/doubling need detail | CONFIRMED | medium | geometry errors fixed; all-ball doubling still a sketch |
| R6 | Prop 5.3 (log product): add Shimizu–Nakano 2017; constant 4 vs 8 normalization | CONFIRMED (does not affect transience) | medium | **cite** (verify); normalization note queued |
| R7 | Appendix A: strictness equivalence false; "flat cylinder" wrong; integrated-asymptotic caveat | CONFIRMED | medium (correctness) | **fixed this round** |
| R8 | Thm 2.1(c) drops Brown's bounded-drift qualifier | CONFIRMED | medium (correctness) | **fixed this round** |
| R9 | Exhaustion open question already answered in existence form by Grigor'yan Thm 7.6 (+ conformal reduction) | CONFIRMED | medium | **fixed** (reworded to ask for explicit exhaustion) |
| R10 | Remark 2.2 priority too strong (Ahlfors–Nevanlinna predate the surface case) | CONFIRMED | low | **fixed** (qualified) |
| R11 | eq. (4) constant 0.28 not uniform in α | CONFIRMED (but prose already said "for α=4") | low | **fixed** (α-dependent 2.62^{-α/2}) |
| R12 | Abstract "supported near" reverses the geometry | CONFIRMED | low | **fixed** ("small along") |
| R13 | "forced" arithmetic is forced within the ansatz only | CONFIRMED | low | **fixed** ("within this ansatz") |
| R14 | Ref [25] first name "Kohei" should be "Kosaku" Takanashi | PLAUSIBLE | low | **verify** against arXiv:2310.17891 |
| R15 | Numerics use axisymmetric modes (a subspace) | PARTIAL / PUSHBACK | low | see §4; m≥1 modes are handled analytically for axis-centred balls |

## 2. Theorem 4.1: the four proof gaps, checked independently

The weight is \(w=((1+d^2)/(1+|x|+d^2))^{\alpha/2}\), \(d=\dist(x,\Gamma)\). With \(s^2=1+|x|\), \(u=d/s\):

  w = ((s^{-2} + u^2)/(1+u^2))^{α/2}.   [I re-derived this; it matches the reviewer.]

**(i) Profile approximation (p. 9) is false, as written.** The covering sub-argument compares \(w\) multiplicatively to
\(W(u)=(u^2/(1+u^2))^{\alpha/2}\). On a circle \(u=0\): \(w=s^{-\alpha}>0\) but \(W(0)=0\); and \(w/W=(1+1/d^2)^{\alpha/2}\)
blows up for \(d<1\). So \(w\asymp W(u)\) fails in the tube \(d<1\). **However** the paper states the correct comparison
two paragraphs earlier: \(w\asymp(1+d^2)^{\alpha/2}/s^\alpha\) (valid for all \(d\le s/2\): \(\asymp s^{-\alpha}\) for
\(d\le1\), \(\asymp(d/s)^\alpha\) for \(1\le d\le s\)). The fix is to run the covering with that comparison, not \(W\).
With it, the cell-mass estimate \(\mu(Q_j)\asymp|Q_j|\) survives (most of a side-\(s/8\) cube has \(d\asymp s/8\), where
\(w\asymp8^{-\alpha}\asymp1\); the tube \(d<1\) is a fraction \(\lesssim s^{-2}\) of the cube). So: real exposition
error, internally inconsistent with the paper's own statement, fix available, conclusion appears to survive.

**(ii) Denominator scale (p. 8) is wrong.** The text claims the second factor varies by \(1+O(1/s_k)\) using
"\(1+|x|\ge4^k\)". But \(1+|x|\asymp2^k=s_k^2\) in shell \(k\), and \(d^2\) varies by \(O(s_k^2)=O(2^k)\) across a
ball of radius \(s_k\), not \(O(s_k)\). So \(1+|x|+d^2\) varies by a **bounded factor** (between \(\asymp2^k\) and
\(\asymp2\cdot2^k\)), not \(1+O(1/s_k)\). A bounded-factor comparison is enough for D+P (constants degrade by a bounded
amount), so the conclusion survives, but the written tightness is wrong. Fix: replace "\(1+O(1/s_k)\)" by "\(\asymp\)".

**(iii) Polar circles (most serious).** Shell radius \(R=2^k\); the pole-most circle has polar angle
\(\theta_0=\pi/(2N_k)=\pi/2^{k+3}\) and Euclidean (axis-)radius \(R\sin\theta_0\to\pi/8\). So some circles have radius
\(O(1)\), not \(\asymp R\); near the axis many small circles cluster and the "\(\sqrt R\)-spaced cylinders" picture
fails. Lemma 4.3 **is** stated uniformly in \(R\) and has a small-\(R\) branch, so the tool exists, but the proof of
4.1(a) does not deploy it in the polar region; that region needs its own covering. This is genuine additional work,
not a one-line fix.

**(iv) Covering / nearest-circle (p. 8–9).** The dichotomy "a cube meets a circle, or is uniformly far from it" is
false: a cube can approach a tube arbitrarily closely without meeting it, so "\(u\ge u_0>0\) on it" does not follow.
Fix: a tube-volume bound (the fraction of any cube within \(\varepsilon s\) of \(\Gamma\) is \(\lesssim\varepsilon^2\))
replaces the dichotomy and still gives \(\mu(Q)\asymp|Q|\). Also "a ball meeting ≤1 circle stays so after enlargement"
needs care. Repairable, standard.

**Lemma 4.3 chart gap.** From \(\rho\le R/2\) and \(\dist(x_0,C_R)\le2\rho\) one gets \(\dist(x,C_R)\le3\rho\le3R/2\) on
\(B\), which exceeds the \(|\nu|<R/2\) Fermi-tube where the straight-cylinder chart is valid. A smaller local regime
(say \(\rho\le R/6\)) plus a separate intermediate-scale step is needed. Also the Fermi chart along a closed circle is
periodic and is not one global straight-line chart. Repairable; the large-scale branch (comparison to the
centre weight \(p_c\)) is unaffected.

**Net on 4.1:** the construction is plausibly correct; the proof as written does not establish it. A convincing
revision needs (a) the \((1+d^2)^{\alpha/2}/s^\alpha\) comparison used consistently, (b) bounded-factor (not
\(1+O(1/s)\)) estimates, (c) an explicit polar-region covering using the uniform Lemma 4.3, (d) a tube-volume covering
lemma, and (e) the Lemma 4.3 chart fix. Numerics (Section 6) check uniformity on finitely many balls but cannot
replace these estimates — the paper already says as much.

## 3. Appendix A errors (all fixed this round)

- **Strictness (Prop A.1).** "nonconstant positive superharmonic ⟺ strict inequality somewhere" is false: a nonconstant
  positive *harmonic* \(u\) (e.g. \(u=\theta_1\), \(\Phi=-2\log\theta_1\) on the half-space \(\theta_1>0\), a restricted
  normal-location Fisher manifold) has \(\Delta u=0\), so \(R^m_\Phi\equiv R\) and the \(O(N^{-2})\) coefficient
  vanishes. Correct statement: dominates at this order iff \(u\) is superharmonic and **not harmonic**
  (\(-\Delta u\ge0\), \(>0\) somewhere). Fixed.
- **"Flat cylinder".** Stein's conformal metric is the round cylinder \(S^{d-1}\times\R\), scalar curvature
  \((d-1)(d-2)>0\) for \(d\ge3\), not flat. Fixed (now "round cylinder, of scalar curvature \((d-1)(d-2)\), parabolic
  despite that positive curvature"). The cylinder observation itself is Komaki's Example 1.
- **Integrated asymptotic (Prop A.2 / eq. 8).** A vanishing boundary term does not license integrating the pointwise
  \(o(N^{-2})\) remainder against \(e^{-\Phi}\dd V\) for improper \(\Phi\); a dominated/uniformly-integrable remainder
  is also needed. Fixed (sentence added restricting it to an identity of leading coefficients).
- Independent check supporting Prop A.2's conclusion: for \(N(\theta,1)\), the Jeffreys predictive is
  \(N(\bar x,1+1/N)\) and its exact expected KL risk is \(\tfrac12\log(1+1/N)=\tfrac1{2N}-\tfrac1{4N^2}+\dots\), while
  the 1-D Fisher scalar curvature is 0. So the \(O(N^{-2})\) term is not proportional to \(R\). (I verified this.)

## 4. Where I push back on the review

- **R15 (axisymmetric modes).** For balls centred on the axis, the paper handles the azimuthal \(m\ge1\) modes
  *analytically* (\(\int|\nabla u|^2\ge\int|u|^2 s^{-2}\ge\rho^{-2}\int|u|^2\) with mean zero in \(\phi\), Poincaré
  constant 1), leaving only the \(m=0\) problem for numerics; and the off-axis checks are full 3-D eigenvalues on
  cubes. So the "subspace lower bound does not bound all test functions" objection is answered for axis-centred balls
  and does not apply to the off-axis cubes. The valid residual point — numerics cover finitely many centres/radii and
  cannot establish uniform constants — the paper already concedes.
- **R11 (eq. 4).** The displayed inequality over-claimed for \(\alpha>4\), but the prose already specialized to
  "\(0.28\) for \(\alpha=4\)", so the error was contained. Now made explicitly \(\alpha\)-dependent.

## 5. Corrections applied this round (main.tex; rebuilt clean, 16 pp, 0 overfull boxes)

Abstract "supported near"→"small along"; Thm 2.1(c) bounded-drift qualifier restored; Remark 2.2 priority qualified
(Ahlfors–Nevanlinna; "in the statistical setting"); eq. (4) constant made \(\alpha\)-dependent (\(2.62^{-\alpha/2}\),
≥0.14 at α=4) and the Section 6 cross-reference updated; Prop 5.2 "unit tube"→"tube of bounded radius" and the false
"touches \(\Sigma_{k+1}\)" replaced by the antipodal-poles statement; Appendix A.1 strictness corrected; A.2
integrability caveat added; "flat cylinder"→"round cylinder, scalar curvature \((d-1)(d-2)\)"; the appendix "separate
volume/sphere" sentence corrected (both integrals converge; the volume criterion decides under D+P); the exhaustion
open question reworded (Thm 7.6 answers existence; explicit exhaustion is the open part); "forced" restricted to the
ansatz. No proof was altered; no mathematics was added beyond these corrections.

## 6. Not done — queued (needs owner direction and/or primary-source verification)

- **Repair the Theorem 4.1 D+P proof** (§2). The real work; owner to decide approach (I can draft the polar-region
  covering + tube-volume lemma + Lemma 4.3 chart fix, but it is a genuine proof-writing task, not a patch).
- **Add references (verify metadata at the primary source before committing; AR-027 / no-invented-metadata rule):**
  - Björn–Buckley–Keith, *Admissible measures in one dimension*, Proc. AMS **134** (2006) 703–705, e-pub 28 Sep 2005
    — Theorem 2, as the predecessor of Lemma 3.3. (reviewer-supplied; `verify`)
  - Shimizu–Nakano, *On the asymptotic behavior of Bessel-like diffusions*, Tsukuba J. Math. **41**(1) (2017) 81–90,
    arXiv:1705.04408 — Theorem 1.3, for Prop 5.3. (reviewer-supplied; `verify`)
  - Grigor'yan, *Heat kernels on weighted manifolds and applications* (Cor. 9.9) as a weighted statement of the volume
    criterion. (reviewer-supplied; `verify`)
  - Ref [25]: confirm first name (Kosaku vs Kohei) Takanashi against arXiv:2310.17891. (`verify`)
- **Prop 5.3 normalization note:** state the generator/speed-measure convention so the origin-kernel constant (4 for
  the full line under the paper's normalization; 8 for the reflected half-line) is unambiguous. Transience is
  unaffected either way.
- **Prop 5.2 all-ball doubling:** give the sub-mesh, polar, and cross-shell cases, not "at the relevant scales".
- **Brown–Hwang comparison** (still an owner checklist item): once transience + Brown's conditions give
  inadmissibility, no valid sufficient *admissibility* theorem can apply; the task is to identify which Brown–Hwang
  hypothesis fails (an explanatory calculation), which needs Volume 1 (document supply, AR-029b §2).
- Consult Brown's 1973 correction when finalizing the Brown citations (reviewer's note; not expected to affect the
  results used).

## 7. Self-corrections

- The eq. (4) "0.28" and the Section 6 "gives 0.28" cross-reference were mutually consistent but over-claimed for
  α>4; corrected together.
- The paper's own proof of 4.1(a) is internally inconsistent (states the correct \((1+d^2)^{\alpha/2}/s^\alpha\)
  comparison, then uses the wrong \(W(u)\) one in the covering). Flagged for the repair, not patched here.

## 8. SC (success criteria for this packet)

- Every review finding has an independent verdict and a disposition: met.
- Correctness errors fixed without altering any proof's logic or adding unverified mathematics: met.
- Bibliographic additions held at `verify` pending primary-source checks (no invented metadata): met.
- The one blocking item (Thm 4.1 proof) is stated as outstanding, not papered over: met.

## 9. Repair of Theorem 4.1 (drafted 2026-10-25; in `main.tex`)

Rewrote the proof of Lemma 4.3 (one circle) and the proof of Theorem 4.1(a). Scratch build clean (16 pp, 0 overfull,
no undefined refs); `main.pdf` not regenerated (viewer lock), source verified via a `-jobname` build.

**Lemma 4.3 (chart fix, R4-Lemma).** Small-scale branch restricted to \(\rho\le R/6\), so every point of the ball is
within \(3\rho\le R/2\) of the circle, strictly inside the focal distance \(R\) where the Fermi normal-exponential
chart is a diffeomorphism; the ball meets a single arc of length \(\le2\rho\ll2\pi R\), so no periodic identification
arises (answers the "cannot globally flatten the tube" point). Large-scale branch \(\rho\ge R/6\) via the centre-weight
comparison \(p_c\) and Lemma 4.2, constants adjusted (cells \(R/12\), (G1) for \(R/12\le\rho'\le R\)).

**Theorem 4.1(a).** Restructured into: (local comparison) the \emph{correct, bounded-factor} identity
\(w\asymp\sigma_0^{-\alpha}(1+d_C^2)^{\alpha/2}\) on balls of radius \(\le\sigma_0/4\) (eq. (5)), replacing the false
\(W(u)\) multiplicative approximation (R4-i) and the false \(1+O(1/s)\) tightness (R4-ii); the distance-to-union \(d\)
is matched to the distance-to-nearest-circle \(d_C\) (equal where \(d_C\le0.2s_k\); elsewhere both \(\asymp s_k\)).
(cell mass) a tube-volume estimate (eq. (6)) giving \(\mu(Q)\asymp|Q|\) for every cell, replacing the false
meets-a-circle/uniformly-far dichotomy (R4-iv). (small balls) the single circle \(C\) may be polar
(\(R_C\asymp1\)) or bulk (\(R_C\asymp2^k\)); both are handled by the \emph{uniform} Lemma 4.3, explicitly not by a
\(\sqrt R\)-scale cylinder approximation (R4-iii). (large balls) gluing against Lebesgue with cells of side
\(\sigma/32\), so each enlarged ball \(B_j\) has radius \(\le\sigma/4\) and is a small ball (removes any circularity),
(G1) = the cell-mass estimate, then Hajłasz–Koskela self-improvement.

**Confidence / residual referee items (honest).** The four gaps are addressed with arguments I believe are correct; I
re-derived each. This is a drafted revision, not a refereed proof. A careful referee should still check: (a) the Fermi
bi-Lipschitz constant and the focal-distance claim with explicit constants; (b) the "\(\le C_0\) circles within
\(s_k\) of a cube" count from the meridian-plane mesh (uniform over shells, including shell boundaries where the
spacing changes by \(\sqrt2\)); (c) that Lemma 4.2's hypotheses (bounded overlap of the \(Q_j\) and \(B_j\), the
\(s_j\asymp s_{j'}\) condition across shell boundaries and near the axis) hold for the chosen cover; (d) the \(d\) vs
\(d_C\) matching near the axis where several small circles cluster within \(\asymp s_k\). None of these is expected to
obstruct the result, but they are the places a referee will press. Parts (b) and (c) of Theorem 4.1 (tests silent,
volume \(\asymp r^3\)) were not in question and are unchanged.
