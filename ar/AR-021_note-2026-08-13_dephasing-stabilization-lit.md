# AR-021 — Dephasing-stabilization literature check (comparative note)

```yaml
id: AR-021
title: "Is the AR-010 dephasing-stabilization effect known physics?"
mode: VERIFY + EXPLORE
parent: AR-010/AR-011 outcome (quasiperiodic/metastable negative log rho);
  first-paper framing decision
priority: P1 (executed 2026-08-13, owner-approved sequencing)
inputs: [ar/AR-010_confirmatory-2026-08-12.md §3.2,
         ar/AR-011_adversarial-2026-08-13.md §5 item 1,
         results/AR-010/confirmatory_summary.json]
question: >
  Is "weak dephasing increases the stationarity of an oscillating
  MI-graph geometry (negative log rho for quasiperiodic/metastable
  classes, positive for chaotic/scrambling)" known physics, and at what
  level — mechanism, object, or framing?
deliverable: this note; SRC-059..063 (verify)
promotion_effect: licenses (or forbids) novelty language in the
  first-paper draft; informs AR-020 priorities
kill_effect: none (framing decision; the measured effect stands
  regardless)
status: DONE (2026-08-13; reconciled in-session)
```

## 0. Verdict (summary)

**Mechanism: KNOWN. Object: NOT FOUND in survey scope. Permitted claim
level: diagnostic/framing novelty only, stated conditionally.**

1. The underlying mechanism — weak local dephasing damps the coherences
   that carry oscillations, shrinking the excursion amplitude of any
   derived functional — is standard open-system physics; its
   strong-coupling limit is the continuous quantum Zeno effect
   (canonical review SRC-059). Our γ = 0.01 sits in the weak/damping
   regime, not the Zeno regime. **No mechanism-novelty claim is
   licensed.**
2. The specific object — the *stationarity of an emergent MI-graph
   geometry over a moving state*, probed class-resolved under a weak
   dephasing channel, with the sign structure "noise pins
   coherence-driven (quasiperiodic/metastable) geometry to its mean
   while further destabilizing chaotic/scrambling geometry" — was NOT
   found. The two closest works: SRC-060 studies emergent MI networks
   under decoherence but as STATIC ground states under projective
   attacks (no dynamics, no channel, no classes); SRC-061 (SRC-049
   lineage) is a stationary phase diagnostic (no time, no noise).
3. The adjacent live literature stabilizes MOTION with noise
   (noise-stabilized DTCs, SRC-062; noise-induced quantum
   synchronization, SRC-063); our effect stabilizes geometric
   STATIONARITY over motion — same family, different object and
   direction. Useful positioning for the paper, not prior art for the
   claim.

**Permitted paper language:** "the class-resolved sign structure of the
geometric response to weak dephasing appears not to have been reported
for information-geometric functionals (we are aware of [SRC-060,
SRC-061] on static MI-network decoherence and [SRC-062, SRC-063] on
noise-stabilized dynamics)" — with the mechanism explicitly attributed
to standard decoherence damping (SRC-059 family). **Forbidden:** any
"new mechanism" or "noise-induced phase" language.

## 1. Method and scope caveat

Opportunistic (non-systematic) survey, 2026-08-13, web search at
abstract/summary level; two closest papers scope-checked individually
(SRC-060, SRC-061 — both confirmed non-overlapping in object). The
verdict is a *survey-scope* statement, not an exhaustiveness proof; the
paper draft should retain the conditional phrasing above. All SRC
metadata flagged `verify` per KB-003 governance (AR-002-series scope);
SRC-061 and SRC-063 author fields are explicitly unconfirmed.

## 2. What the effect is (restated for the record, from AR-010/AR-011)

At the calibrated γ = 0.01 (spec Amendment 3), the §5.2 log drift ratio
under dephasing is NEGATIVE for the quasiperiodic (−0.27) and metastable
(−0.09/−0.11) classes — the perturbed Φ trajectory wanders LESS from the
unperturbed reference geometry than the unperturbed oscillation does —
while chaotic/scrambling read +2.1/+2.2, localized +1.5, integrable
+0.75, replicated at two sizes (criterion (b), both tracks). Per AR-011,
this is a statement at the calibrated strength about the preregistered
instrument (AR-019 framing rider), on the posited site partition
(AR-011 Attack C scope wall).

## 3. Consequences

- **First paper:** the effect is usable as a lead result at
  diagnostic/framing level with the conditional phrasing of §0;
  the mechanism paragraph cites the Zeno/damping family (SRC-059) and
  positions against SRC-060..063.
- **AR-020:** no change to its two design requirements; the survey adds
  one suggestion — a null-subtracted OTOC has precedent-adjacent
  constructions in the monitored-systems literature (not sourced here;
  AR-020 should do its own targeted search).
- **AR-019 conditional follow-up (decay-rate-law):** unchanged; it
  would strengthen the mechanism attribution if the paper wants it.
