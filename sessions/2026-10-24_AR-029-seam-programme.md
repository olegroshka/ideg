# Session 2026-10-24 — theory-stream review, seam programme opened, AR-029 gate A1 executed

- target: AR-029 (new): gate for direction A of the "seam programme" (owner ruling, see below); preceded by a conceptual
  review of the closed theory stream and of the Argon drafts (brainstorm, recorded in AR-029 §6–§7 and below)
- mode: SYNTHESIZE (review) → FORMALIZE + EXPERIMENT + VERIFY (gate)
- substrate versions at load: KB-001 v0.3, KB-002 v0.2, KB-003 v0.8, KB-004 v0.11, KB-005 v0.18
- substrate versions at close: unchanged (deltas queued — parallel-stream rule)
- infrastructure: anaconda python (numpy 2.1.3, scipy 1.15.3, sympy 1.13.3); Chrome through the owner's session (Springer
  Nature Link had full-text access to Johnstone–Lalley 1984 without a sign-in; ScienceDirect not signed in)

## Owner rulings recorded (verbatim)

1. Opening frame: "review this again see if we missed interesting research opportunities in this specific area … step
   aside on run some high level conceptual brainstorming on this and decide together how we explore what outcomes to
   target"; diagnosis of the first pass: "the main problem with the approach was that agent took too literally statements
   from the initial md file and run them".
2. Placement: "I think I put this in the wron repo I was thinking more about coig … but still a parallel seam so I dont see
   any issues here" → stream stays in ideg; handover to coig at the park step.
3. Programme: "maybe we do the seam program we discussed here A, B maybe C.. then park and based on result formulate
   coig-2 research?" → adopted as the sequence of record (AR-029 §7).
4. Access: "ok open the browser i will login if need to.. bt as ou student I have access to their library and partners as
   well" → browser used for Johnstone–Lalley (read, not downloaded) and the ScienceDirect search; no login was needed; no
   credentials entered.

## Outcome

1. **Review (brainstorm of record).** The 2026-10-23 closure stands on the gravitational layer. Two closures were too quick:
   AR-026 tried only radial transfers and Faber–Krahn (the non-radial exhaustion / flux test was never tried); AR-026 §4
   dismissed the curvature route although Wei–Wylie / Munteanu–Wang comparison geometry for Ric_Φ ≥ 0 with bounded ∇Φ is
   exactly Brown's bounded-drift setting (citations from memory, verify). Opportunity map: A non-radial admissibility
   (examples both ways; theorem pending), B Gauss-equation reading of Komaki's curvature terms, C log-concave class via
   Bakry–Émery comparison, D curvature in dynamic prediction (risky), E dictionary alone (no novelty). COIG-2 relevance
   (checked against coig2/substrate KB-201..205 and the originating note, which contain no shrinkage/Bayes vocabulary):
   the parabolicity type of the accessible manifold is a candidate 𝓘(G_c) with a theorem attached (Komaki Thms 1–3),
   strictly finer than identifiable rank (flat R² vs H², both rank 2), and its monotonicity along the Blackwell preorder is
   the KC-201 test; all of it sits on the inference branch; "admissible" needs a collision rule in KB-202.
2. **Argon drafts assessed** (AR-029 §6): Theorem 5 stands; Theorem 6 reversed (parabolic, admissible); Prop 7 plausible
   (citations to verify); Prop 3 is a definition, not a result; tags violate the wording rule; math-note.tex not of record.
3. **Gate A1 executed** (AR-029 §0–§3): Lemma K11 (Thomson bound along a non-spherical exhaustion) proves the ring weight
   parabolic; numerics of record (mesh 3.18; f̄ flat at 0.0201; ray integrals 1.2–3.2 per block; Thomson term flat at
   0.0466 for α = 2, doubling per block for α = 3; Poincaré quotient ∝ ρ^{α−1}; cylinder control bounded; Theorem 5's
   Q ∝ r^{α−2}). Brown's undecided zone is two-sided (G0 example inadmissible; wall example admissible).
4. **Johnstone–Lalley 1984 read in full** (pp. 29–45): Thm 1.1, Prop 1.2, Lemma 3.1, the construction (3.7)–(3.15); the G0
   example is an instance of their phenomenon, not of their construction (wording fixed); their §1/§4 is the earliest
   explicit Dirichlet-form statement of Brown found so far (AR-027 chain updated).
5. **Brown–Hwang 1982 not obtained**: only Volume 2 of the Purdue III proceedings is on ScienceDirect. Owner item (OU
   library).
6. **Verdict for A:** examples note GO; paper-grade theorem PENDING A2 (scattered construction), one session, kill rule in
   AR-029 §7.

## Delta list (QUEUED — parallel-stream rule; apply at reconciliation in dependency order)

- v2 §0: (none) → K10 (Theorem 5, verified numerically, proof chain citations verify), K11 (wall example admissible,
  Lemma K11) — reason: AR-029 §0–§2.
- v2 §8 Q1′ / K8 consequence: "non-product case OPEN" → "inclusion FAILS in m ≥ 3 (Theorem 5); the volume route is not
  subsumed; a Brown-silent D+P transient example is pending A2" — reason: AR-029 §0 item 2.
- v2 §9: "nothing on the table" → "examples note GO; theorem pending A2" — reason: AR-029 §0 item 5.
- v2 references: SRC-T45 Johnstone–Lalley → READ IN FULL; + SRC-T48..T57 as listed in AR-029 §8 (verify).
- AR-027 §2 chain: + Johnstone–Lalley 1984 §1/§4 (Dirichlet-form reading, cites Fukushima 1980) — reason: AR-029 §4.
- AR-028 G0 §6: "non-product case OPEN, no candidate" → "CLOSED by Theorem 5: the inclusion fails in m ≥ 3" — reason:
  AR-029 §0 item 2.
- articles/theory/README.md: status REOPENED; rows added — APPLIED (stream file).
- KB-005 §6: + AR-029 gate DONE; AR-029 A2/A3, AR-030 (B), AR-031 (C optional) PROPOSED; park + handover rule (AR-029 §7).
- KB-002 (coig side, at handover): collision rule "admissible (COIG-2 comparator axes) ≠ admissible (Stein/Brown)".
- CLAUDE.md "Current state": stream bullet to be updated at the next currency pass (not touched this session).

## ADR candidates raised

None. INT-001 untouched; the seam programme is static information geometry with an external sample clock and makes no
IDEG dynamical claim.

## Open items

- A2 (next session): the scattered co-dimension-two construction; Hess log f* ≥ −I check for every example; Thomson's
  principle continuum citation; HKM / Kilpeläinen 1994 citations for Theorem 5.
- Owner: Brown & Hwang 1982 (Purdue III, Vol. 1, pp. 205–230 — verify) from the OU library; Kasahara 1975 / Kotani–Watanabe
  1982 primary texts for Prop 7.
- Memory saved: feedback note that after lint the owner wants a conceptual map, not statement-by-statement execution.
- Browser tabs closed at session end; nothing downloaded; nothing committed; the eleven other-session files untouched.

## Self-corrections (SC-005)

- Check script: spurious 1/ρ in the weighted-area formula, caught from the k-dependence before any number was recorded;
  corrected and rerun (AR-029 §9).
- One wrong ISBN guess for Purdue III Volume 1 on ScienceDirect (page not found); resolved by the book search.
