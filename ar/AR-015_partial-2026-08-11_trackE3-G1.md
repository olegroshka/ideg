# AR-015 partial evidence packet — Track E3 G1 verification (2026-08-11)

```yaml
id: AR-015 (partial 1 of N)
title: Verification of Track E3 G1 scope — SRC-042, SRC-043, SRC-044, SRC-049
mode: VERIFY
parent: HYP-009, RQ-013, SC-006  # partial executed as warm-up remediation for AR-009 per KB-005 §17
priority: P0
inputs: [KB-003 TH-033, KB-003 TH-037, KB-003 §M2 SRC-042..044 + SRC-049]
question: >
  Do the bibliographic records and load-bearing claims of TH-033 (time
  crystals: no-go + driven realization) and TH-037 (MI-graph emergent metric)
  survive primary-record checks, at the level Track E3 (AR-009/AR-010) uses
  them?
deliverable: this packet (claim-by-claim table, exact locations, deltas)
promotion_effect: Track E3 G1 scope cleared (KB-005 §4 G1, per-workstream);
  AR-009 FORMALIZE may cite TH-033/TH-037 as load-bearing
kill_effect: n/a for this partial (failures would have narrowed AR-009)
status: RUNNING (AR-015 overall; this partial DONE 2026-08-11)
```

## 1. Method and confidence notes

Checked 2026-08-11 against arXiv abstract records (metadata) and ar5iv HTML
renderings (content, equation/section locations), plus nature.com/PubMed for
the SRC-044 journal record. Extraction was machine-assisted; equation numbers
are as rendered on ar5iv and should be spot-checked against the published PDFs
if a formal argument ever turns on a specific equation number (the *content*
of each equation was extracted and is recorded below, so drift risk is low).
No claim below rests on memory. TH-034/TH-035 (optional framing for Track E3)
were **not** verified in this partial and remain barred from load-bearing use.

## 2. Claim-by-claim verification table

| # | KB claim | Source | Verified record | Load-bearing content check | Verdict |
|---|---|---|---|---|---|
| 1 | SRC-042 metadata | arXiv:1410.2143 | Watanabe, H.; Oshikawa, M. *Absence of Quantum Time Crystals.* PRL 114, 251603 (2015). DOI 10.1103/PhysRevLett.114.251603 | — | **MATCH** |
| 2 | TH-033 no-go component: "absence of time-crystalline order in ground/equilibrium states" | SRC-042 abstract | — | No-go theorem rules out time crystals "in the ground state or in the canonical ensemble of a general Hamiltonian, which consists of not-too-long-range interactions"; defined via time-dependent correlation functions of order parameters | **CONFIRMED**, with scope condition (not-too-long-range interactions) now recorded |
| 3 | SRC-043 metadata | arXiv:1603.08001 | Else, D. V.; Bauer, B.; Nayak, C. *Floquet Time Crystals.* PRL 117, 090402 (2016). DOI 10.1103/PhysRevLett.117.090402 | — | **MATCH** |
| 4 | TH-033 driven-realization definition + witness template | SRC-043 body | — | TTSB-1: for every short-range-correlated |ψ(t₁)⟩ there is Φ with ⟨Φ⟩(t₁+T) ≠ ⟨Φ⟩(t₁); TTSB-2: Floquet eigenstates not short-range correlated. Signature: subharmonic response at half the drive frequency (period 2T) in ⟨σᶻᵢ⟩; MBL is load-bearing for stability; robustness argued perturbatively + numerically | **CONFIRMED**; witness = subharmonic Fourier response, exactly as CON-034 records |
| 5 | SRC-044 metadata (KB had "Nature 543, 217 (2017)") | arXiv:1609.08684 | Zhang, J.; Hess, P. W.; Kyprianidis, A.; et al. (12 authors, Monroe group). *Observation of a Discrete Time Crystal.* **Nature 543, 217–220 (2017)**. DOI 10.1038/nature21413 | — | **MATCH** (page range completed: 217–220) |
| 6 | TH-033 E4 realization | SRC-044 body | — | 10 ¹⁷¹Yb⁺ trapped ions; period-doubled (2T) response in single-spin magnetizations ⟨σˣᵢ(t)⟩ Fourier spectra; subharmonic peak rigid against drive perturbation ε up to ε_c ≈ 0.11 (their parameters), beyond which symmetry-unbroken phase | **CONFIRMED**; rigidity-curve protocol is directly reusable in T-B |
| 7 | SRC-049 metadata | arXiv:1606.08444 | Cao, C.; Carroll, S. M.; Michalakis, S. *Space from Hilbert Space: Recovering Geometry from Bulk Entanglement.* PRD 95, 024031 (2017). DOI 10.1103/PhysRevD.95.024031 | — | **MATCH** |
| 8 | TH-037 construction (BH-004's Φ) | SRC-049 §III | — | §III.1 redundancy-constrained states: subsystem entropy from pairwise-MI cut function (eq. 9). §III.2 metric from information: graph weights w(p,q) = ℓ·Φ(I(A_p:A_q)/I₀), Φ monotonically decreasing, Φ(1)=0, Φ(x)→∞ as x→0, suggested Φ(x) = −log x (eq. 13); distance = weighted shortest path (eq. 14). §III.3 classical MDS embedding (eqs. 23–25). Stated caveats: factorization posited not derived; embedding unique only up to isometry; Φ-choice distortion; area-law/short-range-entangled regime; "framework is still very incomplete" — no dynamics/time (§VI) | **CONFIRMED**; exact functional now available for AR-009 §2 |

## 3. Corrections and additions to KB-003

1. SRC-044: complete page range 217–220; add DOI 10.1038/nature21413.
2. TH-033: add the no-go's scope condition ("not-too-long-range
   interactions") — present in the abstract, absent from the TH text.
3. SRC-042..044, SRC-049: drop `verify` flag → verified 2026-08-11, this
   packet.
4. Companion sources named inside SRC-044's entry (Choi et al.; Mi et al.)
   remain unverified leads — unchanged status.

## 4. Open gaps

- TH-034 (SRC-045), TH-035 (SRC-046..048), TH-036 (SRC slot reserved),
  TH-038 (SRC-050), TH-012-related SRC-051: still verification-pending;
  owned by AR-015 remainder / AR-016.
- Equation numbers read from ar5iv rendering (see §1) — spot-check against
  published PDFs before any argument that cites an equation *number* rather
  than its content.
