# IBM experiment 1: quasiperiodic sector-admissibility pilot

This directory implements AR-023 for the registered
`TA_ii_quasiperiodic`, `N=10`, run-0 instance.  The primary arm realizes
exact one-magnon snapshots on an IBM QPU and reconstructs every two-site
reduced density matrix with a 27-setting strength-two covering array.

No script in this directory submits a QPU job as a side effect.  A future
submission command must refuse to run until local gates L0-L4 are green,
the frozen bundle is under the QPU-time cap, no receipt already exists, and
the user supplies the exact confirmation `QPU-GO`.

## Current implementation milestone

- deterministic 27-row tomography design and validation;
- paper-site/Qiskit-qubit endianness contract;
- pair-RDM reconstruction, PSD projection, and metric parity helpers;
- fail-closed export of the run-0 T3 comparator populations;
- draft/frozen scientific-manifest builder and JSON Schema;
- focused tests that do not require IBM credentials.

The circuit-construction milestone adds two exact preparation candidates:
an excitation-preserving nine-step nearest-neighbour `XXPlusYY` ladder and
Qiskit's generic state preparation.  `build_circuits.py` verifies both against
all analytic targets, then emits a draft logical QPY bundle and the complete
1,323-row circuit registry.  The `XXPlusYY` candidate is used for the draft;
the final choice remains blocked on backend-specific compilation.

The comparator exporter will not write an artifact unless its recomputed
optimum agrees with the registered AR-020e run-0 T3 miss.

## Status (2026-08-18) — S1 CLOSED under Amendment 2; S2 running

The owner ruled on candidates C1–C6; they are preregistered as AR-023a
**Amendment 2** (A2.1–A2.10) and adjudicated on **fresh seed 24002**,
never on the seeds that motivated them.  The original rule and its
failing batteries below are preserved unaltered (dual record).

Bundle rebuilt for A2.5: **28 settings / 1,372 circuits** (27
reconstruction rows + one all-Z leakage witness, excluded from the RDM
reconstruction so the tomography estimator is unchanged).  Byte-identical
across two independent builds.

**S1 — all four gates PASS at both shot settings:**

| Gate | 768 | 896 |
|---|---|---|
| G1 bias | 0.00542 | 0.00543 |
| G2 power | **100/100** | **100/100** |
| G3 floor | 0.01732 | 0.01658 |
| G4 determinism | byte-identical | byte-identical |

**Null test PASS:** with the comparator replaced by an independent
reconstruction of the same moving average (true separation zero), ε
collapses to the floor (0.0185 vs 0.0184) and the rule declares no
separation — the AR-010 failure mode tested for directly.

**S2 (in progress):** both Heron fakes 100/100 with leakage GREEN
(floor 0.018, Δ 0.20).  The readout correction is load-bearing: the
same states read 0.932 corrected vs 0.852 raw, i.e. GREEN vs AMBER.

Remaining before L4: the 3×3 noise grid, the drift-ramp arm (the only
test of the duplicate floor against a systematic), and the aggregate
envelope.  Then L4 must pull **IBM's own usage estimate** against
compiled circuits rather than the rough formula used here.

### Superseded first adjudication (2026-08-17), preserved

The circuit bundle is **frozen** (`bundle/`, hashes in the manifest and
verified byte-identical across four independent builds).  The exact
37-grid reference endpoint is recorded: **ε_sector^(37) =
0.227910117170944**.

S1 (ideal finite-shot, R = 100, 1,000-replicate bootstrap) is closed at
both shot settings:

| Gate | Criterion | 768 | 896 | Verdict |
|---|---|---|---|---|
| S1-G1 | bias < 0.02 | 0.00590 | 0.00641 | **PASS** |
| S1-G2 | success ≥ 95/100 | 0/100 | 0/100 | **FAIL** |
| S1-G3 | median floor < 0.05 | 0.11375 | 0.11013 | **FAIL** |
| S1-G4 | byte-identical rerun | identical | identical | **PASS** |

S2 (11 noise conditions: 2 Heron fakes + 3×3 sweep) is closed with the
operating envelope and the L4 path-quality pre-commitment in
`results/sim_s2/s2_report.json`.

**The failures are in the decision rule, not the measurement.** The
separation Δ is resolved above the floor in 100/100 ideal and 99/100
noisy experiments; leakage is GREEN through p2 = 6e-3; raw and M3 agree
in direction 100/100.  The frozen floor statistic is a full-matrix
norm compared against a scalar endpoint — measured overstatement 7.8×,
matching √(effective metric directions) — and the projection criterion
penalises a bias correction (projected bias +0.0059 vs unprojected
+0.1004).  Diagnosis, amendment candidates **C1–C6**, and the
repaired-rule counterfactual (95/100 at 768, 99/100 at 896) are in
`ar/AR-023a_findings-2026-08-17.md`.

These failures drove Amendment 2.  C6 was the hardest: the 27-row
array had no all-Z row (max 6 of 10 sites in Z), so AR-023 §5's leakage
traffic light — a registered kill criterion — was not computable from
QPU data at all.  It is now fixed by the added setting above.

**QPU-GO remains blocked** until S2 closes and L4 is green.

Reproduce (Python-3.11 hardware environment):

```powershell
python hardware/ibm_exp1/scripts/compute_s1_reference.py
python hardware/ibm_exp1/scripts/run_s1.py --precompute
python hardware/ibm_exp1/scripts/run_s1.py --run --shots 768 `
  --out hardware/ibm_exp1/results/sim_s1_768
python hardware/ibm_exp1/scripts/run_s2.py --prepare
python hardware/ibm_exp1/scripts/run_ar023a_chain.py
```

Backend discovery against a live account, backend-specific compilation,
immutable QPU result storage, and submission remain later gates.

Build a local-only draft circuit bundle outside the repository:

```powershell
python hardware/ibm_exp1/scripts/build_circuits.py `
  --output-dir <draft-output-directory>
```

This command does not load IBM credentials or contact an IBM backend.

The first verified draft build on 2026-08-16 produced 1,323 ten-qubit
circuits for 47 unique analytic targets.  The maximum exact-statevector
infidelity of the `XXPlusYY` ladder was `6.67e-16`; the generic candidate was
also exact to reported precision.  A second clean build reproduced the QPY,
registry, target-state, and bundle hashes byte for byte.  These are logical
circuits only, not backend-transpiled or submission-ready circuits.

## Local setup

Install the paper package and the isolated, Python-3.11 hardware dependencies
into a dedicated environment.  The versions in `requirements-hardware.txt`
were verified together on Windows on 2026-08-16; every result bundle must also
record a complete environment freeze.

```powershell
python -m pip install -e .
python -m pip install -r hardware/ibm_exp1/requirements-hardware.txt
python -m pytest hardware/ibm_exp1/tests -q
```

Export and freeze the classical comparator before preparing a manifest:

```powershell
python hardware/ibm_exp1/scripts/export_sector_comparator.py --n-sites 10 --run-index 0
python hardware/ibm_exp1/scripts/prepare_manifest.py --n-sites 10 --run-index 0 --time-count 37 --shots 768
```

Comparator replay is a separate provenance environment: Python 3.11,
NumPy 2.3.2, and SciPy 1.15.3 (see `requirements-comparator.txt`).  The
exporter deliberately fails under a numerical stack that does not reproduce
the committed T3 objective.

The originally proposed 25-point grid failed the registered ideal quadrature
gate (`0.13276 > 0.025`).  The first preregistered fallback, 37 points, passes
(`0.01465`).  At 1,024 shots its 1,323 primary circuits exceed the rough
450-second safety cap, so the declared degradation ladder selects 768 shots
pending finite-shot power validation and backend-specific compilation.

The Runtime credential must be provided by the user through IBM's supported
local account flow.  `save_account.py` reads the API key from the
`IBM_QUANTUM` environment variable when it is present, otherwise it uses
hidden terminal input, and then verifies the saved account.  It uses the private
`Documents/Codex/.credentials/ideg-qiskit-ibm.json` file because the managed
Codex shell cannot write Qiskit's default home-directory credential path.
Never put an API key in chat, source files, Markdown, notebook output,
screenshots, or the manifest.

```powershell
python hardware/ibm_exp1/scripts/save_account.py --instance open-instance
```
