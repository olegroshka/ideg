"""AR-023a S1/S2 evidence figure -> results/sim_s2/ar023a_s1s2.{png,pdf}.

Three panels, one job each:
  (a) why the frozen gates fail — signal vs the two floor statistics,
      on the endpoint's own scale (magnitude comparison);
  (b) operating envelope — separation Delta vs two-qubit error, one
      line per readout level (change over an ordered variable);
  (c) sector-leakage envelope with the registered traffic-light bands.

Palette and rcParams are imported verbatim from scripts/make_figures.py
conventions so this figure sits in the paper's visual system: the
quasiperiodic blue is the accent (this IS the qp instance), neutral gray
is the null/defective statistic, status colors carry the traffic light
and always ship with a text label.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "hardware" / "ibm_exp1" / "results"
COND = RES / "sim_s2" / "conditions"

QP, GRAY, INK, INK2, MUT = "#2a78d6", "#898781", "#0b0b0b", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
GOOD, WARN = "#008300", "#eda100"
RO_COLORS = {0.01: "#2a78d6", 0.02: "#1baf7a", 0.03: "#eb6834"}

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


def main() -> int:
    s1_768 = load(RES / "sim_s1_768" / "s1_report.json")
    s1_896 = load(RES / "sim_s1_896" / "s1_report.json")
    if s1_768 is None:
        raise SystemExit("s1_report.json (768) missing")
    recs = s1_768["experiments"]
    eps_ref = float(s1_768["inputs"]["eps_reference"]["eps_sector_37"])
    sd = np.array([(r["eps_boot_q975"] - r["eps_boot_q025"]) / 3.92
                   for r in recs])
    c1_floor = float(np.median(2 * sd))
    frozen_768 = float(s1_768["gates"]["S1-G3"]["measured"])
    frozen_896 = (float(s1_896["gates"]["S1-G3"]["measured"])
                  if s1_896 else None)
    eps_median = float(s1_768["summary"]["eps_main_median"])

    fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.15))

    # ---- (a) signal vs floor statistics -----------------------------
    ax = axes[0]
    labels = ["signal\nε(37) exact", "frozen floor\n768 shots",
              "frozen floor\n896 shots", "endpoint floor\n(C1: 2×SD)",
              "endpoint SD"]
    values = [eps_ref, frozen_768, frozen_896 or np.nan, c1_floor,
              float(np.median(sd))]
    colors = [QP, GRAY, GRAY, GOOD, INK2]
    y = np.arange(len(values))[::-1]
    ax.barh(y, values, height=0.52, color=colors, zorder=3)
    for yi, v in zip(y, values):
        ax.text(v + 0.006, yi, f"{v:.3f}", va="center", ha="left",
                fontsize=7.5, color=INK)
    ax.axvline(0.05, color=WARN, lw=1.0, ls="--", zorder=2)
    ax.text(0.052, y[0] + 0.42, "S1-G3 gate 0.05", fontsize=7,
            color=WARN, ha="left")
    ax.set_yticks(y, labels, fontsize=7.2)
    ax.set_xlim(0, 0.275)
    ax.set_xlabel("normalized metric units")
    ax.set_title("(a) the floor, not the signal, fails the gate",
                 loc="left")
    ax.grid(axis="x", zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    # ---- (b) operating envelope -------------------------------------
    ax = axes[1]
    p2_values = [0.003, 0.006, 0.01]
    all_delta = []
    for ro in (0.01, 0.02, 0.03):
        xs, ys = [], []
        for p2 in p2_values:
            rec = load(COND / f"grid_p2-{p2:g}_ro-{ro:g}"
                       / "battery_report.json")
            if rec:
                xs.append(p2 * 1000)
                ys.append(rec["delta_median"])
                all_delta.append(rec["delta_median"])
        if xs:
            ax.plot(xs, ys, "-o", color=RO_COLORS[ro], lw=2.0, ms=5,
                    mec="white", mew=1.2, zorder=3,
                    label=f"readout {ro:g}")
            ax.text(xs[-1] + 0.25, ys[-1], f"{ro:g}", fontsize=7.2,
                    color=RO_COLORS[ro], va="center")
    ax.set_xlim(2.2, 11.4)
    for name in ("fake_fake_aachen", "fake_fake_boston"):
        rec = load(COND / name / "battery_report.json")
        if rec:
            all_delta.append(rec["delta_median"])
            ax.axhline(rec["delta_median"], color=MUT, lw=0.8, ls=":",
                       zorder=1)
            ax.text(2.35, rec["delta_median"] + 0.0008,
                    name.replace("fake_fake_", "fake "), fontsize=6.8,
                    color=INK2, ha="left", va="bottom")
    if all_delta:
        lo, hi = min(all_delta), max(all_delta)
        span = max(hi - lo, 1e-3)
        # reserve the lower third as whitespace for the legend
        ax.set_ylim(lo - 0.55 * span, hi + 0.10 * span)
    ax.set_xlabel("two-qubit depolarizing error  $p_2$  (×10$^{-3}$)")
    ax.set_ylabel("separation  Δ  (median)")
    ax.set_title("(b) operating envelope: Δ survives the grid",
                 loc="left")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax.grid(zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    # ---- (c) leakage envelope ---------------------------------------
    ax = axes[2]
    xs, med, mn = [], [], []
    for p2 in p2_values:
        rec = load(COND / f"grid_p2-{p2:g}_ro-0.01" / "provenance.json")
        if rec:
            vals = np.array(sorted(rec["survival"].values()))
            xs.append(p2 * 1000)
            med.append(float(np.median(vals)))
            mn.append(float(vals.min()))
    ax.set_xlim(1.4, 12.6)
    ax.axhspan(0.90, 1.02, color=GOOD, alpha=0.07, zorder=0)
    ax.axhspan(0.80, 0.90, color=WARN, alpha=0.09, zorder=0)
    ax.axhline(0.90, color=GOOD, lw=0.9, ls="--", zorder=2)
    ax.axhline(0.80, color=WARN, lw=0.9, ls="--", zorder=2)
    ax.text(12.4, 0.915, "GREEN\nmedian ≥ 0.90", fontsize=6.8,
            color=GOOD, va="bottom", ha="right", linespacing=1.35)
    ax.text(12.4, 0.815, "AMBER", fontsize=6.8, color=WARN,
            va="bottom", ha="right")
    if xs:
        ax.plot(xs, med, "-o", color=QP, lw=2.0, ms=5, mec="white",
                mew=1.2, zorder=3, label="median survival")
        ax.plot(xs, mn, "--o", color=INK2, lw=1.4, ms=4, mec="white",
                mew=1.0, zorder=3, label="minimum")
    for name, mk in (("fake_fake_aachen", "s"),
                     ("fake_fake_boston", "D")):
        rec = load(COND / name / "provenance.json")
        if rec:
            vals = np.array(sorted(rec["survival"].values()))
            ax.scatter([2.0], [np.median(vals)], marker=mk, s=26,
                       color=GOOD, zorder=4, edgecolor="white",
                       linewidth=0.8)
    ax.text(2.0, 0.996, "Heron fakes", fontsize=6.8, color=GOOD,
            ha="left", va="top")
    ax.set_xlabel("two-qubit depolarizing error  $p_2$  (×10$^{-3}$)")
    ax.set_ylabel("one-excitation survival")
    ax.set_ylim(0.775, 1.02)
    ax.set_title("(c) sector leakage: GREEN through $p_2=6{\\times}10^{-3}$",
                 loc="left")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax.grid(zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

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
