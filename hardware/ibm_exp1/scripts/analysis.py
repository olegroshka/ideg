"""The single analysis implementation for S1 and S2 (AR-023a).

Four defects in this programme had one shape: an amendment item was
applied to one analysis path and silently not the other, leaving code
that still ran and still returned plausible numbers while answering a
retired question (A2.1 floor, A2.5c leakage, A2.10 statistic, and the
retired half of S2-G3).  Structural guard tests pin the paths together
but cannot check semantics.  This module removes the second path.

The ideal (S1) case is the degenerate case of the noisy (S2) case:
pass `cal_probs=None` and the M3 branch becomes exactly the identity,
so corrected counts equal raw counts, the M3 endpoint equals the raw
endpoint, and clause 4 is satisfied by construction rather than by a
special case in the caller.

Seed streams are reproduced exactly as the separate implementations had
them, via `seed_prefix`:
    S1: prefix = ()            -> [BASE, canonical, r]
    S2: prefix = (cond_index,) -> [BASE, cond_index, canonical, r]
with bootstrap [BASE, *prefix, 10**6 + r] and M3 calibration
[BASE, *prefix, 5*10**6 + r].
"""

from __future__ import annotations

import numpy as np

import sampling
from sampling import (N_OUT, StateIndex, analyze_pass,  # noqa: F401
                      endpoint_floor, endpoint_from_stacks, phi_from_mi,
                      survival_from_allz)
import s2lib


def structural_excursions(exact_mi_t: np.ndarray,
                          comparator_rdms: np.ndarray,
                          p_star: np.ndarray) -> np.ndarray:
    """Per-variant excursion of eps on the EXACT metric (A2.4).

    Order: leave-one-time-out variants, then leave-one-pair-out.  The
    dominance clause compares the data's excursion against this, so it
    measures MEASUREMENT dominance rather than the graph structure the
    exact metric already exhibits (removing pair (0,9) — the chain's two
    ends — shifts eps by 0.026 with no noise present at all).
    """
    mi_star = sampling.mi_from_pair_rdms(
        np.tensordot(p_star, comparator_rdms, axes=(0, 0)))
    phi_t = phi_from_mi(exact_mi_t)
    star = phi_from_mi(mi_star)
    dbar = phi_t.mean(axis=0)
    e0 = float(np.linalg.norm(star - dbar) / np.linalg.norm(dbar))
    out = []
    total = phi_t.sum(axis=0)
    n_t = len(phi_t)
    for t_index in range(n_t):
        d_t = (total - phi_t[t_index]) / (n_t - 1)
        out.append(abs(float(np.linalg.norm(star - d_t)
                             / np.linalg.norm(d_t)) - e0))
    for k in range(sampling.N_PAIRS):
        stack = np.concatenate([exact_mi_t, mi_star[None]], axis=0)
        phi_all = phi_from_mi(stack, removed_pair=k)
        d_k = phi_all[:n_t].mean(axis=0)
        out.append(abs(float(np.linalg.norm(phi_all[n_t] - d_k)
                             / np.linalg.norm(d_k)) - e0))
    return np.asarray(out)


def _identity_inverses() -> np.ndarray:
    return np.stack([np.eye(2) for _ in range(sampling.N_SITES)])


def evaluate_experiment(*, probs, index: StateIndex, p_star, w1, w2,
                        z_exc, exact_excursions, control_mode, eps_ref,
                        r: int, base: int, shots: int, n_boot: int,
                        seed_prefix: tuple = (), cal_probs=None) -> dict:
    """One synthetic experiment under AR-023a Amendment 2.

    cal_probs=None selects the ideal backend: the M3 correction is the
    identity, so raw and corrected coincide exactly.
    """
    prefix = tuple(int(x) for x in seed_prefix)
    half_shots = shots // 2
    n_circ = len(probs)
    canonical = index.canonical_index

    # ---- main draws: two independent half-shot arms per circuit
    main_halves = np.empty((n_circ, 2, N_OUT), dtype=np.uint16)
    for c in range(n_circ):
        rng = np.random.default_rng(np.random.SeedSequence(
            [base, *prefix, int(canonical[c]), r]))
        main_halves[c] = rng.multinomial(half_shots, probs[c], size=2)
    main_full = main_halves.sum(axis=1)

    def main_counts(state_id):
        rows = index.rows_for[state_id]
        h = main_halves[rows]
        return np.stack([main_full[rows], h[:, 0], h[:, 1]],
                        axis=0).astype(float)

    def rdm_stack(state_ids, source):
        used_list, proj_list = [], []
        for state_id in state_ids:
            counts = source[index.rows_for[state_id]].astype(float)
            raw = sampling.pair_rdms_from_counts(counts, w1, w2)
            used, proj = sampling.hermitize_project_batch(raw, True)
            used_list.append(used)
            proj_list.append(proj)
        return np.stack(used_list), np.concatenate(proj_list)

    dyn_f, proj_dyn = rdm_stack(index.dynamic_ids, main_full)
    sec_f, proj_sec = rdm_stack(index.sector_ids, main_full)
    ctl_f, proj_ctl = rdm_stack(index.control_ids, main_full)
    proj_all = np.concatenate([proj_dyn, proj_sec, proj_ctl])
    proj_max = float(proj_all.max())
    proj_median = float(np.median(proj_all))

    eps_main, phi_t, dbar, star, mi_t, mi_star = endpoint_from_stacks(
        dyn_f, sec_f, p_star)

    # ---- A2.1 floor: split arm (shot noise) and duplicate arm (drift)
    eps_halves = []
    for h in range(2):
        arm = main_halves[:, h]
        eps_halves.append(endpoint_from_stacks(
            rdm_stack(index.dynamic_ids, arm)[0],
            rdm_stack(index.sector_ids, arm)[0], p_star)[0])
    eps_ctrl = []
    for c in range(2):
        sec_alt = sec_f.copy()
        sec_alt[int(control_mode)] = ctl_f[c]
        eps_ctrl.append(endpoint_from_stacks(dyn_f, sec_alt, p_star)[0])
    floors = endpoint_floor(eps_halves[0], eps_halves[1],
                            eps_ctrl[0], eps_ctrl[1])
    duplicate = floors["duplicate"]      # systematic: never bootstrapped

    # ---- M3 branch (identity when cal_probs is None)
    if cal_probs is None:
        inverses = _identity_inverses()
    else:
        cal_root = np.random.SeedSequence(
            [base, *prefix, 5 * 10 ** 6 + r])
        cal_children = cal_root.spawn(2)
        cal_counts = np.stack([
            np.random.default_rng(cal_children[k]).multinomial(
                shots,
                np.clip(cal_probs[k], 0.0, None)
                / cal_probs[k].clip(0).sum())
            for k in range(2)])
        inverses = s2lib.confusion_inverses(
            s2lib.estimate_confusions(cal_counts))

    def m3_counts(state_id):
        return s2lib.apply_confusion(main_counts(state_id), inverses)

    m3_full = s2lib.apply_confusion(main_full.astype(float), inverses)
    m3_h = [s2lib.apply_confusion(main_halves[:, h].astype(float),
                                  inverses) for h in range(2)]
    dyn_m3 = rdm_stack(index.dynamic_ids, m3_full)[0]
    sec_m3 = rdm_stack(index.sector_ids, m3_full)[0]
    ctl_m3 = rdm_stack(index.control_ids, m3_full)[0]
    eps_m3 = endpoint_from_stacks(dyn_m3, sec_m3, p_star)[0]
    eps_m3_halves = [endpoint_from_stacks(
        rdm_stack(index.dynamic_ids, arm)[0],
        rdm_stack(index.sector_ids, arm)[0], p_star)[0] for arm in m3_h]
    eps_m3_ctrl = []
    for c in range(2):
        alt = sec_m3.copy()
        alt[int(control_mode)] = ctl_m3[c]
        eps_m3_ctrl.append(endpoint_from_stacks(dyn_m3, alt, p_star)[0])
    floors_m3 = endpoint_floor(eps_m3_halves[0], eps_m3_halves[1],
                               eps_m3_ctrl[0], eps_m3_ctrl[1])
    delta_m3 = eps_m3 - float(floors_m3["floor"])

    # ---- A2.5 leakage witness, raw and corrected
    surv_raw, surv_corr = [], []
    for state_id in index.dynamic_ids + index.sector_ids:
        row = index.leak_row_for.get(state_id)
        if row is None:
            continue
        raw_counts = main_full[row].astype(float)
        surv_raw.append(float(survival_from_allz(raw_counts)))
        surv_corr.append(float(survival_from_allz(
            s2lib.apply_confusion(raw_counts, inverses), project=True)))
    surv_raw = np.asarray(surv_raw) if surv_raw else np.array([1.0])
    surv_corr = np.asarray(surv_corr) if surv_corr else np.array([1.0])

    # ---- bootstrap: split arm only (A2.2)
    emp = main_full.astype(float) / shots
    boot_root = np.random.SeedSequence([base, *prefix, 10 ** 6 + r])
    children = boot_root.spawn(n_circ)

    def boot_counts(state_id):
        rows = index.rows_for[state_id]
        out = np.empty((n_boot, 3, len(rows), N_OUT), dtype=np.uint16)
        for slot_index, c in enumerate(rows):
            rng = np.random.default_rng(children[c])
            halves = rng.multinomial(half_shots, emp[c], size=(n_boot, 2))
            out[:, 0, slot_index] = halves.sum(axis=1)
            out[:, 1, slot_index] = halves[:, 0]
            out[:, 2, slot_index] = halves[:, 1]
        return out

    boot = analyze_pass(boot_counts, index, p_star, w1, w2, z_exc,
                        project=True, keep_per_time=False,
                        track_leakage=False)
    eps_b = boot["eps"][:, 0]
    split_b = np.abs(boot["eps"][:, 1] - boot["eps"][:, 2])
    delta_b = eps_b - np.maximum(split_b, duplicate)
    eps_floor_exp = float(max(np.median(split_b), duplicate))

    delta_main = eps_main - floors["floor"]
    delta_median = float(np.median(delta_b))
    ci_low = float(np.quantile(delta_b, 0.025))
    ci_high = float(np.quantile(delta_b, 0.975))

    # ---- A2.4 dominance: excess over the exact structural excursion
    variants = []
    total = phi_t.sum(axis=0)
    n_t = len(phi_t)
    for t_index in range(n_t):
        d_t = (total - phi_t[t_index]) / (n_t - 1)
        e = float(np.linalg.norm(star - d_t) / np.linalg.norm(d_t))
        variants.append(e - floors["floor"])
    for k in range(sampling.N_PAIRS):
        stack = np.concatenate([mi_t, mi_star[None]], axis=0)
        phi_all = phi_from_mi(stack, removed_pair=k)
        d_k = phi_all[:n_t].mean(axis=0)
        e = float(np.linalg.norm(phi_all[n_t] - d_k) / np.linalg.norm(d_k))
        variants.append(e - floors["floor"])
    variants = np.asarray(variants)
    raw_exc = np.abs(variants - delta_main)
    excess = np.abs(raw_exc - exact_excursions)
    tol = 0.25 * abs(delta_median)
    sign_flip = bool(np.any(np.sign(variants) != np.sign(delta_main)))

    clause_1 = bool(ci_low > 0.0)
    clause_2 = bool(np.median(eps_b) >= 2.0 * eps_floor_exp)
    clause_3 = bool(surv_corr.min() >= 0.70)
    clause_4 = bool(np.sign(delta_m3) == np.sign(delta_main))
    clause_5 = bool(float(excess.max()) <= tol and not sign_flip
                    and proj_median < 0.05)          # A2.3 + A2.10
    clauses = {
        "1_delta_ci_above_zero": clause_1,
        "2_eps_ge_2floor": clause_2,
        "3_leakage_not_red": clause_3,
        "4_raw_m3_direction": clause_4,
        "5_no_dominance": clause_5,
    }

    return {
        "experiment": r,
        "rule": "AR-023a Amendment 2",
        "eps_main": eps_main,
        "eps_boot_median": float(np.median(eps_b)),
        "eps_boot_q025": float(np.quantile(eps_b, 0.025)),
        "eps_boot_q975": float(np.quantile(eps_b, 0.975)),
        "eps_half_1": eps_halves[0],
        "eps_half_2": eps_halves[1],
        "eps_ctrl_early": eps_ctrl[0],
        "eps_ctrl_late": eps_ctrl[1],
        "eps_m3_main": eps_m3,
        "eps_m3_minus_raw": eps_m3 - eps_main,
        "delta_m3_main": delta_m3,
        "floor_split_main": floors["split"],
        "floor_duplicate_main": duplicate,
        "floor_main": floors["floor"],
        "floor_m3_main": float(floors_m3["floor"]),
        "floor_split_boot_median": float(np.median(split_b)),
        "eps_floor_experiment": eps_floor_exp,
        "delta_main": delta_main,
        "delta_boot_median": delta_median,
        "delta_ci95": [ci_low, ci_high],
        "proj_fro_max_main": proj_max,
        "proj_fro_median_main": proj_median,
        "leakage_survival_min": float(surv_corr.min()),
        "leakage_survival_median": float(np.median(surv_corr)),
        "leakage_survival_corrected_min": float(surv_corr.min()),
        "leakage_survival_corrected_median": float(np.median(surv_corr)),
        "leakage_survival_raw_min": float(surv_raw.min()),
        "leakage_survival_raw_median": float(np.median(surv_raw)),
        "loto_lopo_raw_excursion_max": float(raw_exc.max()),
        "loto_lopo_excess_max": float(excess.max()),
        "loto_lopo_sign_flip": sign_flip,
        "clause_5a_tolerance": float(tol),
        "clauses": clauses,
        "success_rule": all(clauses.values()),
        "abs_eps_minus_ref": (abs(eps_main - eps_ref)
                              if eps_ref is not None else None),
    }
