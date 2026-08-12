"""AR-010 confirmatory analysis (spec §5.1, §5.2, §5.3, §4.4, §6.4).

Reads results/AR-010/confirmatory/*.json (written by confirmatory.py and
confirmatory_tb.py against the committed manifest) and produces
confirmatory_summary.json plus a printed verdict block. All thresholds are
the preregistered ones; nothing here is tunable.
"""

import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.stats import auc, bootstrap_ci_mean, cis_disjoint  # noqa: E402

OUT = ROOT / "results" / "AR-010"
CONF = OUT / "confirmatory"
MAN = json.loads((OUT / "confirmatory_manifest.json").read_text())
_add_path = OUT / "confirmatory_manifest_addendum1.json"
ADDENDUM = json.loads(_add_path.read_text()) if _add_path.exists() else None
if ADDENDUM:
    MAN["criterion_a"]["size_pairs"].update(
        ADDENDUM["criterion_a_size_pairs_override"])
    for prot, tracks in ADDENDUM["criterion_b_size_pairs_override"].items():
        MAN["criterion_b"]["size_pairs"][prot].update(tracks)
    MAN["sizes"]["TA_i_fixed_point"] = [8, 10, 12]
    MAN["sizes"]["TA_ii_quasiperiodic"] = [10, 12]
    MAN["sizes"]["TA_iii_chaotic"] = [8, 10, 12]
    MAN["sizes"]["TA_iv_metastable"] = [8, 10, 12]

TA = ["TA_i_fixed_point", "TA_ii_quasiperiodic", "TA_iii_chaotic",
      "TA_iv_metastable"]
TC = ["TC_scrambling", "TC_integrable", "TC_localized"]
STATS = MAN["criterion_a"]["statistics"]          # pr_A, w2_min, c_sat, t*, xi
AUC_T = MAN["criterion_a"]["auc_threshold"]
MIN_STATS = MAN["criterion_a"]["min_statistics"]
LN_T = MAN["criterion_b"]["effect_threshold_ln"]
PROTOCOLS = ["quench", "dephasing", "loss"]

STAT_KEYS = {"pr_A": ("witnesses", "pr_A"), "w2_min": ("witnesses", "w2_min"),
             "otoc_c_sat": ("witnesses", "otoc_c_sat"),
             "otoc_t_star": ("witnesses", "otoc_t_star"),
             "xi": ("witnesses", "xi")}


def load(group, n):
    return json.loads((CONF / f"{group}_N{n}.json").read_text())


def ensemble_values(group, n, path):
    """Per-ensemble-unit values; TC_localized aggregates its 5 states to the
    realization mean (spec §6.1 resampling unit)."""
    data = load(group, n)
    vals = []
    for run in data["runs"]:
        sv = []
        for st in run["states"]:
            v = st
            for k in path:
                v = v[k]
            sv.append(v)
        vals.append(float(np.mean(sv)))
    return np.array(vals)


def exact_value_sep(exact, other):
    """Class-(i) rule: the other ensemble's range excludes the exact value."""
    return bool(np.min(other) > exact or np.max(other) < exact)


# ---------------- §4.4 null comparator ----------------
null_report = {}
w3_fired_on_null = False
for n in MAN["sizes"]["TA_i_fixed_point"]:
    d = load("TA_i_fixed_point", n)
    w = d["runs"][0]["states"][0]["witnesses"]
    b = d["runs"][0]["states"][0]["baseline"]
    fires_w3 = bool(np.isfinite(w["otoc_t_star"]))
    w3_fired_on_null = w3_fired_on_null or fires_w3
    null_report[str(n)] = {
        "pr_A": w["pr_A"], "w2_min": w["w2_min"], "w2_mean": w["w2_mean"],
        "xi": w["xi"], "otoc_c_sat": w["otoc_c_sat"],
        "otoc_t_star": w["otoc_t_star"],
        "max_delta_phi": b["max_delta_phi"],
        "silent": bool(abs(w["pr_A"] - 1.0) < 1e-9 and w["w2_mean"] < 1e-9
                       and w["xi"] < 1e-9 and not fires_w3),
        "w3_fires": fires_w3,
    }
active_stats = ([s for s in STATS if not s.startswith("otoc")]
                if w3_fired_on_null else STATS)

# ---------------- criterion (a) ----------------
crit_a = {"active_statistics": active_stats,
          "w3_discarded_by_null": w3_fired_on_null, "tracks": {}}
for track, groups, sizes in [("TA", TA, MAN["criterion_a"]["size_pairs"]
                              ["TA"]),
                             ("TC", TC, MAN["criterion_a"]["size_pairs"]
                              ["TC"])]:
    track_out = {}
    for n in sizes:
        vals = {g: {s: ensemble_values(g, n, STAT_KEYS[s])
                    for s in active_stats} for g in groups}
        pairs_out = {}
        for ga, gb in combinations(groups, 2):
            per_stat = {}
            for s in active_stats:
                a_vals, b_vals = vals[ga][s], vals[gb][s]
                if len(a_vals) == 1:            # class (i) singleton
                    per_stat[s] = {"rule": "exact-value",
                                   "exact": float(a_vals[0]),
                                   "separates": exact_value_sep(a_vals[0],
                                                                b_vals)}
                elif len(b_vals) == 1:
                    per_stat[s] = {"rule": "exact-value",
                                   "exact": float(b_vals[0]),
                                   "separates": exact_value_sep(b_vals[0],
                                                                a_vals)}
                else:
                    a_ = auc(a_vals, b_vals)
                    per_stat[s] = {"rule": "auc", "auc": a_,
                                   "separates": bool(a_ >= AUC_T)}
            n_sep = sum(v["separates"] for v in per_stat.values())
            pairs_out[f"{ga}|{gb}"] = {"stats": per_stat,
                                       "n_separating": n_sep,
                                       "pass": bool(n_sep >= MIN_STATS)}
        track_out[str(n)] = {"pairs": pairs_out,
                             "all_pairs_pass": bool(all(
                                 p["pass"] for p in pairs_out.values()))}
    track_out["holds"] = bool(all(track_out[str(n)]["all_pairs_pass"]
                                  for n in sizes))
    crit_a["tracks"][track] = track_out
crit_a["holds"] = bool(all(t["holds"] for t in crit_a["tracks"].values()))

# ---------------- criterion (b) ----------------
crit_b = {"protocols": {}}
for prot in PROTOCOLS:
    prot_out = {"tracks": {}}
    for track, groups in [("TA", TA), ("TC", TC)]:
        sizes = MAN["criterion_b"]["size_pairs"][prot][track]
        track_out = {}
        for n in sizes:
            gvals = {}
            for g in groups:
                try:
                    gvals[g] = ensemble_values(g, n,
                                               ("protocols", prot,
                                                "log_rho"))
                except (FileNotFoundError, KeyError):
                    continue
            cis = {g: bootstrap_ci_mean(v) for g, v in gvals.items()
                   if len(v) > 0}
            pairs = {}
            for ga, gb in combinations([g for g in groups if g in cis], 2):
                diff = cis[ga][0] - cis[gb][0]
                pairs[f"{ga}|{gb}"] = {
                    "mean_diff": diff,
                    "exceeds_ln1.5": bool(abs(diff) > LN_T),
                    "cis_disjoint": cis_disjoint(cis[ga], cis[gb]),
                    "pass": bool(abs(diff) > LN_T
                                 and cis_disjoint(cis[ga], cis[gb])),
                    "direction": int(np.sign(diff)),
                }
            track_out[str(n)] = {
                "group_means": {g: {"mean": c[0], "ci": [c[1], c[2]]}
                                for g, c in cis.items()},
                "pairs": pairs,
            }
        # replication: same pair passing at both sizes with same direction
        replicated = []
        if len(sizes) == 2:
            p0 = track_out[str(sizes[0])]["pairs"]
            p1 = track_out[str(sizes[1])]["pairs"]
            for key in p0:
                if key in p1 and p0[key]["pass"] and p1[key]["pass"] \
                        and p0[key]["direction"] == p1[key]["direction"]:
                    replicated.append(key)
        track_out["replicated_pairs"] = replicated
        prot_out["tracks"][track] = track_out
    prot_out["any_replicated"] = bool(any(
        t["replicated_pairs"] for t in prot_out["tracks"].values()))
    crit_b["protocols"][prot] = prot_out
crit_b["holds"] = bool(any(p["any_replicated"]
                           for p in crit_b["protocols"].values()))

# ---------------- §5.3 sustained-by adjudication (N = 10) ----------------
adjudication = {}
for g in TA + TC:
    d = load(g, 10)
    xi_dyn, xi_bar, so_delta, unpert_post = [], [], [], []
    comp_lr = {p: [] for p in PROTOCOLS}
    dyn_lr = {p: [] for p in PROTOCOLS}
    for run in d["runs"]:
        for st in run["states"]:
            if "comparator" not in st:
                continue
            xi_dyn.append(st["witnesses"]["xi"])
            xi_bar.append(st["comparator"]["xi_rho_bar"])
            so_delta.append(st["comparator"]["switchoff_delta_vs_run"])
            unpert_post.append(st["baseline"]["max_delta_phi_post"])
            for p in PROTOCOLS:
                if p in st["comparator"]["protocols"] \
                        and p in st["protocols"]:
                    comp_lr[p].append(st["comparator"]["protocols"][p]
                                      ["log_rho"])
                    dyn_lr[p].append(st["protocols"][p]["log_rho"])
    check1 = bool(len(xi_dyn) > 0
                  and np.min(xi_dyn) > max(np.max(xi_bar), 1e-9))
    prot_arms = {}
    for p in PROTOCOLS:
        if not dyn_lr[p]:
            continue
        ci_d = bootstrap_ci_mean(np.array(dyn_lr[p]))
        ci_c = bootstrap_ci_mean(np.array(comp_lr[p]))
        prot_arms[p] = {"dyn": {"mean": ci_d[0], "ci": [ci_d[1], ci_d[2]]},
                        "comp": {"mean": ci_c[0], "ci": [ci_c[1], ci_c[2]]},
                        "disjoint": cis_disjoint(ci_d, ci_c)}
    ci_so = bootstrap_ci_mean(np.array(so_delta)) if so_delta else None
    ci_up = bootstrap_ci_mean(np.array(unpert_post)) if unpert_post else None
    switchoff_arm = bool(ci_so and ci_up and cis_disjoint(ci_so, ci_up)
                         and ci_so[0] > ci_up[0])
    check2 = bool(any(v["disjoint"] for v in prot_arms.values())
                  or switchoff_arm)
    adjudication[g] = {
        "check1_witness_vs_comparator": check1,
        "xi_dyn_min": float(np.min(xi_dyn)) if xi_dyn else None,
        "xi_rho_bar_max": float(np.max(xi_bar)) if xi_bar else None,
        "check2_robustness_or_switchoff": check2,
        "protocol_arms": prot_arms,
        "switchoff": {"delta_ci": ci_so, "unpert_post_ci": ci_up,
                      "drift_increase_disjoint": switchoff_arm},
        "verdict": ("sustained-by" if check1 and check2
                    else "compatible-with"),
    }

# ---------------- stationarity + cap diagnostics table ----------------
station = {}
for g in TA + TC:
    for n in MAN["sizes"][g]:
        d = load(g, n)
        mx, cap_sub, cap_frac, slopes, norm_drift = [], [], [], [], []
        for run in d["runs"]:
            for st in run["states"]:
                b = st["baseline"]
                mx.append(b["max_delta_phi"])
                cap_sub.append(b["cap_max_delta_phi_subgraph"])
                cap_frac.append(b["cap_above_fraction"])
                slopes.append(b["drift_slope"])
                norm_drift.append(b["norm_drift"])
        station[f"{g}_N{n}"] = {
            "max_delta_phi_range": [float(np.min(mx)), float(np.max(mx))],
            "n_stationary": int(sum(m < MAN["epsilon_phi"] for m in mx)),
            "n_states": len(mx),
            "cap_subgraph_max_range": [float(np.min(cap_sub)),
                                       float(np.max(cap_sub))],
            "cap_above_fraction_mean": float(np.mean(cap_frac)),
            "drift_slope_mean": float(np.mean(slopes)),
            "max_norm_drift": float(np.max(norm_drift)),
        }

# ---------------- battery summary ----------------
# Corrected pass rule, one consistent instrument for all recorded outputs:
# W1's identity deviation is read RELATIVE to its own magnitude (PR_A is
# O(10^5-10^6) at N = 12, where an absolute 1e-10 demands sub-eps_mach
# relative precision); all other deviations stay absolute at tol.
battery = {}
for g in TA + TC:
    for n in MAN["sizes"][g]:
        d = load(g, n)
        for run in d["runs"]:
            if "battery" not in run:
                continue
            b = run["battery"]
            pr = run["states"][0]["witnesses"]["pr_A"]
            tol = b["tol"]

            def item_pass(it):
                return bool(it["w1_dev"] / max(abs(pr), 1.0) < tol
                            and it["w2_dev"] < tol and it["w3_dev"] < tol
                            and it["w4_dev"] < tol and it["mi_dev"] < tol)

            corrected = bool(item_pass(b["global_phase"])
                             and item_pass(b["consistent_local_basis"])
                             and item_pass(b["reflection"]))
            battery[f"{g}_N{n}"] = {
                "all_must_pass_raw": b["all_must_pass"],
                "all_must_pass_w1_relative": corrected,
                "w1_rel_dev_max": max(
                    b[k]["w1_dev"] for k in ("global_phase",
                                             "consistent_local_basis",
                                             "reflection")) / max(abs(pr),
                                                                  1.0),
                "phi_dev_max": max(b["global_phase"]["phi_dev"],
                                   b["consistent_local_basis"]["phi_dev"],
                                   b["reflection"]["phi_dev"]),
                "state_only_w3_dev":
                    b["state_only_local_basis"]["w3_max_dev"],
                "state_only_phi_dev":
                    b["state_only_local_basis"]["phi_max_dev"],
            }

# ---------------- T-B ----------------
tb_out = {}
tb_main_path = CONF / "TB_main.json"
if tb_main_path.exists():
    tbm = json.loads(tb_main_path.read_text())
    curve = {e: bootstrap_ci_mean(np.array(v))
             for e, v in tbm["rigidity_curve"].items()}
    tb_out["rigidity_curve"] = {e: {"mean": c[0], "ci": [c[1], c[2]]}
                                for e, c in curve.items()}
    eps_sorted = sorted(curve, key=float)
    eps_c = None
    for e0, e1 in zip(eps_sorted[:-1], eps_sorted[1:]):
        h0, h1 = curve[e0][0], curve[e1][0]
        if h0 >= 0.5 > h1:
            eps_c = float(e0) + (h0 - 0.5) / (h0 - h1) \
                * (float(e1) - float(e0))
            break
    tb_out["eps_c_estimate_descriptive"] = eps_c
    regs = {}
    for key, reals in tbm["regimes"].items():
        w5, mx, prA, xi, w5_on, w5_off, dphi_off, dphi_on = ([] for _ in
                                                             range(8))
        for r in reals:
            w5.append(np.mean([s["witnesses"]["w5"] for s in r["states"]]))
            mx.append(np.mean([s["baseline"]["max_delta_phi"]
                               for s in r["states"]]))
            prA.append(np.mean([s["witnesses"]["pr_A"]
                                for s in r["states"]]))
            xi.append(np.mean([s["witnesses"]["xi"] for s in r["states"]]))
            w5_on.append(np.mean([s["switchoff"]["w5_post_on"]
                                  for s in r["states"]]))
            w5_off.append(np.mean([s["switchoff"]["w5_post_off"]
                                   for s in r["states"]]))
            dphi_off.append(np.mean([s["switchoff"]["max_delta_phi_off"]
                                     for s in r["states"]]))
            dphi_on.append(np.mean([s["switchoff"]["max_delta_phi_post_on"]
                                    for s in r["states"]]))
        n_stat = sum(1 for r in reals for s in r["states"]
                     if s["baseline"]["stationary"])
        n_tot = sum(len(r["states"]) for r in reals)
        regs[key] = {
            "w5_mean": float(np.mean(w5)), "pr_A_mean": float(np.mean(prA)),
            "xi_mean": float(np.mean(xi)),
            "max_delta_phi_mean": float(np.mean(mx)),
            "n_stationary": n_stat, "n_states": n_tot,
            "switchoff": {"w5_post_on_mean": float(np.mean(w5_on)),
                          "w5_post_off_mean": float(np.mean(w5_off)),
                          "max_delta_phi_off_mean": float(np.mean(dphi_off)),
                          "max_delta_phi_post_on_mean": float(np.mean(
                              dphi_on))},
        }
    tb_out["regimes"] = regs
tb_prot_path = CONF / "TB_protocols.json"
if tb_prot_path.exists():
    tbp = json.loads(tb_prot_path.read_text())
    pr = {}
    for key, reals in tbp["protocols"].items():
        pr[key] = {}
        for p in PROTOCOLS:
            v = [np.mean([s[p]["log_rho"] for s in r["states"]])
                 for r in reals]
            ci = bootstrap_ci_mean(np.array(v))
            pr[key][p] = {"mean_log_rho": ci[0], "ci": [ci[1], ci[2]]}
    tb_out["protocols_descriptive"] = pr

# ---------------- §5.4 outcome ----------------
outcome = {
    "criterion_a_holds": crit_a["holds"],
    "criterion_b_holds": crit_b["holds"],
    "spec_5_4_row": (
        "(a) and (b) hold -> BH-004 supported in-model; BH-005 licensed; "
        "HYP-009 geometric part gains first model realization"
        if crit_a["holds"] and crit_b["holds"] else
        "(a) holds, (b) null -> clean null on the robustness differential; "
        "BH-004 partially supported"
        if crit_a["holds"] else
        "(a) fails -> witness scheme returns to FORMALIZE; recorded "
        "negative (SC-005)"),
    "sustained_by_verdicts": {g: adjudication[g]["verdict"]
                              for g in adjudication},
    "note": "promotion gated on AR-011 adversarial companion (KB-005 §10)",
}

summary = {"date": "2026-08-12", "manifest": "confirmatory_manifest.json",
           "null_comparator_4_4": null_report, "criterion_a": crit_a,
           "criterion_b": crit_b, "adjudication_5_3": adjudication,
           "stationarity_cap": station, "battery_4_3": battery,
           "TB": tb_out, "outcome_5_4": outcome}
with open(OUT / "confirmatory_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=" * 70)
print("AR-010 CONFIRMATORY SUMMARY")
print("=" * 70)
print(f"§4.4 null: {json.dumps(null_report, indent=1)[:400]}")
print(f"W3 discarded by null: {w3_fired_on_null}")
print(f"criterion (a): {'HOLDS' if crit_a['holds'] else 'FAILS'}"
      f"  [TA: {crit_a['tracks']['TA']['holds']}, "
      f"TC: {crit_a['tracks']['TC']['holds']}]")
for prot, p in crit_b["protocols"].items():
    reps = {t: p["tracks"][t]["replicated_pairs"] for t in p["tracks"]}
    print(f"criterion (b) {prot}: replicated {reps}")
print(f"criterion (b): {'HOLDS' if crit_b['holds'] else 'NULL'}")
print("§5.3 verdicts:")
for g, a in adjudication.items():
    print(f"  {g}: {a['verdict']} (check1={a['check1_witness_vs_comparator']}"
          f", check2={a['check2_robustness_or_switchoff']})")
print(f"outcome: {outcome['spec_5_4_row']}")
print(f"\nwritten: {OUT / 'confirmatory_summary.json'}")
