# AR-019 — Robustness-instrument survey by analogy (comparative note)

```yaml
id: AR-019
title: "Robustness-instrument survey by analogy"
mode: EXPLORE
parent: BH-004, AR-009 §5.2
priority: P1
inputs: [KB-003 (TH-033, SRC-044), KB-004 (BH-004), KB-005 §6,
         ar/AR-009_spec.md §5.2/§5.2.1/§8, results/AR-010/pilot_summary.json]
question: >
  What do analogous perturbation-response literatures — fidelity/Loschmidt-echo
  decay classes, DTC rigidity/critical-strength curves, MBL stability analyses,
  dose–response calibration methodology — suggest as the best-instrumented
  effect measure for AR-009 criterion (b): fixed-strength response vs
  failure-threshold (λ*-style), ratio vs difference measures?
deliverable: this note (adopt/keep recommendation); SRC-052..058 (verify)
promotion_effect: AR-009 §8 amendment (only before confirmatory runs) — NOT exercised
kill_effect: none (advisory)
status: DONE (2026-08-12; reconciled in-session)
```

## 0. Recommendation (summary)

**KEEP** the preregistered §5.2 log-ratio instrument as the criterion-(b)
primary, unchanged. No §8 amendment to any preregistered threshold. Two
advisory riders, neither changing preregistered content:

1. **Framing discipline** for the confirmatory write-up: criterion-(b)
   conclusions are statements *at the calibrated strengths* (λ = 0.1,
   γ = 0.01), not strength-independent class properties. The fidelity-decay
   literature shows response-vs-strength is generically regime-structured
   (§3.1 below); a fixed-strength contrast is regime-relative by construction.
2. **Follow-up candidate** (queue only if criterion (b) returns a positive
   and AR-011 wants a mechanism-level check): a decay-rate-law analysis
   (fit log ρ across a strength grid; classify FGR-like ∝ λ² vs saturated
   response) as a *separate*, budgeted AR — not a change to AR-010.

## 1. Scope and method

Opportunistic (non-systematic) survey, executed 2026-08-12 via web search at
abstract/summary level plus the already-verified SRC-044 protocol and the
AR-010 pilot record. The analogy is **instrument-level only**: what these
literatures teach about *measuring* perturbation response. No physics-level
claim connects dose–response endpoints or MBL transitions to Φ-stationarity
(scope wall, KB-002 collision rule 10). All new sources are flagged `verify`
per KB-003 §N governance; none is load-bearing for any formal argument —
they inform an advisory methodology ruling whose default (keep) stands on
the pilot evidence alone.

## 2. The decision space

The AR-019 question factors into two axes:

- **Design axis:** (A) fixed-strength response contrast (current §5.2
  primary); (B) failure-threshold location, λ*-style (the §5.2.1 exploratory
  candidate); (C) full response-curve instruments (rigidity curve h(ε),
  regression-derived effective-strength ECx-style, decay-rate-law
  classification).
- **Measure axis:** ratio (fold-change, log-transformed) vs difference
  (absolute retention R).

The §5.2 primary is (A)+ratio: log ρ at pilot-calibrated strengths, floored
denominator, bootstrap CIs, two-size replication. R (difference) is already
demoted to descriptive (Amendment 1).

## 3. Survey by domain

### 3.1 Fidelity / Loschmidt-echo decay classes (SRC-052, SRC-053; verify)

Structure reported in the literature: fidelity decay as a function of
perturbation strength passes through distinct regimes — perturbative/Gaussian
(coupling below mean level spacing), Fermi-golden-rule exponential (rate
∝ λ²), and, for classically chaotic dynamics, a perturbation-independent
Lyapunov regime where the decay rate saturates at the Lyapunov exponent
(SRC-053); local perturbations add a non-monotonic FGR → escape-rate
crossover. The comprehensive regime taxonomy is the SRC-052 review.

**Lessons.** (i) The class-diagnostic object in this literature is the *rate
law* (functional dependence on λ), not a single response value — but
extracting it needs a strength grid × ensemble and preregistered functional
forms; at N = 10–12 with 𝒲 = [100, 200], fit-based rate extraction would be
a study redesign, not an instrument swap. (ii) A single fixed strength can
place different classes in different regimes — this is exactly the failure
mode the §5.2.1 pilot was built to avoid, and the pilot's own record shows
regime structure (dephasing discrimination saturates by γ = 0.01;
Amendment 3.2 reasoning). (iii) Fidelity itself is a normalized, scale-free
(ratio-type) quantity — the log ρ convention matches.

### 3.2 DTC rigidity / critical-strength curves (SRC-044 verified; SRC-054 verify)

The verified SRC-044 protocol measures the subharmonic peak while varying
perturbation ε, tracing a rigidity curve whose crossover locates melting;
SRC-054 (Yao–Potter–Potirniche–Vishwanath) maps the phase diagram and the
melting transition numerically. Caution recorded: SRC-054's phase diagram
drew a 2021 Comment (arXiv:2109.00551) and Reply (arXiv:2109.07485) —
critical-point location from small-size numerics proved contestable even in
the flagship rigidity paper.

**Lessons.** (i) Rigidity-style instruments measure the *entire curve* and
read the transition off its shape; they do not preregister a single tested
strength as the threshold estimator. The affordable home for this style in
AR-010 already exists in the spec: T-B's h_sub(ε) rigidity curve
(confirmatory) and the §5.2.1 exploratory λ*/γ* curves (descriptive).
(ii) Critical-strength estimates at toy-model sizes carry real
controversy risk (the Comment/Reply episode) — a reason not to hang the
paper's primary criterion on one.

### 3.3 MBL stability analyses (SRC-055, SRC-056; verify)

SRC-055 (Šuntajs et al.) reports that extracting the MBL critical disorder
W_c is unreliable at accessible sizes — the estimates drift strongly with
system size; SRC-056 (De Roeck–Huveneers avalanche theory) shows threshold
locations can be asymptotically unstable in ways invisible to small-size
numerics.

**Lessons.** At AR-010's sizes (N = 8–12), a threshold-*location* instrument
(λ*) would largely measure finite-size drift. The existing two-size
replication requirement tests stability of a *response contrast*, which the
MBL episode suggests is far more robust than stability of a *critical
point*. AR-010's own open item (localized-class ε_Φ straddle, size-scaling
to adjudicate) is a live instance of exactly this fragility.

### 3.4 Dose–response calibration methodology (SRC-057, SRC-058; verify)

The NOEC/LOEC-vs-ECx debate in regulatory ecotoxicology maps onto the
AR-019 question almost term-for-term. NOEC (highest tested dose with no
statistically significant effect) is structurally the mirror of λ* (smallest
tested strength at which the ε_Φ criterion first fails): both are
*tested-grid statistics*, not parameters of the response curve. The recorded
criticisms of NOEC — value restricted to the tested concentrations; depends
on sample size and test power (rewards noisy experiments with higher NOECs);
carries no confidence interval — transfer verbatim to λ*. OECD guidance
(SRC-057) recommends regression-based ECx estimates instead; the recorded
dissent (SRC-058) argues regression estimates have their own model-dependence
and extrapolation flaws, i.e., neither side of that debate endorses the
grid-statistic. Standard practice for the *other* design — a calibrated
fixed-dose contrast — is a dose-finding pilot followed by a log-fold-change
(ratio) comparison with resampled CIs, which is precisely the §5.2.1 → §5.2
construction. Ratio measures are preferred there for scale-free
comparability across baselines of different magnitude — matching log ρ and
its δ_floor guard for zero-baseline denominators.

## 4. Cross-check against the AR-010 pilot record

- **λ*/γ* as measured were grid-censored:** under the superseded
  ε_Φ = 0.05, λ* sat at the grid minimum (0.02) for 6/7 groups and γ* at the
  grid minimum (0.003) for 7/7 (results/AR-010/pilot_summary.json). A
  λ*-primary instrument would need a finer, lower grid — a budget multiplier
  with no demonstrated discrimination gain.
- **λ* is criterion-derived:** its value is a function of the ε_Φ ruling,
  whose calibration was itself amended in-pilot (Amendment 3.1). log ρ is
  criterion-independent; it survived that amendment unchanged.
- **The current instrument already discriminates:** dephasing log ρ is
  monotone and class-ordered with sign structure (negative for
  quasiperiodic/metastable — the early sustained-by signature), and the
  owner-chosen strengths sit in the responsive, non-saturated band. The
  instrument the spec preregisters is the one the pilot validated.

## 5. Why not adopt (C) — full response-curve instruments?

They are the best-instrumented option in every surveyed literature, and the
spec already deploys them where they are affordable: T-B's h_sub(ε) rigidity
curve is confirmatory-mandatory, and the T-A/T-C λ*/γ* curves are §5.2.1
exploratory outputs. Promoting a curve instrument to the criterion-(b)
primary for all classes would multiply the confirmatory ensemble by the
strength grid (~4–12×), require preregistering curve families now, and
re-open Layer-3 thresholds that survived owner review — for a study whose
question is a *class contrast*, not a threshold location. Rejected on
budget and preregistration-hygiene grounds; revisit via the §0 rider-2
follow-up AR if warranted.

## 6. Sources consulted (survey level; all new entries flagged verify)

Consulted 2026-08-12 via web search (abstract/summary level unless noted):

- SRC-052 — Gorin, Prosen, Seligman, Žnidarič, *Phys. Rep.* 435, 33–156
  (2006) — regime taxonomy (survey level; exact section locations not yet
  extracted — verification task).
- SRC-053 — Jalabert & Pastawski, *PRL* 86, 2490 (2001) —
  perturbation-independent (Lyapunov) decoherence-rate regime.
- SRC-054 — Yao, Potter, Potirniche, Vishwanath, *PRL* 118, 030401 (2017),
  arXiv:1608.02589; Comment arXiv:2109.00551; Reply arXiv:2109.07485.
- SRC-055 — Šuntajs, Bonča, Prosen, Vidmar, *PRE* 102, 062144 (2020).
- SRC-056 — De Roeck & Huveneers, *PRB* 95, 155129 (2017).
- SRC-057 — OECD Series on Testing and Assessment No. 54 (2006),
  DOI 10.1787/9789264085275-en.
- SRC-058 — Green (2013), *Integr. Environ. Assess. Manag.* 9, 12–16,
  DOI 10.1002/ieam.1367 (dissenting view).
- SRC-044 (verified 2026-08-11) — rigidity protocol template.
- results/AR-010/pilot_summary.json; ar/AR-009_spec.md §5.2/§5.2.1/§8
  (repo-internal, read in full).

## 7. Confidence notes and open gaps

- Survey is opportunistic, not systematic; a targeted VERIFY pass on
  SRC-052..058 (AR-002-series) should precede any *formal* citation of their
  content. The **keep** recommendation does not depend on them: it stands on
  the pilot record (grid-censoring, criterion-dependence, saturation) alone;
  the literature converges on, rather than establishes, the ruling.
- Bibliographic metadata recorded to best current knowledge; arXiv IDs for
  SRC-055/056 and the SRC-058 author initials are unconfirmed recollections
  — explicitly part of the verify task.
- Not surveyed (out of budget): linear-response/Kubo formalism as a
  criterion-(b) framing; quantum-metrology susceptibility measures. Neither
  appeared likely to overturn a keep ruling; noted for completeness.

## 8. Proposed KB deltas (applied in reconciliation, this session)

1. KB-003: add SRC-052..058 (all `verify`); changelog §S; v0.3 → v0.4.
2. KB-005 §6 AR-019: progress line, status DONE/reconciled; changelog §22;
   v0.5 → v0.6.
3. ar/AR-009_spec.md §8: dated **no-change** entry recording that the
   instrument-upgrade window was exercised and the log-ratio primary stands;
   framing-discipline rider recorded; stale G0 open-item annotated resolved.
4. No KB-001/KB-002/KB-004 changes. No ADR candidates.
