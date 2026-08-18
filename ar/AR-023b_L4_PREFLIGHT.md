# AR-023b — L4 preflight checklist and kickoff (backend selection → QPU-GO)

```yaml
id: AR-023b
parent: AR-023 (design of record), AR-023a (S1/S2 spec + Amendments 1-2)
mode: PREFLIGHT (requires owner decisions and network access)
status: BLOCKED on S2 closure; written 2026-08-18 so the next session
  starts from a checklist rather than from reconstruction
scope: everything between "S1/S2 green" and the owner typing QPU-GO
```

## 0. Do not start until

- [ ] S2 closed, **including the drift arm** (AR-023a A2.6).
- [ ] `s2_report.json` records the operating envelope and the frozen L4
      path-quality requirement.
- [ ] The S1/S2 shared-implementation refactor has landed, or the owner
      has explicitly accepted the duplicated paths with the compliance
      guards as the mitigation (see §4).

## 1. What is already frozen (do not re-derive)

| Item | Value |
|---|---|
| instance | `TA_ii_quasiperiodic`, N = 10, run 0, seed 2100294288 |
| exact reference | ε_sector^(37) = **0.227910117170944** |
| bundle | 28 settings × 49 states = **1,372 circuits**, hashes in the manifest |
| comparator | `sector_comparator_N10_run0.npz`, sha256 `73b66f94…` |
| decision rule | AR-023a Amendment 2 (A2.1–A2.10) |
| shots | **not** frozen — A2.8 defers this to L4 (see §3) |

## 2. Backend selection (no outcome data may influence it)

- [ ] List operational QPUs on the account's instance.
- [ ] Enumerate every connected 10-qubit simple path in the coupling map.
- [ ] Score paths **before** any outcome data, by the AR-023 §7 formula
      (max/median two-qubit error, max/median readout, compiled depth,
      worst edge as tie-break).
- [ ] Reject any path failing the **frozen envelope pre-commitment**
      derived from S2: median two-qubit ≤ 6×10⁻³, median readout ≤
      2×10⁻², max edge ≤ 1×10⁻². Confirm against the final
      `s2_report.json` — the numbers above predate the drift arm.
- [ ] Freeze backend, path, calibration timestamp, and properties
      snapshot into the manifest.
- [ ] Transpile at optimization level 3, `seed_transpiler=1701`,
      `initial_layout=<frozen path>`; verify **no SWAP** and that only
      the ten intended physical qubits are used.

## 3. Budget — the arithmetic here is ours, not IBM's

Current estimates (rough formula + M3's 20 balanced calibration
circuits), against the 450 s cap and a 600 s free allocation:

| shots | executions | estimate | of free allocation |
|---|---|---|---|
| 768 | 1,069,056 | **376.2 s** | 63% |
| 896 | 1,247,232 | **438.5 s** | 73% |

- [ ] **Obtain IBM's own usage estimate** against the compiled circuits
      (AR-023 §8 requires this). Our figure is the documented rough
      formula and has never been checked against the platform.
- [ ] Choose shots. Recommendation **768**: S1 passed 100/100 at both
      settings under Amendment 2, so the statistical argument for 896
      evaporated, and 768 leaves 224 s of allocation instead of 161 s.
      896 also leaves only ~12 s under the 450 s cap.
- [ ] Confirm the free-allocation balance (10 min per **28-day rolling**
      window; a promotional 180 min may also be active — check, it
      changes the risk calculus entirely).
- [ ] **Set an instance cost limit.** The account is Pay-As-You-Go, and
      IBM's cost limits are **not preemptive**: a running job can exceed
      the limit, be cancelled as "Ran too long", and still be billed.
- [ ] Note: a job failing from **user error or user cancellation**
      consumes usage including QPU preparation overhead; only IBM-side
      system errors are zero-rated. One clean attempt fits the window; a
      full retry does not (376 + 376 > 600). The rolling window means
      the fallback is *waiting*, not paying.

## 4. Code state to resolve before submission

- [ ] **Unify the S1/S2 analysis paths.** Two defects this programme
      (A2.1 floor, A2.5c leakage) were amendment items ported into one
      path and not the other; both produced code that ran cleanly and
      returned plausible wrong numbers. `test_amendment2_compliance.py`
      pins them structurally but cannot check semantics.
- [ ] The QPU analysis path must reuse the *same* implementation the
      simulations validated — this is the AR-023 §12 B7 immutability
      requirement in practice.
- [ ] Re-run the full suite (currently 28/28) plus the infinite-shot
      acceptance gate after any refactor.

## 5. Submission protocol (unchanged from AR-023 §13)

- [ ] Browser phase B1–B4 with the owner present; no credential ever
      enters chat, files, or screenshots.
- [ ] Final dry run from the frozen bundle on a noisy simulator.
- [ ] Authorization stop B5 — the prompt must now state **both** the
      estimated QPU seconds **and** the worst-case cost exposure, since
      the account is billable.
- [ ] `QPU-GO` is owner-typed, for one identified bundle, once.
- [ ] One SamplerV2 job in job mode; save job ID, receipt, manifest hash
      immediately; monitor without cancelling a healthy job.

## 6. After data (B7 discipline)

- [ ] Decode by `circuit_id` and the saved bit maps, never list position.
- [ ] Raw and M3 analyses side by side, identical pipeline.
- [ ] Every diagnostic before the headline: leakage (corrected **and**
      raw), projection, drift/duplicate floor, per-time and per-pair
      influence.
- [ ] Evaluate the Amendment 2 success rule exactly as written; record
      the verdict whatever it is.
- [ ] If a bug is found, preserve the first analysis, write a dated
      amendment, and rerun from the same raw data — never conceal a
      superseded result.

## 7. Stop conditions specific to this pilot

Beyond AR-023 §17: stop and report rather than amend if
- the drift arm shows the duplicate floor breaching 0.05 (that is a
  **hardware-stability requirement**, not a rule defect — three rule
  amendments in one programme is already the outer edge of defensible);
- IBM's usage estimate materially exceeds ours (re-derive the budget,
  do not shave the design to fit);
- the selected path cannot meet the frozen envelope pre-commitment.
