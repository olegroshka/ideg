# Session 2026-08-12 — AR-010 confirmatory phase

- target: AR-010 confirmatory runs (owner-confirmed at session start;
  starting them closes the AR-019 window for good)
- mode: EXPERIMENT
- substrate versions at load: KB-001 v0.3, KB-002 v0.2, KB-003 v0.4,
  KB-004 v0.2, KB-005 v0.6
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

(in progress — campaign running)

**Early finding of record (N = 8 outputs, preliminary): W3 fires on the
null.** The class-(i) eigenstate shows C(r_max, t) rising to c_sat ≈ 1.11
with t* = 1.5 — decisively time-dependent, refuting the §4.4 silence
prediction "W3: C(r, t) time-independent" (the state is frozen; the OTOC
probes operator spreading, which a gapped ground state supports). The §4.4
discard clause is itself preregistered, so W3's statistics (c_sat, t*)
leave the criterion-(a) set, which then runs on {PR_A, min d_phys, Ξ}.
Consequence at N = 8: pair (i, iv) separates on Ξ only (PR_A tied at 1 —
known W1 doublet blindness; min d_phys tied at machine zero — recurrence
depth of a slowly-rotating state is ~0), i.e. ONE statistic where (a)
requires two. All other pairs separate on ≥ 2. Two integrity notes:
(i) the outcome does not hinge on the Ξ degeneracy fix — label-based Ξ
also leaves (i, iv) with a single separating statistic once W3 is
discarded; (ii) w2_mean (≥ 3.5e-3 for class (iv)) WOULD separate the pair
but §5.1 preregisters min, not mean — recorded as a spec-amendment
candidate for owner/AR-011 review, not applied.

## Delta list

(pending campaign completion)

## ADR candidates raised

None so far.

## Open items

(pending)
