# AR-020 — Witness-battery reformalization (evidence packet)

```yaml
id: AR-020
title: "Witness-battery reformalization after the AR-010/AR-011 negative"
mode: FORMALIZE
parent: BH-004, CON-034; requirements set by AR-011
priority: P0 (owner-approved as scoped, 2026-08-13)
inputs: [ar/AR-010_confirmatory-2026-08-12.md,
         ar/AR-011_adversarial-2026-08-13.md,
         results/AR-010/confirmatory/*.json,
         results/AR-010/ar020_comparator_probe.json]
question: >
  (1) Is there a null-silent witness statistic set that doubly-witnesses
  every class pair, including scrambling|localized? (2) Does a
  Phi-matched motionless comparator exist in the family, or is its
  absence provable/characterizable?
deliverable: this packet; spec §8 Amendment 4 (owner-ratified);
  fresh-seed confirmatory witness runs re-adjudicating criterion (a)
promotion_effect: criterion (a) becomes re-adjudicable; BH-004's
  witnessed-stationarity leg unblocks
kill_effect: none reached (the requirement had a constructive answer)
status: DONE (2026-08-13; Amendment 4 ratified + executed; fresh-seed
  re-adjudication FAILS on scrambling|integrable at N = 10 — recorded
  negative, three forward paths queued for owner)
```

## 1. Requirement 1 — the null-silent statistic set

**Proposal: replace the criterion-(a) statistic set
{PR_A, min d_phys, C_sat, t*, Ξ} with {PR_A, w2_mean (mean d_phys), Ξ}.**

- **Null-silence:** w2_mean ≡ 0 identically for any frozen state
  (d_phys(t) = 1 − |⟨ψ(t_eq)|ψ(t)⟩|² vanishes under global-phase
  evolution) — measured on the class-(i) null at machine zero
  (−4.6e-15). It is a witness OF state motion in exactly the CON-034
  sense: it vanishes iff the motion stops. PR_A and Ξ retain their
  proven silence (PR_A = 1, Ξ = 0 on the null; §4.4 record).
- **W3 (OTOC) is REMOVED as a CON-034 witness** (fires on the null —
  AR-010 finding of record); retained in the outputs as a descriptive
  operator-spreading diagnostic only. min d_phys demoted to descriptive
  (structurally uninformative for slow classes — AR-011).
- **Validation on the existing confirmatory data (post-hoc, labeled as
  such):** all 18 pair × size checks pass with ≥ 2 separating
  statistics — including the previously-failing scrambling|localized
  pair at BOTH criterion sizes (w2_mean AUC 0.985/0.985; Ξ 0.985/0.99).
  Full table in the session log. Because the redesign was informed by
  this data, the table is VALIDATION; the confirmatory re-adjudication
  uses fresh manifest-committed seeds (witness-only runs — no
  perturbation protocols needed for criterion (a)).

## 2. Requirement 2 — the Φ-matched motionless comparator

Probe (results/AR-010/ar020_comparator_probe.json): minimize
‖Φ[σ] − D̄‖/‖D̄‖ over three natural stationary families ([H, σ] = 0:
thermal e^{−βH} incl. β < 0; depolarized ρ̄; Gaussian microcanonical),
one representative run per class, N = 10:

| class | ρ̄ (AR-011) | best family miss | family |
|---|---|---|---|
| chaotic | 0.619 | **0.066** | microcanonical |
| metastable | 0.896 | 0.234 | depolarized ρ̄ |
| localized | 0.392 | 0.316 | microcanonical |
| quasiperiodic | 0.465 | 0.361 | thermal |

**Class-split answer.** For the CHAOTIC class a Φ-matched motionless
comparator EXISTS constructively (microcanonical, miss 0.066 ≪ ε_Φ) —
ETH-consistent: the chaotic running geometry is thermal, so at the
geometry level the chaotic classes lean *compatible-with*. For the
coherence-carried classes (quasiperiodic, metastable) and localized,
every natural family misses at ≳ ε_Φ: **the running geometry has no
natural motionless counterpart — it is motion-borne.** This sharpens
BH-004's sustained-by claim along class lines and corrects the
narrative once more: the strongest sustained-by evidence lives in the
quasiperiodic/metastable/localized classes, not the chaotic ones.
Caveat (recorded): family-relative statement (three natural families,
grid-optimized, one run per class) — not an impossibility proof; a
general diagonal-state optimization is a bounded follow-up if AR-011-
style adversarial pressure demands it.

> **CORRECTION (2026-08-13, hardened probe AR-020b —
> `results/AR-010/ar020b_hardened_probe_N{10,12}.json`).** The
> family-relative miss claims above are PARTIALLY REFUTED by the
> general smooth-f(H) optimization over full ensembles at both
> criterion sizes: metastable (20/20 matched, median 0.091–0.132),
> integrable (20/20, 0.161–0.170) and partially localized (3–6/20,
> median ≈ 0.27, boundary) ARE matchable within ε_Φ. **The
> size-robust survivor is the QUASIPERIODIC class alone: 0/40 matched
> across both sizes, median miss 0.32–0.34.** The corrected finding:
> only incommensurate coherence-carried motion produces a
> time-averaged geometry that no searched stationary state (three
> natural families + smooth-f(H), K = 12 Chebyshev, Powell) can
> reproduce — the same class singled out by the negative dephasing
> log ρ. Chaotic/scrambling matches strengthen (median 0.035–0.046).
> Scope: smooth-f(H) parameterization; not an impossibility proof over
> arbitrary diagonal states. Third self-correction of the cycle,
> caught internally before publication.

## 3. Proposed spec §8 Amendment 4 (owner ratification required)

1. §5.1 statistic set → {PR_A, w2_mean, Ξ}; min d_phys and the W3
   statistics demoted to descriptive outputs; §3 W3 loses its CON-034
   witness designation (kept as a diagnostic; its §4.4 failure is the
   recorded reason).
2. §4.1 matching language corrected: the diagonal ensemble matches the
   time-averaged two-site RDMs, NOT the MI graph (AR-011); the
   class-split comparator finding (§2 above) is recorded; for future
   sustained-by adjudications the chaotic-class comparator of choice is
   the fitted microcanonical state (parameters preregistered from the
   probe method, fitted per run).
3. Criterion (a) re-adjudication runs on FRESH manifest-committed seeds
   (witness-only; both criterion sizes; ensembles as before). The
   existing-data table is validation only.
4. No thresholds change (AUC ≥ 0.95, ≥ 2 statistics, two sizes,
   exact-value rule for class (i) — all as amended through
   Amendment 3).

## 4. Outcome

**Amendment 4 ratified and executed; fresh-seed re-adjudication:
criterion (a) FAILS — honestly, on a different pair.** Fresh seeds
(addendum 2, committed pre-execution; results in rerun_summary.json):

- T-A: HOLDS — all six pairs, both sizes, every statistic separating.
- The AR-020 target pair scrambling|localized now PASSES at both sizes
  (w2_mean 0.97/0.985; Ξ 0.9775/0.9925) — the reformalization achieved
  its design requirement.
- **scrambling|integrable FAILS at N = 10** (pr_A 0.925, w2_mean 0.85,
  Ξ 0.855 — no statistic reaches 0.95) while passing at N = 12
  (0.955/0.9475/0.95). Two-size replication therefore fails.

Findings of record:

1. **The fresh-seed discipline earned its keep:** the same battery
   passed 18/18 on the original (redesign-informing) seeds — the
   scrambling|integrable margin at N = 10 is genuinely threshold-
   straddling (AUC SE ≈ 0.05–0.08 at n = 20), and the original pass
   (0.9525/0.95) was partly seed luck. A validation-only adoption would
   have over-claimed.
2. The remaining obstruction is FINITE-SIZE, not structural: the
   scrambling|integrable distinction sharpens with N (all three
   statistics rise from N = 10 to 12). The battery has no null-silence
   defect and no under-witnessed pair left; what it lacks is resolving
   power at the smaller criterion size.
3. Paths forward (owner decision; none enacted): (a) accept and report
   — the paper states witnessed class separation holds at N = 12 and is
   threshold-marginal at N = 10; (b) extend to criterion sizes (12, 14)
   — N = 14 needs Krylov (the spec's own noted amendment path);
   (c) raise ensemble size (n = 40 halves the AUC SE) at the current
   sizes — cheapest fix, needs a dated amendment + fresh seeds.

## 5. Amendment 5 and the FINAL verdict (owner ruling: n = 40 then
accept)

Amendment 5 ratified and executed same-day (addendum-3 fresh seeds,
n = 40, both sizes; ~30 min compute). **Criterion (a): HOLDS — all 18
pair × size checks pass** (rerun40_summary.json). The marginal pair
stabilized above threshold (scrambling|integrable N = 10:
0.9788/0.9519/0.9563); scrambling|localized passes both sizes
(w2_mean + Ξ ≈ 0.987–0.992). Verdict accepted as final per the ruling.

Honest dual-record framing (mandatory in all downstream use): the
ORIGINAL preregistered battery failed its own null test; criterion (a)
holds under the owner-ratified reformalized battery on fresh seeds at
stabilized ensembles. Both facts are results.

§5.4 row-1 effects now standing: BH-004 supported in-model (evidence
note updated); **BH-005 licensed** (BH-004 survived); HYP-009's
geometric part has its first model realization (dated evidence line;
status unchanged — owner scope note of 2026-08-13 stands).

Ops incident (recorded): the first Amendment-5 launch wrote n = 40 data
over the Amendment-4 filenames (the runner's output prefix was defined
but unused — my defect). Recovery: n = 40 data renamed to rerun40_*,
n = 20 files restored byte-identical from commit 5efaa73, runner fixed.
No data lost; the incident and fix are in the session log.

