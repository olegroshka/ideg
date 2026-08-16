# AR-023 — IBM Quantum hardware pilot for the quasiperiodic stationary-impostor result

```yaml
id: AR-023
title: "IBM Quantum hardware pilot for the quasiperiodic stationary-impostor result"
mode: DESIGN
parent: AR-010, AR-020
priority: P1 (owner-requested implementation roadmap, 2026-08-16)
inputs: [ar/AR-010_confirmatory-2026-08-12.md,
         ar/AR-020_reformalization-2026-08-13.md,
         results/AR-010/confirmatory_manifest.json,
         results/AR-010/ar020e_sector_N10*.json,
         paper/latex/main.tex]
question: >
  Does the best stationary state confined to the dynamically accessible
  one-magnon sector still fail to reproduce the hardware-reconstructed
  time-averaged information metric for the registered N=10 quasiperiodic
  instance, by more than the hardware reconstruction floor?
deliverable: executable IBM Quantum Open Plan roadmap, frozen analysis
  contract, browser-assisted submission protocol, and SparQ scaling path
promotion_effect: one-instance exploratory hardware validation only;
  cannot promote the paper's full multi-class claim or establish advantage
kill_effect: red sector leakage, reconstruction-dominated separation, or
  a bootstrap interval for the primary separation that includes zero
status: DESIGN COMPLETE; EXECUTION BLOCKED pending final AR-020e output and
  serialization/freezing of the selected T3 comparator populations
```

**Paper:** *The price of standing still: stationary impostors for emergent information metrics*  
**Primary paper instance:** `TA_ii_quasiperiodic`, `N=10`, manifest run index `0`  
**Intended platform:** IBM Quantum Open Plan first; NQCC SparQ follow-on  
**Experiment type:** preregistered hardware pilot, not a claim of quantum advantage  
**Last updated:** 2026-08-16

---

## 1. Executive decision

Run the paper's actual ten-site quasiperiodic one-magnon instance on one IBM QPU and ask one narrow question:

> After reconstructing the same mutual-information metric from hardware measurements, does the best stationary state confined to the dynamically accessible one-magnon sector still fail to reproduce the time-averaged moving geometry by more than the hardware reconstruction floor?

The primary hardware arm will prepare shallow, exact snapshots of the analytically evolved one-magnon state. This is **state-realization mode**: it validates the paper's geometry reconstruction and sector-admissibility separation on real hardware without pretending that a deep circuit physically evolved for paper times `t=20...200`. A small optional Trotter subset can validate the dynamical circuit construction, but it is secondary.

Use `N=10`, not `N=6` or `N=8`. The paper's incommensurability certificate is exhaustively unsatisfiable at `N=8` (0/56 mode triples), so a smaller demonstration would no longer instantiate the registered quasiperiodic class.

One combined Sampler job should contain approximately 999 circuits at 1,024 shots, or about 1.02 million executions. IBM's rough no-mitigation estimate is approximately 360 QPU seconds before device-specific circuit duration, reset delay, calibration, and mitigation overhead. The submission gate is an estimated total below 450 seconds, leaving safety margin inside the standard 600-second Open Plan allowance.

---

## 2. What this experiment can and cannot establish

### It can establish

1. The paper's pairwise-information geometry can be reconstructed on an IBM QPU for the selected `N=10` quasiperiodic instance.
2. The hardware time-averaged metric is measurably separated from the best **sector-pinned stationary comparator** fixed by the classical study.
3. The separation is larger than shot, reconstruction, and observed drift floors under a frozen analysis pipeline.
4. The result survives both raw and readout-mitigated analysis, with sector leakage reported explicitly.

### It cannot establish

1. Quantum advantage or a classically inaccessible calculation.
2. Long-time coherent evolution to `t=200` on the processor; the primary arm directly prepares each exact evolved snapshot.
3. A universal statement about all stationary states or all notions of geometry.
4. A hardware realization of gravity, holography, or a new phase of matter.

The precise paper wording after a positive result should be: **"a hardware pilot reproduced the qualitative sector-admissibility separation for one preregistered `N=10` instance."**

---

## 3. Frozen scientific specification

### 3.1 Model and state

Use the paper convention

\[
H=\frac12\sum_{i=0}^{8}\left(X_iX_{i+1}+Y_iY_{i+1}\right),
\]

with open boundaries and `J=1`. Within the one-magnon sector this is the ten-site hopping matrix with unit off-diagonal entries.

Recreate the state only from the committed manifest:

- class: `TA_ii_quasiperiodic`
- size: `N=10`
- run: index `0`
- seed: read from `results/AR-010/confirmatory_manifest.json`; never type a replacement seed manually
- constructor: `ideg.states.magnon_superposition`
- time window: `20.0` through `200.0`, step `0.5` in the full classical reference

The run-selection rule is fixed before hardware data exist. Do not inspect multiple hardware runs and retain the most favourable one. If run 0 fails a preflight requirement for a reason already visible in ideal simulation, document the reason and freeze a deterministic replacement rule before any QPU submission.

### 3.2 Exact snapshot amplitudes

Let `a(0)` be the ten-component site-amplitude vector of the selected one-magnon state. Diagonalize the one-magnon hopping matrix once:

\[
h_1=V\,\mathrm{diag}(E_k)V^\dagger,
\qquad
a(t)=V\,\mathrm{diag}(e^{-iE_kt})V^\dagger a(0).
\]

Prepare

\[
|\psi(t)\rangle=\sum_{s=0}^{9} a_s(t)|1_s\rangle
\]

directly with a nearest-neighbour complex Givens ladder. Start from one excitation and use at most nine neighbouring two-qubit mixing stages plus the required phases. Compare two implementations in local compilation:

1. a hand-built ladder based on `XXPlusYYGate(theta, beta)`;
2. Qiskit's generic state-preparation synthesis.

Freeze whichever has the lower two-qubit count/depth on the selected physical path, provided its exact statevector infidelity is below `1e-10` for every target state.

**Endianness rule:** the paper uses site 0 as the most-significant tensor factor; Qiskit statevector index bits use qubit 0 as the least-significant bit. Use the explicit mapping `qiskit_qubit = N - 1 - paper_site`, test it, and store it in the manifest. Never repair an apparent mirror image during analysis by eye.

### 3.3 Primary time grid

Start with 25 deterministic samples taken from the paper's 361-point grid:

```python
full_times = np.arange(20.0, 200.0 + 1e-9, 0.5)
indices = np.unique(np.rint(np.linspace(0, 360, 25)).astype(int))
hardware_times = full_times[indices]
```

Preflight requirement:

\[
\frac{\|\bar D_{25}^{\rm ideal}-\bar D_{361}^{\rm ideal}\|_F}
{\|\bar D_{361}^{\rm ideal}\|_F}\le 0.025.
\]

If this fails, try 37 and then 49 points with the same deterministic rule. Re-estimate QPU usage and reduce shots if needed. Do not silently choose visually favourable times. Write the final indices and values into the hardware manifest before compilation.

### 3.4 Sector-pinned stationary comparator

For this open XX chain, the one-magnon energy levels are nondegenerate. The admissible stationary comparator therefore has the form

\[
\sigma^*_{\rm sector}=\sum_{k=0}^{9}p_k^*|E_k,q{=}1\rangle\langle E_k,q{=}1|.
\]

The ten weights `p_star` must be the final optimizer output for the selected paper run, frozen **before** hardware data are accessed.

Important current dependency: `scripts/ar020e_sector_suite.py` writes the T3 miss and diagnostics but does not currently serialize the optimized block matrices/populations. Add a result-export step that writes:

- `p_star` in a fixed eigenvalue ordering;
- the corresponding ten eigenvalues and eigenvectors' content hash;
- optimizer objective and full-density-matrix recheck;
- seed, run index, code commit, and output-file hash;
- normalization, minimum population, stationarity residual, and sector-weight checks.

Do not re-optimize `p_star` against hardware data.

On hardware, do not attempt to prepare `sigma*` as a coherent pure state. Prepare each eigenmode `|E_k,q=1>` separately, reconstruct its pair reduced density matrices, then mix **density matrices first**:

\[
\rho_{ij}^{\sigma^*}=\sum_k p_k^*\rho_{ij}^{(k)}.
\]

Only after mixing the RDMs should mutual information and the metric be computed. Averaging the ten metrics would be mathematically wrong because the metric functional is nonlinear.

---

## 4. Measurement design: all pair RDMs in 27 settings

The paper requires every two-site reduced density matrix, not only populations. Full local Pauli tomography naively needs `3^10` settings. Instead use a 27-row strength-two covering array over `X/Y/Z` that covers all nine ordered basis pairs for every one of the 45 qubit pairs exactly three times.

Enumerate all rows `r=(r0,r1,r2)` in `GF(3)^3`. Assign the ten logical qubits these projective vectors:

```text
v0=(1,0,0)  v1=(0,1,0)  v2=(0,0,1)  v3=(1,1,0)  v4=(1,2,0)
v5=(1,0,1)  v6=(1,0,2)  v7=(0,1,1)  v8=(0,1,2)  v9=(1,1,1)
```

For row `r`, qubit `i` receives symbol `dot(r, vi) mod 3`, with `0 -> X`, `1 -> Y`, and `2 -> Z`. Apply basis rotations:

- `X`: `H`
- `Y`: `Sdg`, then `H`
- `Z`: no rotation

Unit test the covering property for all 45 pairs before building any QPU job.

From the measured Pauli expectations reconstruct

\[
\rho_{ij}=\frac14\sum_{a,b\in\{I,X,Y,Z\}}
\langle\sigma_a\otimes\sigma_b\rangle
\,\sigma_a\otimes\sigma_b.
\]

For each estimate:

1. hermitize: `(rho + rho.conj().T)/2`;
2. record trace and the most negative eigenvalue;
3. project to the positive semidefinite cone by clipping negative eigenvalues;
4. renormalize to trace one;
5. record `||rho_projected-rho_raw||_F`.

Apply the identical reconstruction to all arms, all bootstrap samples, raw counts, mitigated counts, and simulator controls. If positivity projection is large enough to control the headline result, the hardware claim fails even if the plotted curves look attractive.

This full tomography is intentional: it does not assume that noisy hardware remained inside the ideal one-magnon sector.

---

## 5. Arms, controls, and circuit count

| Arm | Prepared states | Settings each | Circuits | Purpose |
|---|---:|---:|---:|---|
| A: moving snapshots | 25 | 27 | 675 | reconstruct each `D(t)` and then `Dbar_HW` |
| B: stationary sector basis | 10 | 27 | 270 | construct the fixed `sigma*_sector` mixture |
| C: drift/null duplicates | 2 | 27 | 54 | repeated eigenmode at early/late job positions |
| **Primary total** | **37** |  | **999** | approximately 1.02M executions at 1,024 shots |

Randomize/interleave circuit order with a frozen seed while ensuring the two control duplicates bracket the job. Store an inverse permutation so results return to logical order.

Optional Arm D, included only if the usage estimate remains safely below the cap: use three short physical-evolution checkpoints and compare a first-order/even-odd XX Trotter circuit with the exact snapshot at the same time. This is a circuit-validation appendix, not part of the primary endpoint.

Every prepared state also receives a sector-leakage diagnostic from its Z-basis data: the probability that the measured bit string has exactly one excitation. Use the appropriate rows already present in the covering array; add no redundant circuits unless required by the mitigation package.

### Leakage traffic light

- **Green:** median one-excitation survival at least 0.90 and minimum at least 0.80.
- **Amber:** median in `[0.80, 0.90)`; complete analysis but label it a noisy feasibility result.
- **Red:** any primary state below 0.70, or the result becomes controlled by PSD projection; do not make the primary scientific claim.

---

## 6. Frozen metric and endpoints

For every reconstructed pair RDM compute natural-log von Neumann entropies and

\[
I(i:j)=S(\rho_i)+S(\rho_j)-S(\rho_{ij}).
\]

Use exactly the paper's metric implementation:

\[
x_{ij}=\mathrm{clip}\left(\frac{I(i:j)}{2\ln2},10^{-6},1\right),
\quad w_{ij}=-\ln x_{ij},
\]

followed by all-pairs shortest paths. Do not tune the floor after hardware results.

The moving target is

\[
\bar D_{\rm HW}=\frac{1}{T}\sum_t\Phi[\rho_{\rm HW}(t)].
\]

It is **not** `Phi` of a time-averaged state or a time-averaged RDM.

The primary endpoint is

\[
\epsilon_{\rm sector}^{\rm HW}=
\frac{\|\Phi[\sigma^*_{\rm sector,HW}]-\bar D_{\rm HW}\|_F}
{\|\bar D_{\rm HW}\|_F}.
\]

### Technical floor

Use two independent diagnostics:

1. randomly split every circuit's shots into two equal halves and reconstruct both complete arms independently;
2. compare the duplicated eigenmode circuits placed near the beginning and end of the job.

Define `epsilon_floor` conservatively as the larger median normalized discrepancy produced by these two diagnostics. Use a nested, setting-aware bootstrap with 1,000 replicates to propagate count noise through readout correction, RDM projection, entropy, shortest paths, time averaging, and the comparator mixture.

### Success rule

The pilot is positive only if all of the following are true:

1. the 95% bootstrap interval for `Delta = epsilon_sector_HW - epsilon_floor` is strictly above zero;
2. median `epsilon_sector_HW >= 2 * median epsilon_floor`;
3. the primary leakage gate is not red;
4. raw and readout-mitigated estimates agree in direction;
5. no single time, pair, or large PSD projection dominates the result.

As a predeclared secondary comparison, report whether the hardware median is within `0.10` absolute of the exact finite-grid value and remains above `0.15`. These numerical bounds are pilot tolerances, not replacements for the paper's registered `epsilon_Phi` threshold. Hardware has its own measurement floor, so do not reuse the paper's `0.25` threshold as the sole decision rule.

Also report the hardware noncommutation diagnostic

\[
\frac{\|\Phi[\overline{\rho}_{\rm pair}]-\overline{\Phi[\rho(t)]}\|_F}
{\|\overline{\Phi[\rho(t)]}\|_F},
\]

where `Phi[average pair RDMs]` and `average Phi` are calculated through the same reconstructed-data pipeline.

---

## 7. IBM backend and compilation policy

Do not hardcode a backend name in the paper or scripts. At execution time:

1. list operational QPUs accessible to the user's Open Plan instance;
2. prefer a current Heron processor when available, but select on measured path quality rather than family name alone;
3. enumerate every connected ten-qubit simple path in the backend coupling map;
4. score each path before outcome data exist using:
   - maximum and median two-qubit error on path edges;
   - maximum and median readout error;
   - compiled two-qubit count and depth for the full circuit family;
   - worst edge as a tie-breaker;
5. freeze the backend, physical path, score formula, calibration timestamp, and backend-properties snapshot.

Compile with a preset pass manager at optimization level 3, fixed `seed_transpiler=1701`, and `initial_layout=<frozen path>`. Check every compiled circuit:

- exactly the intended ten physical qubits are used;
- no SWAP is introduced; if a SWAP appears, reject the path or state-preparation layout;
- measurement-to-logical-bit mapping is saved;
- two-qubit count/depth and total duration are recorded;
- circuit parameters are fully bound;
- exact logical-circuit fidelity passed before hardware compilation.

Fractional gates may be evaluated during local compilation if the selected backend supports them, but keep only one frozen compilation path. IBM documents restrictions between fractional gates and some mitigation features. The primary plan therefore uses Sampler, explicitly disables gate twirling and dynamical decoupling, and applies M3 readout mitigation during analysis. Do not add ZNE or other advanced mitigation to a 10-minute pilot.

---

## 8. QPU-time budget and degradation ladder

At 999 circuits and 1,024 shots:

```text
executions = 999 * 1024 = 1,022,976
rough_seconds = 2 + 0.00035 * executions ~= 360 seconds
```

This IBM formula is only an initial estimate. Before submission, use the compiled circuits and the current backend to obtain the platform's available usage estimate, then add M3 calibration overhead and margin.

Hard gates:

- estimated primary job at or below 450 QPU seconds;
- `max_execution_time` set conservatively, normally 480 seconds;
- at least 500 Open Plan seconds visibly remaining before submission;
- total executions below IBM's Sampler job limit;
- no optional arm if it endangers primary completion.

If over budget, degrade in this order:

1. remove optional Trotter circuits;
2. reduce shots from 1,024 to 768 and rerun finite-shot simulation;
3. reduce duplicate controls while retaining split-shot analysis;
4. only then reduce time points, and only if the time-quadrature gate is rechecked.

Never reduce tomography settings, remove difficult pairs, or select a better-looking subset after seeing QPU results.

Open Plan users cannot use Runtime sessions, so submit the primary circuits as one SamplerV2 job rather than many sub-minute jobs. Failed or user-cancelled jobs can still consume usage; local validation must therefore be complete before submission.

---

## 9. Reproducible project layout

Add the following under the paper repository after the current classical runs finish:

```text
hardware/ibm_exp1/
  README.md
  requirements-hardware.txt
  manifest/
    hardware_manifest.json
    hardware_manifest.schema.json
  scripts/
    export_sector_comparator.py
    prepare_manifest.py
    build_circuits.py
    select_backend_path.py
    estimate_usage.py
    run_local.py
    submit_ibm.py
    fetch_ibm.py
    analyze.py
  tests/
    test_covering_array.py
    test_endianness.py
    test_state_prep.py
    test_rdm_reconstruction.py
    test_metric_parity.py
    test_manifest_frozen.py
  results/
    <run_id>/
      manifest.json
      manifest.sha256
      circuits.qpy
      transpile_report.json
      backend_snapshot.json
      usage_estimate.json
      job_receipt.json
      raw_result.*
      analysis.json
      figures/
```

Suggested hardware-only dependencies, pinned after a clean local installation succeeds:

```text
qiskit
qiskit-aer
qiskit-ibm-runtime
mthree
pytest
```

Do not disturb the paper's core dependency set. Put hardware dependencies in a separate file and record exact installed versions in every result bundle.

### Required command interfaces

Each script should support `--help` and fail closed:

```powershell
python hardware/ibm_exp1/scripts/export_sector_comparator.py --n-sites 10 --run-index 0
python hardware/ibm_exp1/scripts/prepare_manifest.py --n-sites 10 --run-index 0 --time-count 25 --shots 1024
python hardware/ibm_exp1/scripts/run_local.py --manifest hardware/ibm_exp1/manifest/hardware_manifest.json
python hardware/ibm_exp1/scripts/select_backend_path.py --manifest ... --backend AUTO
python hardware/ibm_exp1/scripts/build_circuits.py --manifest ...
python hardware/ibm_exp1/scripts/estimate_usage.py --manifest ...
python hardware/ibm_exp1/scripts/submit_ibm.py --manifest ... --confirm QPU-GO
python hardware/ibm_exp1/scripts/fetch_ibm.py --job-id <IBM_JOB_ID>
python hardware/ibm_exp1/scripts/analyze.py --result-dir hardware/ibm_exp1/results/<run_id>
```

`submit_ibm.py` must refuse to run unless:

- the manifest hash matches the compiled bundle;
- all tests and preflight gates are green;
- `--confirm QPU-GO` is present;
- the usage estimate is inside the cap;
- no existing job receipt exists for that run ID.

The submission script should print backend, layout, circuit count, shots, estimated QPU seconds, and remaining allowance, then require one final local confirmation. It must never submit on import or as a side effect of a notebook cell.

---

## 10. Hardware manifest: minimum schema

The immutable manifest must include at least:

```json
{
  "experiment_id": "ibm-exp1-qp-sector",
  "paper_commit": "FILL_BEFORE_FREEZE",
  "code_commit": "FILL_BEFORE_FREEZE",
  "class": "TA_ii_quasiperiodic",
  "n_sites": 10,
  "run_index": 0,
  "paper_seed": "READ_FROM_COMMITTED_MANIFEST",
  "model": {"name": "open_xx", "J": 1.0},
  "paper_site_to_qiskit_qubit": [9,8,7,6,5,4,3,2,1,0],
  "full_time_grid": {"start": 20.0, "stop": 200.0, "step": 0.5},
  "hardware_time_indices": [],
  "hardware_times": [],
  "time_quadrature_error": null,
  "p_star": [],
  "p_star_source_sha256": "",
  "tomography": {"design": "GF3_projective_CA_27", "settings": 27},
  "shots": 1024,
  "bootstrap_replicates": 1000,
  "transpiler_seed": 1701,
  "optimization_level": 3,
  "sampler": {
    "gate_twirling": false,
    "measurement_twirling": false,
    "dynamical_decoupling": false,
    "max_execution_time_seconds": 480
  },
  "readout_analysis": ["raw", "m3"],
  "backend": "FILL_AT_PREFLIGHT",
  "physical_path": [],
  "backend_calibration_timestamp": "",
  "estimated_qpu_seconds": null,
  "qpu_go": false
}
```

After freezing, write `manifest.sha256`. Any change creates a new run ID and a dated amendment; never overwrite the frozen manifest.

---

## 11. AR-023 script-change and saved-data contract

This section is binding for implementation. Its purpose is to ensure that the classical comparator, simulated controls, compiled circuits, and QPU result can be reconstructed without rerunning an optimizer or relying on a plot. A script is not ready merely because it produces the final scalar endpoint.

### 11.1 Change boundary and timing

Do not change `scripts/ar020e_sector_suite.py` while any current AR-020e process is running. The sequence is:

1. let every current AR-020e process finish;
2. retain its original result files unchanged;
3. record the exact commands, manifest files, source commit or source snapshot, dependency versions, and SHA-256 hashes of the script and outputs;
4. create a dated AR-023 implementation branch or otherwise record a clean source snapshot;
5. only then add the comparator-export path and hardware package;
6. rerun only `TA_ii_quasiperiodic`, `N=10`, run index `0` for the frozen hardware comparator.

The default AR-020e output and calculation must remain unchanged. The preferred minimal modification is an explicit opt-in export path, for example `IDEG_AR023_EXPORT_DIR`, executed after `sig3` has been obtained. With the option absent, the script must behave exactly as before. Do not overwrite or silently augment the original AR-020e JSON files.

If the nested optimizer code is later refactored into `src/ideg`, establish numerical parity against the unmodified AR-020e result before using the refactor. A refactor and a hardware result must not become one unreviewed change.

### 11.2 Comparator rerun contract

The export rerun must use:

- the committed `TA_ii_quasiperiodic`, `N=10`, run-0 seed;
- the existing `magnon_superposition` and `xx_chain` constructors;
- the full registered window `20.0:0.5:200.0`;
- T3 sector weights fixed to the run's one-magnon sector;
- the current optimizer's deterministic search seed `11`;
- L-BFGS-B, `maxiter=300`, `ftol=1e-10`, unless a dated amendment is written before the rerun;
- no access to IBM or noisy-simulator outcomes when selecting or rerunning the comparator.

The rerun is accepted only if:

```text
abs(exported_T3_miss - recorded_AR020e_T3_miss) <= 5e-6
abs(full_density_recheck - exported_T3_miss)     <= 1e-8
abs(sum(p_star) - 1)                             <= 1e-12
min(p_star)                                      >= -1e-12
||[sigma_star, H]||_F                            <= 1e-10
weight outside q=1                               <= 1e-12
```

If the first comparison fails, stop and investigate numerical/library differences. Do not choose whichever optimum is more favourable for hardware.

### 11.3 Canonical comparator artifact

Write the comparator to:

```text
results/AR-023/preflight/comparator_N10_run0.npz
results/AR-023/preflight/comparator_N10_run0.json
results/AR-023/preflight/comparator_N10_run0.sha256
```

The NPZ must use named, non-object arrays and contain at least:

| Array | Shape | Meaning |
|---|---:|---|
| `p_star` | `(10,)` | T3 stationary populations in increasing-energy order |
| `one_magnon_energies` | `(10,)` | ordered hopping-matrix eigenvalues |
| `one_magnon_modes_site` | `(10,10)` complex | eigenmodes in paper site order |
| `psi0_site` | `(10,)` complex | selected initial one-magnon amplitudes |
| `full_times` | `(361,)` | registered classical time grid |
| `dynamic_site_amplitudes_full` | `(361,10)` complex | exact amplitudes at every registered time |
| `D_series_full` | `(361,10,10)` | exact metric at every registered time |
| `Dbar_full` | `(10,10)` | exact 361-time mean metric |
| `hardware_time_indices` | `(T,)` integer | selected indices into `full_times` |
| `hardware_times` | `(T,)` | frozen hardware time values |
| `dynamic_site_amplitudes_hardware` | `(T,10)` complex | state-preparation targets |
| `D_series_hardware_ideal` | `(T,10,10)` | ideal metrics for the selected grid |
| `Dbar_hardware_ideal` | `(10,10)` | ideal selected-grid mean metric |
| `sigma_star_one_magnon_site` | `(10,10)` complex | comparator density matrix in site basis |
| `pair_rdms_star` | `(45,4,4)` complex | comparator RDMs in lexicographic pair order |
| `mi_star` | `(10,10)` | comparator mutual-information matrix |
| `D_star` | `(10,10)` | comparator metric |
| `pairs` | `(45,2)` integer | exact pair ordering used by all arrays |

Canonicalize each eigenvector's arbitrary phase before saving: locate its largest-magnitude component and rotate the vector so that component is positive real. Record this convention. The density matrices do not depend on this phase, but circuit targets and hashes do.

The JSON sidecar must contain:

- `schema_version` and creation timestamp in UTC;
- AR ID, class, size, run index, manifest path and manifest seed;
- source paths and SHA-256 hashes;
- Git commit; if the tree is dirty, the saved source-snapshot/diff hash;
- Python, NumPy, SciPy, Qiskit, Runtime, Aer, M3 and IDEG versions as applicable;
- optimizer seed, method, tolerances, termination status, iteration/evaluation counts;
- recorded miss, rerun miss, full-density recheck and all acceptance residuals;
- eigenvalue ordering and eigenvector phase convention;
- time-grid selection rule and quadrature error;
- dtype, shape and semantic description of every NPZ array.

JSON must be UTF-8, deterministic (`sort_keys=True`), and written with full floating-point precision. NPZ arrays must not use `dtype=object` or require pickle loading.

### 11.4 Required simulator tiers

All three tiers are mandatory and use the same frozen circuit registry and analysis code:

| Tier | Run kind | Purpose | Required saved raw data |
|---|---|---|---|
| S0 | `statevector_reference` | verify state preparation, endianness, RDMs and metric without sampling | statevectors or target amplitudes, exact RDMs, MI and metrics |
| S1 | `ideal_shot_sampler` | quantify finite-shot/nonlinear reconstruction floor | per-circuit counts and simulator seeds |
| S2 | `noisy_shot_sampler` | rehearse hardware analysis under a frozen device-derived noise model | per-circuit counts, noise-model source and backend snapshot |

S0 must compare the synthesized logical circuit with the analytic one-magnon target for every dynamic snapshot and eigenmode. S1 and S2 must use exactly the QPU-intended shot count, circuit ordering, tomography settings, bit mapping, raw/M3 analysis branches, positivity projection, leakage diagnostics, and bootstrap code.

The S2 backend/noise snapshot must be acquired without looking at QPU experiment outcomes. Save the source backend name, calibration timestamp, properties hash, basis gates, coupling map, and the procedure used to construct the noise model. Never label a generic depolarizing model as a backend snapshot.

Optional lower-shot alternatives such as 768 shots must be separate manifests and separate run directories. They may inform the pre-QPU budget decision but may not overwrite the 1,024-shot simulation.

### 11.5 Circuit registry

Every circuit, simulated or physical, must have one row in `circuit_registry.json`. Each row contains:

```text
circuit_id                 stable AR-023 identifier, not a display label
pub_index                  position submitted to SamplerV2
canonical_index            position before frozen shuffle
arm                        dynamic | sector_basis | control | m3_calibration
state_id                   stable state target identifier
paper_time                 number or null
hardware_time_index        integer or null
eigenmode_index            integer or null
control_occurrence         early | late | null
tomography_row             integer 0..26 or null
tomography_GF3_r           three integers or null
logical_basis_string       ten symbols in paper-site order
paper_site_to_qiskit       explicit ten-integer mapping
logical_to_physical        explicit ten-integer mapping after compilation
classical_bit_mapping      explicit result-bit decoding map
shots                      requested shots
shuffle_seed               frozen seed
transpiler_seed            frozen seed
simulator_seed             frozen seed or null
logical_circuit_sha256     hash of canonical logical representation
transpiled_circuit_sha256  hash of serialized transpiled circuit or null
```

The registry hash belongs in the run manifest. Analysis must join results by `circuit_id`, never by an assumed list position alone.

### 11.6 Raw and derived saved data

For a finite-shot run, `raw/` must contain enough information to repeat analysis without the simulator or IBM service:

- canonical raw counts as a dense `uint32` array of shape `(n_circuits, 2**10)`, where column `x` means integer outcome `x` under the frozen bit convention;
- requested and returned shots per circuit;
- the circuit registry and its hash;
- logical and transpiled circuits in QPY plus Qiskit version;
- full Runtime job metadata or simulator configuration;
- backend/calibration/noise snapshot;
- raw M3 calibration circuits and counts;
- warnings, failed circuits, timestamps, queue/execution times and actual QPU usage when applicable.

Do not preserve only plotted values, expectation values, quasi-probabilities, or final metrics. Counts are the canonical measurement record.

`derived/` must contain, separately for `raw` and `m3` pipelines:

- Pauli expectations with standard errors;
- unprojected and PSD-projected pair RDMs;
- trace, minimum eigenvalue and projection correction for every RDM;
- MI matrices, edge-weight matrices, shortest-path metrics and cap-hit masks;
- `D(t)`, `Dbar`, mixed comparator RDMs and comparator metric;
- split-shot and duplicate-control floors;
- sector survival per circuit/state;
- primary endpoint, `Delta`, influence diagnostics and success-gate booleans;
- bootstrap summaries and either the replicate arrays or the exact seeds/indices needed to recreate them.

Use NPZ/NPY for numeric arrays and JSON for scalar metadata. If an IBM SDK object is also archived, it is supplementary: a pickle or version-specific provider object must never be the sole raw record.

### 11.7 Seed contract

Keep independent random streams and save all of them in the manifest:

```json
{
  "paper_state_seed": "FROM_AR010_MANIFEST",
  "optimizer_seed": 11,
  "transpiler_seed": 1701,
  "circuit_shuffle_seed": 23001,
  "ideal_sampler_seed": 23002,
  "noisy_sampler_seed": 23003,
  "bootstrap_seed": 23004,
  "shot_split_seed": 23005
}
```

Changing one seed creates a new manifest and run ID. Do not reuse the paper-state seed as a general-purpose simulator or bootstrap seed.

### 11.8 Run immutability and completion protocol

Use a run ID of the form:

```text
YYYYMMDDTHHMMSSZ_<manifest-sha256-first12>_<run-kind>
```

Write into a new directory only. Refuse to start if that directory already contains a `COMPLETE` marker or IBM job receipt. During execution, write temporary files and atomically rename them after validation. On success, write:

```text
checksums.sha256
COMPLETE.json
```

`COMPLETE.json` records the manifest hash, registry hash, result hash, analysis hash, exit status and completion time. On failure, retain the partial directory and write `FAILED.json`; do not present it as an analysable completed run and do not delete it merely to reuse the run ID.

Any corrected analysis of unchanged raw data goes into a new versioned `analysis_<version>/` directory with a dated amendment. Preserve the superseded analysis.

### 11.9 Script-level acceptance tests

The code-change phase is complete only when automated tests establish:

- [ ] default AR-020e behaviour and existing JSON schema remain unchanged when export is disabled;
- [ ] the selected comparator rerun satisfies every tolerance in section 11.2;
- [ ] NPZ loads with `allow_pickle=False` and matches its declared schema;
- [ ] eigenmode ordering and canonical phases are deterministic across two fresh processes;
- [ ] S0 circuit statevectors reproduce all analytic target states below `1e-10` infidelity;
- [ ] S0 reconstructed RDMs and metrics match `src/ideg/migraph.py` below declared tolerances;
- [ ] S1 is exactly reproducible from its saved seed and manifest;
- [ ] S1 can be fully reanalysed after deleting all in-memory Qiskit result objects;
- [ ] S2 records the complete noise/calibration provenance and can be reanalysed from saved counts;
- [ ] shuffled results decode correctly by `circuit_id` and explicit bit maps;
- [ ] raw and M3 branches operate on the same canonical counts;
- [ ] modifying any frozen manifest, registry, circuit or raw-count file breaks checksum validation;
- [ ] submission refuses incomplete, over-budget, previously submitted or non-`QPU-GO` bundles.

The QPU browser phase may begin only after these tests and gates L0-L4 pass on one immutable simulator bundle.

---

## 12. Local implementation and validation gates

### Gate L0 — paper calculation frozen

- [ ] final `N=10` sector result exists for run 0
- [ ] T3 comparator populations are exported and hashed
- [ ] full-density-matrix objective recheck agrees with optimizer objective
- [ ] no calculation still running can change the selected comparator
- [ ] paper commit and result hashes recorded

### Gate L1 — construction parity

- [ ] manifest seed reproduces the paper's initial state bit-for-bit or within `1e-14`
- [ ] one-magnon evolution agrees with the full `2^10` evolution below `1e-10`
- [ ] paper/Qiskit endianness test passes for every site
- [ ] all dynamic and eigenmode preparations have infidelity below `1e-10`
- [ ] stationary mixture is formed from RDMs before applying `Phi`

### Gate L2 — tomography parity

- [ ] 27-setting array covers all nine ordered axes for all 45 pairs exactly three times
- [ ] noiseless counts reconstruct every test RDM within tolerance
- [ ] reconstructed metric matches `src/ideg/migraph.py`
- [ ] entropy log base, MI cap, and shortest-path procedure match the paper exactly

### Gate L3 — sampling robustness

- [ ] 25-point quadrature error at or below 0.025, or documented expansion used
- [ ] finite-shot simulation at chosen shots satisfies the success-rule power target
- [ ] bootstrap coverage checked on simulated data
- [ ] raw and synthetic-readout-error pipelines both run end-to-end
- [ ] failure cases produce explicit errors, not partial plots

### Gate L4 — backend compilation

- [ ] operational backend and calibration snapshot recorded
- [ ] ten-qubit path selected without outcome data
- [ ] no SWAPs
- [ ] compiled duration/count/depth report saved
- [ ] M3 calibration circuits included in budget
- [ ] estimated QPU time at or below 450 seconds
- [ ] result-decoding dry run succeeds on a fake/noisy backend

Only after L0-L4 are green may the project proceed to `QPU-GO`.

---

## 13. Browser-assisted execution protocol

This section is written so a browser-controlling assistant can carry out the run with the user while preserving account security and quota control.

### Phase B1 — account and plan check (browser, user present)

1. Open IBM Quantum Platform and ask the user to sign in.
2. The user completes password, MFA, consent, and any CAPTCHA. The assistant must not request or expose those values.
3. Open **Instances** and confirm an active Open Plan instance, normally in `us-east`.
4. Record the visible remaining QPU allowance and whether the current 180-minute promotional allocation is active for this account.
5. If fewer than 500 seconds remain, stop. Do not submit.

### Phase B2 — local credential handoff

1. If the Runtime credential is not already saved, the user obtains it through IBM's supported account flow.
2. The user enters it directly into the local credential setup, not into chat, a Markdown file, source control, notebook output, or a screenshot.
3. Save the account through `QiskitRuntimeService.save_account(...)` using the intended instance/CRN.
4. Immediately verify `QiskitRuntimeService()` can list accessible backends.

Never inspect browser cookies, local storage, password-manager fields, or network traffic to recover a token.

### Phase B3 — backend inspection and freeze

1. In **Compute resources**, inspect operational status and the current backend/calibration pages.
2. Through the Runtime API, collect the same backend metadata for reproducibility.
3. Run the frozen path selector and display its ranked table.
4. Freeze the winning backend/path and save the calibration snapshot.
5. Recompile and rerun L4. If the selected backend goes offline or recalibrates materially before submission, create a dated pre-run amendment and repeat B3; do not substitute silently.

### Phase B4 — final dry run

1. Display the frozen scientific summary, manifest hash, circuit count, shots, backend, path, and usage estimate.
2. Run the complete noisy simulator pipeline once more from the frozen bundle.
3. Confirm there is no existing job receipt for this run ID.

### Phase B5 — mandatory authorization stop

Stop and ask the user:

> The frozen bundle is ready to submit to `<backend>`. It contains `<circuits>` circuits at `<shots>` shots with estimated usage `<seconds>` QPU seconds. This consumes IBM quota and may still be charged if cancelled or if a user-side error occurs. Type **QPU-GO** to authorize this one submission.

No QPU call is authorized by preparation of this document. Only the user's explicit `QPU-GO` authorizes submission.

### Phase B6 — submit and monitor

1. Submit one SamplerV2 job in job mode.
2. Immediately save job ID, submission timestamp, manifest hash, backend, and local receipt.
3. Open **Workloads** in the browser and monitor state without cancelling a healthy queued/running job.
4. If IBM reports an infrastructure failure, save the status and usage record before deciding whether a resubmission is justified. A second submission requires a new `QPU-GO`.
5. When complete, fetch the immutable raw result and verify its job ID/backend against the receipt.

### Phase B7 — analyze without tuning

1. Decode results using the saved logical/physical mapping.
2. Produce raw and M3-corrected analyses side by side.
3. Run the frozen 1,000-replicate bootstrap.
4. Emit every leakage, projection, drift, and dominance diagnostic before the headline endpoint.
5. Save `analysis.json`, figures, environment versions, and a content hash of the raw result.
6. If a bug is found, preserve the first analysis, write a dated amendment, repair the code, and rerun from the same raw data. Never conceal the superseded result.

---

## 14. Analysis outputs and paper figure

The minimum analysis table should contain, for raw and M3 pipelines:

- ideal finite-grid `epsilon_sector`;
- hardware `epsilon_sector` median and 95% interval;
- split-shot floor and duplicate-control floor;
- `Delta` median and 95% interval;
- one-excitation survival median/minimum;
- RDM projection correction median/maximum;
- cap-hit fraction and shortest-path edge changes;
- per-time residual and leave-one-time-out endpoint range;
- per-pair influence or leave-one-pair-out stability;
- QPU seconds actually consumed.

Preferred three-panel paper figure:

1. representative hardware `D(t)` and `Dbar_HW` against exact values;
2. sector-pinned comparator miss versus the reconstruction floor, with bootstrap intervals;
3. ideal, raw, and M3-corrected endpoints plus sector leakage.

Caption and methods must report backend, calibration timestamp, physical layout, Qiskit/Runtime versions, shots, settings, job ID, QPU seconds, manifest hash, and code commit.

Add a paper section only after the analysis is frozen. Label it **Hardware pilot** or **Exploratory hardware validation**. Do not promote it to a confirmatory replication of the whole seven-class study.

---

## 15. Roadmap and effort estimate

| Stage | Work | Exit condition | Expected hands-on time |
|---|---|---|---:|
| 0 | finish current AR-020e calculations and freeze run 0 | comparator weights and hashes exported | depends on current compute |
| 1 | implement manifest, state prep, covering array, reconstruction | L1-L2 green | 1-2 days |
| 2 | finite-shot/noisy simulations and bootstrap | L3 green; power acceptable | 1 day |
| 3 | IBM account, backend selection, compilation, budget | L4 green | 2-4 hours |
| 4 | user `QPU-GO`, submit and monitor | raw result safely fetched | queue-dependent; under 10 QPU min |
| 5 | frozen analysis and robustness report | success rule evaluated without tuning | 1 day |
| 6 | paper pilot section and SparQ evidence pack | auditable supplement ready | 1 day |

If the 10-minute pilot is positive, the next resource request should scale scientific breadth, not merely shots:

- `N=10` and `N=12`;
- multiple preregistered quasiperiodic seeds;
- full dynamical/Trotter implementation rather than snapshot-only realization;
- at least one second hardware architecture through SparQ;
- interleaved calibration/drift controls;
- sufficient allocation to compare sector-pinned and unrestricted-commutant constructions where physically meaningful.

---

## 16. SparQ evidence pack produced by this pilot

Package the following for an NQCC SparQ technical-scoping request:

1. the current paper draft and a one-page nontechnical summary;
2. frozen hardware manifest and code repository/archival link;
3. IBM job receipt and actual QPU usage;
4. the three-panel pilot figure with raw and mitigated results;
5. a one-page limitations statement distinguishing state-realization from long-time physical evolution;
6. the scaled experiment matrix and requested QPU hours;
7. a short explanation of why multi-platform access tests whether the effect survives architecture-specific noise.

Ask for technical collaboration and feasibility review, not just free compute. The strongest request is: the IBM pilot has shown that the observable and analysis pipeline are runnable; SparQ access is needed to test scaling, true circuit evolution, and cross-platform robustness.

---

## 17. Stop conditions

Stop before QPU submission if any of these occurs:

- sector comparator weights are not exported reproducibly;
- run selection, time grid, or analysis threshold remains changeable;
- exact snapshot preparation or endianness tests fail;
- the covering array or RDM reconstruction does not reproduce exact simulation;
- estimated use exceeds the available allowance or safety cap;
- backend mapping introduces SWAPs or unacceptable depth;
- the user has not explicitly supplied `QPU-GO`.

Stop the scientific claim after data collection if:

- leakage is red;
- positivity projection dominates the metric separation;
- the bootstrap interval for `Delta` includes zero;
- raw and mitigated pipelines reverse the conclusion without a predeclared reason;
- the result depends on removing a time, pair, circuit, or calibration interval after inspection.

A null or failed pilot is still useful: it gives a measured resource requirement and identifies whether the limiting factor is state preparation, readout, tomography, leakage, or drift.

---

## 18. Definition of done

The first experiment is complete when:

- [ ] all local gates L0-L4 are green;
- [ ] user gave explicit `QPU-GO` for one identified bundle;
- [ ] one immutable IBM job result and receipt are archived;
- [ ] raw and M3 analyses were generated from the same frozen pipeline;
- [ ] all failure diagnostics are visible alongside the endpoint;
- [ ] the success rule was evaluated exactly as written;
- [ ] code, manifest, backend snapshot, versions, and hashes reproduce the result;
- [ ] paper wording accurately labels the scope as a one-instance hardware pilot;
- [ ] the SparQ follow-on request states what larger access would test that the pilot could not.

---

## 19. Official implementation references

- [IBM Quantum plans overview](https://quantum.cloud.ibm.com/docs/en/guides/plans-overview) — Open Plan allocation and current additional-access programme.
- [Estimate workload usage](https://quantum.cloud.ibm.com/docs/en/guides/estimate-job-run-time) — QPU-time accounting and rough execution estimate.
- [Choose an execution mode](https://quantum.cloud.ibm.com/docs/en/guides/choose-execution-mode) — job, batch, and session availability; Open Plan session restriction.
- [Runtime job limits](https://quantum.cloud.ibm.com/docs/en/guides/job-limits) — Sampler execution limits.
- [Install Qiskit Runtime](https://quantum.cloud.ibm.com/docs/en/guides/install-qiskit-runtime) and [QiskitRuntimeService API](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service) — local installation, account saving, instances, and backend discovery.
- [Transpile with preset pass managers](https://quantum.cloud.ibm.com/docs/en/guides/transpile-with-pass-managers) — backend-aware compilation.
- [Sampler examples](https://quantum.cloud.ibm.com/docs/en/guides/sampler-examples) and [Sampler options](https://quantum.cloud.ibm.com/docs/en/guides/sampler-options) — multi-circuit SamplerV2 jobs and explicit runtime options.
- [M3 readout mitigation tutorial](https://quantum.cloud.ibm.com/docs/en/tutorials/readout-error-mitigation-sampler) — Sampler-compatible measurement mitigation.
- [QPU information](https://quantum.cloud.ibm.com/docs/en/guides/qpu-information), [processor types](https://quantum.cloud.ibm.com/docs/en/guides/processor-types), and [fractional gates](https://quantum.cloud.ibm.com/docs/en/guides/fractional-gates) — calibration inspection, processor families, and feature restrictions.
- [`XXPlusYYGate` API](https://quantum.cloud.ibm.com/docs/api/qiskit/qiskit.circuit.library.XXPlusYYGate) — excitation-preserving two-qubit mixing primitive.
- [Local statevector simulation](https://quantum.cloud.ibm.com/docs/en/guides/simulate-with-qiskit-sdk-primitives) — exact SDK preflight.
- [NQCC SparQ programme](https://www.nqcc.ac.uk/engage/sparq-programme/) and [SparQ access](https://www.nqcc.ac.uk/sparq-access/) — follow-on proof-of-concept and multi-platform access route.

---

## 20. One-sentence operational summary

Freeze the paper's run-0 sector comparator, reconstruct 25 exact `N=10` quasiperiodic snapshots and that comparator through a 27-setting all-pairs tomography design on one carefully selected IBM qubit path, submit only after an explicit `QPU-GO`, and judge the fixed comparator miss against a predeclared hardware reconstruction floor rather than against a visually chosen curve.
