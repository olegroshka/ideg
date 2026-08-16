"""Shared vectorized S1/S2 sampling and analysis machinery (AR-023a).

Implements the complete hardware-intended analysis path on batched count
arrays: covering-array Pauli aggregation -> pair-RDM assembly -> hermitize
-> PSD clip -> renormalize -> natural-log MI -> x-clip -> -ln weights ->
Floyd-Warshall -> per-time metrics -> time-averaged moving metric, with
the comparator arm mixing eigenmode RDMs with the exported p* BEFORE any
entropy/metric step (AR-023 SS4, SS6; AR-023a SS1).

Shot-split equivalence: every 768-shot draw is realized as two
independent Multinomial(384, p) halves h1, h2.  Then h1 + h2 is exactly
Multinomial(768, p) and, conditional on the total, (h1, h2) is a
uniformly random split of the shots -- the AR-023 SS6 split-shot
diagnostic with no extra randomness stream.

Seed policy (AR-023a SS1, enumeration documented in the S1 report):
  main draws      SeedSequence([BASE, circuit_canonical_index, r])
  bootstrap       SeedSequence([BASE, 10**6 + r]).spawn(n_circuits)[c],
                  one multinomial call of size (B, 2) per circuit
where r is the synthetic-experiment index.  BASE is committed to the
manifest before any sampled result is inspected.

Everything here is deterministic given (probs, BASE, r); no wall-clock,
no Qiskit objects retained.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from experiment import I0, X_MIN, N_SITES  # noqa: F401

SHOTS = 768
HALF_SHOTS = SHOTS // 2
N_OUT = 2 ** N_SITES
PAIRS = [(i, j) for i in range(N_SITES) for j in range(i + 1, N_SITES)]
N_PAIRS = len(PAIRS)
AXES3 = "XYZ"

_I2 = np.eye(2, dtype=complex)
_PAULI4 = np.stack([
    _I2,
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex),
    np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex),
    np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex),
])
# KRON[a, b] = sigma_a (site i, first factor) x sigma_b (site j).
KRON = np.einsum("aij,bkl->abikjl", _PAULI4, _PAULI4).reshape(4, 4, 4, 4)


def site_signs() -> np.ndarray:
    """(N_OUT, N_SITES) +/-1: sign of paper site s in counts outcome x."""
    x = np.arange(N_OUT)
    bits = (x[:, None] >> (N_SITES - 1 - np.arange(N_SITES))[None, :]) & 1
    return (1 - 2 * bits).astype(np.int8)


SITE_SIGN = site_signs()
PAIR_SIGN = np.stack(
    [SITE_SIGN[:, i] * SITE_SIGN[:, j] for (i, j) in PAIRS], axis=1)


def aggregation_weights(basis_rows: list[str]):
    """W1 (27, N_SITES, 3) and W2 (27, N_PAIRS, 3, 3) covering weights."""
    n_rows = len(basis_rows)
    w1 = np.zeros((n_rows, N_SITES, 3))
    w2 = np.zeros((n_rows, N_PAIRS, 3, 3))
    for r, row in enumerate(basis_rows):
        for s in range(N_SITES):
            w1[r, s, AXES3.index(row[s])] += 1.0
        for k, (i, j) in enumerate(PAIRS):
            w2[r, k, AXES3.index(row[i]), AXES3.index(row[j])] += 1.0
    w1 /= w1.sum(axis=0, keepdims=True)
    w2 /= w2.sum(axis=0, keepdims=True)
    return w1, w2


def zrow_masks(basis_rows: list[str]):
    """Per-row Z-subset excitation tables for the leakage witness.

    Returns (27, N_OUT) int8 excitation counts within each row's
    Z-measured site subset, and the per-row Z-site counts.
    """
    counts = np.zeros((len(basis_rows), N_OUT), dtype=np.int8)
    sizes = np.zeros(len(basis_rows), dtype=int)
    x = np.arange(N_OUT)
    for r, row in enumerate(basis_rows):
        z_sites = [s for s in range(N_SITES) if row[s] == "Z"]
        sizes[r] = len(z_sites)
        total = np.zeros(N_OUT, dtype=np.int8)
        for s in z_sites:
            total += ((x >> (N_SITES - 1 - s)) & 1).astype(np.int8)
        counts[r] = total
    return counts, sizes


def pair_rdms_from_counts(counts: np.ndarray, w1: np.ndarray,
                          w2: np.ndarray) -> np.ndarray:
    """counts (..., 27, N_OUT) -> raw pair RDMs (..., N_PAIRS, 4, 4)."""
    shots = counts.sum(axis=-1, keepdims=True)
    freq = counts / np.maximum(shots, 1.0)
    e1 = freq @ SITE_SIGN.astype(float)          # (..., 27, N_SITES)
    e2 = freq @ PAIR_SIGN.astype(float)          # (..., 27, N_PAIRS)
    e1_avg = np.einsum("...ri,ria->...ia", e1, w1)
    e2_avg = np.einsum("...rk,rkab->...kab", e2, w2)
    m = np.zeros(e2_avg.shape[:-3] + (N_PAIRS, 4, 4))
    m[..., 0, 0] = 1.0
    idx_i = np.array([i for (i, j) in PAIRS])
    idx_j = np.array([j for (i, j) in PAIRS])
    for a in range(3):
        m[..., a + 1, 0] = e1_avg[..., idx_i, a]
        m[..., 0, a + 1] = e1_avg[..., idx_j, a]
    m[..., 1:, 1:] = e2_avg
    return 0.25 * np.einsum("...kab,abuv->...kuv", m, KRON)


def hermitize_project_batch(rho_raw: np.ndarray, project: bool = True):
    """Hermitize (+ optional PSD clip and renormalize) a (...,4,4) batch.

    Returns (rho_used, projection_fro) where projection_fro is the
    Frobenius distance between the projected matrix and the raw input
    (matching experiment.hermitize_and_project).  With project=False the
    hermitized matrix is returned unchanged (unprojected pipeline) and
    projection_fro is still reported for diagnostics.
    """
    herm = 0.5 * (rho_raw + np.conj(np.swapaxes(rho_raw, -1, -2)))
    vals, vecs = np.linalg.eigh(herm)
    clipped = np.clip(vals, 0.0, None)
    total = clipped.sum(axis=-1, keepdims=True)
    if np.any(total <= 0.0):
        raise ValueError("PSD projection has zero trace")
    proj = np.einsum("...ik,...k,...jk->...ij",
                     vecs, clipped, np.conj(vecs))
    proj = proj / total[..., None]
    projection_fro = np.linalg.norm(proj - rho_raw, axis=(-2, -1))
    return (proj if project else herm), projection_fro


def _entropy_batch_4(rho: np.ndarray) -> np.ndarray:
    vals = np.linalg.eigvalsh(
        0.5 * (rho + np.conj(np.swapaxes(rho, -1, -2))))
    safe = np.where(vals > 1.0e-14, vals, 1.0)
    return -(np.where(vals > 1.0e-14, vals, 0.0) * np.log(safe)).sum(axis=-1)


def _entropy_batch_2(rho: np.ndarray) -> np.ndarray:
    a = rho[..., 0, 0].real
    d = rho[..., 1, 1].real
    c = rho[..., 0, 1]
    half_tr = 0.5 * (a + d)
    disc = np.sqrt(np.maximum(0.25 * (a - d) ** 2 + np.abs(c) ** 2, 0.0))
    lam = np.stack([half_tr + disc, half_tr - disc], axis=-1)
    safe = np.where(lam > 1.0e-14, lam, 1.0)
    return -(np.where(lam > 1.0e-14, lam, 0.0) * np.log(safe)).sum(axis=-1)


def mi_from_pair_rdms(rho: np.ndarray) -> np.ndarray:
    """(..., N_PAIRS, 4, 4) -> full symmetric MI matrices (..., N, N)."""
    r = rho.reshape(rho.shape[:-2] + (2, 2, 2, 2))
    rho_i = np.einsum("...abcb->...ac", r)
    rho_j = np.einsum("...abac->...bc", r)
    s_ij = _entropy_batch_4(rho)
    s_i = _entropy_batch_2(rho_i)
    s_j = _entropy_batch_2(rho_j)
    mi_pairs = np.maximum(s_i + s_j - s_ij, 0.0)
    mi = np.zeros(rho.shape[:-3] + (N_SITES, N_SITES))
    for k, (i, j) in enumerate(PAIRS):
        mi[..., i, j] = mi_pairs[..., k]
        mi[..., j, i] = mi_pairs[..., k]
    return mi


def phi_from_mi(mi: np.ndarray, removed_pair: int | None = None
                ) -> np.ndarray:
    """Batched paper metric: clip, weight, Floyd-Warshall (k ascending)."""
    x = np.clip(mi / I0, X_MIN, 1.0)
    w = -np.log(x)
    idx = np.arange(N_SITES)
    w[..., idx, idx] = 0.0
    if removed_pair is not None:
        i, j = PAIRS[removed_pair]
        w[..., i, j] = np.inf
        w[..., j, i] = np.inf
    d = w
    for k in range(N_SITES):
        d = np.minimum(d, d[..., :, k:k + 1] + d[..., k:k + 1, :])
    return d


def leakage_witness(counts: np.ndarray, z_exc: np.ndarray):
    """counts (..., 27, N_OUT) -> (subset witness, mean excitation).

    witness = 1 - max_r P(>=2 excitations within row r's Z subset);
    mean excitation from pooled Z-marginals: sum_i (1 - <Z_i>)/2.
    """
    shots = counts.sum(axis=-1)
    ge2 = (z_exc >= 2).astype(float)                     # (27, N_OUT)
    p_ge2 = np.einsum("...rx,rx->...r", counts, ge2) / np.maximum(shots, 1.0)
    witness = 1.0 - p_ge2.max(axis=-1)
    freq = counts / np.maximum(shots[..., None], 1.0)
    e_z = freq @ SITE_SIGN.astype(float)                 # (..., 27, N_SITES)
    return witness, e_z


class StateIndex:
    """Frozen bundle layout: state ids -> ordered registry row indices."""

    def __init__(self, registry_rows: list[dict], basis_rows: list[str]):
        self.basis_rows = basis_rows
        by_state: dict[str, list[tuple[int, int]]] = {}
        self.canonical_index = np.array(
            [row["canonical_index"] for row in registry_rows])
        for file_index, row in enumerate(registry_rows):
            if row["arm"] == "control":
                key = f"control_{row['control_occurrence']}"
            else:
                key = row["state_id"]
            by_state.setdefault(key, []).append(
                (row["tomography_row"], file_index))
        self.rows_for = {
            state: np.array([fi for _, fi in sorted(entries)])
            for state, entries in by_state.items()}
        for state, rows in self.rows_for.items():
            if len(rows) != 27:
                raise ValueError(f"state {state} has {len(rows)} settings")
        self.dynamic_ids = [f"dynamic_t{t:03d}" for t in range(37)]
        self.sector_ids = [f"sector_e{k:02d}" for k in range(N_SITES)]
        control_ids = sorted(s for s in self.rows_for
                             if s.startswith("control_"))
        if len(control_ids) != 2:
            raise ValueError(f"expected 2 control states: {control_ids}")
        self.control_ids = control_ids
        missing = [s for s in self.dynamic_ids + self.sector_ids
                   if s not in self.rows_for]
        if missing:
            raise ValueError(f"missing states in registry: {missing}")


def analyze_pass(counts_by_state, index: StateIndex, p_star: np.ndarray,
                 w1: np.ndarray, w2: np.ndarray, z_exc: np.ndarray,
                 project: bool = True, keep_per_time: bool = False,
                 track_leakage: bool = True):
    """Run the complete analysis path on per-state count batches.

    counts_by_state: callable state_id -> (..., 27, N_OUT) float/int array
    (leading batch dims shared across states, e.g. (B, 3) for bootstrap
    replicates x {full, h1, h2} slots).

    Returns a dict with dbar, phi_star, eps, per-state metric pieces,
    projection diagnostics, leakage witness stats, and (optionally) the
    per-time metric and MI stacks needed for LOTO/LOPO.
    """
    dbar_sum = None
    phi_t_list = [] if keep_per_time else None
    mi_t_list = [] if keep_per_time else None
    proj_max = None
    proj_sum = None
    proj_cnt = 0
    witness_min = None
    exc_sums = []

    def _reconstruct(state_id):
        counts = counts_by_state(state_id)
        rho_raw = pair_rdms_from_counts(counts, w1, w2)
        rho_used, proj_fro = hermitize_project_batch(rho_raw, project)
        return counts, rho_used, proj_fro

    def _track_proj(proj_fro):
        nonlocal proj_max, proj_sum, proj_cnt
        m = proj_fro.max(axis=-1)
        s = proj_fro.sum(axis=-1)
        proj_max = m if proj_max is None else np.maximum(proj_max, m)
        proj_sum = s if proj_sum is None else proj_sum + s
        proj_cnt += proj_fro.shape[-1]

    def _track_leakage(counts):
        nonlocal witness_min
        if not track_leakage:
            return
        witness, e_z = leakage_witness(counts, z_exc)
        witness_min = (witness if witness_min is None
                       else np.minimum(witness_min, witness))
        exc_sums.append(e_z)

    for t, state_id in enumerate(index.dynamic_ids):
        counts, rho_used, proj_fro = _reconstruct(state_id)
        _track_proj(proj_fro)
        _track_leakage(counts)
        mi_t = mi_from_pair_rdms(rho_used)
        phi_t = phi_from_mi(mi_t)
        dbar_sum = phi_t if dbar_sum is None else dbar_sum + phi_t
        if keep_per_time:
            phi_t_list.append(phi_t)
            mi_t_list.append(mi_t)
    dbar = dbar_sum / len(index.dynamic_ids)

    sigma_mix = None
    for k, state_id in enumerate(index.sector_ids):
        counts, rho_used, proj_fro = _reconstruct(state_id)
        _track_proj(proj_fro)
        _track_leakage(counts)
        term = p_star[k] * rho_used
        sigma_mix = term if sigma_mix is None else sigma_mix + term
    mi_star = mi_from_pair_rdms(sigma_mix)
    phi_star = phi_from_mi(mi_star)

    phi_controls = []
    for state_id in index.control_ids:
        counts, rho_used, proj_fro = _reconstruct(state_id)
        _track_proj(proj_fro)
        _track_leakage(counts)
        phi_controls.append(phi_from_mi(mi_from_pair_rdms(rho_used)))

    dbar_norm = np.linalg.norm(dbar, axis=(-2, -1))
    eps = np.linalg.norm(phi_star - dbar, axis=(-2, -1)) / dbar_norm

    # mean excitation across all prepared states from pooled Z-marginals
    if track_leakage:
        e_z_all = np.stack(exc_sums, axis=0)  # (n_states, ..., 27, N_SITES)
        z_site = np.einsum("s...ri,ri->s...i", e_z_all, w1[:, :, 2])
        mean_exc = ((1.0 - z_site) / 2.0).sum(axis=-1)
    else:
        mean_exc = None

    return {
        "dbar": dbar,
        "dbar_norm": dbar_norm,
        "phi_star": phi_star,
        "mi_star": mi_star,
        "eps": eps,
        "phi_controls": phi_controls,
        "phi_t": phi_t_list,
        "mi_t": mi_t_list,
        "proj_max": proj_max,
        "proj_mean": proj_sum / proj_cnt,
        "witness_min": witness_min,
        "mean_excitation": mean_exc,
    }


def floors_from_slots(result: dict) -> dict:
    """Split-shot and duplicate-control floors from {full, h1, h2} slots.

    Expects every batched quantity to carry a slot axis of size 3 as its
    LAST batch dimension (slot 0 = full counts, 1 and 2 = the two random
    half-shot arms).  All discrepancies are normalized by the full-slot
    ||Dbar||_F, conservative max over moving-arm and comparator-arm
    splits.
    """
    dbar, phi_star = result["dbar"], result["phi_star"]
    norm_full = result["dbar_norm"][..., 0]
    split_moving = np.linalg.norm(
        dbar[..., 1, :, :] - dbar[..., 2, :, :], axis=(-2, -1)) / norm_full
    split_comp = np.linalg.norm(
        phi_star[..., 1, :, :] - phi_star[..., 2, :, :],
        axis=(-2, -1)) / norm_full
    dup = np.linalg.norm(
        result["phi_controls"][0][..., 0, :, :]
        - result["phi_controls"][1][..., 0, :, :], axis=(-2, -1)) / norm_full
    split = np.maximum(split_moving, split_comp)
    return {
        "split_moving": split_moving,
        "split_comparator": split_comp,
        "split": split,
        "duplicate": dup,
        "floor": np.maximum(split, dup),
    }


def draw_main_halves(probs: np.ndarray, base: int, experiment: int,
                     canonical_index: np.ndarray,
                     shots: int = SHOTS) -> np.ndarray:
    """(n_circuits, 2, N_OUT) uint16 main-experiment half draws."""
    n = len(probs)
    half = shots // 2
    out = np.empty((n, 2, N_OUT), dtype=np.uint16)
    for c in range(n):
        rng = np.random.default_rng(np.random.SeedSequence(
            [base, int(canonical_index[c]), experiment]))
        out[c] = rng.multinomial(half, probs[c], size=2)
    return out


def load_bundle(root: Path):
    """Load registry rows, manifest, and basis strings for the analysis."""
    bundle_dir = root / "hardware" / "ibm_exp1" / "bundle"
    manifest = json.loads(
        (root / "hardware" / "ibm_exp1" / "manifest"
         / "hardware_manifest.json").read_text(encoding="utf-8"))
    registry = json.loads(
        (bundle_dir / "circuit_registry.json").read_text(encoding="utf-8"))
    basis_rows = manifest["tomography"]["basis_strings_paper_order"]
    return manifest, registry, basis_rows
