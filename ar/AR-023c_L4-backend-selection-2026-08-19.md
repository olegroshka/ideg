# AR-023c — L4 backend/path selection: scan result and an envelope defect

```yaml
id: AR-023c
parent: AR-023 §7 (selection protocol), AR-023b (L4 preflight),
  AR-023a Amendment 2 (the rule the selection must serve)
mode: PREFLIGHT (live, read-only) + ADVERSARIAL (the frozen envelope)
date: 2026-08-19
status: RESOLVED — L4-A1 applied, L4-A2 ruled, backend and path frozen,
  compilation gate PASSED; remaining: instance cost limit, pre-submission
  re-scan, and owner `QPU-GO` (see §6)
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

## 5. RESOLUTION (owner ruling, 2026-08-19)

**L4-A1 APPLIED.** `max_readout_error ≤ 5×10⁻²` is now part of the
envelope pre-commitment, implemented in `select_backend_path.py`
alongside the S2-derived bounds.

**L4-A2 RULED.** Readout is promoted above two-qubit error; the score
formula is now lexicographic on (median readout, max readout, max 2q,
median 2q). The superseded AR-023 §7 ordering is retained in the code
and in the scan output for the dual record.

**A consequence the owner should see, recorded because the ruling
changed the ranking it was reasoned from.** L4-A1 disqualifies bad
*paths*, not bad *backends*. Re-scanning under the amended rule, every
backend's best qualifying path improved, and `ibm_fez` — excluded before
only because its top-scoring path carried the 0.31 qubit — came back
with the best numbers overall:

| backend | median RO | max RO | median 2q | qualifying paths |
|---|---|---|---|---|
| ibm_fez | **5.25e-3** | 1.12e-2 | **2.63e-3** | 185 |
| ibm_marrakesh | 5.92e-3 | 2.91e-2 | 2.48e-3 | 177 |
| **ibm_kingston (selected)** | 6.23e-3 | **1.09e-2** | 4.55e-3 | **764** |

**Owner selected `ibm_kingston`** with the amended numbers in hand. The
stated basis is drift robustness: 764 qualifying paths against fez's
185 means far more margin if the chosen path degrades between now and
submission, which AR-023 §13 B3 requires re-checking. All three
candidates sit well inside the envelope, so the trade was margin-now
versus margin-later, and the ruling took margin-later.

**Frozen selection**

```
backend        ibm_kingston (Heron r2)
physical path  [89, 88, 87, 97, 107, 108, 109, 118, 129, 128]
median RO 6.226e-3 | max RO 1.086e-2
median 2q 4.546e-3 | max 2q 5.968e-3
```

### Compilation gate — PASS

All 1,372 circuits transpiled to the frozen path at optimization level
3, `seed_transpiler = 1701`:

| check | result |
|---|---|
| SWAPs introduced | **0** |
| circuits touching qubits outside the path | **0** |
| unbound parameters | **0** |
| two-qubit gates per circuit | 18 (median = max) |
| depth | 92–94 |

The uniformity is expected and is itself a check: the family differs
only in rotation angles, so identical structure across all 1,372
circuits is what a correct compilation looks like.

### Usage estimate

| method | seconds | of 450 s cap | of 600 s free |
|---|---|---|---|
| AR-023 §8 rough formula | **376.2** | 84% | 63% |
| duration-based (compiled durations + rep delay) | 269.3 | 60% | 45% |

**Plan against 376 s**, the conservative figure. *Partially unmet
requirement, disclosed:* AR-023b §3 asks for IBM's own usage estimate
against the compiled circuits. No pre-submission estimate API was found
in `qiskit-ibm-runtime` that works without constructing a job, so this
remains outstanding; the platform surfaces its figure at submission
time, and it must be read there before `QPU-GO` is typed.

## 6. What is still not done

- [x] ~~L4-A1/A2 ruling, freeze backend + path~~ — done, §5.
- [x] ~~Transpile and verify no SWAP~~ — done, gate PASS, §5.
- [ ] **Read IBM's own usage estimate** on the submission page before
      confirming (no pre-submission API; the platform shows it at
      submission time).
- [ ] **Set an instance cost limit.** Pay-As-You-Go account; IBM's cost
      limits are *not* preemptive — a running job can exceed one, be
      cancelled as "Ran too long", and still be billed.
- [ ] **Re-run `select_backend_path.py` immediately before submitting.**
      Calibration is time-varying and this selection is a snapshot; if
      the frozen path has degraded, the 764 qualifying alternatives are
      the margin the ruling bought. A material change is a dated pre-run
      amendment, never a silent substitution.
- [ ] Then, and only then, `QPU-GO` — owner-typed, once, for one bundle.

## 7. Reproducing this selection

```powershell
python hardware/ibm_exp1/scripts/select_backend_path.py
python hardware/ibm_exp1/scripts/compile_and_estimate.py
```

Both are read-only with respect to the QPU: they query backend
properties and transpile locally. Neither can construct or send a job.
