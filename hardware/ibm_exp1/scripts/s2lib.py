"""S2 noisy-simulation library (AR-023a §2, Amendments A1.4/A1.8).

Prepare phase: fake-backend selection (A1.4), path scoring, opt-3
transpilation with no-SWAP verification, per-condition noisy outcome
distributions via one density-matrix simulation per circuit with the
readout confusion applied analytically (A1.8), M3 calibration
distributions, and exact one-excitation survival per prepared state.

Battery phase: the S1 synthetic-experiment core extended with an M3
branch.  The M3 correction uses per-experiment calibration counts to
estimate per-clbit confusion matrices and folds their tensor-product
inverse into the Pauli sign tables — algebraically identical to
applying the independent-readout inverse to the counts, with no
1024x1024 matrices anywhere.

No IBM credentials, no network access, no QPU submission.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from experiment import N_SITES  # noqa: E402
import sampling
from sampling import (N_OUT, SHOTS, StateIndex, aggregation_weights,
                      analyze_pass, floors_from_slots, phi_from_mi,
                      zrow_masks)

GRID_P2 = (3.0e-3, 6.0e-3, 1.0e-2)
GRID_RO = (1.0e-2, 2.0e-2, 3.0e-2)
SWEEP_BASIS = ["cz", "sx", "x", "rz", "id"]


# ------------------------------------------------------ fake selection

def heron_fake_enumeration():
    """All installed >=10-qubit Heron-family fakes, sorted by name."""
    from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2

    rows = []
    for backend in FakeProviderForBackendV2().backends():
        try:
            pt = getattr(backend, "processor_type", None)
            family = pt.get("family") if isinstance(pt, dict) else None
            if backend.num_qubits >= N_SITES and family == "Heron":
                rows.append({
                    "name": backend.name,
                    "num_qubits": int(backend.num_qubits),
                    "processor_type": dict(pt),
                })
        except Exception:  # noqa: BLE001 - enumeration must not die
            continue
    return sorted(rows, key=lambda row: row["name"])


def select_fakes():
    """A1.4: the two lexicographically smallest qualifying Heron fakes."""
    enumeration = heron_fake_enumeration()
    if len(enumeration) < 2:
        raise RuntimeError("fewer than two Heron-class fakes installed")
    return enumeration, [row["name"] for row in enumeration[:2]]


def get_fake(name: str):
    from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2

    for backend in FakeProviderForBackendV2().backends():
        if backend.name == name:
            return backend
    raise RuntimeError(f"fake backend {name} not found")


# --------------------------------------------------------- path scoring

def _edge_errors(backend):
    """(edge -> two-qubit error, qubit -> readout error) from the target."""
    target = backend.target
    twoq = {}
    for op_name in target.operation_names:
        try:
            props = target[op_name]
        except Exception:  # noqa: BLE001
            continue
        for qargs, inst_props in props.items():
            if qargs is None or len(qargs) != 2:
                continue
            error = getattr(inst_props, "error", None)
            if error is None:
                continue
            edge = tuple(sorted(qargs))
            twoq[edge] = min(twoq.get(edge, 1.0), float(error))
    readout = {}
    measure = target["measure"]
    for qargs, inst_props in measure.items():
        readout[qargs[0]] = float(getattr(inst_props, "error", 0.0))
    return twoq, readout


def score_paths(backend, length: int = N_SITES):
    """Enumerate simple paths and score (max2q, med2q, maxRO, medRO)."""
    twoq, readout = _edge_errors(backend)
    adjacency: dict[int, set[int]] = {}
    for (a, b) in twoq:
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    best = None
    counter = 0

    def extend(path):
        nonlocal best, counter
        if len(path) == length:
            counter += 1
            if path[0] > path[-1]:
                return                      # deduplicate reversals
            edges = [tuple(sorted((path[i], path[i + 1])))
                     for i in range(length - 1)]
            e2 = np.array([twoq[e] for e in edges])
            ro = np.array([readout[q] for q in path])
            score = (float(e2.max()), float(np.median(e2)),
                     float(ro.max()), float(np.median(ro)))
            if best is None or score < best[0]:
                best = (score, list(path))
            return
        for nxt in sorted(adjacency.get(path[-1], ())):
            if nxt not in path:
                path.append(nxt)
                extend(path)
                path.pop()

    for start in sorted(adjacency):
        extend([start])
    if best is None:
        raise RuntimeError("no ten-qubit line found")
    score, path = best
    return {
        "path": path,
        "score": {"max_2q_error": score[0], "median_2q_error": score[1],
                  "max_readout_error": score[2],
                  "median_readout_error": score[3]},
        "paths_scored": counter,
        "score_formula": "lexicographic (max 2q, median 2q, max readout, "
                         "median readout) over path edges/qubits",
    }


# -------------------------------------------------------- transpilation

def transpile_bundle(circuits, backend=None, initial_layout=None,
                     coupling_map=None, basis_gates=None):
    """Opt-3 transpile with the frozen seed; verify no SWAP, layout use."""
    from qiskit.transpiler.preset_passmanagers import (
        generate_preset_pass_manager)

    pm = generate_preset_pass_manager(
        optimization_level=3, backend=backend, coupling_map=coupling_map,
        basis_gates=basis_gates, initial_layout=initial_layout,
        seed_transpiler=1701)
    transpiled = pm.run(circuits)
    twoq_counts, depths = [], []
    for circuit in transpiled:
        ops = circuit.count_ops()
        if "swap" in ops:
            raise RuntimeError(f"SWAP introduced in {circuit.name}")
        active = set()
        twoq = 0
        for inst in circuit.data:
            qubits = [circuit.find_bit(q).index for q in inst.qubits]
            if inst.operation.name in ("barrier", "measure"):
                active.update(qubits)
                continue
            active.update(qubits)
            if len(qubits) == 2:
                twoq += 1
        if initial_layout is not None:
            if not active.issubset(set(initial_layout)):
                raise RuntimeError(
                    f"{circuit.name} uses qubits outside the frozen path")
        twoq_counts.append(twoq)
        depths.append(circuit.depth())
    return transpiled, {
        "two_qubit_count_max": int(max(twoq_counts)),
        "two_qubit_count_median": float(np.median(twoq_counts)),
        "depth_max": int(max(depths)),
        "depth_median": float(np.median(depths)),
        "no_swap": True,
        "seed_transpiler": 1701,
        "optimization_level": 3,
    }


# ----------------------------------------------- noise + distributions

def sweep_noise_model(p2: float):
    """Two-qubit depolarizing p2 on cz, p1 = p2/10 on sx/x; no readout."""
    from qiskit_aer.noise import NoiseModel, depolarizing_error

    model = NoiseModel(basis_gates=SWEEP_BASIS)
    model.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cz"])
    model.add_all_qubit_quantum_error(
        depolarizing_error(p2 / 10.0, 1), ["sx", "x"])
    return model


def backend_noise_model(backend, readout: bool):
    from qiskit_aer.noise import NoiseModel

    return NoiseModel.from_backend(
        backend, gate_error=True, thermal_relaxation=True,
        readout_error=readout)


def backend_readout_confusions(backend, phys_for_clbit: list[int]):
    """Per-clbit 2x2 confusion A[m, t] = P(measured m | true t)."""
    model = backend_noise_model(backend, readout=True)
    per_qubit = {}
    for entry in model.to_dict()["errors"]:
        if entry["type"] != "roerror":
            continue
        qubit = entry["gate_qubits"][0][0]
        probs = np.asarray(entry["probabilities"])   # rows: true state
        per_qubit[qubit] = probs.T                   # A[m, t]
    out = []
    for phys in phys_for_clbit:
        out.append(per_qubit.get(phys, np.eye(2)))
    return np.stack(out)


def symmetric_confusions(rate: float):
    a = np.array([[1.0 - rate, rate], [rate, 1.0 - rate]])
    return np.stack([a] * N_SITES)


def apply_confusion(probs: np.ndarray, confusions: np.ndarray) -> np.ndarray:
    """Apply per-clbit confusion A_b along outcome-bit axes.

    probs (..., N_OUT) with bit b of the outcome index = clbit b, i.e.
    reshape axis (N_SITES-1-b) corresponds to clbit b.
    """
    shaped = probs.reshape(probs.shape[:-1] + (2,) * N_SITES)
    for b in range(N_SITES):
        axis = probs.ndim - 1 + (N_SITES - 1 - b)
        shaped = np.moveaxis(
            np.tensordot(confusions[b], shaped, axes=([1], [axis])),
            0, axis)
    return shaped.reshape(probs.shape)


def measured_qubit_order(circuit) -> list[int]:
    """Physical qubit measured into each clbit, ordered by clbit index."""
    mapping = {}
    for inst in circuit.data:
        if inst.operation.name != "measure":
            continue
        q = circuit.find_bit(inst.qubits[0]).index
        c = circuit.find_bit(inst.clbits[0]).index
        mapping[c] = q
    if sorted(mapping) != list(range(N_SITES)):
        raise RuntimeError("unexpected classical bit mapping")
    return [mapping[c] for c in range(N_SITES)]


def dm_probabilities(transpiled, noise_model, label: str = "p"):
    """One density-matrix simulation per circuit -> exact outcome probs.

    Returns (n_circuits, N_OUT) with bit b of the index = clbit b
    (achieved by ordering save_probabilities qubits clbit-wise).
    """
    from qiskit_aer import AerSimulator

    simulator = AerSimulator(method="density_matrix",
                             noise_model=noise_model)
    out = np.empty((len(transpiled), N_OUT))
    jobs = []
    for circuit in transpiled:
        order = measured_qubit_order(circuit)
        bare = circuit.remove_final_measurements(inplace=False)
        bare.save_probabilities(qubits=order, label=label)
        jobs.append(bare)
    # batch in chunks to bound memory
    chunk = 64
    for start in range(0, len(jobs), chunk):
        result = simulator.run(jobs[start:start + chunk]).result()
        for offset in range(len(jobs[start:start + chunk])):
            out[start + offset] = np.asarray(
                result.data(offset)[label], dtype=float)
    norm = out.sum(axis=1)
    if not np.allclose(norm, 1.0, atol=1.0e-9):
        raise RuntimeError("DM probabilities do not normalize")
    return np.clip(out, 0.0, None) / out.sum(axis=1, keepdims=True)


def survival_from_probs(probs_z: np.ndarray) -> np.ndarray:
    """P(exactly one excitation) from Z-basis outcome distributions."""
    x = np.arange(N_OUT)
    popcount = np.array([bin(v).count("1") for v in x])
    return probs_z[..., popcount == 1].sum(axis=-1)


# ------------------------------------------------------- M3 correction
#
# The M3 branch estimates per-clbit confusion matrices from the two
# calibration circuits and applies their tensor-product INVERSE to the
# counts via apply_confusion(counts, inverses).  Column sums of A^{-1}
# are 1, so total (quasi-)counts are preserved; negative entries are
# legitimate quasi-counts and flow through the identical pipeline.

def estimate_confusions(cal_counts: np.ndarray) -> np.ndarray:
    """(2, N_OUT) counts for |0...0> and |1...1> -> (N_SITES, 2, 2)."""
    shots = cal_counts.sum(axis=-1)
    out = np.empty((N_SITES, 2, 2))
    for b in range(N_SITES):
        bits = ((np.arange(N_OUT) >> b) & 1).astype(float)
        p1_given_0 = float(cal_counts[0] @ bits / shots[0])
        p1_given_1 = float(cal_counts[1] @ bits / shots[1])
        out[b] = np.array([[1.0 - p1_given_0, 1.0 - p1_given_1],
                           [p1_given_0, p1_given_1]])
    return out


def confusion_inverses(confusion_estimates: np.ndarray) -> np.ndarray:
    """(N_SITES, 2, 2) per-clbit inverse confusion matrices."""
    return np.stack([np.linalg.inv(a) for a in confusion_estimates])


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()
