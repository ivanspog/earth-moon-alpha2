# P-003 — No biplanar graph with independence number ≤ 2 has n ≥ 20; the α=2 route lives only at n = 19

**Status: PROVEN** (elementary; externally reviewed; not peer-reviewed).

## Statement

**Theorem.** If G is biplanar on n vertices with α(G) ≤ 2, then n ≤ 19.

**Corollary.** The classical "α=2 route" to a 10-chromatic biplanar graph (α ≤ 2 ⟹ χ ≥ ⌈n/2⌉ ≥ 10 requires n ≥ 19) is possible **only at exactly n = 19**.

## Proof

If n ≤ 19 there is nothing to prove; assume n ≥ 20 (so in particular n ≥ 3 and the biplanar edge bound e ≤ 6n−12 applies — domain split added 2026-08-24 after external review).

Let H = complement of G. α(G) ≤ 2 means H is triangle-free.

1. K₉ has thickness 3 (classical: Battle–Harary–Kodama 1962 / Tutte 1963; restated in Eppstein 2023, p.2). So a biplanar G contains no K₉: ω(G) ≤ 8.
2. ω(G) = α(H), so α(H) ≤ 8.
3. In a triangle-free graph every neighbourhood is an independent set, so Δ(H) ≤ α(H) ≤ 8, giving |E(H)| ≤ 8n/2 = 4n.
4. Hence |E(G)| = C(n,2) − |E(H)| ≥ n(n−1)/2 − 4n = n(n−9)/2.
5. Biplanarity gives |E(G)| ≤ 6n − 12 (Euler). So n(n−9)/2 ≤ 6n − 12, i.e. n² − 21n + 24 ≤ 0, i.e. n ≤ (21+√345)/2 < 19.8. ∎

Numeric check (this session): n=19 forces |E(G)| ≥ 95 ≤ 102 ✓ (consistent); n=20 forces ≥ 110 > 108 ✗; n=21 forces ≥ 126 > 114 ✗.

## Scope note (added 2026-08-24, self re-review)

For α(G) ≤ 2, χ(G) = n − ν(H) exactly (H = complement; color classes are
singletons or H-edges). At n = 19, ν(H) ≤ 9 makes χ ≥ 10 **automatic** —
the corollary's "only at n = 19" refers to where α ≤ 2 *forces* χ ≥ 10.
It does NOT exclude α ≤ 2 biplanar graphs with χ ≥ 10 at n ∈ {14,…,18}
(14 = the KSS 2023 floor): those would additionally need ν(H) ≤ n − 10,
which no ledger claim rules out. Inflations are immune (P-004's Exactness
Lemma pins χ = max(ω, ⌈n/k⌉), ≤ 9 there); the residual n ≤ 18 territory
is unstructured only.

## Consequences for the project

- Earlier heuristic-search targets at n = 20, 21 were **provably futile** — corrected here. The α=2 hunt is a single finite question: *does a biplanar graph on 19 vertices with triangle-free complement exist?* (Weaver 2023 and our own heuristic search both failed; KSS-style exhaustion at n=19 with the complement constraint is the natural complete attack.)
- Novelty status (documented search, 2026-08-23): the **sufficiency** direction (19-vertex triangle-free-complement target) is classical — posed in Gethner–Sulanke 2009 p. 215 (via Weaver 2023's quotation; GS-II itself paywalled). The **impossibility for n ≥ 20** (this theorem) was not found in any searched source (zbMATH sweep, arXiv sweep, ABG 2010/2011, GS-I, KSS 2023, Eppstein 2023, Weaver 2023, forward citations). novelty provisional; folklore risk remains (elementary argument; MathSciNet unsearched; GS-II and Gethner 2018 unread at source).

## Dependencies

Theorem and corollary: the 6n−12 biplanar edge bound and the classical fact that K₉ has thickness 3. Nothing else.
The 2026-08-24 scope note additionally cites the KSS 2023 floor (n ≥ 14 for any 10-chromatic biplanar graph) and P-004's Exactness Lemma; both are informative context for the residual-pocket remark, not load-bearing for this claim. (Dependency declaration fixed 2026-08-24 after external review.)
