# Session log — 2026-08-15 — external review round 2: AR-020d + second major revision

- **Target:** paper-1 second review response (owner-relayed review, verdict: major
  revision) — degeneracy criticism, complexity-language criticism, finite-window
  criticism, textual errors, references.
- **Mode:** ADVERSARIAL (externally seeded) + EXPERIMENT + SYNTHESIZE.

## Outcome summary

1. **Reviewer's degeneracy criticism confirmed decisive.** Exact counts
   reproduced (XX N = 10: 243 distinct energies in dim 1024, largest block 32,
   Σ|B|² = 7776; N = 12: 729/4096/64/46656). The AR-020c "unrestricted" search
   was unrestricted only within the diagonal family.
2. **AR-020d executed** (`scripts/ar020d_stationary_suite.py`, five stages;
   `results/AR-010/ar020d_*.json`):
   - **blocks** (full commutant): quasiperiodic N = 10 **20/20, median 0.0052**
     (best 1e-9); integrable 20/20, 0.0077. N = 12 launched (running at log
     time). The designed containment check (block ⊇ diagonal) caught an
     objective sign error pre-record (fix + relaunch) and flags one integrable
     run of optimizer shortfall (diagonal 1e-8 vs block 0.02) — reported.
   - **gge**: integrable 20/20 (0.14/0.17 at N = 10/12); quasiperiodic 0/20
     both sizes (0.63/0.47).
   - **kcurve**: smooth-f(H) plateau ~0.32 from K = 2 to 96.
   - **sparse**: top-k ≤ 32 scrapes 0.23–0.25; k > 32 optimizer regression.
   - **windowgap**: window-averaged state ≈ diagonal ensemble for relaxing
     classes (0.003–0.23); reviewer's qp spot-check 0.012 reproduced exactly;
     metastable N = 10 slow-doublet exception (0.84; 0.02 at N = 12).
3. **Corrected claim of record (sixth major self-correction, second externally
   triggered): resource split.** Every class has a near-exact stationary
   impostor; classes differ in the stationary resource required (thermal
   window / GGE charges / degenerate-block coherence). Discriminator renamed
   **smooth-in-energy representation gap** (qp 0.32 vs 0.005; chaotic 0.04 vs
   0.01).
4. **Paper second major revision executed** (`paper/latex/main.tex`):
   physics-first abstract; five-stage search narrative; price table
   (`tab:price`, with a compile-tripwire token for the pending N = 12 block
   number); window-gap paragraph; §2.3 infinite-time/degeneracy
   qualifications; §6 resource split; §8 search-scope correction; §9
   representation-gap open question; App. A GGE/block/sparse/window specs incl.
   the optimizer-shortfall honesty note; App. C three new rows; "matched in
   0 of 80" reversal fixed; fig5 panel (b) retitled and regenerated.
   References 12 → 17 (SRC-065..068 + existing).
5. Review's page-10/12 gutter-collision claim again NOT reproduced by
   independent rasterization (second extraction artifact); no action.

## Delta list (applied this session, dependency order)

- KB-003 §sources/changelog: v0.7 → **v0.8** — SRC-065 (Rigol/Dunjko/Olshanii,
  Nature 452, 854 (2008)), SRC-066 (D'Alessio et al., Adv. Phys. 65, 239
  (2016)), SRC-067 (Vidmar–Rigol, J. Stat. Mech. 064007 (2016)), SRC-068
  (Abanin et al., RMP 91, 021001 (2019)) — added + verified (paper-1 round-2
  bibliography gate).
- KB-004 BH-004: v0.8 → **v0.9** — dated v0.9 correction note (AR-020d resource
  split; representation-gap rename; status unchanged).
- KB-005: v0.15 → **v0.16** — §32 changelog (this session).
- ar/AR-009_spec.md §8: consolidated dated AR-020c/d comparator-scope entry
  (no preregistered threshold changed).
- CLAUDE.md current-state block refreshed.

## ADR candidates

None. (No intent reinterpretation; comparator scope extensions are
instrument-level corrections logged in spec §8.)

## Open items

- **N = 12 block search (task biy1670b4)**: slot median/count into `tab:price`
  (replaces the `\BLOCKSNTWELVE` tripwire), rebuild, commit, send PDF.
- Owner proof pass of revision 2; then repo tag `paper-v1`, endorsement
  outreach (parked in `paper/ENDORSEMENT_*.md`), arXiv/Quantum submission.
- AR-022 philosophy survey (parked, not for the paper); BH-005 sequencing;
  AR-015 census; SRC-036..058 verification backlog.
- Possible referee follow-up: block-coherent search at N = 12 uses one warm
  start; if a referee asks for multi-start parity with the diagonal stage,
  rerun with 5 starts (cheap at N = 10, expensive at N = 12).
