# Session 2026-08-13 — Paper 1 outline

- target: first-paper structure (owner-directed: "plan the paper first")
- mode: SYNTHESIZE
- substrate versions at load/close: KB-001 v0.3, KB-002 v0.2, KB-003
  v0.5, KB-004 v0.6, KB-005 v0.12 (no KB changes this session)

## Outcome

`paper/OUTLINE.md` drafted for owner sign-off. Structure anchored on
KB-004 §9 item 1 (the preregistered first-deliverable paper spec, which
the completed AR-010/011/020/021 cycle satisfies clause-for-clause) with
the post-spec findings given first-class sections:

- Thesis: motion-borne vs thermally-matchable geometry (the class-split
  comparator dichotomy) as the headline; dephasing-stabilization sign
  structure as the mechanism-level figure; the witness discipline's
  dual record (W3 null-fire → reformalization → fresh-seed n = 40
  confirmation) as the methods contribution.
- Non-claims NC-001/006/008/009/010 binding on framing; AR-021 novelty
  constraints embedded in §5; AR-019 calibrated-strength rider in §5;
  partition-dependence scope wall in §8.
- Appendix C = the full dated amendment log as a transparency artifact.
- Figure inventory: 6 figures, all from data already on disk.

## Delta list

- paper/OUTLINE.md (new; not canonical substrate — a working artifact).
- No KB changes.

## ADR candidates raised

None.

## Open items (owner decisions before drafting)

1. Title (A/B/C), 2. venue (rec: SciPost Physics), 3. author line,
4. repo public at submission?, 5. fund decay-rate-law AR before
submission? Then: draft §2 first per the writing plan.

## Reflection addendum (same session — owner-directed objectivity audit)

Joint reflection on novelty/overclaim; rulings folded into the outline:

1. **Test-first reframing** — the operational instantiated-vs-maintained
   test is the contribution; the class-split is its first measurement
   (not "motion-borne geometry" as established fact).
2. **Hardened probe gate** before §6 drafting: full ensembles, both
   sizes, smooth-f(H) Chebyshev optimization
   (scripts/ar020b_hardened_probe.py, running). Claim wording bound to
   probe scope.
3. Localized class → boundary case, out of headline counts.
4. No firstness claims anywhere.
5. Cross-discipline template fenced (proposed, not demonstrated);
   **philosophy OUT of the paper** — AR-022 queued (KB-005 v0.13) for
   the owner's own interest.

Classification of record (for venue/tone): an INSTRUMENT paper
(r-statistic/imbalance/OTOC-diagnostic genre) executed as a REGISTERED
STUDY; claim types = instrument + measured in-model facts +
methodological demonstration; zero mechanism/universality/gravity/
firstness claims. Epistemically: the first severe test inside the IDEG
programme (preregistration + adversarial companion as manufactured
severity).

## Hardened-probe outcome (same session — gate cleared)

AR-020b (full ensembles, both sizes, smooth-f(H) Chebyshev-Powell):
the family-only class-split is CORRECTED — metastable 20/20 and
integrable 20/20 matchable within ε_Φ (medians 0.09–0.17), localized
boundary (3–6/20, ≈ 0.27); **quasiperiodic is the sole size-robust
motion-borne survivor (0/40, median 0.32–0.34)** — the same class the
negative dephasing log ρ singles out. Two instruments, one survivor:
the paper's corrected headline. Third internal self-correction of the
cycle. Dated corrections applied to the AR-020 packet, spec §8,
KB-004 (v0.7), outline §0/§6; KB-005 → v0.14. §6 drafting gate CLEARED.
Substrate versions at close: KB-003 v0.5, KB-004 v0.7, KB-005 v0.14.

## Quality-sprint outcome (same session; owner-directed "expand runs")

Six descriptive extensions executed (in-script fixed seeds; committed
JSONs in results/AR-010/quality_sprint_*.json + ar020b files; no
preregistered verdict touched). All six landed and are folded into the
outline:

1. **Rigidity curve completed: ε_c ≈ 0.23 measured** (0.652 at ε=0.20 →
   0.420 at 0.25 → collapse by 0.45); Fig 6 complete.
2. **r2 comparator: subharmonic persists undiminished (0.89–0.90) to
   2000 periods** — the 200-period prethermal caveat becomes a measured
   statement; r1 carries the comparator role at small ε.
3. **Quasiperiodic headline reinforced: 0/80 matchable** (doubled
   ensembles, K = 24 + random starts; median 0.31, closest run 0.264 >
   ε_Φ); m-scan flat across m = 3/4/5 — generic to incommensurate
   coherent motion.
4. **γ-grid: the sign structure spans two decades** (quasiperiodic flat
   ≈ −0.25 for γ ∈ [0.001, 0.1]; metastable strengthens to −0.22;
   chaotic/scrambling saturate +2.5; ordering never reorders); Fig 4
   becomes curves.
5. **Partition-dependence class-resolved** (n = 24–72/class): chaotic
   0.11 … metastable 0.53 (max 0.82); largest for coherence-carried
   classes incl. the survivor — §8 scope wall now stated per class
   (supersedes the 2-run "9–20%" figure).
6. **Three-size trend for the marginal pair** (N = 14 point via
   coefficients-only witnesses): monotone, all statistics ≥ 0.976 at
   N = 14.

KB reconciliation of sprint results rides with the final paper
reconciliation (descriptive-extension record lives here + in the
committed JSONs + outline). NEXT: draft §2.
