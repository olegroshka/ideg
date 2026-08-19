# AR-023c — L4 backend/path selection: scan result and an envelope defect

```yaml
id: AR-023c
parent: AR-023 §7 (selection protocol), AR-023b (L4 preflight),
  AR-023a Amendment 2 (the rule the selection must serve)
mode: PREFLIGHT (live, read-only) + ADVERSARIAL (the frozen envelope)
date: 2026-08-19
status: SCAN COMPLETE; selection BLOCKED on an owner ruling
scope: backend properties and calibration read only; no job was built,
  no run() was called, nothing was submitted; `QPU-GO` untouched
```

## 1. What was scanned

Three operational Heron r2 QPUs on the account's Open instance:
`ibm_fez`, `ibm_marrakesh`, `ibm_kingston`. For each, every connected
ten-qubit simple path was enumerated (1,674 per backend after reversal
dedupe) and scored **before any outcome data exists**, by AR-023 §7's
frozen lexicographic formula: (max 2q, median 2q, max readout, median
readout).

| backend | paths | meeting envelope | best median 2q | best median RO |
|---|---:|---:|---|---|
| ibm_fez | 1,674 | 760 | 2.13e-3 | 1.42e-2 |
| ibm_marrakesh | 1,674 | 761 | 1.56e-3 | 1.24e-2 |
| ibm_kingston | 1,674 | 968 | 2.96e-3 | 6.41e-3 |

## 2. The defect: the envelope cannot see a per-qubit readout outlier

Applied as frozen, the formula recommends **`ibm_fez`, path
[98, 91, 92, 93, 94, 95, 99, 115, 114, 113]** — excellent two-qubit
error (max 2.68e-3), median readout 1.42e-2, comfortably inside the
envelope on every constrained quantity.

That path contains a qubit with **readout error 0.3098**.

The envelope (AR-023b §2, derived from S2) bounds *median* two-qubit
error, *median* readout, and *max edge* two-qubit error. It does **not**
bound maximum readout — because S2 varied readout **uniformly across all
qubits**, so a per-qubit outlier was never in the model that produced
the pre-commitment.

This matters because A2.5's leakage witness is a **joint ten-qubit
measurement**: raw one-excitation survival is scaled by
$\prod_i (1 - p_i)$, so one bad qubit multiplies the entire diagnostic.

| backend | median RO | max RO | survival factor | a true 0.97 state measures as | light |
|---|---|---|---|---|---|
| ibm_fez (formula's pick) | 0.0142 | **0.3098** | 0.607 | **0.589** | **RED** |
| ibm_marrakesh | 0.0124 | 0.0404 | 0.858 | 0.832 | AMBER |
| ibm_kingston | 0.0064 | 0.0310 | 0.915 | 0.887 | AMBER |

A device whose true sector fidelity is 97% would present a raw leakage
witness of 0.59 — below the 0.70 **RED** threshold, which AR-023 §17
registers as a kill criterion. M3 correction (A2.5c) recovers the
quantity in principle, but inverting a 31% confusion matrix amplifies
statistical error precisely on the diagnostic S2 identified as the
binding constraint. Selecting that path would be choosing to fight the
kill criterion for no gain.

**This is the C6 defect in a new place.** C6 was a diagnostic that could
not be computed from the measurement design; this is a pre-commitment
that cannot see the failure mode it exists to prevent. Both were found
by asking what the frozen artefact would actually do on hardware.

## 3. Proposed amendments — owner ruling required

Not applied. Adjusting a pre-commitment after seeing the data it ranks
is exactly what the discipline forbids without a dated amendment.

**L4-A1 — bound maximum readout (recommended, and I believe required).**
Add `max_readout_error ≤ 5×10⁻²` to the envelope. Justification is
structural, not fitted: the witness is multiplicative over ten qubits,
so a bound on the median is provably blind to the outlier that dominates
it. The threshold follows from the traffic light — keeping the raw
witness above AMBER for a healthy state requires the survival factor
above ~0.9, i.e. roughly 1e-2 per qubit sustained, with 5e-2 as the
single-qubit tolerance before one outlier controls the product.

*Effect:* `ibm_fez` is excluded; by the unchanged frozen formula
**`ibm_marrakesh` becomes the selection** (max 2q 2.75e-3 beats
kingston's 5.06e-3 on the first component).

**L4-A2 — reconsider the formula's ordering (genuine question, no
recommendation).** AR-023 §7 ranks two-qubit error first. S2 found that
under drift the binding constraint is **leakage**, which is
readout-driven. Both candidates sit far inside the envelope on
two-qubit error (2.75e-3 and 5.06e-3 against a 1e-2 limit), while their
readout differs by ~2× in the median and materially in the survival
factor (0.858 vs 0.915).

| | ibm_marrakesh | ibm_kingston |
|---|---|---|
| max / median 2q | 2.75e-3 / 1.56e-3 | 5.06e-3 / 2.96e-3 |
| max / median RO | 4.04e-2 / 1.24e-2 | 3.10e-2 / **6.41e-3** |
| witness survival factor | 0.858 | **0.915** |
| paths meeting envelope | 761 | **968** |

If the ordering stands, marrakesh. If the owner judges that S2's
leakage finding should promote readout above two-qubit error, kingston.
**Both are defensible; the point is that the choice must be made
explicitly and dated, not smuggled in by re-running a scan until a
preferred backend wins.**

## 4. Standing caveat

Calibration is time-varying. This scan is a snapshot
(`results/l4/backend_scan.meta.json` carries the UTC timestamp). AR-023
§13 B3 requires re-running the selector and re-freezing the snapshot
immediately before submission; if the selected backend recalibrates
materially in between, that is a dated pre-run amendment, not a silent
substitution.

## 5. What is still not done

- L4-A1/A2 ruling, then freeze backend + path into the manifest.
- Transpile the frozen 1,372-circuit bundle onto the chosen path at
  optimization level 3, `seed_transpiler=1701`; verify **no SWAP** and
  that only the ten intended physical qubits are used.
- Obtain **IBM's own usage estimate** against those compiled circuits —
  the 376 s figure is the documented rough formula plus M3 calibration,
  never checked against the platform.
- Set an instance **cost limit** (Pay-As-You-Go; IBM's limits are not
  preemptive).
- Then, and only then, `QPU-GO` — owner-typed, once, for one bundle.
