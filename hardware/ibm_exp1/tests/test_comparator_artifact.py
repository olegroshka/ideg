from hashlib import sha256
import json
from pathlib import Path

import numpy as np


MANIFEST_DIR = Path(__file__).resolve().parents[1] / "manifest"


def test_frozen_comparator_artifact_is_self_consistent():
    metadata_path = MANIFEST_DIR / "sector_comparator_N10_run0.json"
    npz_path = MANIFEST_DIR / "sector_comparator_N10_run0.npz"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert sha256(npz_path.read_bytes()).hexdigest() == metadata["npz_sha256"]
    with np.load(npz_path, allow_pickle=False) as archive:
        assert set(archive.files) == {
            "p_star", "eigenvalues", "eigenvectors", "mode_pair_rdms"
        }
        assert archive["p_star"].shape == (10,)
        assert archive["eigenvalues"].shape == (10,)
        assert archive["eigenvectors"].shape == (10, 10)
        assert archive["mode_pair_rdms"].shape == (10, 45, 4, 4)
        assert np.isclose(archive["p_star"].sum(), 1.0, atol=1.0e-12)
        assert np.min(archive["p_star"]) >= -1.0e-12
    assert abs(metadata["optimizer"]["objective"]
               - metadata["optimizer"]["registered_objective"]) < 5.0e-10
    assert abs(metadata["optimizer"]["fullrho_recheck"]
               - metadata["optimizer"]["objective"]) < 1.0e-10
    assert metadata["environment"] == {
        "python": "3.11.14",
        "numpy": "2.3.2",
        "scipy": "1.15.3",
    }

