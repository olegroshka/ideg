# The price of standing still

**Can a motionless state fake the geometry of a moving one?**

When a quantum system evolves, you can build a *geometry* out of it: treat
every pair of sites as connected by how much information they share, and
let distance be the shortest path through that web of correlations. Watch
the system move, average the geometry over time, and you get a stable
structure.

Here is the awkward question. That structure is stable — so does it
actually *require* the motion? Or could some frozen, stationary state have
produced the very same geometry, making the dynamics incidental to it?

This repository is the complete, commit-hashed record of taking that
question seriously: a registered study that searches hard for the
motionless impostor, and reports exactly when it is found.

---

## The setup

Take a finite spin chain. At each instant, compute the mutual information
$I(i{:}j)$ between every pair of sites, turn it into an edge weight
$w_{ij} = -\ln\big(I_{ij}/2\ln 2\big)$, and run all-pairs shortest paths.
That yields a distance matrix $D(t)$ — an emergent geometry. Average it
over a long window to get $\bar D$.

![Pipeline: mutual-information graph to shortest-path metric](paper/figures/fig1_pipeline.png)

*Two dynamical classes, same pipeline. The chaotic chain (top) scrambles
into a nearly featureless web; the quasiperiodic chain (bottom) keeps a
visibly structured, breathing geometry. Right column: the window-averaged
metric each one settles into.*

Then ask a stationary state $\sigma$ to reproduce $\bar D$, and measure how
badly the best one misses:

$$\varepsilon = \frac{\lVert \Phi[\sigma] - \bar D\rVert_F}{\lVert \bar D \rVert_F}$$

The whole study is about how that number behaves once you take the search
for $\sigma$ seriously.

---

## Three results

### 1. Time-averaging and geometry-building do not commute

The obvious candidate impostor is the system's own infinite-time average
state. It fails — by **36–55%** (class medians, both system sizes; 8% for
the metastable class). Mutual information is nonlinear in the state, so
"average the state, then build the geometry" is simply not the same object
as "build the geometry, then average it." This is not a finite-window
artifact, and not an artifact of deleting stationary structure; both
alternatives were tested and excluded.

### 2. What matters is *which stationary states you allow*

This is the corrected headline, and it took several rounds of adversarial
review to reach:

| dynamical class | best stationary impostor | miss |
|---|---|---|
| chaotic / scrambling | thermal window | **≈ 0.04** (consistent with ETH) |
| integrable (generic quench) | generalized Gibbs ensemble | **≈ 0.15** |
| quasiperiodic | any population-only family in a fixed eigenbasis | **0.23–0.32** (fails) |
| quasiperiodic | the *full commutant* of $H$ | **≈ 0.005** (near-exact) |

So every class has *some* stationary impostor. What separates the classes
is the **resource the impostor needs** — and for the quasiperiodic case
that resource turns out to be inadmissible:

> The commutant impostor achieves its near-exact match by placing
> **~70% of its weight in magnetization sectors the dynamics never
> populates.** Restrict it to the conserved sector the state actually
> lives in, and the near-exact match collapses back to the
> population-only plateau (**0.24–0.26**).

**No near-exact sector-admissible impostor of the quasiperiodic metric was
found.** That is the claim of record — carefully weaker than "none
exists," because a search establishes upper bounds, not impossibility.

![Comparator results](paper/figures/fig5_comparator.png)

*(a) Removing the motion (filled) versus ablating stationary structure
(open) — the two are different, and conflating them was one of the
corrections. (b) The representation gap across classes at both sizes.
(c) Fraction of quasiperiodic runs matched versus threshold: the
unrestricted commutant (light blue) matches almost everything
immediately; pinned to the accessible sector (dark blue) it does not.*

### 3. Noise pins the one class that resists

Weak dephasing *stabilizes* the moving quasiperiodic metric toward its own
time average, while destabilizing chaotic-class metrics — singling out the
same class through an independent, dynamical instrument.

---

## Honest limits

This is a **toy-model, in-model study** on finite chains ($N = 10, 12$).
It makes no claim about gravity, holography, spacetime, universality, or
priority. The threshold used throughout ($\varepsilon_\Phi = 0.25$) is a
calibrated finite-size noise floor, and at that value the sector-pinned
quasiperiodic counts *straddle* it (15/20 at $N=10$, 9/20 at $N=12$) —
stated precisely rather than rounded into a clean win.

**Seven claim-level corrections** were made during this programme, each
caught by the study's own audit mechanisms, and each is reported as a
result rather than quietly folded away. One preregistered witness scheme
failed its own null test and was retired. The corrections are in
`ar/` and `sessions/`, with dates and commit hashes.

---

## Hardware pilot (in progress)

A preregistered pilot to reconstruct the same geometry on an IBM quantum
processor for one registered $N=10$ quasiperiodic instance: 1,372 circuits
realizing exact evolved snapshots plus the sector-pinned comparator, with
every two-site density matrix reconstructed via a 27-setting covering-array
tomography, and a 28th all-Z setting as a sector-leakage witness.

![S1/S2 simulation gates](hardware/ibm_exp1/results/sim_s2/ar023a_s1s2.png)

*Local validation before any quota is spent. (a) The reconstruction floor:
the originally specified statistic (grey) is a full-matrix norm compared
against a scalar endpoint — it overstates the endpoint's own uncertainty by
7.8×, matching √(effective metric directions). (b) The separation survives
device-realistic noise across the tested grid. (c) Sector leakage must be
readout-corrected: raw counts read AMBER on a perfectly healthy device.*

Nothing has been submitted to a QPU. The simulation gates are green; backend
selection and authorization remain. Details: `ar/AR-023_hardware-pilot-2026-08-16.md`
and `hardware/ibm_exp1/README.md`.

---

## Reproducing

```bash
pip install -e .
pytest tests -q                      # core package
python scripts/make_figures.py all   # regenerate paper figures
```

The classical campaigns are driven by `scripts/`, with results and
manifests under `results/AR-010/`. Every headline number resolves to a
committed evidence packet in `ar/`.

---

## How this repo is organised

| path | what it holds |
|---|---|
| `substrate/` | the canonical record: charter, ontology, theory landscape, hypotheses, programme |
| `ar/` | evidence packets — one per activity, with the numbers behind every claim |
| `sessions/` | dated session logs, including every correction and why it happened |
| `paper/` | the manuscript and its figures |
| `src/ideg/` | the model, metric, and witness implementations |
| `hardware/ibm_exp1/` | the IBM pilot: circuits, manifests, simulation gates |

The method is the [Shared Substrate](https://github.com/olegroshka/shared-substrate)
discipline (SSRN `10.2139/ssrn.7218019`): **no result exists until it is
recorded**, claims must resolve to a packet, and negative results are
recorded with the same care as positive ones.

---

**Status:** manuscript complete, preprint pending. If you want the
argument in full, read `paper/latex/main.pdf`; if you want to check
whether we fooled ourselves, read `sessions/` — that is where the
corrections live.
