# AR-011 — Toy-model adversarial analysis (evidence packet)

```yaml
id: AR-011
title: "Adversarial analysis of the AR-010 confirmatory results"
mode: ADVERSARIAL
parent: BH-004, BH-005 (KB-004 §4); attacks per KB-004 §7 checklist
priority: P0
inputs: [ar/AR-010_confirmatory-2026-08-12.md,
         results/AR-010/confirmatory_summary.json,
         results/AR-010/confirmatory/*.json, ar/AR-009_spec.md,
         results/AR-010/ar011_attacks.json]
question: >
  Which AR-010 conclusions survive the KB-004 §7 adversarial checklist —
  representation-dependence, stationary-state indistinguishability
  (item 12), sustained-by vs compatible-with (item 9), hidden clocks
  (item 3), finite-N and instrument-floor sensitivity?
deliverable: this packet; corrections issued to the AR-010 packet
  (dated) and KB-004 (v0.4)
promotion_effect: surviving claims become promotable evidence for BH-004
  (owner decision); refuted interpretations corrected in place, dated
kill_effect: if the sustained-by evidence reduces entirely to instrument
  artifact, §5.4 row 4 pressure on BH-004 (KC-007 → HYP-009) is recorded
status: DONE (2026-08-13; attacks A/B/C executed, written audit complete,
  corrections issued, reconciled in-session)
```

## 1. Attack A (checklist items 9, 13): the floor/denominator audit

**Claim attacked:** AR-010 packet §3.3 — "the matched stationary
comparator ρ̄ is FAR MORE FRAGILE than the dynamical state … the
dynamical state holds its Φ against perturbations that scatter the
motionless matched ensemble."

**Result: the interpretation is REFUTED; the preregistered verdict
survives on corrected grounds.** Perturbed-drift numerators
(max δΦ_pert, N = 10 ensemble means, dyn vs comparator):

| class | quench dyn/comp | dephasing dyn/comp | loss dyn/comp |
|---|---|---|---|
| (ii) quasiperiodic | 0.94 / 0.065 | 0.70 / 0.32 | 1.19 / 0.000 |
| (iii) chaotic | 0.12 / 0.073 | 1.01 / 0.36 | 0.14 / 0.000 |
| (iv) metastable | 0.21 / 0.002 | 0.19 / 0.049 | 0.23 / 0.000 |
| scrambling | 0.13 / 0.069 | 1.08 / 0.42 | 0.15 / 0.000 |
| integrable | 0.31 / 0.073 | 0.77 / 0.28 | 0.45 / 0.000 |
| localized | 0.18 / 0.081 | 0.92 / 0.20 | 0.22 / 0.000 |

The comparator responds LESS in absolute drift under every protocol and
every class. The "fragile comparator" direction was manufactured by the
log-ratio denominator: the comparator's own unperturbed drift is exactly
zero, floored at δ_floor = 1e-3, which inflates its log ρ by
ln(δΦ_pert/10⁻³) ≈ 4–6 regardless of physics. Sub-findings:

1. **§5.3 check-2 arm-1 STANDS formally** — the preregistered criterion
   asks for a *difference* with disjoint CIs, not a direction, and the
   difference survives instrument choice (a numerator-only contrast
   separates just as cleanly, with the opposite sign).
2. **The floor-free switch-off arm carries the genuine sustained-by
   signal:** dephasing at t_off moves Φ by 43–90% of ‖D̄‖ (quasiperiodic
   0.43, chaotic 0.54, scrambling 0.52, integrable 0.85, metastable
   0.90, localized 0.90). Killing the motion does not freeze the
   geometry in place — it *changes* the geometry. The correct
   sustained-by statement: **the stationary geometry the dynamics
   maintains is not the geometry the dephased (motionless) state holds.**
3. **Spec-assumption refutation (§4.1):** "ρ̄ … matched to the run's
   long-time-averaged Φ by construction (its MI pattern is the time
   average's)" is FALSE as written. The two-site RDMs of ρ̄ are the
   time-averaged RDMs (reduction is linear), but MI is nonlinear in the
   RDM: Φ[ρ̄] sits 43–90% away from D̄. The comparator never realized
   "same geometry, no motion". All §5.3 conclusions must be read with
   this confound; a Φ-matched motionless comparator does not currently
   exist in the family (whether one is constructible is an open design
   question for the reformalization, AR-020).

**Item-13 stakes resolved:** the sustained-by evidence does NOT reduce
entirely to artifact — arm 2 (switch-off geometry change) is floor-free
and large — but it is weaker and differently shaped than the AR-010
packet stated. Corrections issued (§4 below).

## 2. Attack B (items 6, 12): metastable Ξ tolerance sensitivity

**Claim attacked:** the (i, iv) exact-value separation and §5.3 check-1
rest on Ξ(iv) ≈ 5e-3 — is that margin an artifact of the 1e-10
degeneracy-grouping tolerance (which sat inside the splitting
distribution at N = 8)?

**Result: SURVIVES.** Recomputed Ξ for the full TA_iv ensembles under
tol ∈ {1e-8, 1e-10, 1e-12}: values are IDENTICAL to machine precision at
both criterion sizes (N = 10: [0.00373, 0.00592]; N = 12:
[0.00475, 0.00617]) — the doublet splitting lies far below every
candidate tolerance at N ≥ 10, so the grouping never flips. The N = 8
bimodality seen in the descriptive data was N = 8-specific, and N = 8 is
not a criterion size (Addendum 1). The Ξ margin is physical
(transverse-dressing weight outside the doublet), not a tolerance
artifact.

## 3. Attack C (item 5): Φ partition-dependence probe

**Claim attacked:** the §4.3 battery showed Φ invariant under
single-site frames — but TH-037's caveat lives at the PARTITION, which
single-site unitaries never move.

**Result: partition-dependence is REAL and now QUANTIFIED.** Fixed
random two-site (entangling, adjacent-pair) basis changes on three
disjoint pairs move Φ by 9.3% mean / 11.0% max (chaotic, N = 10) and
17.4% / 19.7% (localized) in relative Frobenius norm across the window.
**Scope consequence: this is the same order as ε_Φ = 0.25.** The
stationarity verdicts and robustness margins are PARTITION-RELATIVE at
the 10–20% level; Φ is a geometry *of the posited site factorization*,
not of the state alone. This makes the TH-037 caveat quantitative for
our family (as §4.3 intended) and sets a floor on how much geometric
meaning the ε_Φ threshold can carry. Recorded as a standing scope wall;
not a violation (the partition is preregistered).

## 4. Corrections issued (dated, non-silent)

- AR-010 packet: dated correction appended to §3.3 (fragility direction
  retracted; switch-off arm promoted to the load-bearing evidence;
  §4.1 matching-assumption refutation recorded).
- KB-004 → v0.4: BH-004 evidence note amended accordingly.
- AR-009 spec §8: dated AR-011 outcome entry (no preregistered content
  changed; §4.1 matching language flagged for the AR-020
  reformalization).

## 5. Written audit of the remaining checklist items

- **1 (known theorem?):** the *existence* leg — stationary Φ over moving
  chaotic states — is expected from equilibration/typicality theory
  (local observables of quench-equilibrated states are stationary; the
  MI graph is built from 2-site observables). AR-010's value-add is
  (i) the class-resolved robustness differential and (ii) the switch-off
  geometry change; neither is a standard equilibration statement. The
  quasiperiodic *negative* log ρ under dephasing (noise stabilizes the
  moving geometry) appears genuinely non-textbook; flagged as the most
  publication-worthy single number pending literature check (no SRC yet
  — do not cite from memory).
- **2 (geometry hidden in the variable?):** the −log/cap construction
  fixes the large-distance scale by fiat (w_max = ln 10⁶); cap-above
  fraction 1.000 in all mean graphs shows verdicts are not cap-dominated,
  and the cap diagnostic is preregistered. Standing instrument note, not
  a hidden-geometry violation.
- **3 (hidden clock?):** external lab clock declared (spec §0),
  T-B stroboscopic clock derived from it; no geometry-dependent time
  enters any dynamics; dephasing rate γ is lab-time. The OL-4 caveat
  (NC-010) stands untouched. PASS.
- **4 (target dynamics in the reconstruction map?):** Φ is computed from
  instantaneous states; the only temporal construct is the declared
  window mean D̄. PASS.
- **7 (AdS-specific?):** not applicable (open spin chains). PASS.
- **8 (conventional channel reproduces it?):** the deflationary reading
  — "class-ordered dephasing response is just different spectra reacting
  to a standard channel" — is accepted AS SCOPE: BH-004 is an in-model
  structural claim, not a novel-mechanism claim (KB-002 collision
  rule 10). The claim content is the class-resolved differential and its
  witnesses, not the channel.
- **10 (coarse-graining creates the arrow?):** Φ-stationarity of
  chaotic classes is indeed an equilibration effect (item 1); the
  arrow/dynamics claims rest on witnesses evaluated at OL-0/1, not on
  Φ's stationarity. PASS with the item-1 scope note.
- **11 (recurrence):** invoked only in T-B (W5, stroboscopic clock,
  period-2T witness declared; r1 comparator excludes fine-tuned flips).
  BH-005 remains gated on the BH-004 outcome. PASS.

## 6. Verdict summary

| AR-010 claim | AR-011 verdict |
|---|---|
| criterion (a) fails (W3 null-discard, scr\|loc) | SURVIVES (no attack found; the discard clause did its job) |
| criterion (b) holds (dephasing, both tracks) | SURVIVES (floor-free: both sides of every replicated pair are dynamical classes with real baselines) |
| §5.3 formal verdicts (sustained-by × 6) | SURVIVE as preregistered rulings |
| "comparator far more fragile" interpretation | **REFUTED** (denominator artifact; direction inverted — Attack A) |
| switch-off geometry change (43–90%) | SURVIVES and is PROMOTED to the load-bearing sustained-by evidence |
| §4.1 "Φ-matched comparator" design assumption | **REFUTED** (MI nonlinearity; no Φ-matched motionless comparator exists in the family) |
| (i, iv) separation via PR_A + Ξ | SURVIVES (tolerance-robust — Attack B) |
| Φ-stationarity as partition-geometry | SCOPE-BOUNDED (10–20% partition-dependence, same order as ε_Φ — Attack C) |
| T-B compatible-with, rigidity bound, r2 prethermal | SURVIVE (no attack found) |

Net effect on BH-004: the sustained-by clause retains in-model support,
now correctly stated — *the geometry the dynamics maintains is not the
geometry the motionless state holds* (switch-off arm), and robustness
is class-resolved relative to own baselines (criterion (b)) — while the
absolute-fragility narrative is withdrawn. Item-13 kill condition NOT
met. AR-020 (witness reformalization) inherits two new requirements:
a null-silent scrambling/localization witness AND a genuinely Φ-matched
motionless comparator (or a proof that none exists in the family, which
would itself sharpen the sustained-by claim).
