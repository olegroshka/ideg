# AR-010 — Track E3 confirmatory runs (evidence packet)

```yaml
id: AR-010
title: "Toy-model confirmatory runs against the AR-009 spec"
mode: EXPERIMENT
parent: BH-004, HYP-009; spec: ar/AR-009_spec.md (§8 Amendments 1-3 +
  AR-019 no-change entry)
priority: P0
inputs: [ar/AR-009_spec.md, results/AR-010/confirmatory_manifest.json,
         results/AR-010/confirmatory_manifest_addendum1.json,
         results/AR-010/sanity_checks*.json, KB-005 §21 licensing]
question: >
  Do the preregistered criteria hold — (a) witnesses separate dynamical
  classes (AUC >= 0.95, >= 2 statistics per pair, two sizes); (b) the
  robustness of Phi-stationarity differs by class (|Delta mean log rho| >
  ln 1.5, disjoint BCa CIs, two-size replication) — and what does §5.3
  adjudicate per class?
deliverable: this packet; results/AR-010/confirmatory/*.json;
  results/AR-010/confirmatory_summary.json
promotion_effect: per spec §5.4 (gated on AR-011 adversarial companion,
  KB-005 §10)
kill_effect: per spec §5.4 row 3 if (a) fails
status: DONE (2026-08-12/13; campaign executed and analysed per the
  preregistered plan; reconciled in-session)
```

## 1. Execution record

- Per-size §6.3 sanity checks ALL PASS before any run: N = 8 (chaotic
  ⟨r⟩ = 0.542; free-spectrum 8.0e-15; localized ⟨r⟩ = 0.405/20 real.),
  N = 12 (0.529; 5.9e-14; 0.390/20 real.); N = 10 record of 2026-08-11
  stands (incl. DTC 20/20).
- Confirmatory manifest (seeds, sizes, ensembles, implementation
  clarifications) committed b91ad54 BEFORE execution. First execution
  closed the AR-019 instrument-upgrade window (spec §8).
- **Addendum 1 (a76db0e), measured obstruction:** the §1 T-A(ii)
  incommensurability certificate is exhaustively unsatisfiable at N = 8
  (0/56 nondegenerate-gap magnon triples; 17/120 at N = 10, 27/220 at
  N = 12). T-A criterion sizing reverted to the spec §5.1 primary
  (10, 12); T-A N = 12 seeds committed before those runs. N = 8 runs for
  classes (i)/(iii)/(iv) remain valid, descriptive. T-A dephasing pairs
  involving class (ii) are single-size (§6.2 bounds dephasing at
  N ≤ 10) → ineligible for criterion-(b) replication (recorded, not a
  null).
- Campaign: T-A 4 classes × {8*, 10, 12}, T-C 3 regimes × {8, 10, 12}
  (dephasing at N ≤ 10), T-B N = 10 (11-point ε rigidity grid, 3 DTC ε,
  r1/r2 comparators, switch-off, descriptive protocols), as parallel
  background jobs (BLAS 4 threads/process). (*class (ii) absent at 8.)

## 2. Finding: W3 fires on the null (§4.4) — witness discarded

The class-(i) null (TFIM g = 1.5 ground state, global-phase dynamics)
shows a decisively time-dependent OTOC: C(r_max, t) reaches 0.1 at
t* = 1.5 and saturates at c_sat ≈ 1.11 (N = 8; N = 10/12 records in the
summary JSON). The §4.4 silence prediction ("W3: C(r, t)
time-independent") is REFUTED: the state is frozen, but the OTOC probes
Heisenberg-operator spreading, which a gapped ground state supports
(V|ψ⟩ creates a propagating excitation). Per the preregistered §4.4
discard clause, W3's statistics (c_sat, t*) leave the criterion-(a)
statistic set, which therefore runs on {PR_A, min d_phys, Ξ}.

Consequence for pair (i, iv): min d_phys is uninformative (tied at
machine zero — recurrence DEPTH of a slowly-rotating state returns ~0
within the window), so the pair rests on PR_A and Ξ. Both separate:
PR_A(iv) sits strictly above 1 with a clear margin (N = 8:
[1.0071, 1.0105]; N = 12: [1.010, 1.012] — dressing weight at the gap
frequency; the pilot's "W1 doublet blindness" applies to the doublet
LINE, not to the exact-value contrast with the null), and Ξ(iv) excludes
0 at every size. Two statistics — the pair passes despite the W3
discard. A first in-session read on rounded output suggested otherwise;
corrected in the session log.

Integrity note: w2_mean-vs-w2_min is queued as a spec-amendment candidate
(min is structurally uninformative for slow classes) — no longer
verdict-relevant, NOT applied.

## 3. Criterion (a) / criterion (b) / §5.3 adjudication

### 3.1 Criterion (a): FAILS — single cause, localized to one T-C pair

Active statistic set after the §4.4 W3 discard: {PR_A, min d_phys, Ξ}.

- **T-A HOLDS** at the (10, 12) criterion sizes: all six class pairs
  separate on ≥ 2 statistics at both sizes (pairs with class (i) by the
  exact-value rule — see §2 for the decisive (i, iv) margins).
- **T-C FAILS** at both sizes on **scrambling | localized**: only Ξ
  separates (AUC 0.985 at N = 10, 0.990 at N = 12). PR_A degrades with
  size (0.8875 → 0.5575 — realization-averaged localized PR_A overlaps
  scrambling); min d_phys rises with size but misses threshold
  (0.705 → 0.945 vs 0.95). The other T-C pairs pass:
  scrambling | integrable via PR_A (0.9525/0.9575) + Ξ (0.95/0.95);
  integrable | localized via PR_A (1.0/1.0) + Ξ (0.99/0.995).
- **Counterfactual (descriptive, not applied):** had W3 been retained,
  t*(r_max) separates scrambling | localized with AUC 1.0 (scrambling
  t* = 2.0 uniformly; localized t* = ∞ across the ensemble). The (a)
  failure is therefore SINGLE-CAUSE: the preregistered null-discard of
  W3 removed the only statistic pair that doubly-witnesses the
  scrambling/localization distinction. This is a genuine finding about
  witness design, not an accident: the natural discriminator is not a
  valid CON-034 witness (it fires on frozen states).

### 3.2 Criterion (b): HOLDS — dephasing replicates in both tracks

Mean log ρ (BCa 95% CIs in the summary JSON; realization = resampling
unit for disordered groups):

- **Dephasing** (γ = 0.01; sizes 8/10): T-A — fixed point 7.15/6.99,
  chaotic 2.20/2.10, metastable −0.09/−0.11, quasiperiodic —/−0.27;
  T-C — scrambling 2.19/2.14, localized 1.53/1.57, integrable 0.73/0.75.
  Replicated pairs with direction agreement (§6.4): T-A (i,iii), (i,iv),
  (iii,iv); T-C ALL THREE pairs — (scr,int) Δ ≈ 1.4, (scr,loc) Δ ≈ 0.6,
  (int,loc) Δ ≈ 0.8, each > ln 1.5 ≈ 0.405 with disjoint CIs at both
  sizes. The pilot's class ordering (chaotic/scrambling ≫ localized >
  integrable > metastable ≥ quasiperiodic, the last two negative —
  dephasing pins oscillating Φ) is CONFIRMED at full ensembles and both
  sizes.
- **Quench** (λ = 0.1; T-A sizes 10/12): replicated only for class-(i)
  pairs — the fixed point reads log ρ ≈ 4.35/4.38 while every dynamical
  class is quench-null (|mean| ≤ 0.07). Instrument note: class (i)'s
  unperturbed drift is the preregistered δ_floor, so its log ρ measures
  response-vs-floor; the (b) headline should rest on the dephasing
  replications, which involve no floor.
- **Subsystem loss**: no replicated pairs (means 0.07–0.25) — a clean
  null for the discrete protocol.

**Criterion (b) verdict: HOLDS** (≥ 1 protocol, ≥ 1 pair, both sizes,
direction-consistent — comfortably exceeded).

### 3.3 §5.3 sustained-by adjudication (N = 10, all comparator checks)

| class | check 1 (Ξ vs ρ̄) | check 2 | verdict |
|---|---|---|---|
| (i) fixed point | fails — definitional (ρ̄ ≡ ρ) | (floored) | **compatible-with** |
| (ii) quasiperiodic | 0.667 vs 0 | quench+deph+loss disjoint | **sustained-by** |
| (iii) chaotic | 0.994 vs 0 | all arms + switch-off | **sustained-by** |
| (iv) metastable | 0.0037 vs 0 | quench+deph + switch-off | **sustained-by** |
| scrambling | 0.957 vs 0 | all arms + switch-off | **sustained-by** |
| integrable | 0.969 vs 0 | all arms + switch-off | **sustained-by** |
| localized | 0.352 vs 0 | all arms + switch-off | **sustained-by** |

The quantitative heart of the sustained-by result: the matched
stationary comparator ρ̄ is FAR MORE FRAGILE than the dynamical state —
quench log ρ ≈ 4.1–4.3 (comparator) vs ≈ 0 (dynamical), dephasing
≈ 3.9–5.95 vs ≤ 2.2, with disjoint CIs in every dynamical class. The
motion does not merely coexist with the stationary geometry; the
dynamical state holds its Φ against perturbations that scatter the
motionless matched ensemble. This affirms BH-004's sustained-by clause
in-model for all six dynamical classes.

### 3.4 Stationarity table (ε_Φ = 0.25 verdicts, baseline)

Stationary-with-witness (the BH-004 candidate regime): chaotic 20/20
(N = 10, max δΦ 0.111–0.136), scrambling 20/20 (N = 12, 0.090–0.213),
T-B DTC ε = 0.03 100/100 (§4). Straddler: localized 80/100 at N = 12
(0.138–0.336; the pilot's ε_Φ-straddle flag persists at scale).
Genuinely moving: integrable 0/20 (N = 12, 0.354–0.637), quasiperiodic
0/20 (0.558–1.612), metastable 0/20 (0.525–0.696, artifact-dominated —
§2 cap note; cap-above fraction 1.000 for all groups, so no verdict is
cap-dominated).

## 4. T-B results (main stage complete)

- **Rigidity curve h_sub(ε)** (realization means, 20 × 5 paired runs per
  point): 0.991 (ε = 0.01) → 0.939 (0.03) → 0.879 (0.06) → 0.806 (0.10)
  → 0.742 (0.16) → 0.652 (0.20). The locked peak survives the entire
  preregistered grid: **ε_c > 0.20 at our drive parameters** (measured;
  the SRC-044 value ≈ 0.11 at different parameters was never assumed).
- **DTC ε = 0.03 is a BH-004 candidate regime:** 100/100 states
  Φ-stationary under ε_Φ = 0.25 (max δΦ range 0.075–0.219) with the W5
  witness at 0.939 — stationary emergent geometry over witnessed
  period-2T microdynamics. ε = 0.06: 88/100 stationary; ε = 0.10: 52/100.
- **Switch-off (§4.2) resolves the preregistered open question to
  *compatible-with*:** removing the drive at n_off = 100 collapses W5
  (0.950 → 0.000) while Φ-stationarity persists and slightly improves
  (mean max post-drift 0.110 → 0.086). MBL holds the MI pattern without
  the drive — the honest reportable outcome the spec anticipated; the
  witnessed motion is not required to sustain this Φ.
- **r1 (no interactions, ε = 0.03):** W5 = 0.131 — peak destroyed, as
  predicted for the fine-tuned comparator (no rigidity without
  interactions). Φ trivially frozen (no entanglement generated; empty MI
  graph).
- **r2 (no disorder, ε = 0.03): comparator surprise.** W5 = 0.891 over
  200 periods — NOT thermalizing on this window, consistent with a
  prethermal DTC plateau in the clean interacting drive. The r2
  comparator does not discriminate at (ε = 0.03, 200 periods); recorded
  as a comparator-scope finding, not suppressed.

## 5. Battery (§4.3) and instrument notes

Battery MUST items (global phase, consistent local basis, reflection —
witness + MI identity at 1e-10, W1 read relative to its magnitude) PASS
for every group × size EXCEPT the metastable class, whose residuals sit
exactly in the two channels this class stresses: Ξ deviations up to
2.8e-9 (quasi-degenerate manifolds under jittered eigenbases; relative
to Ξ ≈ 4e-3 this is ~1e-6) and W1 3.9e-10 relative at N = 12. All are
ε_mach-amplification scale; no representation-dependence is indicated.
Recorded as measured. T-B protocol log ρ (descriptive): DTC ε = 0.03
quench 0.01 / dephasing 0.12 / loss 0.19; r2 −0.00 / 0.12 / 0.12 —
the DTC's Φ-robustness is comparator-level (MBL holds the pattern, cf.
the §4 switch-off finding).

Standing instrument notes: the 1e-10 identity contract binds
on witness statistics and MI matrices; Φ-space deviations carry an
irreducible numerical floor from the −log cap (up to 1/x_min = 1e6 ×
ε_mach, measured ~1e-9 in near-cap classes); W1's identity deviation is
read relative to its own magnitude (PR_A is O(10⁵⁻⁶) at N = 12). The
"state-only local basis change" item measures Φ's factorization-
dependence under strictly LOCAL frames as ~0 (provable: single-site
entropies are local-unitary invariant) — the TH-037 caveat lives at the
choice of site partition, not local frames; W3 changes by O(0.3–0.9)
as expected.

## 6. §6.2 numerics checks

Max state-norm drift across every unitary run: 4.0e-15 (bound 1e-10 ✓).
Dephasing trace drift recorded per run in the JSONs (same scale). Seeds
per committed manifest + addendum; pilot data excluded throughout.
Compute: ~3 h wall-clock as parallel background jobs (≪ 200 CPU-h
budget).

## 7. Outcome per §5.4 and KB effects

**Formal outcome — §5.4 row 3: criterion (a) FAILS → the witness scheme
returns to FORMALIZE; recorded negative (SC-005).** The failure is
narrow, single-cause, and constructive: the preregistered §4.4
null-discard removed W3, and the remaining battery under-determines
exactly one distinction (scrambling | localized). Findings of record
that survive alongside the negative:

1. **Criterion (b) HOLDS** — the robustness differential of
   Φ-stationarity is real, replicated at two sizes in both tracks under
   dephasing, with the pilot's class ordering confirmed (§3.2).
2. **§5.3 affirms sustained-by for all six dynamical classes** — the
   stationary comparator is far more fragile than the dynamical state
   (§3.3). BH-004's sustained-by clause has its first in-model support;
   promotion remains gated on AR-011 (KB-005 §10).
3. **T-B**: DTC ε = 0.03 is a stationary-with-witness regime (100/100);
   switch-off resolves to compatible-with (W5 collapse, Φ persistence);
   rigidity ε_c > 0.20 at our parameters; r2 comparator does not
   thermalize on the 200-period window (prethermal plateau) — recorded.
4. **W3 is not a valid CON-034 witness as instantiated** (fires on the
   null); the natural scrambling/localization discriminator needs a
   null-compatible reformulation (e.g. null-subtracted OTOC), and
   w2_mean-vs-w2_min is a second amendment candidate (min is
   structurally uninformative for slow classes). Both queued for
   owner/AR-011 — NOT applied post-hoc.
5. **T-A(ii) certificate unsatisfiable at N = 8** (exhaustive; Addendum
   1) — a spec-hygiene finding for any future size plan.

KB deltas applied this session (see session log): KB-004 BH-004 dated
evidence annotation (no epistemic-status change — AR-011-gated);
KB-005 AR-010 → EXECUTED/RECONCILED, AR-020 (witness-battery
reformalization) queued as owner-review candidate; AR-009 spec §8 dated
outcome entry (no preregistered content changed).
