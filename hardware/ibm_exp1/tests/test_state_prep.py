import json
from pathlib import Path

import numpy as np

from circuits import (generic_state_preparation, preparation_infidelity,
                      xxplusyy_state_preparation)
from experiment import (canonicalize_mode_columns,
                        embed_one_magnon_amplitudes,
                        evolve_one_magnon_amplitudes,
                        one_magnon_hopping,
                        registered_initial_site_amplitudes)
from ideg.models import xx_chain


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "hardware" / "ibm_exp1" / "manifest"


def _registered_targets():
    manifest = json.loads(
        (MANIFEST / "hardware_manifest.json").read_text(encoding="utf-8")
    )
    with np.load(MANIFEST / "sector_comparator_N10_run0.npz",
                 allow_pickle=False) as archive:
        energies = archive["eigenvalues"].copy()
        modes = canonicalize_mode_columns(archive["eigenvectors"])
    initial = registered_initial_site_amplitudes(
        manifest["selection"]["paper_state_seed"], 10
    )
    dynamic = evolve_one_magnon_amplitudes(
        initial, np.asarray(manifest["time_grid"]["values"]),
        energies, modes,
    )
    return dynamic, modes


def test_one_magnon_hopping_matches_full_xx_hamiltonian_block():
    full_hamiltonian = xx_chain(10)
    hopping = one_magnon_hopping(10)
    for site in range(10):
        unit = np.zeros(10, dtype=complex)
        unit[site] = 1.0
        embedded = embed_one_magnon_amplitudes(unit)
        expected = np.zeros(2**10, dtype=complex)
        for target_site, amplitude in enumerate(hopping @ unit):
            expected[1 << (9 - target_site)] = amplitude
        assert np.allclose(full_hamiltonian @ embedded, expected,
                           atol=1.0e-14)


def test_xxplusyy_ladder_prepares_every_registered_target():
    dynamic, modes = _registered_targets()
    targets = [*dynamic, *(modes[:, mode] for mode in range(10))]
    infidelities = []
    for target in targets:
        circuit = xxplusyy_state_preparation(target)
        infidelities.append(preparation_infidelity(circuit, target))
        assert circuit.count_ops().get("xx_plus_yy", 0) == 9
        assert circuit.count_ops().get("x", 0) == 1
    assert max(infidelities) < 1.0e-10


def test_generic_candidate_prepares_representative_targets():
    dynamic, modes = _registered_targets()
    for target in (dynamic[0], dynamic[len(dynamic) // 2], dynamic[-1],
                   modes[:, 0], modes[:, -1]):
        circuit = generic_state_preparation(target)
        assert preparation_infidelity(circuit, target) < 1.0e-10


def test_canonical_mode_phase_is_positive_at_each_pivot():
    _, modes = _registered_targets()
    for column in range(modes.shape[1]):
        pivot = int(np.argmax(np.abs(modes[:, column])))
        assert modes[pivot, column].imag == 0.0
        assert modes[pivot, column].real > 0.0
