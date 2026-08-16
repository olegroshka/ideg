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

[Superseded 2026-08-16 by Amendment A1.6: the canonical kickoff prompt
is the standalone `ar/AR-023a_KICKOFF_PROMPT.md` (v2). The blockquote
formerly embedded here had already diverged from the committed
standalone file; keeping two copies invited drift.]

## 5. Amendment 1 — 2026-08-16 (authoring side, pre-implementation)

Raised while iterating the kickoff prompt against the committed
scaffold state (07ab256). No S1/S2 gate value is changed; A1.1–A1.8
correct one factual error, fill voids the implementing session would
hit immediately, and freeze evaluation details before any sample is
drawn.

**A1.1 — §1 escalation step (ii) struck (factually dead).** The
25-point grid already failed the registered quadrature gate:
`0.13276 > 0.025`, recorded in
`hardware/ibm_exp1/manifest/sector_comparator_N10_run0.json`
(`checks.time_quadrature_error`) and the 2026-08-16 session log. The
quadrature error is a deterministic property of the grid; a re-run
cannot pass, so "reduce 37 → 25" is not an escalation path.
Replacement step (ii): raise shots 768 → 896 on the 37-point grid —
1,323 × 896 = 1,185,408 executions ≈ 416.9 s by the rough formula,
inside the 450 s cap with ≈ 33 s margin. (1,024 shots ≈ 476 s stays
over-cap; 960 shots ≈ 446.5 s leaves no margin and is not permitted.)
Step (iii) unchanged: if S1 gates still fail at 896 shots, return to
the AR-023 §8 ladder.

**A1.2 — QPY-bundle freeze bootstrap (fills a void).** As of commit
07ab256, no bundle bytes and no bundle hashes are committed anywhere:
the 2026-08-16 double build wrote them only to draft directories
outside the repository, so "verify their hashes" had no committed
referent. Frozen procedure: (1) rebuild the logical bundle with
`build_circuits.py` into two fresh directories; (2) require the QPY,
registry, target-state, and bundle hashes byte-identical across the
two builds (reproducing the recorded double-build result); (3) commit
`logical_circuits.qpy`, the circuit registry, and a hash record under
`hardware/ibm_exp1/bundle/`, and write the four hashes into the DRAFT
`hardware_manifest.json`; (4) from that commit on, the bundle is a
frozen input — verified by hash, never regenerated. The comparator
artifact is unaffected (its hash is already committed twice).

**A1.3 — mechanical evaluation of AR-023 §6 clauses 4 and 5 in
S1/S2.** Clause 4 (raw/mitigated direction agreement) in S1: run the
M3 branch calibrated on the ideal backend at the same shot budget; the
clause reads as written and doubles as an M3-plumbing check; report
median |ε_raw − ε_M3|. Clause 5 (no dominance) is operationalized for
S1/S2 evaluation only: the clause passes iff (a) leave-one-time-out
and leave-one-pair-out excursions of Δ each stay within 25% of the
experiment's median Δ and never flip its sign, and (b) the
projection-attributable endpoint shift is < 0.02 (the S2-G3
quantity). These numbers bind S1/S2 only; the hardware-run
operationalization is frozen at L4, with these values as the default
proposal.

**A1.4 — deterministic fake-backend pair selection (§2a).** If more
than two installed Heron-class fakes expose a connected 10-qubit line,
select the two with lexicographically smallest backend names; record
the full enumeration and the selection in `s2_report.json`.

**A1.5 — comparator-artifact scope of record.** The frozen artifact is
the minimal four-array NPZ (`p_star`, `eigenvalues`, `eigenvectors`,
`mode_pair_rdms`) plus JSON sidecar at
`hardware/ibm_exp1/manifest/sector_comparator_N10_run0.*` — not the
full AR-023 §11.3 array list, and not at §11.3's
`results/AR-023/preflight/` path. For this pilot the `manifest/` path
is the path of record; the remaining §11.3 arrays (ideal D-series,
D̄ grids, Φ[σ*], …) are S0/S1 derived outputs computed from committed
inputs into `hardware/ibm_exp1/results/sim_<id>/`, never by
regenerating the artifact.

**A1.6 — §4 superseded.** The standalone
`ar/AR-023a_KICKOFF_PROMPT.md` (v2) is the canonical kickoff prompt;
the §4 blockquote is retired.

**A1.7 — S1-G4 byte-determinism scope.** `s1_report.json` (and
`s2_report.json`) must contain no wall-clock timestamps, hostnames, or
absolute paths, and must be written as canonical JSON
(`sort_keys=True`, `ensure_ascii`, full-precision floats). Timestamps
and the environment freeze go in `s1_report.meta.json` /
`s2_report.meta.json`, which are excluded from the S1-G4 byte
comparison. This interprets the gate; it does not weaken it.

**A1.8 — sanctioned efficient S2 implementation.** "Run with Aer under
the fake backend's noise model" may be implemented as: density-matrix
simulate each transpiled circuit once per noise condition, apply the
readout confusion channel to the outcome distribution analytically,
then multinomial-sample replicates from the exact noisy distribution.
This is statistically identical to per-replicate shot execution and is
the intended implementation; per-replicate Aer re-execution is
permitted but not required.
