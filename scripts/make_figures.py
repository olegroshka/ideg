"""Paper figures 1-6 (paper/OUTLINE.md inventory) -> paper/figures/.

    python scripts/make_figures.py [1|2|3|4|5|6|all]

Class colors: one fixed entity mapping across every figure (validated
categorical order on white; null/fixed point = neutral gray; DTC track =
violet). Recomputed panels use manifest run-0 seeds; everything else
reads committed result JSONs.
"""

import json
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ideg.evolve import EigenEvolver                        # noqa: E402
from ideg.migraph import (I0, delta_phi,                    # noqa: E402
                          mutual_information_matrix, phi_series)
from ideg.models import (ferro_ising_weak_tf,               # noqa: E402
                         mixed_field_ising, tfim, xx_chain, xxz_disordered)
from ideg.states import (all_up, ground_state,              # noqa: E402
                         haar_product_state, magnon_superposition, neel)
from ideg.witnesses import otoc                             # noqa: E402

RES = ROOT / "results" / "AR-010"
FIG = ROOT / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
MAN = json.loads((RES / "confirmatory_manifest.json").read_text())

# ---- palette (validated) ----
C = {
    "quasiperiodic": "#2a78d6",   # slot 1 blue — the survivor/accent
    "chaotic":       "#eb6834",   # slot 2 orange
    "scrambling":    "#1baf7a",   # slot 3 aqua
    "integrable":    "#eda100",   # slot 4 yellow
    "localized":     "#e87ba4",   # slot 5 magenta
    "metastable":    "#008300",   # slot 6 green
    "fixed point":   "#898781",   # neutral gray (null comparator)
    "dtc":           "#4a3aa7",   # violet (driven track)
    "r2":            "#e34948",   # red (non-thermalizing comparator)
}
INK, INK2, MUT = "#0b0b0b", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
BLUES = LinearSegmentedColormap.from_list(
    "seqblue", ["#ffffff", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab",
                "#0d366b"])

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 8.0,
    "axes.edgecolor": BASE, "axes.linewidth": 0.6,
    "axes.labelcolor": INK, "xtick.color": MUT, "ytick.color": MUT,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.titlesize": 8.5, "axes.titlecolor": INK,
    "grid.color": GRID, "grid.linewidth": 0.5,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.dpi": 150, "pdf.fonttype": 42,
})

GROUPS7 = ["TA_i_fixed_point", "TA_ii_quasiperiodic", "TA_iii_chaotic",
           "TA_iv_metastable", "TC_scrambling", "TC_integrable",
           "TC_localized"]
LABEL = {"TA_i_fixed_point": "fixed point",
         "TA_ii_quasiperiodic": "quasiperiodic",
         "TA_iii_chaotic": "chaotic", "TA_iv_metastable": "metastable",
         "TC_scrambling": "scrambling", "TC_integrable": "integrable",
         "TC_localized": "localized"}
N10 = 10
WINDOW = np.arange(20.0, 200.0 + 1e-9, 0.5)


def rep_run(group, n=N10):
    seed = MAN["seeds"][group][str(n)][0]
    rng = np.random.default_rng(seed)
    if group == "TA_i_fixed_point":
        h = tfim(n, g=1.5)
        return h, ground_state(h)
    if group == "TA_ii_quasiperiodic":
        psi, _ = magnon_superposition(n, rng)
        return xx_chain(n), psi
    if group == "TA_iii_chaotic":
        return mixed_field_ising(n), haar_product_state(n, rng)
    if group == "TA_iv_metastable":
        dg = rng.uniform(-0.01, 0.01, size=n)
        return ferro_ising_weak_tf(n, g=0.05, dg=dg), all_up(n)
    if group == "TC_scrambling":
        return mixed_field_ising(n), neel(n)
    if group == "TC_integrable":
        return xx_chain(n), neel(n)
    if group == "TC_localized":
        return xxz_disordered(n, rng), neel(n)


def strip(ax, xc, vals, color, w=0.28, ms=7):
    rng = np.random.default_rng(0)
    x = xc + rng.uniform(-w, w, size=len(vals))
    ax.scatter(x, vals, s=ms, c=color, alpha=0.75, linewidths=0, zorder=3)


def savefig(fig, name):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print(f"saved {name}")


# ---------------- Fig 1: pipeline — MI graphs in time, two classes ----
def fig1():
    times = [30.0, 105.0, 180.0]
    rows = [("TA_iii_chaotic", "chaotic"),
            ("TA_ii_quasiperiodic", "quasiperiodic")]
    fig, axes = plt.subplots(2, 4, figsize=(7.0, 3.5))
    theta = np.linspace(0, 2 * np.pi, N10, endpoint=False) + np.pi / 2
    xy = np.c_[np.cos(theta), np.sin(theta)]
    for r, (group, lab) in enumerate(rows):
        h, psi0 = rep_run(group)
        ev = EigenEvolver(h)
        for k, t in enumerate(times):
            ax = axes[r, k]
            mi = mutual_information_matrix(ev.state_at(psi0, t), N10)
            x = np.clip(mi / I0, 0, 1)
            for i in range(N10):
                for j in range(i + 1, N10):
                    ax.plot(*zip(xy[i], xy[j]), lw=0.5 + 3.0 * x[i, j] ** 0.5,
                            color=C[lab], alpha=min(0.08 + x[i, j] ** 0.5, 1),
                            solid_capstyle="round", zorder=1)
            ax.scatter(*xy.T, s=14, c=INK2, zorder=2, linewidths=0)
            ax.set_title(f"$t = {t:.0f}$", pad=2)
            ax.set_xlim(-1.25, 1.25)
            ax.set_ylim(-1.25, 1.25)
            ax.set_aspect("equal")
            ax.axis("off")
        states = ev.states_at(psi0, WINDOW)
        dbar = phi_series(states, N10).mean(axis=0)
        ax = axes[r, 3]
        im = ax.imshow(dbar, cmap=BLUES, vmin=0)
        ax.set_title(r"window mean $\bar D$", pad=2)
        ax.set_xticks([])
        ax.set_yticks([])
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cb.ax.tick_params(labelsize=6.5, color=MUT)
        cb.outline.set_edgecolor(BASE)
        axes[r, 0].text(-0.18, 0.5, lab, transform=axes[r, 0].transAxes,
                        rotation=90, va="center", ha="center", fontsize=9,
                        color=C[lab], fontweight="bold")
    fig.suptitle("mutual-information graph  →  shortest-path metric",
                 y=1.005, fontsize=9, color=INK)
    fig.tight_layout()
    savefig(fig, "fig1_pipeline")


# ---------------- Fig 2: baseline drift trajectories ----------------
def fig2():
    show = ["TA_iii_chaotic", "TC_localized", "TA_iv_metastable",
            "TA_ii_quasiperiodic"]
    label_dy = {"chaotic": -9, "localized": 6, "metastable": 2,
                "quasiperiodic": 0}
    fig, (ax, axz) = plt.subplots(
        2, 1, figsize=(5.4, 3.2), sharex=True,
        gridspec_kw={"height_ratios": [5, 1], "hspace": 0.08})
    for group in show:
        lab = LABEL[group]
        h, psi0 = rep_run(group)
        ev = EigenEvolver(h)
        delta, _ = delta_phi(phi_series(ev.states_at(psi0, WINDOW), N10))
        ax.plot(WINDOW, delta, lw=1.1, color=C[lab])
        ax.annotate(lab, (WINDOW[-1], delta[-1]),
                    xytext=(4, label_dy[lab]), textcoords="offset points",
                    va="center", fontsize=7.5, color=C[lab])
    ax.axhline(0.25, color=INK2, lw=0.8, ls=(0, (4, 3)))
    ax.annotate(r"$\varepsilon_\Phi = 0.25$", (200, 0.25), xytext=(0, -11),
                textcoords="offset points", fontsize=7.5, color=INK2,
                ha="right")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel(r"metric drift  $\delta\Phi(t)$")
    ax.grid(True, axis="y")
    # machine-zero strip: the frozen null
    h, psi0 = rep_run("TA_i_fixed_point")
    ev = EigenEvolver(h)
    delta, _ = delta_phi(phi_series(ev.states_at(psi0, WINDOW), N10))
    axz.plot(WINDOW, np.maximum(delta, 1e-14), lw=1.0,
             color=C["fixed point"])
    axz.annotate("fixed point (null)", (WINDOW[-1], 3e-13), xytext=(4, 0),
                 textcoords="offset points", va="center", fontsize=7.5,
                 color=C["fixed point"])
    axz.set_yscale("log")
    axz.set_ylim(1e-14, 1e-11)
    axz.set_yticks([1e-13])
    axz.set_xlim(20, 252)
    axz.set_xticks([20, 60, 100, 140, 180])
    axz.set_xlabel("time  $t$  (units of $1/J$)")
    for a in (ax, axz):
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    savefig(fig, "fig2_drift")


# ---------------- Fig 3: witness battery + the discarded W3 ----------
def fig3():
    stats = [("pr_A", r"$\mathrm{PR}_A$  (Bohr ratio)", True),
             ("w2_mean", r"$\overline{d}$  (recurrence mean)", False),
             ("xi", r"$\Xi$  (energy coherence)", False)]
    order = ["TA_ii_quasiperiodic", "TA_iii_chaotic", "TA_iv_metastable",
             "TC_scrambling", "TC_integrable", "TC_localized"]
    data = {g: json.loads((RES / "confirmatory" /
                           f"rerun40_{g}_N12.json").read_text())
            for g in order + ["TA_i_fixed_point"]}

    def vals(g, s):
        return [np.mean([st[s] for st in run["states"]])
                for run in data[g]["runs"]]

    fig, axes = plt.subplots(1, 4, figsize=(7.0, 2.6))
    for a, (s, title, logy) in enumerate(stats):
        ax = axes[a]
        for k, g in enumerate(order):
            v = np.array(vals(g, s))
            if logy:
                v = np.maximum(v, 1.0)
            strip(ax, k, v, C[LABEL[g]])
        nv = vals("TA_i_fixed_point", s)[0]
        ax.axhline(max(nv, 1.0) if logy else nv, color=MUT, lw=0.8,
                   ls=(0, (2, 2)))
        ax.annotate("null", (5.45, max(nv, 1.0) if logy else nv),
                    xytext=(0, 3), textcoords="offset points", fontsize=7,
                    color=MUT, ha="right")
        if logy:
            ax.set_yscale("log")
        ax.set_title(title, pad=3)
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels([LABEL[g][:6] for g in order], rotation=60,
                           ha="right", fontsize=6.5)
        for tick, g in zip(ax.get_xticklabels(), order):
            tick.set_color(C[LABEL[g]])
        ax.grid(True, axis="y")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)

    # panel: W3 on the null
    ax = axes[3]
    h, psi0 = rep_run("TA_i_fixed_point")
    ev = EigenEvolver(h)
    ts = np.arange(0.0, 20.0 + 1e-9, 0.25)
    cnull = otoc(ev, psi0, N10, site_w=9, site_v=5, times=ts)
    ax.plot(ts, cnull, lw=1.2, color=MUT)
    ax.axhline(0.1, color=INK2, lw=0.8, ls=(0, (4, 3)))
    ax.annotate("arrival threshold", (19.5, 0.1), xytext=(0, -9),
                textcoords="offset points", fontsize=6.5, color=INK2,
                ha="right")
    ax.set_title("W3 (OTOC) on the frozen null", pad=3)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$C(r_{\\max}, t)$")
    ax.set_ylim(-0.06, 2.25)
    ax.text(0.97, 0.965, "fires on the null\n→ discarded as witness",
            transform=ax.transAxes, ha="right", va="top", fontsize=7,
            color=INK, bbox=dict(fc="white", ec=BASE, lw=0.6, pad=2.5))
    ax.grid(True, axis="y")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    savefig(fig, "fig3_witnesses")


# ---------------- Fig 4: dephasing response curves ------------------
def fig4():
    d = json.loads((RES / "quality_sprint_gamma.json").read_text())
    summ = json.loads((RES / "confirmatory_summary.json").read_text())
    gm = {}
    for tr in ("TA", "TC"):
        blk = summ["criterion_b"]["protocols"]["dephasing"]["tracks"][tr]
        gm.update(blk["10"]["group_means"])
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    gammas = [float(g) for g in d["gammas"]]
    label_dy = {"scrambling": 5, "chaotic": -5, "localized": 5,
                "integrable": -5, "metastable": 5, "quasiperiodic": -6}
    for g, v in d["groups"].items():
        lab = LABEL[g]
        ys = [v[str(x)]["mean_log_rho"] for x in d["gammas"]]
        ax.plot(gammas, ys, lw=1.4, color=C[lab], marker="o", ms=3.2,
                markeredgewidth=0)
        ax.annotate(lab, (gammas[-1], ys[-1]),
                    xytext=(5, label_dy[lab]), textcoords="offset points",
                    va="center", fontsize=7.5, color=C[lab])
    for g, v in gm.items():
        lab = LABEL[g]
        lo, hi = v["ci"]
        ax.errorbar([0.01], [v["mean"]],
                    yerr=[[v["mean"] - lo], [hi - v["mean"]]],
                    fmt="s", ms=4, color=C[lab], elinewidth=1.0,
                    capsize=2, zorder=4, markeredgecolor="white",
                    markeredgewidth=0.6)
        if lab == "localized":  # confirmatory ensemble differs (5 states
            ax.annotate("$\\dagger$", (0.0113, v["mean"]), fontsize=8,
                        color=C[lab], va="center")  # /realization); caption
    ax.axhline(0.0, color=BASE, lw=0.9)
    ax.axvline(0.01, color=GRID, lw=0.8)
    ax.annotate("confirmatory\n$\\gamma = 0.01$", (0.01, 2.95),
                fontsize=6.5, color=MUT, ha="center")
    ax.set_xscale("log")
    ax.set_xlim(8e-4, 0.45)
    ax.set_ylim(-0.75, 3.1)
    ax.set_xlabel(r"dephasing rate  $\gamma$")
    ax.set_ylabel(r"mean  $\log\rho$")
    ax.grid(True, axis="y")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    savefig(fig, "fig4_gamma")


# ------------- Fig 5: coherence removal + representation gap --------
def fig5():
    fig, (ax1, ax2, ax3) = plt.subplots(
        1, 3, figsize=(7.0, 2.9),
        gridspec_kw={"width_ratios": [0.9, 1.5, 0.9]})
    order = ["TA_ii_quasiperiodic", "TA_iii_chaotic", "TA_iv_metastable",
             "TC_scrambling", "TC_integrable", "TC_localized"]
    # (a) coherence removal: motion-removal channel (filled) vs the
    # stronger full-diagonalization ablation (rings), ar020e all runs
    for k, g in enumerate(order):
        d = json.loads((RES / f"ar020e_channels_{g}_N10.json").read_text())
        inf_ = [r["miss_inf"] for r in d["runs"]]
        diag = [r["miss_diag"] for r in d["runs"]]
        rng = np.random.default_rng(2)
        x = k + 0.17 + rng.uniform(-0.10, 0.10, size=len(diag))
        ax1.scatter(x, diag, s=7, facecolors="none",
                    edgecolors=C[LABEL[g]], linewidths=0.5, zorder=2)
        strip(ax1, k - 0.15, inf_, C[LABEL[g]], w=0.12, ms=6)
    ax1.axhline(0.25, color=INK2, lw=0.8, ls=(0, (4, 3)))
    ax1.annotate(r"$\varepsilon_\Phi$", (-0.42, 0.25), xytext=(0, 3),
                 textcoords="offset points", fontsize=7, color=INK2)
    ax1.scatter([], [], s=10, c=INK2, label=r"$\rho_\infty$")
    ax1.scatter([], [], s=10, facecolors="none", edgecolors=INK2,
                linewidths=0.6, label=r"$\bar\rho$ (ablation)")
    ax1.legend(loc="upper left", frameon=False, fontsize=6,
               handletextpad=0.15, borderaxespad=0.1)
    ax1.set_ylabel(r"$\|\Phi[\sigma]-\bar D\|/\|\bar D\|$")
    ax1.set_title("(a)  motion removal vs ablation", pad=3)
    # (b) representation gap: smooth (filled) vs unrestricted (rings)
    for k, g in enumerate(order):
        sm, un = [], []
        for n in (10, 12):
            pb = json.loads((RES / f"ar020b_hardened_probe_N{n}.json"
                             ).read_text())
            sm += [r["overall_min"] for r in pb["groups"][g]["runs"]]
            pc = json.loads((RES / f"ar020c_unrestricted_N{n}.json"
                             ).read_text())
            un += pc["groups"][g]["runs"]
        strip(ax2, k - 0.19, sm, C[LABEL[g]], w=0.12, ms=6)
        rng = np.random.default_rng(1)
        x = k + 0.19 + rng.uniform(-0.12, 0.12, size=len(un))
        ax2.scatter(x, un, s=8, facecolors="none",
                    edgecolors=C[LABEL[g]], linewidths=0.6, zorder=3)
    ax2.axhline(0.25, color=INK2, lw=0.8, ls=(0, (4, 3)))
    ax2.annotate(r"$\varepsilon_\Phi = 0.25$", (4.7, 0.25), xytext=(0, 3),
                 textcoords="offset points", fontsize=7, color=INK2,
                 ha="center")
    ax2.scatter([], [], s=10, c=INK2, label="smooth $f(H)$")
    ax2.scatter([], [], s=10, facecolors="none", edgecolors=INK2,
                linewidths=0.7, label="unrestricted")
    ax2.legend(loc="upper right", frameon=False, fontsize=6.5,
               handletextpad=0.15, borderaxespad=0.1)
    ax2.set_ylabel("best stationary-state miss")
    ax2.set_title("(b)  representation gap (both sizes)", pad=3)
    ax2.set_ylim(-0.02, 0.45)
    # (c) threshold sensitivity, quasiperiodic
    eps_grid = np.linspace(0.0, 0.45, 200)
    styles = [(10, "-"), (12, (0, (4, 2)))]
    for n, ls in styles:
        pb = json.loads((RES / f"ar020b_hardened_probe_N{n}.json"
                         ).read_text())
        sm = np.array([r["overall_min"] for r in
                       pb["groups"]["TA_ii_quasiperiodic"]["runs"]])
        pc = json.loads((RES / f"ar020c_unrestricted_N{n}.json"
                         ).read_text())
        un = np.array(pc["groups"]["TA_ii_quasiperiodic"]["runs"])
        ax3.plot(eps_grid, [np.mean(sm < e) for e in eps_grid], color=INK2,
                 lw=1.1, ls=ls)
        ax3.plot(eps_grid, [np.mean(un < e) for e in eps_grid],
                 color=C["quasiperiodic"], lw=1.1, ls=ls)
    ax3.axvline(0.25, color=INK2, lw=0.8, ls=(0, (4, 3)))
    ax3.annotate("smooth", (0.36, 0.06), fontsize=6.5, color=INK2)
    ax3.annotate("unrestricted", (0.02, 0.86), fontsize=6.5,
                 color=C["quasiperiodic"])
    ax3.annotate(r"solid $N{=}10$, dashed $N{=}12$", (0.02, 0.6),
                 fontsize=6, color=MUT)
    ax3.set_xlabel(r"threshold  $\varepsilon$")
    ax3.set_ylabel("fraction matched")
    ax3.set_title("(c)  quasiperiodic sensitivity", pad=3)
    ax3.set_ylim(-0.03, 1.05)
    for ax, has_ticks in ((ax1, True), (ax2, True), (ax3, False)):
        if has_ticks:
            ax.set_xticks(range(len(order)))
            ax.set_xticklabels([LABEL[g][:6] for g in order], rotation=60,
                               ha="right", fontsize=6.5)
            for tick, g in zip(ax.get_xticklabels(), order):
                tick.set_color(C[LABEL[g]])
        ax.grid(True, axis="y")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout()
    savefig(fig, "fig5_comparator")


# ---------------- Fig 6: driven regime ------------------------------
def fig6():
    tbm = json.loads((RES / "confirmatory" / "TB_main.json").read_text())
    spr = json.loads((RES / "quality_sprint_tb.json").read_text())
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.9))
    # (a) rigidity curve
    eps, mean, lo, hi = [], [], [], []
    for e, v in tbm["rigidity_curve"].items():
        eps.append(float(e))
        mean.append(np.mean(v))
        lo.append(np.min(v))
        hi.append(np.max(v))
    for e, v in spr["rigidity_extension"].items():
        eps.append(float(e))
        mean.append(v["mean"])
        lo.append(v["min"])
        hi.append(v["max"])
    o = np.argsort(eps)
    eps, mean = np.array(eps)[o], np.array(mean)[o]
    lo, hi = np.array(lo)[o], np.array(hi)[o]
    ax1.fill_between(eps, lo, hi, color=C["dtc"], alpha=0.14, lw=0)
    ax1.plot(eps, mean, lw=1.5, color=C["dtc"], marker="o", ms=3.2,
             markeredgewidth=0)
    ax1.axhline(0.5, color=BASE, lw=0.9)
    ec = 0.20 + 0.05 * (mean[eps == 0.20][0] - 0.5) / (
        mean[eps == 0.20][0] - mean[eps == 0.25][0])
    ax1.axvline(ec, color=INK2, lw=0.8, ls=(0, (4, 3)))
    ax1.annotate(rf"$\varepsilon_c \approx {ec:.2f}$", (ec, 1.0),
                 xytext=(5, -2), textcoords="offset points", fontsize=7.5,
                 color=INK2)
    ax1.set_xlabel(r"drive imperfection  $\varepsilon$")
    ax1.set_ylabel(r"subharmonic weight  $h_{\rm sub}$")
    ax1.set_title("(a)  rigidity curve (realization mean, range)", pad=3)
    ax1.set_ylim(-0.03, 1.05)
    ax1.grid(True, axis="y")
    # (b) switch-off dumbbells + r2 persistence
    reals = tbm["regimes"]["dtc_eps0.03"]
    w5_on = [s["switchoff"]["w5_post_on"] for r in reals
             for s in r["states"]]
    w5_off = [s["switchoff"]["w5_post_off"] for r in reals
              for s in r["states"]]
    dp_on = [s["switchoff"]["max_delta_phi_post_on"] for r in reals
             for s in r["states"]]
    dp_off = [s["switchoff"]["max_delta_phi_off"] for r in reals
              for s in r["states"]]
    pairs = [("witness  $W_5$", np.mean(w5_on), np.mean(w5_off), 2.05),
             (r"drift  $\max\delta\Phi$", np.mean(dp_on),
              np.mean(dp_off), 1.45)]
    for lab, on, off, y in pairs:
        ax2.plot([off, on], [y, y], color=BASE, lw=1.0, zorder=1)
        ax2.scatter([on], [y], s=42, color=C["dtc"], zorder=3,
                    edgecolors="white", linewidths=0.7)
        ax2.scatter([off], [y], s=42, color=MUT, zorder=3,
                    edgecolors="white", linewidths=0.7)
        if abs(on - off) > 0.2:
            ax2.annotate(f"{on:.2f}", (on, y), xytext=(0, 8),
                         textcoords="offset points", ha="center",
                         fontsize=7, color=C["dtc"])
            ax2.annotate(f"{off:.2f}", (off, y), xytext=(0, 8),
                         textcoords="offset points", ha="center",
                         fontsize=7, color=MUT)
        else:
            ax2.annotate(f"{on:.2f} → {off:.2f}  (persists)",
                         (max(on, off), y), xytext=(10, 10),
                         textcoords="offset points", va="center",
                         fontsize=7, color=INK2)
        ax2.annotate(lab, (0.0, y), xytext=(-8, 0),
                     textcoords="offset points", ha="right", va="center",
                     fontsize=7.5, color=INK,
                     annotation_clip=False)
    ax2.scatter([], [], s=42, color=C["dtc"], label="drive on")
    ax2.scatter([], [], s=42, color=MUT, label="drive off")
    lw = spr["long_window"]["regimes"]["r2_no_disorder"]
    xs = [float(k) for k in lw]
    ys = [lw[k]["w5_mean"] for k in lw]
    o = np.argsort(xs)
    ax2i = ax2.inset_axes([0.32, 0.16, 0.63, 0.38])
    ax2i.plot(np.array(xs)[o], np.array(ys)[o], lw=1.2, color=C["r2"],
              marker="o", ms=2.5, markeredgewidth=0)
    ax2i.set_ylim(0, 1.08)
    ax2i.set_title("r2 (clean drive): $W_5$ to 2000 periods",
                   fontsize=6.5, pad=2)
    ax2i.tick_params(labelsize=6)
    for sp in ("top", "right"):
        ax2i.spines[sp].set_visible(False)
    ax2.set_xlim(0.0, 1.06)
    ax2.set_ylim(-0.15, 2.85)
    ax2.set_yticks([])
    ax2.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax2.set_xlabel("value after period 100")
    ax2.set_title("(b)  drive removal: witness collapses, metric persists",
                  pad=3)
    ax2.legend(loc="upper center", ncol=2, frameon=False, fontsize=7,
               handletextpad=0.2, borderaxespad=0.1, columnspacing=0.9)
    for ax in (ax1, ax2):
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout()
    savefig(fig, "fig6_driven")


ALL = {"1": fig1, "2": fig2, "3": fig3, "4": fig4, "5": fig5, "6": fig6}
which = sys.argv[1] if len(sys.argv) > 1 else "all"
t0 = time.time()
for k, fn in ALL.items():
    if which in ("all", k):
        fn()
print(f"done ({time.time() - t0:.1f}s)")
