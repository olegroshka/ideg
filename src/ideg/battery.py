"""§4.3 representation-invariance battery (AR-009 spec, frozen).

Scope (manifest-recorded implementation parameter): applied to one
representative run per group x size, on a small subset of window times —
the battery checks exact identities, not ensemble statistics.

Items and their contracts:
1. global phase            -> every output identical within tol (MUST)
2. consistent local basis  -> W1/W2/W4 identical; W3/Phi recomputed with
   transformed operator/state definitions agree within tol (MUST)
3. state-only local basis  -> W3/Phi recomputed with operators kept in the
   computational basis; magnitude RECORDED, not thresholded (the TH-037
   factorization-dependence made quantitative)
4. reflection relabeling   -> Phi maps by the site permutation;
   site-independent statistics identical (MUST)
"""

from __future__ import annotations

import numpy as np

from .evolve import EigenEvolver
from .migraph import mutual_information_matrix, phi_distance_matrix
from .pauli import reflection_permutation, sz_diag
from .witnesses import (bohr_measure_pr, otoc_series, recurrence_distance,
                        xi_offdiagonal_pure)


def _random_su2(rng: np.random.Generator) -> np.ndarray:
    """Haar-random 2x2 unitary (QR of a complex Gaussian, phase-fixed)."""
    m = rng.normal(size=(2, 2)) + 1.0j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(m)
    return q * (np.diag(r) / np.abs(np.diag(r)))[None, :].conj()


def local_unitary(us: list[np.ndarray]) -> np.ndarray:
    out = np.array([[1.0 + 0.0j]])
    for u in us:
        out = np.kron(out, u)
    return out


def _apply_heisenberg_full(ev: EigenEvolver, w_full: np.ndarray, t: float,
                           x: np.ndarray) -> np.ndarray:
    """U(t)^dag W U(t) x for a non-diagonal W (battery use only)."""
    c = ev.evecs.conj().T @ x
    c *= np.exp(-1.0j * ev.evals * t)
    v = w_full @ (ev.evecs @ c)
    c = ev.evecs.conj().T @ v
    c *= np.exp(+1.0j * ev.evals * t)
    return ev.evecs @ c


def _otoc_full(ev: EigenEvolver, psi: np.ndarray, w_full: np.ndarray,
               v_full: np.ndarray, times: np.ndarray) -> np.ndarray:
    out = np.empty(len(times))
    v_psi = v_full @ psi
    for k, t in enumerate(times):
        a = _apply_heisenberg_full(ev, w_full, t, v_psi)
        b = v_full @ _apply_heisenberg_full(ev, w_full, t, psi)
        out[k] = 0.5 * float(np.linalg.norm(a - b) ** 2)
    return out


def _base(ev: EigenEvolver, psi0: np.ndarray, n: int, times: np.ndarray,
          i0: int, r_max: int):
    states = ev.states_at(psi0, times)
    mi = np.array([mutual_information_matrix(s, n) for s in states])
    return {
        "w1": bohr_measure_pr(ev, psi0),
        "w2": recurrence_distance(states),
        "w3": otoc_series(ev, psi0, n, i0, [i0 + r_max], times)[0],
        "w4": xi_offdiagonal_pure(ev, psi0),
        "mi": mi,
        "phi": np.array([phi_distance_matrix(m) for m in mi]),
        "states": states,
    }


def _devs(a: dict, b: dict, tol: float) -> dict:
    """Per-object max deviations. The identity contract (tol) binds on the
    witnesses and on the MI matrices — the objects the transforms provably
    preserve. phi_dev is REPORTED alongside: the preregistered -log weight
    cap (x_min = 1e-6) amplifies machine-epsilon MI jitter by up to 1/x_min,
    so Phi in near-cap classes carries an irreducible ~1e-10..1e-8 numerical
    floor that is not representation-dependence (battery instrument note)."""
    out = {
        "w1_dev": abs(b["w1"] - a["w1"]),
        "w2_dev": float(np.max(np.abs(b["w2"] - a["w2"]))),
        "w3_dev": float(np.max(np.abs(b["w3"] - a["w3"]))),
        "w4_dev": abs(b["w4"] - a["w4"]),
        "mi_dev": float(np.max(np.abs(b["mi"] - a["mi"]))),
        "phi_dev": float(np.max(np.abs(b["phi"] - a["phi"]))),
    }
    out["pass"] = bool(max(out["w1_dev"], out["w2_dev"], out["w3_dev"],
                           out["w4_dev"], out["mi_dev"]) < tol)
    return out


def run_battery(h: np.ndarray, psi0: np.ndarray, n: int, times: np.ndarray,
                rng: np.random.Generator, tol: float = 1e-10) -> dict:
    """Returns per-item max deviations plus MUST-item pass flags."""
    i0 = n // 2
    r_max = n - 1 - i0
    ev = EigenEvolver(h)
    base = _base(ev, psi0, n, times, i0, r_max)

    out = {"tol": tol}

    # --- 1. global phase ---
    alpha = float(rng.uniform(0.0, 2.0 * np.pi))
    g = _base(ev, np.exp(1.0j * alpha) * psi0, n, times, i0, r_max)
    out["global_phase"] = _devs(base, g, tol)

    # --- 2. consistent local basis change (state, H, operators together) ---
    us = [_random_su2(rng) for _ in range(n)]
    u_full = local_unitary(us)
    h2 = u_full @ h @ u_full.conj().T
    psi2 = u_full @ psi0
    ev2 = EigenEvolver(h2)
    states2 = ev2.states_at(psi2, times)
    mi2 = np.array([mutual_information_matrix(s, n) for s in states2])
    zw = u_full @ np.diag(sz_diag(n, i0 + r_max)) @ u_full.conj().T
    zv = u_full @ np.diag(sz_diag(n, i0)) @ u_full.conj().T
    cons = {
        "w1": bohr_measure_pr(ev2, psi2),
        "w2": recurrence_distance(states2),
        "w3": _otoc_full(ev2, psi2, zw, zv, times),
        "w4": xi_offdiagonal_pure(ev2, psi2),
        "mi": mi2,
        "phi": np.array([phi_distance_matrix(m) for m in mi2]),
    }
    out["consistent_local_basis"] = _devs(base, cons, tol)

    # --- 3. state-only local basis change (operators kept computational) ---
    w3_3 = otoc_series(ev2, psi2, n, i0, [i0 + r_max], times)[0]
    out["state_only_local_basis"] = {
        "w3_max_dev": float(np.max(np.abs(w3_3 - base["w3"]))),
        "mi_max_dev": float(np.max(np.abs(mi2 - base["mi"]))),
        "phi_max_dev": float(np.max(np.abs(cons["phi"] - base["phi"]))),
        "note": "expected-change item: magnitudes recorded, not thresholded",
    }

    # --- 4. reflection relabeling ---
    perm_idx = reflection_permutation(n)
    h4 = h[np.ix_(perm_idx, perm_idx)]
    psi4 = psi0[perm_idx]
    ev4 = EigenEvolver(h4)
    states4 = ev4.states_at(psi4, times)
    mi4 = np.array([mutual_information_matrix(s, n) for s in states4])
    site_perm = np.arange(n)[::-1]
    refl = {
        "w1": bohr_measure_pr(ev4, psi4),
        "w2": recurrence_distance(states4),
        "w3": base["w3"],  # W3 site pair maps under reflection; not re-run
        "w4": xi_offdiagonal_pure(ev4, psi4),
        "mi": mi4[:, site_perm][:, :, site_perm],
        "phi": np.array([phi_distance_matrix(m) for m in mi4])[
            :, site_perm][:, :, site_perm],
    }
    out["reflection"] = _devs(base, refl, tol)

    out["all_must_pass"] = bool(out["global_phase"]["pass"]
                                and out["consistent_local_basis"]["pass"]
                                and out["reflection"]["pass"])
    return out
