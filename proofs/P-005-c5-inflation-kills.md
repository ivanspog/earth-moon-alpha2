# P-005 — C₅[3,3,5,3,5] and C₅[3,4,4,3,5] are not biplanar; no odd-cycle inflation except possibly C₇⊠K₄ is 10-chromatic and biplanar

**Status: PROVEN** (machine UNSAT, single implementation, both directions of the pipeline control-validated; hardening owed before external claim — see TODO).
**Date:** 2026-08-23/24. **Method:** SAT attack with a certificate-validating planarity propagator (details below).

## Statement

**Theorem A.** C₅[3,3,5,3,5] (19 vertices, 98 edges) is not biplanar.

**Theorem B.** C₅[3,4,4,3,5] (19 vertices, 98 edges) is not biplanar.

**Corollary (with P-003, P-004, and KSS 2023).** Among ALL inflations C_L[w] of ALL odd cycles L ≥ 5, the only graph with χ ≥ 10 whose biplanarity remains open is **C₇⊠K₄ = C₇[4,4,4,4,4,4,4]**. Every other member of this infinite family is excluded: by the K₉/adjacent-sum lemma or the edge bound (P-004's landscape collapse, using the Exactness Lemma χ = max(ω, ⌈n/k⌉), classical, attributed in P-004), by KSS 2023 (C₅[3,4,4,4,4]), or by Theorems A/B. In particular the α=2 route to a 10-chromatic biplanar graph (forced by α alone only at n = 19, P-003) has **no structured (inflation) instance**. What remains on the α=2 side is unstructured only: the classical 19-vertex triangle-free-complement target (GS-II 2009 p.215, where Weaver 2023 and our heuristic search both failed), plus — see the 2026-08-24 scope note in P-003 — the never-charted n ∈ {14,…,18} pocket where an α=2 biplanar graph would need ν(complement) ≤ n − 10 to reach χ ≥ 10.

## Method

Complete SAT decision, not sampling: one Boolean per edge (part1/part2); per-part cardinality ≤ 3n−6; pre-seeded split clauses for every K₅ (209–210) and every K₃,₃ (1816–1876) subgraph; lex-leader symmetry breaking over 15 automorphism generators (within-bag transpositions + weight-preserving dihedral maps) + part-swap unit; and a **lazy planarity propagator** (IPASIR-UP, CaDiCaL 1.9.5 via pysat) that tests each part's planarity on partial assignments and hands the solver the falsified Kuratowski clause (networkx left-right certificate) on failure. Any SAT model would be independently re-verified (disjointness, exact union, planarity of both parts). Code: `verifier/biplanar_sat_prop.py`.

Runs (Apple Silicon, pure Python propagator):
| graph | verdict | wall | planarity checks | conflict clauses |
|---|---|---|---|---|
| C₅[3,3,5,3,5] | UNSAT | 73 min | 4.35M | ~493k |
| C₅[3,4,4,3,5] | UNSAT | 160 min | 9.6M+ | ~840k |

Logs: `population/satprop-c5-33535.log`, `population/satprop-c5-34435.log`.

## Controls (all pre-registered as mandatory before trusting UNSAT)

1. **Positive, known instance:** Sulanke's C₅∨K₆ — partition found and verified (also by the CEGAR variant). PASSED.
2. **Positive, symmetric machinery active:** C₅[2,2,2,2,2], C₅[3,3,3,3,3] — partitions found and verified with lex symmetry breaking on. PASSED.
3. **Negative, independent replication:** C₅[3,4,4,4,4] → UNSAT in 107 min, exactly reproducing Kirchweger–Scheucher–Szeider 2023 (they report the exclusion "within 12 hours" on an SMS setup retrofitted from graph enumeration — not a like-for-like comparison). PASSED.
4. **Positive, planted at target density:** 3 random 19-vertex unions of two edge-disjoint planar graphs (99–101 edges), split guaranteed by construction — all SAT instantly with verified partitions (core-encoding completeness; no symmetry constraints active there). PASSED.
5. **Ambiguous by design:** shrunk sibling C₅[3,3,5,3,4] (n=18, 88 edges, ceiling 2·(3n−6)=96) → UNSAT in 80 min. (An earlier draft said "93 edges"; the solver logs and the formula Σ C(wᵢ,2) + Σ wᵢwᵢ₊₁ = 25 + 63 both give 88 — corrected 2026-08-24.) Ground truth was not known in advance, so this is not a control result; recorded as a candidate bonus fact pending the lex-off audit below.

## Soundness argument

Every clause given to the solver is implied by biplanarity: cardinality is Euler's bound; K₅/K₃,₃/Kuratowski split clauses forbid a monochromatic non-planar subgraph; lex constraints only exclude assignments whose orbit under Aut(G) × (part swap) contains a lex-smaller solution. SAT answers are certified externally. The residual risk is a bug in the hand-written lex encoding or propagator trail bookkeeping producing a false UNSAT; controls 2–4 bound this, and the audit below targets it directly.

## TODO (hardening before any external claim)

- [ ] **Certificate-validated re-runs (required by external review, 2026-08-24).** The review validated the entire encoding surface (cert checker, cardinality, lex+part-swap, pre-seeds, propagator desync-harmlessness) but correctly ruled that the two reported UNSAT runs predate `is_kuratowski_subdivision` and that queued computations are not evidence: the emitted clauses of the original 73/160-min runs were never independently validated. The lex-off cube audits below run the ENTIRE decision again with the certificate check active, so completing them discharges this item; until then Theorems A/B rest on the original runs (controls both directions, KSS replication) minus per-clause certificate validation. The reviewer also noted: historical-run provenance is log-header-level only. Strengthened 2026-08-24 by git archaeology: the graph constructor `verifier/c5_inflation_attack.py` has a SINGLE commit in its entire history (0cbeeea, pre-dating the runs) — `git diff` against the run-recording commit (2651bc7) is empty — so the edge sets the original runs decided are byte-identical to the ones `verify_inflation_graph.py` validated against the definition today; the solver's only post-run changes are today's certificate checker + cube hook (+59 lines, both committed after review). The replication kit's SHA-256 edge lists fix fingerprinting going forward.
- [ ] **Lex-off audit:** rerun C₅[3,3,5,3,4] (running now, chained solo) and then both theorems' graphs with `--no-sym` (no hand-written symmetry constraints; cube-and-conquer via `verifier/run_cube_audit.py`, chained behind the sibling by `verifier/audit_chain_cubes.sh`). UNSAT surviving with the riskiest component removed closes the over-pruning bug class — and, with the certificate check now wired in, simultaneously discharges the item above.
- [ ] Independent replication with KSS's open-source SMS (needs a machine with a working C++ toolchain; this machine's CLT is broken).
- [ ] Further external adversarial review.
- [ ] Novelty: our documented search already covers the territory (these graphs appear nowhere; enumeration absent); refresh the forward-citation check at write-up time.

## Dependencies

P-003 (α≤2 ⟹ n≤19), P-004 (landscape collapse; Exactness Lemma cited to Gao–Zhu 1996 / Niessen–Kind 2000), the 6n−12 edge bound, K₉ thickness 3 (classical), KSS 2023's kill of C₅[3,4,4,4,4], and our independent replication of that kill (log included).
