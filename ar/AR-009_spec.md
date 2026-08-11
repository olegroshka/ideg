# AR-009 — Track E3 toy-model family specification

```yaml
id: AR-009
title: Toy-model family specification (Track E3, first deliverable)
mode: FORMALIZE
parent: BH-004, HYP-009
priority: P0
inputs: [KB-004 §4 BH-004, KB-005 §7, TH-033, TH-037, CON-034, CON-035, CON-036]
question: >
  What exact models, observables, witnesses, comparators, and pass/fail
  thresholds adjudicate BH-004: stationary emergent geometry from witnessed,
  sustained-by nonstationary microdynamics — and does robustness of
  Φ-stationarity differ by dynamical class?
deliverable: this document, reviewable standalone before any AR-010 code
promotion_effect: AR-010 implementation licensed against this spec
kill_effect: if no well-posed witness/comparator scheme exists, BH-004 returns
  to FORMALIZE with the obstruction recorded
status: PLANNED
```

> **Preregistration rule:** every metric, threshold, and comparison below is
> fixed before AR-010 runs. Post-hoc additions are recorded as amendments with
> dates and reasons, and analysed separately (exploratory, not confirmatory).

## 1. Models

### T-A — Closed finite quantum system
- Hilbert space / system size N: __ (target: __ qubits; justify tractability)
- Hamiltonian classes:
  - (i) fixed point: __
  - (ii) quasiperiodic (few incommensurate gaps): __
  - (iii) chaotic (random-matrix class): __
  - (iv) metastable / code subspace: __
- Initial-state ensembles per class: __
- Clock: external lab clock (scope-noted; OL-4 caveat recorded per CON-035)

### T-B — Driven / Floquet system
- Drive protocol and period: __
- DTC regime parameters (TH-033 template): __
- Subharmonic witness definition: __

### T-C — Interacting spin chain with MI-graph geometry
- Chain length / boundary conditions: __
- Dynamics regimes (scrambling / integrable / localized): __
- Φ[X]: MI-graph metric per TH-037 (SRC-049) — exact construction: __

## 2. Emergent-geometry functional Φ
- Definition(s), including graph→distance map and any regularization: __
- Stationarity criterion for Φ (tolerance ε, time window): __

## 3. Witnesses (CON-034)
For each model class, the invariant observable(s) certifying microdynamics:
- candidates: relative phases, OTOCs, recurrence distance d_phys, spectral
  gap structure, subharmonic response (T-B)
- invariance argument for each (what redundancies it survives): __

## 4. Mandatory comparators and controls
- **Stationary-state comparator:** construction of an exactly stationary state
  matched on Φ; the discriminating observable(s): __ (KB-004 §7 item 12)
- **Switch-off test:** quench protocol; predicted degradation signature of
  Φ-stationarity if sustained-by holds (CON-036): __
- **Representation-invariance battery:** basis/gauge/subsystem changes applied
  to every witness: __
- **Null comparator:** pure global-phase evolution (NC-009 guard): __

## 5. Success / failure metrics (preregistered)
- (a) witness separates dynamical classes: statistic __, threshold __
- (b) robustness differential: perturbation/noise/subsystem-loss protocols __,
  effect measure __, threshold __
- Outcomes and their KB effects:
  - (a) and (b) hold → BH-004 supported in-model; BH-005 licensed
  - (a) holds, (b) null → paper reports clean null on the novel question
  - (a) fails → witness scheme returns to FORMALIZE; recorded negative

## 6. Analysis plan
- Estimators, error bars, seeds, number of disorder/ensemble realizations: __
- Compute budget and size-scaling checks: __

## 7. Non-goals and scope walls
- No claim T-A/B/C are gravity; no OL-4 conclusions beyond model realization
  (collision rule 10; KB-005 §7 non-goals).

## 8. Open items / amendments log
- __
