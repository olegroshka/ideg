import json
from pathlib import Path

from qiskit import qpy

from circuits import (canonical_circuit_descriptors,
                      submission_permutation, tomography_circuit,
                      xxplusyy_state_preparation)


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = (ROOT / "hardware" / "ibm_exp1" / "manifest"
                 / "hardware_manifest.json")


def _manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_registered_family_size_and_bracketed_controls():
    """Counts derive from the manifest's settings count, never hardcoded."""
    manifest = _manifest()
    settings = int(manifest["tomography"]["settings"])
    expected = 49 * settings
    descriptors = canonical_circuit_descriptors(manifest, control_mode=9)
    assert len(descriptors) == expected
    assert expected == int(manifest["arms"]["primary_circuit_count"])
    assert len({row["circuit_id"] for row in descriptors}) == expected
    assert sum(row["arm"] == "dynamic" for row in descriptors) == 37 * settings
    assert sum(row["arm"] == "sector_basis"
               for row in descriptors) == 10 * settings
    assert sum(row["arm"] == "control" for row in descriptors) == 2 * settings
    # A2.5: exactly one leakage-witness circuit per prepared state
    assert sum(row["purpose"] == "leakage_witness"
               for row in descriptors) == 49

    pub_to_canonical, canonical_to_pub = submission_permutation(
        descriptors, manifest["seeds"]["circuit_shuffle_seed"]
    )
    by_index = {row["canonical_index"]: row for row in descriptors}
    assert all(by_index[index]["control_occurrence"] == "early"
               for index in pub_to_canonical[:settings])
    assert all(by_index[index]["control_occurrence"] == "late"
               for index in pub_to_canonical[-settings:])
    assert all(canonical_to_pub[canonical] == pub
               for pub, canonical in enumerate(pub_to_canonical))


def test_tomography_rotations_follow_paper_to_qiskit_mapping():
    target = [1.0] + [0.0] * 9
    preparation = xxplusyy_state_preparation(target)
    circuit = tomography_circuit(preparation, "XYZXYZXYZX", "mapping_test")
    operations = circuit.count_ops()
    assert operations.get("measure", 0) == 10
    assert operations.get("h", 0) == 7
    assert operations.get("sdg", 0) == 3


def test_logical_circuit_qpy_round_trip(tmp_path):
    preparation = xxplusyy_state_preparation([1.0] + [0.0] * 9)
    circuit = tomography_circuit(preparation, "XXXXXXXXXX", "qpy_test")
    path = tmp_path / "one.qpy"
    with path.open("wb") as handle:
        qpy.dump(circuit, handle)
    with path.open("rb") as handle:
        restored = qpy.load(handle)
    assert len(restored) == 1
    assert restored[0] == circuit
