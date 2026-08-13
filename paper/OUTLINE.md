# Paper 1 outline — Stationary emergent geometry from witnessed nonstationary microdynamics

Status: OUTLINE FOR OWNER SIGN-OFF (2026-08-13). Charter basis: KB-004 §9
item 1 (the preregistered first-deliverable paper); every claim below
resolves to the AR-009 spec + AR-010/011/020/021 packets. Non-claims
NC-001/006/008/009/010 are binding on the framing throughout.

## 0. Thesis (one paragraph) — TEST-FIRST FRAMING (reflection ruling
2026-08-13)

We introduce an **operational test** of whether a stable emergent
structure is merely *instantiated* by its substrate or *actively
maintained* by the substrate's dynamics — switch-off response,
motionless-comparator matching, and own-baseline robustness — and
report its first measurement, on the mutual-information-graph metric
[SRC-049] of finite spin chains. The measured outcome (HARDENED
probe, final: full ensembles, both sizes, smooth-f(H) optimization) is
a single-survivor split: every class's time-averaged structure is
matchable by some stationary state within ε_Φ — chaotic/scrambling
strongly (miss ≈ 0.04), metastable (≈ 0.09–0.13), integrable
(≈ 0.16–0.17), localized as a boundary case (3–6/20, ≈ 0.27) — EXCEPT
the quasiperiodic class: 0/40 matched across both sizes (miss
0.32–0.34). The same class is independently singled out by the
negative dephasing response (noise pins its moving structure to its
mean). Two instruments, one survivor: incommensurate coherence-carried
motion is the one regime whose time-averaged information metric no
searched stationary state reproduces. A preregistered
witness discipline makes the claims falsifiable — its self-correction,
when one witness failed its own null test, is reported as a result.

**Classification (for tone/venue):** an INSTRUMENT paper (genre of the
r-statistic/imbalance/OTOC-diagnostic papers) executed as a
REGISTERED STUDY. Claim types: instrument claims + measured in-model
facts + methodological demonstration; explicitly zero mechanism,
universality, gravity, or firstness claims.

## 1. Candidate titles (owner picks)

- A. *Stationary emergent geometry from witnessed nonstationary
  microdynamics: a preregistered toy-model study*
- B. *Motion-borne geometry: when an information metric needs the
  dynamics beneath it*
- C. *Witnessing motion beneath stationary information geometry*

## 2. Venue candidates (owner picks; ordered by my recommendation)

1. **SciPost Physics** — open peer review matches the preregistration
   trail exceptionally well; length-tolerant; the amendment-log
   appendix becomes a feature.
2. **PRX Quantum** — methods + results visibility; tighter length.
3. **Quantum** — open access, methods-friendly.

## 3. Structure

### §1 Introduction (~1.5 pp)
- The question, stated at toy-model scope: can stationary effective
  geometry be *sustained by* — not merely compatible with —
  nonstationary microdynamics? (CON-036 language, defined here.)
- Why finite models and why preregistration (lookahead discipline;
  every metric/threshold fixed before runs; the full amendment log is
  Appendix C).
- Positioning: MI-network/emergent-metric lineage [SRC-049, SRC-060,
  SRC-061]; DTC/Floquet matter [SRC-043, SRC-044]; noise-stabilized
  dynamics [SRC-062, SRC-063]; Zeno/damping mechanism family [SRC-059].
- Contributions list (5 bullets = Results I–V below).
- Explicit non-claims box: no gravity/OL-4 claims, no primitive-
  information assumption, external lab clock declared (NC-006/001/010).

### §2 Models, functional, witnesses, protocol (~2.5 pp)
- Model family T-A (4 classes), T-C (3 regimes), T-B (Floquet DTC +
  comparator regimes); table with class, H, initial ensemble, sanity
  certificate (incl. the free-spectrum certificate replacing the
  mis-specified Poisson window — first taste of the discipline).
- Φ construction: MI → −log weights with cap → shortest-path metric;
  stationarity criterion (ε_Φ = 0.25 with its pilot-measured
  noise-floor justification); cap diagnostic.
- CON-034 witness requirements, THE NULL-SILENCE CLAUSE stated as a
  design principle; witness battery W1–W5 with invariances.
- Comparators: diagonal ensemble, switch-off, invariance battery, null.
- Preregistration mechanics: spec → committed seed manifests →
  amendments only by dated log entry; pilot/confirmatory split.
- Fig. 1: pipeline schematic (state → MI graph → metric) + class table.

### §3 Results I — Existence: stationary geometry over witnessed motion (~1.5 pp)
- Baseline stationarity table (all classes/sizes/T-B): chaotic 20/20,
  scrambling 20/20, DTC 100/100 stationary with witnesses firing
  (Ξ ≈ 0.95–0.99, W5 = 0.94); quasiperiodic/integrable/metastable
  genuinely moving; localized straddles.
- Honest context: for chaotic classes this existence is equilibration
  physics (typicality); the paper's content is what follows.
- Fig. 2: δΦ(t) trajectories per class + stationarity/witness table.

### §4 Results II — The witness discipline at work (dual record) (~2 pp)
- W3 (OTOC) fires on the frozen null (c_sat ≈ 1.11, t* = 1.5):
  operator spreading ≠ state motion; preregistered discard clause
  executes → criterion (a) FAILS as originally registered
  (scrambling|localized left singly witnessed).
- Reformalization (owner-ratified, dated): {PR_A, w2_mean, Ξ} — all
  null-silent by construction; fresh-seed re-adjudication at n = 20
  FAILS on a different, threshold-straddling pair (seed-luck exposed:
  AUC SE ≈ 0.05–0.08); n = 40 stabilization → (a) HOLDS, 18/18.
- The methodological claims: (i) null-silence is a nontrivial filter —
  the field's default scrambling diagnostic fails it; (ii) sharp AUC
  thresholds at small ensembles are seed-sensitive by construction —
  fresh-seed confirmation is not optional. NO FIRSTNESS CLAIMS anywhere
  (no "first preregistered many-body study" language — we show the
  artifact and let it speak; we have not surveyed for precedents).
- **Three-size trend (sprint):** the marginal scrambling|integrable
  AUCs rise monotonically N = 10 → 12 → 14 (w2_mean 0.952 → 0.975 →
  0.976; PR_A 0.979 → 0.979 → 1.000; Ξ 0.956 → 0.975 → 0.976) —
  descriptive third-size support for the final verdict (appendix
  figure).
- Fig. 3: witness values per class (null row highlighted; discarded-W3
  panel shown struck through — the dual record as a figure).

### §5 Results III — Class-resolved robustness of stationarity (criterion b) (~2 pp)
- Dephasing at calibrated γ: class-ordered log ρ replicated at two
  sizes in both tracks; the SIGN STRUCTURE: negative for
  coherence-carried classes (weak dephasing pins oscillating geometry
  to its mean) vs +2.1 for chaotic.
- **γ-grid curves (sprint; Fig 4 upgrade):** the sign structure spans
  TWO DECADES (γ = 0.001–0.1): quasiperiodic flat at ≈ −0.25;
  metastable negative, strengthening monotonically (−0.02 → −0.22);
  chaotic/scrambling positive, saturating (+0.9 → +2.5);
  integrable/localized mild plateau (+0.6). Class ordering never
  reorders — the confirmatory single-γ statement generalizes to a
  regime statement (descriptive; the preregistered verdict remains the
  single-γ one).
- Mechanism attribution: standard decoherence damping of
  coherence-carried beats [SRC-059 family]; the class-resolved
  geometric reading is, to our survey's knowledge, unreported
  [conditional novelty phrasing per AR-021 — exact permitted wording
  in the AR-021 note §0].
- Quench and loss: clean nulls (reported; fixed-point pairs
  floor-referenced, instrument note).
- Calibrated-strength framing rider (AR-019): statements at λ = 0.1,
  γ = 0.01, not strength-independent class properties.
- Fig. 4: log ρ bar chart per class/protocol, negative bars
  highlighted; two-size replication panel.

### §6 Results IV — Sustained-by vs compatible-with: motion-borne geometry (~2 pp)
- The adjudication and its adversarial correction, told straight:
  the fragility-direction artifact (floored denominator) caught by
  our own adversarial pass; what survives is stronger:
- Switch-off geometry jump: dephasing the state at t_off moves Φ by
  43–90% of ‖D̄‖ — killing the motion CHANGES the geometry.
- The comparator finding: MI is nonlinear in the time-averaged RDMs,
  so the diagonal ensemble is NOT Φ-matched (43–90% away). The
  dichotomy is stated TEST-FIRST: the instrument is the matched-
  comparator search; its measured outcome is the class-split.
- **HARDENED PROBE RESULTS (final; gate cleared 2026-08-13):**
  matchable within ε_Φ — chaotic 20/20 (median 0.035–0.042),
  scrambling 20/20 (0.037–0.046), metastable 20/20 (0.091–0.132),
  integrable 20/20 (0.161–0.170); boundary — localized 3–6/20
  (≈ 0.27); **UNMATCHED — quasiperiodic 0/40 across both sizes
  (0.32–0.34)**. **Sprint reinforcement: 0/80 total** (doubled
  ensembles, K = 24 + extra random starts; median 0.31, closest single
  run 0.264 > ε_Φ); m-mode scan flat across m = 3/4/5 (0.31–0.33) —
  unmatchability is generic to incommensurate coherent motion. The family-only claims for metastable/integrable were
  corrected by this probe (third internal self-correction — reported in
  §4's discipline narrative). Claim wording bound to probe scope
  ("no stationary state that is a smooth function of H, within the
  searched families and parameterization").
- The two-instrument convergence paragraph: the comparator survivor and
  the negative-dephasing class are the SAME class — quasiperiodic.
- Localized class: BOUNDARY CASE (straddles ε_Φ itself), excluded from
  headline counts.
- Fig. 5: (a) switch-off jump per class; (b) miss distributions over
  the full ensembles per class/size, ε_Φ line drawn, quasiperiodic
  isolated above it.

### §7 Results V — Driven geometry: the DTC regime (~1.5 pp)
- Stationary-with-witness 100/100 at ε = 0.03; rigidity h_sub(ε)
  measured over the FULL curve (sprint): locked to ε = 0.20 (0.65),
  crossing h_sub = 0.5 at **ε_c ≈ 0.23**, collapsed by ε ≈ 0.45 —
  a complete critical-strength measurement, not a bound.
- r1 comparator behaves (peak destroyed); **r2's subharmonic persists
  UNDIMINISHED (0.89–0.90) to 2000 periods** (sprint) — at ε = 0.03
  the clean interacting drive does not thermalize on any feasible
  horizon; r1, not r2, is the discriminating comparator at small ε
  (measured statement, replaces the 200-period caveat).
- Switch-off: W5 collapses (0.95 → 0.00) while Φ persists and
  improves — the preregistered open question resolves to
  compatible-with: MBL, not the drive, holds this geometry.
- Fig. 6: rigidity curve + switch-off panel (W5 collapse vs Φ
  persistence).

### §8 Scope walls and limitations (~1 p)
- Partition-dependence: CLASS-RESOLVED distribution (sprint, n = 24–72
  samples/class): chaotic 0.11, scrambling 0.15, integrable 0.22,
  localized 0.20, quasiperiodic 0.42, metastable 0.53 (max 0.82).
  Largest for the coherence-carried classes — including the survivor
  class. All claims are per-the-posited-partition (matchability
  compares both sides in the same frame); Φ is a geometry OF the
  factorization (TH-037 caveat made quantitative, per class).
- Finite size: N ≤ 12; the quasiperiodic construction is EXHAUSTIVELY
  unsatisfiable at N = 8 (0/56 triples) — a certificate-hygiene
  finding; scrambling|integrable AUC threshold-marginal at N = 10.
- Cap construction; calibrated strengths; external lab clock; no OL-4
  extrapolation (NC-006/009/010 restated).

### §9 Discussion and outlook (~1 p)
- The licensed next question (BH-005): does recurrence/quasiperiodic
  structure provide robustness unavailable to fixed points? — the
  negative-log ρ and motion-borne findings point directly at it.
- **Cross-disciplinary template paragraph (fenced):** the sustained-by
  test battery as a PROPOSED template for other fields where stable
  emergent structure rides on flux — resting-state functional
  connectivity, metabolic steady states, dynamically-maintained
  ecological/market stability. Explicitly "proposed, not demonstrated;
  we have results only in spin chains."
- **Philosophy: OUT OF SCOPE for this paper** (owner ruling
  2026-08-13). The operationalization of instantiated-vs-maintained
  emergence is queued as a separate survey (AR-022, KB-005) for the
  owner's own interest; at most one citation-free sentence here, or
  nothing.
- Decay-rate-law analysis (pre-approved conditional follow-up).
- The census companion paper (KB-004 §9 item 2).
- What an OL-4 version would require (posed, not claimed).

### Appendices
- A. Numerics: ED, evolvers, seeds/manifests, §6.2 checks (norm drift
  4e-15), compute budget.
- B. Statistics: exact AUC, BCa bootstrap, replication rule,
  exact-value rule; the seed-luck analysis.
- C. **The full amendment log as a table** (Amendments 1–5 + AR-019
  no-change + dispositions, each dated with reason) — the
  transparency artifact; links to the public repo + commit hashes.
- D. Battery details (invariance results incl. the cap-amplification
  and W1-relative instrument notes).
- E. T-B implementation notes (paired realizations, W5 Nyquist
  alignment, switch-off convention).

## 4. Figure/asset inventory (all data already on disk)

| fig | content | source |
|---|---|---|
| 1 | pipeline + class table | schematic (new) |
| 2 | δΦ(t) per class + stationarity table | confirmatory/*.json |
| 3 | witness values + null row + discarded W3 | confirmatory + rerun40 |
| 4 | log ρ bars + replication | confirmatory_summary.json |
| 5 | switch-off jump + family-miss table | summary + ar020 probe |
| 6 | rigidity curve + T-B switch-off | TB_main.json |

## 5. Open decisions for the owner

1. Title (A/B/C or other); 2. venue; 3. author line and
acknowledgements; 4. whether the repo goes public at submission
(Appendix C links need it); 5. whether §5's mechanism section wants the
decay-rate-law AR funded before submission.

## 6. Writing plan

Draft order: §2 → §3–§7 (results, figures generated alongside) → §8–§9
→ §1 last → appendices from the packets. Estimate: 2–3 sessions for a
full draft + 1 for figures polish. SRC-059..063 metadata verification
folds into §1/§5 drafting (30 min; three already scope-checked).
