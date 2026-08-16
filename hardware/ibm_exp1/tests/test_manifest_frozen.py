from experiment import canonical_json_sha256


def test_manifest_hash_changes_on_frozen_field_change():
    manifest = {"shots": 1024, "seed": 23001, "times": [20.0, 200.0]}
    original = canonical_json_sha256(manifest)
    changed = dict(manifest, shots=768)
    assert canonical_json_sha256(changed) != original

