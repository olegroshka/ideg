# AR-023a — S1/S2 local-simulation specification (addendum to AR-023)

```yaml
id: AR-023a
parent: AR-023 (design of record; this file adds the numeric gates and
  procedures for its stages S1/S2 and does NOT modify AR-023)
authored: 2026-08-16, paper session (owner-requested), against the
  hardware scaffolding state of the same date (16 tests green, 1,323
  logical circuits built and hash-reproducible, run-0 T3 comparator
  export fail-closed and verified)
status: SPEC FROZEN for the implementing session; deviations become
  dated amendments in this file, never silent edits
```

## 0. Anchors of record (do not recompute ad hoc; cite these)

- Instance: `TA_ii_quasiperiodic`, N = 10, manifest run 0.
- Registered classical values (`results/AR-010/ar020e_sector_N10.json`):
  run-0 **T3 = 0.2241**, T1 = 0.0030; class T3 median 0.244.
- ε_Φ = 0.25 is the metric construction's calibrated finite-size noise
  floor (spec Amendment 3); the qp metric's own typical instantaneous
  drift is 0.26–0.33 (paper §6) — context for floor interpretation.
- Bundle: 1,323 circuits = 49 prepared states (37 times + 10 eigenmodes
  + 2 duplicate controls; 47 unique targets) × 27 settings, **768
  shots**; 37-time quadrature error 0.01465 < 0.025 (passed).
- **First required computation (before any sampling):** the exact
  37-grid endpoint ε_sector^(37) — Φ[σ*] vs D̄ on the hardware time
  grid through the same finite-grid pipeline — recorded in the
  manifest as the S1 reference value. (The 361-grid value is 0.2241;
  the 37-grid value is the S1 target and must be computed, not
  assumed.)

## 1. S1 — ideal finite-shot end-to-end simulation

**Procedure.** For each of the 1,323 circuits: exact outcome
distribution (statevector + basis rotations, from the verified QPY
bundle), multinomial sampling at 768 shots. Then the COMPLETE analysis
path, identical to the intended hardware path: per-state 45 pair-RDM
reconstruction from the 16-term Pauli expansion → hermitize → PSD clip
→ renormalize (recording ‖ρ_proj − ρ_raw‖_F) → MI (natural log) →
x-clip at 1e-6 → −ln weights → Floyd–Warshall → per-time metrics →
D̄_HW; comparator arm mixes eigenmode RDMs with the exported p*
BEFORE any entropy/metric step. Floors exactly as AR-023 §6: split-shot
(384/384 full-pipeline rerun) and duplicate-pair discrepancy; the
setting-aware bootstrap (1,000 replicates) runs the full path per
replicate. Repeat the whole synthetic experiment **R = 100** times with
independent sampling seeds.

**Seed policy (reproducibility, no tuning):** every random draw from
`np.random.SeedSequence([BASE, circuit_index, replicate_index])`;
BASE committed to the manifest before S1 results are inspected;
bootstrap seeds likewise `[BASE, 10**6 + replicate]`.

**Gates (all must pass to close S1):**
- **S1-G1 (bias):** |median over R of ε_sector^S1 − ε_sector^(37)| <
  0.02. This is the entropy-estimator-bias gate: finite-shot MI bias
  moves both arms; it must not move the endpoint materially.
- **S1-G2 (power):** the full AR-023 §6 success rule (all five
  clauses) fires in ≥ 95 of the 100 synthetic experiments.
- **S1-G3 (floor sanity):** median ε_floor < 0.05 (an ideal-noise
  floor at ~20% of the signal would leave no headroom for hardware).
- **S1-G4 (determinism):** rerunning with the committed seeds
  reproduces `s1_report.json` byte-for-byte.

**Escalation if any gate fails at 768 shots:** shots may rise ONLY
together with a budget re-check; 1,323 × 1,024 ≈ 1.354M executions ≈
476 s by the rough formula — OVER the 450 s cap. The permitted ladder
(AR-023 §8 order, made explicit): (i) drop the 2 duplicate circuits'
settings? NO — controls stay; (ii) reduce the time grid 37 → 25
(re-check quadrature ≤ 0.025 — it passed at 0.0146 for 37; the 25-point
gate must be re-run) giving 999 circuits × 1,024 = 1.023M ≈ 360 s;
(iii) only if both fail, return to AR-023 §8 for the full ladder.
Record every escalation as a dated amendment here.

## 2. S2 — noisy simulation (backend not yet selected)

Because L4 (backend selection) intentionally comes AFTER S2, S2 uses
two noise sources, both recorded exactly:

- **(a) Fake-backend arm:** enumerate the installed
  `qiskit-ibm-runtime` fake providers, select programmatically (do not
  hardcode names) the two Heron-class fakes with a connected 10-qubit
  line; transpile the bundle at optimization level 3,
  `seed_transpiler = 1701`, verify NO SWAP on the chosen line; run
  with Aer under the fake backend's noise model.
- **(b) Parameterized sweep arm:** synthetic noise grid — two-qubit
  depolarizing p2 ∈ {3e-3, 6e-3, 1e-2}, one-qubit p1 = p2/10, readout
  error ∈ {1e-2, 2e-2, 3e-2} (3×3 grid, thermal relaxation off) —
  bracketing current-generation device medians.

**M3 path:** calibrate M3 against the same noise model, apply to
counts; analysis produced RAW and M3 side by side, identical pipeline.
Leakage diagnostic (one-excitation survival) computed per state from
Z-rows, exactly as the hardware analysis will.

**Gates:**
- **S2-G1 (leakage):** on both fake backends and the mildest grid
  point: leakage GREEN per AR-023 §5 (median ≥ 0.90, min ≥ 0.80).
- **S2-G2 (power under noise):** success rule fires in ≥ 90/100
  synthetic experiments at the mildest grid point and on ≥ 1 fake
  backend. Report the grid's red line: the first noise level where the
  rule fails, and where leakage goes amber/red.
- **S2-G3 (projection control):** median per-RDM PSD correction
  ‖ρ_proj − ρ_raw‖_F < 0.05 AND endpoint shift attributable to
  projection < 0.02 at the operating point (evaluate by comparing
  projected vs unprojected pipelines on the same counts).
- **S2-G4 (mitigation coherence):** raw and M3 endpoints agree in
  direction of Δ in ≥ 95% of replicates at the operating point.

**Deliverable beyond gates:** the operating envelope — Δ versus noise
level — translated into an explicit L4 path-quality requirement
("median two-qubit error on the selected path ≤ X, readout ≤ Y"),
handed to backend selection as a frozen pre-commitment.

## 3. Artifacts and hygiene

- Results under `hardware/ibm_exp1/results/sim_<id>/`: `s1_report.json`,
  `s2_report.json`, power/envelope figure, complete environment freeze,
  seeds, and content hashes of the QPY bundle and comparator artifact
  used.
- README status list updated as gates close; one commit per milestone.
- S1/S2 code may iterate freely — that is their purpose — but the
  FINAL pipeline's content hash enters the frozen manifest, and after
  QPU data exist the pipeline is immutable (AR-023 §12 B7 discipline).
- No IBM credentials, no network calls to IBM, no QPU submission
  anywhere in S1/S2. `QPU-GO` remains owner-typed, later, after L4.

## 4. Kickoff prompt for the implementing session

Copy-paste to start the new session:

> Read CLAUDE.md first. Then read, in order:
> `ar/AR-023_hardware-pilot-2026-08-16.md` (design of record),
> `ar/AR-023a_s1s2-simulation-spec-2026-08-16.md` (this session's
> spec — its gates are frozen), `hardware/ibm_exp1/README.md`, and
> the anchors in `ar/AR-020e_sector-2026-08-16.md`.
>
> **Single target: implement and close S1 and S2 per AR-023a** (ideal
> finite-shot and noisy end-to-end simulations with their numeric
> gates), in `hardware/ibm_exp1/`. Definition of done: S1-G1..G4 and
> S2-G1..G4 evaluated and reported in committed `s1_report.json` /
> `s2_report.json` with the operating envelope; README status updated;
> a dated session log in `sessions/`; every gate result stated
> pass/fail with its measured number — no rounding a fail into a pass.
>
> Constraints: do not modify `paper/`, `substrate/`, or
> `ar/AR-023*.md` (deviations from AR-023a = dated amendments proposed
> in the session log, applied only to AR-023a); no IBM credentials or
> network calls; no QPU submission — `QPU-GO` does not exist in this
> session's vocabulary. The comparator artifact and QPY bundle are
> frozen inputs — verify their hashes, never regenerate them. If a
> gate fails, follow the escalation ladder in AR-023a §1 and record
> it; a failed gate honestly reported is a valid session outcome
> (negative results are results).
