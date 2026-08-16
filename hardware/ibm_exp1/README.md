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

Backend discovery, path scoring, backend-specific compilation,
finite-shot/noisy simulation, immutable result storage, M3 analysis, and
submission remain later gates.  The comparator exporter will not write an
artifact unless its recomputed optimum agrees with the registered AR-020e
run-0 T3 miss.

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
