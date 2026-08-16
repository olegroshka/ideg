# Session log — 2026-08-16 — third audit round: AR-020e + admissibility revision

- **Target:** paper-1 third adversarial-audit response (owner-relayed;
  multi-model, internal — no review-history framing in the paper per the
  standing vocabulary rule).
- **Mode:** ADVERSARIAL (externally seeded) + EXPERIMENT + SYNTHESIZE.

## Outcome summary

1. **All three central criticisms verified, then accepted:** (i) basis-
   relativity of "block coherence" (any stationary σ diagonalizes in some
   valid eigenbasis); (ii) sector-inadmissibility suspicion (XX many-body
   degeneracies all cross-sector; eigh bases sector-mixed — 755/1024
   states); (iii) ρ̄ ≠ infinite-time average for degenerate spectra
   (audit's spot checks reproduced exactly: qp 0.465/0.465; integrable
   Haar 0.878 full-diag vs 0.511 block-dephased).
2. **AR-020e executed** (channels + sector stages; N = 10 complete,
   N = 12 wave running at log time). Headline N = 10 verdicts:
   - T2 = T1 run-by-run (0.0052): cross-sector coherence never used.
   - Commutant impostor: median 69% (max 76%) weight in sectors the
     dynamics never populates; ‖[σ,N_mag]‖ ≈ 0.2.
   - Accessible-sector tier (T3): qp collapses to 0.244 (the
     population-only plateau — forced: one-magnon stationarity ⇒
     diagonal on N nondegenerate levels); integrable sector-honest
     (T3 = 0.030, outside-weight 0.000).
   - Channels: metastable 0.90 → 0.078, integrable 0.86 → 0.47 under
     ρ∞; nondegenerately-supported classes unchanged; corrected
     non-commutation span 38–55% (8% metastable); window ≈ infinite-time
     on all 120 runs (median gaps 0.006–0.13) — round-2's
     one-representative metastable anomaly fully resolved.
   - Validation battery machine-exact; per-sector gradient FD-verified
     (1.4e-4).
3. **Seventh claim-level correction:** discriminator = ADMISSIBILITY.
   Within the stationary algebra the dynamics itself licenses, no
   faithful impostor of the quasiperiodic metric was found. Sufficiency
   wording everywhere (found upper bounds, not necessity).
4. **Paper round-3 revision executed:** abstract, §1 (seven corrections),
   §2.3 two-channel definition, §6 (basis-relativity + sector-control
   passages; T2/T3 price-table rows, N = 12 tripwired), §8, §9
   (admissibility as the open question), App-A (joint basis, per-sector
   gradient, validation battery, trapezoid), App-C rows; two-channel
   fig 5(a); fig5(b) title + fig6 inset fixes; microtype +
   emergencystretch; sparse → top-k relabeling; p2 driven-track
   attribution fix; warm-start description fix. Alleged column
   collisions NOT reproduced (third time; rasterized clean).
5. AR-022 seeds extended (contract/admissibility framing; information-
   veil log archived). AR-023 hardware-pilot design (authored in a
   concurrent owner session) swept into the round-3 progress commit,
   read, and registered in KB-005 §34.

## Delta list (applied, dependency order)

- KB-004: v0.10 → **v0.11** — AR-020e correction note (admissibility);
  BH-004 status unchanged, evidence now three-legged.
- KB-005: v0.17 → **v0.18** — §34; AR-023 registered with its AR-020e
  dependency.
- ar/AR-020e_sector-2026-08-16.md — evidence packet (N = 12 cells
  pending).
- ar/AR-009_spec.md §8 — [PENDING final N = 12 entry, added at wave-2
  reconciliation]
- paper/latex/main.tex — round-3 revision (see §4 above).
- CLAUDE.md — [PENDING update at wave-2 reconciliation]

## ADR candidates

None.

## Open items

- ~~Wave 2 (N = 12)~~ LANDED same session: T2 0.0031 = T1 0.0035
  (28% of parameters); T3 0.256 (9/20); outside-weight median 83%,
  max 100%; channels replicate. Slotted, packet/spec/CLAUDE.md
  updated, rebuilt below.
- **AR-023 dependency:** add a T3 comparator-population export
  (p*, hashes, recheck) to ar020e for the hardware pilot's Gate L0.
- Owner proof pass of round-3 build; then paper-v1 retag; endorsement
  outreach; arXiv/Quantum.
- Parked: AR-022 execution; BH-005; AR-015 census; SRC-036..058 backlog.
