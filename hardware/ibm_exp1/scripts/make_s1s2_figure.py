"""AR-023a S1/S2 evidence figure -> results/sim_s2/ar023a_s1s2.{png,pdf}.

Three panels, one job each:
  (a) floor anatomy — why the frozen gate failed and what the amended
      statistic measures instead (magnitude comparison on one scale);
  (b) operating envelope — separation Delta vs two-qubit error, one
      line per readout level, with the fake backends and the drift arm
      marked (change over an ordered variable);
  (c) leakage — the readout artefact: the same states judged on raw vs
      M3-corrected counts against the registered traffic-light bands.

Palette and rcParams follow scripts/make_figures.py so this figure sits
in the paper's visual system: quasiperiodic blue is the accent (this IS
the qp instance), neutral gray marks the retired/defective statistic,
and status colors carry the traffic light, always with a text label.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "hardware" / "ibm_exp1" / "results"
COND = RES / "sim_s2" / "conditions"

QP, GRAY, INK, INK2, MUT = "#2a78d6", "#898781", "#0b0b0b", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
GOOD, WARN, BAD = "#008300", "#eda100", "#e34948"
VIOLET = "#4a3aa7"
RO_COLORS = {0.01: "#2a78d6", 0.02: "#1baf7a", 0.03: "#eb6834"}
P2_VALUES = [0.003, 0.006, 0.01]

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


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def battery(cond: str):
    return load(COND / cond / "battery_report.json")


def _spines(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        if side not in keep:
            ax.spines[side].set_visible(False)


def panel_floor(ax):
    """(a) signal vs the retired and amended floor statistics."""
    old = load(RES / "sim_s1_768" / "s1_report.json")
    new = load(RES / "sim_s1_768_v2" / "s1_report.json")
    if new is None:
        ax.text(0.5, 0.5, "S1 v2 pending", ha="center", va="center")
        return
    eps_ref = float(new["inputs"]["eps_reference"]["eps_sector_37"])
    summary = new["summary"]
    labels = ["signal  ε(37)", "retired floor\n(matrix norm)",
              "amended floor\nmax(split, dup)", "  split arm",
              "  duplicate arm\n  (drift-sensitive)"]
    values = [eps_ref,
              float(old["gates"]["S1-G3"]["measured"]) if old else np.nan,
              summary["eps_floor_median"],
              summary["floor_split_median"],
              summary["floor_duplicate_median"]]
    colors = [QP, GRAY, GOOD, INK2, VIOLET]
    y = np.arange(len(values))[::-1]
    ax.barh(y, values, height=0.5, color=colors, zorder=3)
    for yi, v in zip(y, values):
        if np.isfinite(v):
            ax.text(v + 0.005, yi, f"{v:.3f}", va="center", ha="left",
                    fontsize=7.4, color=INK)
    ax.axvline(0.05, color=WARN, lw=1.0, ls="--", zorder=2)
    ax.text(0.053, y[0] + 0.40, "S1-G3 gate 0.05", fontsize=7, color=WARN)
    ax.set_yticks(y, labels, fontsize=7.1)
    ax.set_xlim(0, 0.27)
    ax.set_xlabel("normalized metric units")
    ax.set_title("(a) the floor failed the gate, not the signal", loc="left")
    ax.grid(axis="x", zorder=0)
    ax.set_axisbelow(True)
    _spines(ax, keep=("bottom",))


def panel_envelope(ax):
    """(b) separation vs noise, with fakes and the drift arm marked."""
    deltas = []
    for ro in (0.01, 0.02, 0.03):
        xs, ys = [], []
        for p2 in P2_VALUES:
            rec = battery(f"grid_p2-{p2:g}_ro-{ro:g}")
            if rec:
                xs.append(p2 * 1000)
                ys.append(rec["delta_median"])
                deltas.append(rec["delta_median"])
        if xs:
            ax.plot(xs, ys, "-o", color=RO_COLORS[ro], lw=2.0, ms=5,
                    mec="white", mew=1.2, zorder=3, label=f"readout {ro:g}")
            ax.text(xs[-1] + 0.3, ys[-1], f"{ro:g}", fontsize=7.2,
                    color=RO_COLORS[ro], va="center")
    ax.set_xlim(2.2, 11.6)
    for name, label in (("fake_fake_aachen", "fake aachen"),
                        ("fake_fake_boston", "fake boston")):
        rec = battery(name)
        if rec:
            deltas.append(rec["delta_median"])
            ax.axhline(rec["delta_median"], color=MUT, lw=0.8, ls=":",
                       zorder=1)
            ax.text(2.35, rec["delta_median"] + 0.001, label,
                    fontsize=6.8, color=INK2, va="bottom")
    drift = battery("drift_ramp")
    if drift:
        deltas.append(drift["delta_median"])
        ax.axhline(drift["delta_median"], color=VIOLET, lw=1.2, ls="-.",
                   zorder=2)
        ax.text(11.4, drift["delta_median"] + 0.001,
                f"drift ramp  {drift['success_count']}/100", fontsize=6.9,
                color=VIOLET, ha="right", va="bottom")
    if deltas:
        lo, hi = min(deltas), max(deltas)
        span = max(hi - lo, 1e-3)
        ax.set_ylim(lo - 0.55 * span, hi + 0.12 * span)
    ax.set_xlabel("two-qubit depolarizing error  $p_2$  (×10$^{-3}$)")
    ax.set_ylabel("separation  Δ  (median)")
    ax.set_title("(b) operating envelope", loc="left")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax.grid(zorder=0)
    ax.set_axisbelow(True)
    _spines(ax)


def panel_leakage(ax):
    """(c) raw vs M3-corrected leakage against the traffic-light bands."""
    conds, corr, raw = [], [], []
    for p2 in P2_VALUES:
        rec = battery(f"grid_p2-{p2:g}_ro-0.02")
        if rec and "leakage_survival_corrected_median" in rec["experiments"][0]:
            conds.append(f"{p2*1000:g}")
            corr.append(float(np.median(
                [e["leakage_survival_corrected_median"]
                 for e in rec["experiments"]])))
            raw.append(float(np.median(
                [e["leakage_survival_raw_median"]
                 for e in rec["experiments"]])))
    for name, short in (("fake_fake_aachen", "aachen"),
                        ("fake_fake_boston", "boston")):
        rec = battery(name)
        if rec and "leakage_survival_corrected_median" in rec["experiments"][0]:
            conds.append(short)
            corr.append(float(np.median(
                [e["leakage_survival_corrected_median"]
                 for e in rec["experiments"]])))
            raw.append(float(np.median(
                [e["leakage_survival_raw_median"]
                 for e in rec["experiments"]])))
    if not conds:
        ax.text(0.5, 0.5, "leakage data pending", ha="center", va="center")
        return
    x = np.arange(len(conds))
    ax.axhspan(0.90, 1.02, color=GOOD, alpha=0.07, zorder=0)
    ax.axhspan(0.80, 0.90, color=WARN, alpha=0.09, zorder=0)
    ax.axhspan(0.60, 0.80, color=BAD, alpha=0.06, zorder=0)
    ax.axhline(0.90, color=GOOD, lw=0.9, ls="--", zorder=2)
    ax.axhline(0.80, color=WARN, lw=0.9, ls="--", zorder=2)
    width = 0.36
    ax.bar(x - width / 2, corr, width, color=QP, zorder=3,
           label="M3-corrected (the gate)")
    ax.bar(x + width / 2, raw, width, color=GRAY, zorder=3,
           label="raw measured")
    ax.set_xticks(x, conds, fontsize=7.2)
    ax.set_ylim(0.60, 1.02)
    ax.set_ylabel("one-excitation survival")
    ax.set_xlabel("$p_2$ (×10$^{-3}$) at readout 2×10$^{-2}$, then fakes")
    ax.text(len(conds) - 0.4, 0.915, "GREEN", fontsize=6.9, color=GOOD,
            ha="right")
    ax.text(len(conds) - 0.4, 0.815, "AMBER", fontsize=6.9, color=WARN,
            ha="right")
    ax.set_title("(c) leakage: raw reads AMBER on a healthy device",
                 loc="left")
    ax.legend(frameon=False, fontsize=6.9, loc="lower left")
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)
    _spines(ax)


def main() -> int:
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.25))
    panel_floor(axes[0])
    panel_envelope(axes[1])
    panel_leakage(axes[2])
    fig.tight_layout(pad=0.9)
    out_png = RES / "sim_s2" / "ar023a_s1s2.png"
    out_pdf = RES / "sim_s2" / "ar023a_s1s2.pdf"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    print("wrote", out_png)
    print("wrote", out_pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
