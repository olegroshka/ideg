# Session 2026-08-12/13 — AR-010 confirmatory phase

- target: AR-010 confirmatory runs (owner-confirmed at session start;
  starting them closes the AR-019 window for good)
- mode: EXPERIMENT
- substrate versions at load: KB-001 v0.3, KB-002 v0.2, KB-003 v0.4,
  KB-004 v0.2, KB-005 v0.6
- substrate versions at close: KB-001 v0.3, KB-002 v0.2, KB-003 v0.4,
  KB-004 v0.3, KB-005 v0.7
- infrastructure notes: Python 3.11.14, numpy 2.3.5, scipy 1.15.3,
  Windows 11 workstation (24 logical cores, 31 GB). BLAS capped at 4
  threads per process for the parallel campaign.

## Warm-up check (KB-005 §17)

Parent chain resolves: AR-010 → AR-009 spec (frozen; §8 Amendments 1–3 +
AR-019 no-change entry) → BH-004 (KB-004 §4) → TH-033/TH-037 (SRC-043/044,
SRC-049 — primary-source verified 2026-08-11, AR-015 partial). No VERIFY
conversion needed. AR-019 reconciled RECONCILED/KEEP before this session;
its window closes at first confirmatory execution below.

## Plan (per amended spec; licensing KB-005 §21)

1. Per-size §6.3 sanity checks (N = 8, 12) BEFORE any confirmatory run.
2. Confirmatory manifest (seeds, sizes, ensembles, implementation
   clarifications) fixed and committed BEFORE execution.
3. Campaign: T-A (4 classes) at N = 8, 10; T-C (3 regimes) at N = 8, 10,
   12 (dephasing N ≤ 10 per §6.2); T-B at N = 10 (rigidity curve over an
   11-point ε grid + 3 preregistered DTC ε + r1/r2 comparators +
   switch-off + descriptive protocols). All witnesses W1–W5, comparators
   §4.1/§4.4, switch-off §4.2, battery §4.3, protocols §5.2 at the
   Amendment-3 strengths (λ = 0.1, γ = 0.01), ε_Φ = 0.25.
4. Analysis per §5.1 (AUC ≥ 0.95, ≥ 2 statistics, both sizes;
   class-(i) exact-value rule), §5.2 (|Δ mean log ρ| > ln 1.5, disjoint
   BCa CIs, two-size replication with §6.4 direction agreement), §5.3
   adjudication, §5.4 outcome mapping.

## Progress record

- §6.3 sanity N = 8: ALL PASS (chaotic ⟨r⟩ = 0.542; free-spectrum dev
  8.0e-15; localized ⟨r⟩ = 0.405, 20 realizations).
- §6.3 sanity N = 12: ALL PASS (chaotic ⟨r⟩ = 0.529; free-spectrum dev
  5.9e-14; localized ⟨r⟩ = 0.390, 20 realizations).
- Confirmatory manifest committed (b91ad54) with all implementation
  clarifications BEFORE execution; 29 unit tests green; every runner path
  smoke-tested at N = 6 against a scratch manifest (no confirmatory data
  touched).
- **AR-019 window CLOSED** at first campaign execution (6 parallel
  background jobs launched after the manifest commit).
- **Manifest Addendum 1 (a76db0e), measured obstruction:** the T-A(ii)
  incommensurability certificate (no p/q, q ≤ 50, within 1e-3) is
  EXHAUSTIVELY unsatisfiable at N = 8 — 0/56 nondegenerate-gap magnon
  triples pass (17/120 at N = 10; 27/220 at N = 12). The manifest's
  (8, 10) budget election is obstructed; T-A criterion sizing reverts to
  the spec §5.1 primary (10, 12). T-A N = 12 seeds fixed and committed
  BEFORE those runs launched. N = 8 runs for classes (i)/(iii)/(iv)
  remain valid (descriptive). T-A dephasing pairs involving class (ii)
  are single-size (N = 10, §6.2 bound) → ineligible for criterion-(b)
  replication, recorded as such.

## Implementation clarifications adopted (recorded in the manifest;
candidates for a clarifying spec note — none changes a preregistered
threshold)

- **Ξ (W4) degeneracy fix:** Ξ sums over energy-DISTINCT eigenpairs
  (grouping tol 1e-10). The spec's own defining property ("Ξ > 0 iff the
  state moves under H") fails for label-based m ≠ n on the degenerate XX
  spectrum (a superposition inside a degenerate level is stationary but
  had Ξ > 0). Unit-tested. Exploratory pilot Ξ values for XX-based groups
  shift slightly; no pilot conclusion depended on them.
- **log ρ numerator floor** at δ_floor (binds only for exactly-stationary
  objects under subsystem loss, where the spec formula reads log 0).
- **Subsystem-loss drift convention** and **switch-off ≡ diagonal-ensemble
  identity** (populations conserved ⇒ dephasing ψ(t_off) in the energy
  eigenbasis IS ρ̄; one computation reported under both headings).
- **Comparator fair-perturbation at N = 10** (dephasing is §6.2-bound to
  N ≤ 10; comparison kept within one size); comparator drift measured
  against Φ[ρ̄].
- **T-B protocols descriptive** (criterion (b) is preregistered over T-A
  classes / T-C regimes); T-B instrument = rigidity curve h_sub(ε).
- **W5 on periods 21..200** (even count: the rfft Nyquist bin is the exact
  period-2T line); T-B switch-off = lab-time H₂-alone continuation.
- **Battery instrument notes** (measured, not assumed): (i) the −log
  weight cap amplifies machine-epsilon MI jitter by up to 1/x_min = 1e6,
  so Φ-space identity deviations in near-cap classes (metastable) have an
  irreducible ~1e-9 floor — the 1e-10 identity contract binds on witness
  statistics and MI matrices, Φ-space deviation reported alongside;
  (ii) W1's identity deviation is read RELATIVE to its own magnitude
  (PR_A is O(10⁵⁻⁶) at N = 12; absolute 1e-10 would demand sub-ε_mach
  relative precision). Applied as one consistent rule in analysis over the
  recorded per-item deviations.
- **floquet_dtc paired draws:** J and h drawn unconditionally so r1/r2
  comparator realizations pair with DTC realizations at equal seed (DTC
  draw order unchanged; verified against the committed sanity record).

## Outcome

**Campaign executed and analysed in full per the preregistered plan**
(~3 h wall-clock, parallel background jobs; max norm drift 4.0e-15;
pilot data excluded). Verdicts of record
(results/AR-010/confirmatory_summary.json;
ar/AR-010_confirmatory-2026-08-12.md):

1. **§4.4 null: W3 FIRES** (c_sat ≈ 1.11, t* = 1.5 on the frozen class-(i)
   state) → discarded from the criterion-(a) set by the preregistered
   clause. The OTOC probes operator spreading, not state motion — not a
   valid CON-034 witness as instantiated.
2. **Criterion (a) FAILS** — T-A holds at (10, 12) (all six pairs, incl.
   (i, iv) via PR_A exact-value + Ξ); T-C fails at both sizes on
   scrambling|localized (Ξ only: 0.985/0.990; PR_A 0.8875/0.5575;
   min d_phys 0.705/0.945). Single-cause: retained-W3 t* would separate
   that pair at AUC 1.0. §5.4 row 3: witness scheme → FORMALIZE
   (SC-005 negative, → AR-020).
3. **Criterion (b) HOLDS** — dephasing replicates at two sizes in both
   tracks with direction agreement (T-C: all three pairs; ordering as
   piloted, quasiperiodic/metastable negative). Quench replicates only
   fixed-point pairs (floor-referenced; instrument note); loss null.
4. **§5.3: sustained-by for ALL six dynamical classes** — the diagonal
   ensemble is far more fragile than the dynamical state (quench
   log ρ ≈ 4.2 vs ≈ 0; dephasing 3.9–5.95 vs ≤ 2.2; disjoint CIs).
   Class (i): compatible-with (definitional).
5. **T-B:** DTC ε = 0.03 stationary-with-witness 100/100; switch-off →
   compatible-with (W5 0.95 → 0.00, Φ persists/improves); rigidity
   ε_c > 0.20 at our parameters; r1 comparator behaves as predicted;
   **r2 does not thermalize in 200 periods** (prethermal plateau) —
   comparator-scope finding.
6. Battery: MUST items pass everywhere except metastable residuals at
   1e-10..4e-9 (cap/quasi-degeneracy amplification; diagnosed numerical).

**Early finding of record (N = 8 outputs, preliminary): W3 fires on the
null.** The class-(i) eigenstate shows C(r_max, t) rising to c_sat ≈ 1.11
with t* = 1.5 — decisively time-dependent, refuting the §4.4 silence
prediction "W3: C(r, t) time-independent" (the state is frozen; the OTOC
probes operator spreading, which a gapped ground state supports). The §4.4
discard clause is itself preregistered, so W3's statistics (c_sat, t*)
leave the criterion-(a) set, which then runs on {PR_A, min d_phys, Ξ}.
Consequence for pair (i, iv): min d_phys is tied at machine zero
(recurrence DEPTH of a slowly-rotating state is ~0), so the pair rests on
the remaining two statistics. **Correction to the first in-session read:**
a rounded display suggested PR_A(iv) = 1 (tied with the null); precise
values show PR_A(iv) strictly above 1 with a clear margin at every size
measured (N = 8: [1.0071, 1.0105]; N = 12: [1.010, 1.012]) — the
transverse-dressing weight at the gap frequency. The exact-value rule
therefore separates (i, iv) on PR_A as well as on Ξ ([3.5e-3, 0.5] at
N = 8; [4.8e-3, 6.2e-3] at N = 12, excludes 0) — two statistics, so the
pair is expected to PASS despite the W3 discard (final verdict from the
preregistered analysis). w2_mean-vs-w2_min remains a spec-amendment
candidate for the record (min is uninformative for slow classes), no
longer verdict-relevant.

## Delta list

- ar/AR-009_spec.md §8: dated confirmatory-outcome entry (results of
  record; W3 discard operative; amendment candidates queued, NOT
  applied) — reason: close the preregistration loop in the spec's log.
- KB-004 §4 BH-004: dated evidence note appended; v0.2 → v0.3;
  changelog + last_reviewed — reason: AR-010 outcome; no
  epistemic-status change (AR-011-gated).
- KB-005 §6 AR-010: → EXECUTED/RECONCILED with outcome line; §6 AR-019:
  window-closed line; §6 AR-020 added (PROPOSED, owner review pending);
  §23 changelog; v0.6 → v0.7 — reason: campaign executed and
  reconciled.
- ar/AR-010_confirmatory-2026-08-12.md: new evidence packet.
- results/AR-010/: confirmatory_manifest.json, addendum 1, per-size
  sanity, confirmatory/*.json, confirmatory_summary.json (committed).
- src/ideg/ + scripts/ + tests/: confirmatory infrastructure (committed
  b91ad54, a76db0e pre-execution).
- CLAUDE.md current-state block updated.
- Nothing marked STALE (no downstream item depended on a changed value).

## ADR candidates raised

None. (All findings live at spec/witness-instrument level; intent
untouched.)

## Open items

1. **AR-011 adversarial companion** — required before any promotion
   (KB-005 §10); natural next-session target. Attack surface is rich:
   floor-referenced quench log ρ for class (i); Ξ margins for
   metastable (4e-3-scale); localized ε_Φ straddle (80/100 at N = 12);
   cap-uniformity of stationarity verdicts.
2. **Owner review of AR-020** (witness reformalization: null-compatible
   W3 variant; w2_mean-vs-min) and of the two spec-amendment candidates
   recorded in spec §8.
3. AR-019 conditional follow-up now LIVE: criterion (b) returned a
   positive → the strength-grid decay-rate-law analysis is a fundable
   AR candidate (owner to decide).
4. T-B rigidity grid never crosses h_sub = 0.5 → ε_c > 0.20 is a bound,
   not a location; extending the grid is a cheap follow-up if wanted.
5. r2 comparator non-thermalizing at 200 periods (prethermal plateau) —
   any future T-B use of r2 as a "thermalizing" control needs a longer
   window or a different clean comparator.
6. Carried: SRC-052..058 metadata verification (AR-002-series);
   localized ε_Φ straddle size-scaling; W1 metastable-doublet
   limitation (Ξ carries TA_iv separation — margin now quantified).
