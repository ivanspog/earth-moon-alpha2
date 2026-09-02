# P-004 — The odd-cycle-inflation landscape for χ ≥ 10 collapses to four graphs

**Status: PROVEN** (elementary lemmas + exhaustive enumeration, machine-checked; externally reviewed; not peer-reviewed).
**Revision 2026-08-23:** an external adversarial review (2026-08-23) found a real gap — the original text inferred "χ ≥ 10 needs n ≥ 9k+1" from the lower bound χ ≥ ⌈n/k⌉ alone, i.e. assumed that bound tight. Repaired by the Exactness Lemma below (χ of an odd-cycle inflation is exactly max(ω, ⌈n/k⌉)); conclusion unchanged. Gap and repair recorded.
**Revision 2026-08-24:** a second external adversarial review (2026-08-24, GAP verdict) — three prose-level repairs, theorem untouched: (1) the Consequences claim "the α=2 route is now n = 19 exactly" was unsupported for *arbitrary* α=2 graphs (P-003 gives only n ≤ 19; an independent internal re-review found the same ν-loophole) — qualified below and scope-noted in P-003; (2) "every C₉-or-longer inflation is dead" now explicitly qualified to χ ≥ 10 biplanar *candidates* (C₉ itself is planar); (3) integrality of the gaps gᵢ made explicit in the Exactness Lemma.

## Setup

For an odd cycle C_L (L = 2k+1, L ≥ 5) and positive weights w = (w₁,…,w_L), the inflation C_L[w] replaces bag i by K_{w_i} and joins adjacent bags completely. n = Σw_i. Since bags are cliques and only consecutive bags are adjacent: α(C_L[w]) = k (one vertex from each of k pairwise non-consecutive bags). Cliques are single bags or unions of two adjacent bags (C_L has no bag-triangles for L ≥ 5), so ω = max adjacent sum maxᵢ(w_i + w_{i+1}).

## Exactness Lemma (chromatic number of an odd-cycle inflation)

**χ(C_L[w]) = max(ω, ⌈n/k⌉).**

*Lower bound:* χ ≥ ω always, and χ ≥ n/α = n/k with χ integral.

*Upper bound (explicit circular-arc coloring):* let T = max(ω, ⌈n/k⌉) and identify the colors with Z_T. Choose **integer** gaps g_i ≥ 0 (i = 1..L, cyclically) with Σg_i = kT − n and g_i ≤ T − w_i − w_{i+1}; since the target kT − n and every cap T − w_i − w_{i+1} are nonnegative integers, a greedy integer allocation exists whenever the caps sum to at least the target. This is feasible: kT − n ≥ 0 since T ≥ n/k; each cap is ≥ 0 since T ≥ ω; and the caps sum to LT − 2n = (2k+1)T − 2n ≥ kT − n because (k+1)T ≥ n. Now set a₁ = 0, a_{i+1} = a_i + w_i + g_i, and color bag i with the arc {a_i, a_i+1, …, a_i + w_i − 1} mod T. The total advance is Σ(w_i + g_i) = kT ≡ 0 (mod T), so the assignment closes up consistently around the cycle. Each bag gets w_i ≤ ω ≤ T distinct colors, so bags (cliques) are properly colored. Adjacent bags i, i+1 get disjoint arcs: arc i+1 starts w_i + g_i after arc i's start and ends w_i + g_i + w_{i+1} ≤ T after it, so it lies inside the complement of arc i on the color circle; the wrap constraint i = L vs i = 1 is the cyclic instance of the same inequality. Non-adjacent bags may share colors freely. ∎

Machine check: `verifier/chi_inflation_check.py` verifies, for exhaustive/sampled weight sweeps on C₅–C₁₁, that this arc coloring is a proper coloring in exactly max(ω, ⌈n/k⌉) colors and that an exact SAT computation of χ agrees (log: `population/chi-formula-check.log`).

Consequently **χ ≥ 10 ⟺ max(ω, ⌈n/k⌉) ≥ 10**; and for biplanar candidates ω ≤ 8 (adjacent-sum lemma below), so **χ ≥ 10 ⟺ ⌈n/k⌉ ≥ 10 ⟺ n ≥ 9k+1** — the step the original version left unjustified. (Attribution, per our documented novelty search: the uniform case w ≡ r is Gao–Zhu 1996 / Catlin 1979, as cited in Albertson–Boutin–Gethner 2010 Thm 7; the general case also follows from Niessen–Kind 2000's round-up property for proper circular arc graphs. The lemma is kept here as self-contained scaffolding, NOT claimed as new; it incidentally answers ABG 2010's Open Problem 2 for odd cycles.)

## Lemma (adjacent-sum bound)

If C_L[w] is biplanar then w_i + w_{i+1} ≤ 8 for every i (indices mod L): adjacent bags span a complete subgraph K_{w_i+w_{i+1}}, and K₉ has thickness 3 (Battle–Harary–Kodama 1962 / Tutte 1963).

## Theorem

The only inflations C_{2k+1}[w] with χ ≥ 10 that are not excluded by the lemma or the edge bound |E| ≤ 6n−12 are:

- **k = 3 (C₇):** exactly one — C₇[4,4,4,4,4,4,4] = C₇⊠K₄ (n = 28, 154 edges).
- **k = 2 (C₅):** exactly three dihedral classes at n = 19 — **C₅[3,4,4,4,4]** (99 edges; = KSS 2023's C₅[4,4,4,4,3], proven non-biplanar by KSS 2023), **C₅[3,3,5,3,5]** (98 edges), **C₅[3,4,4,3,5]** (98 edges).
- **k ≥ 4 (C₉, C₁₁, …):** none.

## Proof

Summing the lemma over the L cycle edges: Σᵢ(w_i + w_{i+1}) = 2n ≤ 8L, so n ≤ 4L = 8k+4. But for a biplanar candidate ω ≤ 8, so by the Exactness Lemma χ ≥ 10 needs ⌈n/k⌉ ≥ 10, i.e. n ≥ 9k+1. So 9k+1 ≤ 8k+4, i.e. **k ≤ 3**.

*k = 3:* n must satisfy 28 = 9k+1 ≤ n ≤ 8k+4 = 28, so n = 28 and every adjacent sum is exactly 8. On an odd cycle, w_i + w_{i+1} = 8 for all i forces w constant (= alternation a, 8−a closing on an odd cycle ⟹ a = 8−a), so w ≡ 4: the graph is C₇⊠K₄.

*k = 2:* 19 ≤ n ≤ 20. For n = 20 the same forcing gives w ≡ 4, and C₅[4,4,4,4,4] has 110 > 6·20−12 = 108 edges — excluded. For n = 19, exhaustive enumeration over all positive w with Σw = 19 and adjacent sums ≤ 8, up to the dihedral symmetry of C₅, yields exactly the three classes listed, all within the edge bound (98, 98, 99 ≤ 102). (Enumeration run 2026-08-23, code in session transcript; re-runnable in ~1 s.)

*k ≥ 4:* excluded by k ≤ 3. ∎

## Consequences

- The two once-proposed graphs C₉[5,4⁸] (adjacent sum 9) and C₇[5,3,5,3,5,3,4] (wrap sum 9) both contain K₉: dead, as is **every** C₉-or-longer inflation *as a χ ≥ 10 biplanar candidate* — no need to test any of them ever. (Qualification added 2026-08-24: many C₉₊ inflations are of course biplanar — C₉ itself is planar — they just cannot reach χ ≥ 10 while biplanar.)
- **Two live candidates emerge: C₅[3,3,5,3,5] and C₅[3,4,4,3,5]** — χ ≥ 10 (α = 2, consistent with P-003's n = 19 window), 98 edges vs ceiling 102 (slack 4, double C₇⊠K₄'s), no rotational symmetry (so rotation-invariant-partition obstructions do not even apply), and we find no trace of them in KSS 2023 / Eppstein 2023 / Weaver 2023 / Gethner-2018-as-summarized. (A heuristic partition hunt found nothing; the question is settled by the SAT attack in P-005.)
- With P-003, the α=2 route *as classically posed* (χ ≥ 10 forced by α ≤ 2 alone) is now: n = 19 exactly; and if one further demands the graph be a C₅-inflation, there are just these two open graphs. (Precision, 2026-08-24 — external review and our own re-review independently: for *arbitrary* α=2 biplanar graphs with χ ≥ 10, P-003 caps n at 19 but does not force n = 19; an unstructured n ∈ {14,…,18} graph with ν(complement) ≤ n − 10 would also qualify — uncharted, see P-003's scope note. For inflations the Exactness Lemma closes this loophole.)

## Dependencies

the 6n−12 edge bound, K₉ thickness 3 (classical), and KSS 2023's kill of C₅[3,4,4,4,4]. Enumeration is machine-checked; the rest is elementary and self-contained.

## TODO

- [ ] Further external review.
- [ ] Novelty search: "inflation of C5", "unequal blowup earth-moon", zbMATH/OEIS-adjacent queries — the lemma is easy enough that parts may be folklore; the specific two-candidate list is the claim most likely new.
