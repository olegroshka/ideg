"""Logical Qiskit circuits for the AR-023 IBM experiment.

This module performs local circuit construction only.  It neither connects to
IBM Quantum nor submits a workload.
"""

from __future__ import annotations

from io import BytesIO
from hashlib import sha256
from itertools import product
from typing import Any

import numpy as np

from experiment import (ALL_Z_ROW, covering_array_rows,  # noqa: F401
                        embed_one_magnon_amplitudes,
                        paper_site_to_qiskit)


def _normalized_site_amplitudes(amplitudes: np.ndarray) -> np.ndarray:
    site = np.asarray(amplitudes, dtype=complex)
    if site.ndim != 1 or len(site) < 2:
        raise ValueError("site amplitudes must be a one-dimensional chain")
    norm = float(np.linalg.norm(site))
    if not np.isclose(norm, 1.0, atol=1.0e-12):
        raise ValueError(f"site amplitudes have norm {norm:.16g}")
    return site / norm


def xxplusyy_state_preparation(
    site_amplitudes: np.ndarray,
    name: str | None = None,
):
    """Prepare a one-magnon state with a nearest-neighbour Givens ladder."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import XXPlusYYGate

    site = _normalized_site_amplitudes(site_amplitudes)
    n_sites = len(site)
    qiskit_order = site[::-1].copy()
    nonzero = np.flatnonzero(np.abs(qiskit_order) > 1.0e-14)
    if not len(nonzero):
        raise ValueError("one-magnon target cannot be zero")
    anchor_phase = float(np.angle(qiskit_order[int(nonzero[0])]))
    target = qiskit_order * np.exp(-1.0j * anchor_phase)

    circuit = QuantumCircuit(n_sites, name=name or "one_magnon_xxyy")
    circuit.global_phase = anchor_phase
    circuit.x(0)
    incoming_phase = 0.0
    for qubit in range(n_sites - 1):
        remaining_norm = float(np.linalg.norm(target[qubit:]))
        if remaining_norm <= 0.0:
            theta = 0.0
        else:
            ratio = float(np.clip(
                abs(target[qubit]) / remaining_norm, 0.0, 1.0
            ))
            theta = float(2.0 * np.arccos(ratio))
        if abs(target[qubit + 1]) > 1.0e-14:
            outgoing_phase = float(np.angle(target[qubit + 1]))
        else:
            outgoing_phase = 0.0
        beta = float(outgoing_phase - incoming_phase + np.pi / 2.0)
        circuit.append(XXPlusYYGate(theta, beta), [qubit, qubit + 1])
        incoming_phase = outgoing_phase
    return circuit


def generic_state_preparation(
    site_amplitudes: np.ndarray,
    name: str | None = None,
):
    """Prepare the same target with Qiskit's generic synthesis candidate."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import StatePreparation

    site = _normalized_site_amplitudes(site_amplitudes)
    circuit = QuantumCircuit(len(site), name=name or "one_magnon_generic")
    circuit.append(StatePreparation(embed_one_magnon_amplitudes(site)),
                   range(len(site)))
    return circuit


def preparation_circuit(
    site_amplitudes: np.ndarray,
    method: str,
    name: str | None = None,
):
    if method == "xxplusyy":
        return xxplusyy_state_preparation(site_amplitudes, name=name)
    if method == "generic":
        return generic_state_preparation(site_amplitudes, name=name)
    raise ValueError("method must be 'xxplusyy' or 'generic'")


def preparation_infidelity(circuit, site_amplitudes: np.ndarray) -> float:
    """Return one minus exact statevector fidelity for a preparation."""
    from qiskit.quantum_info import Statevector, state_fidelity

    actual = Statevector.from_instruction(circuit)
    target = embed_one_magnon_amplitudes(
        _normalized_site_amplitudes(site_amplitudes)
    )
    fidelity = float(state_fidelity(actual, target, validate=True))
    return max(0.0, 1.0 - min(fidelity, 1.0))


def tomography_circuit(preparation, basis_paper: str, circuit_id: str):
    """Append one registered tomography setting and q->c measurement."""
    from qiskit import QuantumCircuit

    n_sites = preparation.num_qubits
    if len(basis_paper) != n_sites or set(basis_paper) - {"X", "Y", "Z"}:
        raise ValueError("invalid paper-order tomography basis string")
    circuit = QuantumCircuit(n_sites, n_sites, name=circuit_id)
    circuit.compose(preparation, qubits=range(n_sites), inplace=True)
    for paper_site, axis in enumerate(basis_paper):
        qubit = n_sites - 1 - paper_site
        if axis == "X":
            circuit.h(qubit)
        elif axis == "Y":
            circuit.sdg(qubit)
            circuit.h(qubit)
    circuit.measure(range(n_sites), range(n_sites))
    return circuit


def qpy_sha256(circuit) -> str:
    """Hash one circuit's QPY representation in the active Qiskit version."""
    from qiskit import qpy

    buffer = BytesIO()
    qpy.dump(circuit, buffer)
    return sha256(buffer.getvalue()).hexdigest()


def canonical_circuit_descriptors(
    manifest: dict[str, Any],
    control_mode: int,
) -> list[dict[str, Any]]:
    """Create the complete pre-shuffle logical registry skeleton."""
    rows = tuple(manifest["tomography"]["basis_strings_paper_order"])
    base = covering_array_rows()
    if rows == base:
        leakage_index = None
    elif rows == base + (ALL_Z_ROW,):
        leakage_index = len(base)          # A2.5 witness row
    else:
        raise ValueError("manifest tomography rows differ from AR-023")
    times = manifest["time_grid"]["values"]
    n_modes = int(manifest["selection"]["n_sites"])
    if not 0 <= control_mode < n_modes:
        raise ValueError("control_mode is outside the one-magnon spectrum")
    gf3_rows = list(product(range(3), repeat=3))
    mapping = list(paper_site_to_qiskit(n_modes))
    shots = int(manifest["shots"])
    shuffle_seed = int(manifest["seeds"]["circuit_shuffle_seed"])
    transpiler_seed = int(manifest["seeds"]["transpiler_seed"])
    simulator_seed = int(manifest["seeds"]["ideal_sampler_seed"])
    descriptors: list[dict[str, Any]] = []

    def append_state(
        arm: str,
        state_id: str,
        id_prefix: str,
        paper_time: float | None,
        hardware_time_index: int | None,
        eigenmode_index: int | None,
        control_occurrence: str | None,
    ) -> None:
        for row_index, basis in enumerate(rows):
            is_leak = row_index == leakage_index
            descriptors.append({
                "circuit_id": f"ar023_{id_prefix}_r{row_index:02d}",
                "purpose": "leakage_witness" if is_leak else "tomography",
                "pub_index": None,
                "canonical_index": len(descriptors),
                "arm": arm,
                "state_id": state_id,
                "paper_time": paper_time,
                "hardware_time_index": hardware_time_index,
                "eigenmode_index": eigenmode_index,
                "control_occurrence": control_occurrence,
                "tomography_row": row_index,
                "tomography_GF3_r": (None if is_leak
                                     else list(gf3_rows[row_index])),
                "logical_basis_string": basis,
                "paper_site_to_qiskit": mapping,
                "logical_to_physical": None,
                "classical_bit_mapping": list(range(n_modes)),
                "shots": shots,
                "shuffle_seed": shuffle_seed,
                "transpiler_seed": transpiler_seed,
                "simulator_seed": simulator_seed,
                "logical_circuit_sha256": None,
                "transpiled_circuit_sha256": None,
            })

    for index, paper_time in enumerate(times):
        append_state("dynamic", f"dynamic_t{index:03d}",
                     f"dynamic_t{index:03d}", float(paper_time), index,
                     None, None)
    for mode in range(n_modes):
        append_state("sector_basis", f"sector_e{mode:02d}",
                     f"sector_e{mode:02d}", None, None, mode, None)
    for occurrence in ("early", "late"):
        append_state("control", f"sector_e{control_mode:02d}",
                     f"control_{occurrence}_e{control_mode:02d}", None,
                     None, control_mode, occurrence)
    return descriptors


def submission_permutation(
    descriptors: list[dict[str, Any]], seed: int
) -> tuple[list[int], list[int]]:
    """Shuffle primary rows while placing control blocks at both brackets."""
    early = [row["canonical_index"] for row in descriptors
             if row["control_occurrence"] == "early"]
    late = [row["canonical_index"] for row in descriptors
            if row["control_occurrence"] == "late"]
    primary = [row["canonical_index"] for row in descriptors
               if row["control_occurrence"] is None]
    rng = np.random.default_rng(int(seed))
    rng.shuffle(primary)
    pub_to_canonical = early + primary + late
    if sorted(pub_to_canonical) != list(range(len(descriptors))):
        raise RuntimeError("submission permutation is not bijective")
    canonical_to_pub = [0] * len(descriptors)
    for pub_index, canonical_index in enumerate(pub_to_canonical):
        canonical_to_pub[canonical_index] = pub_index
    return pub_to_canonical, canonical_to_pub
