# P-006 — The α=2 pocket collapses: empty for n ∈ {14,…,17}, rigid at n = 18

**Status:** PROVEN (hand-proved lemmas + machine-checked finite shape sweep; externally reviewed: SOUND; not peer-reviewed)
**Claim:** this file resolves n = 14–17 and reduces n = 18
**Date:** 2026-08-29
**Depends on:** the classical fact that K₉ has thickness 3 (Battle–Harary–Kodama 1962 / Tutte 1963), the
classical Gallai–Edmonds structure theorem (Gallai 1964; Edmonds 1965; see Lovász–Plummer,
*Matching Theory*, §3.2), classical Ramsey values R(3,3)=6, R(3,4)=9, R(3,5)=14
(Greenwood–Gleason 1955; standard reference: Radziszowski, *Small Ramsey Numbers*, DS1).
Context (not used in any proof): P-003; KSS 2023.
**Machine artifacts:** `verifier/alpha2_pocket_sweep.py` (finite case sweep; pure stdlib, no
solver), output banked at `population/alpha2-pocket-sweep.log` with git hash + script SHA-256.
Reproduce: `.venv/bin/python verifier/alpha2_pocket_sweep.py`.

---

## 0. Results

Throughout, G is a graph on n vertices with **α(G) ≤ 2** and **χ(G) ≥ 10**, and H = Ḡ.
"Biplanar-necessary conditions" means the two classical necessary conditions for
biplanarity used here: **e(G) ≤ 6n − 12** and **K₉ ⊄ G** (Battle–Harary–Kodama 1962 / Tutte 1963).

**Theorem 1 (pocket emptiness).** For n ∈ {14, 15, 16, 17} there is NO graph G on n
vertices with α(G) ≤ 2, χ(G) ≥ 10 satisfying the biplanar-necessary conditions. In
particular no biplanar graph with α ≤ 2 and χ ≥ 10 exists on 14–17 vertices.

**Theorem 2 (n = 18 rigidity).** If G is a biplanar graph on 18 vertices with α(G) ≤ 2 and
χ(G) ≥ 10, then H = Ḡ = K₁ ⊔ F where F is a **factor-critical triangle-free graph on 17
vertices with α(F) = 7, Δ(F) ≤ 7, 57 ≤ e(F) ≤ 59** (so ν(F) = 8, χ(G) = 10 exactly, and
G = K₁ ∨ F̄ with e(G) = 153 − e(F) ∈ {94, 95, 96}). Moreover if e(F) = 57 then e(G) = 96 =
6·18 − 12, so in any biplanar partition of G **both parts are planar triangulations** (48
edges each).

**Converse half of Theorem 2.** For ANY triangle-free graph F on 17 vertices, G = K₁ ∨ F̄
has α(G) ≤ 2 and χ(G) = 18 − ν(F) ≥ 10 (since ν(F) ≤ 8 on 17 vertices). So the n = 18
pocket question is *exactly*: **(Q18) is K₁ ∨ F̄ biplanar for some triangle-free F on 17
vertices?** — and Theorem 2 says any witness F must lie in the rigid window above.

**Corollary (α=2 route reduction).** Combining with KSS 2023 (no 10-chromatic biplanar graph
on n ≤ 13) and P-003 (biplanar + α ≤ 2 ⟹ n ≤ 19; at n = 19, χ ≥ 10 is automatic): the
entire α ≤ 2 route to a 10-chromatic biplanar graph is equivalent to the disjunction of
exactly two finite questions:
- **(Q18)** ∃ factor-critical triangle-free F on 17 vertices, α(F) = 7, 57 ≤ e(F) ≤ 59,
  with K₁ ∨ F̄ biplanar;
- **(Q19)** ∃ biplanar G on 19 vertices with α(G) ≤ 2 (the P-003 endpoint).

---

## 1. Notation and the exact identity

H = Ḡ. α(G) ≤ 2 ⟺ H is triangle-free. All structure work happens in H.

**Lemma 0 (identity; classical, also used in P-003).** If α(G) ≤ 2 then
χ(G) = n − ν(H).
*Proof.* Color classes of G are independent sets, hence of size ≤ 2; a class of size 2 is
an edge of H. A proper coloring with k colors is thus a partition of V into k parts each a
singleton or an H-edge, so k = n − (number of 2-classes) ≥ n − ν(H); conversely any
maximum matching of H yields a proper coloring with n − ν(H) classes. ∎

So **χ(G) ≥ 10 ⟺ ν(H) ≤ n − 10 ⟺ def(H) := n − 2ν(H) ≥ 20 − n.**

**Lemma 1 (α cap).** Under the K₉-necessary condition, α(H) = ω(G) ≤ 8.
*Proof.* An independent set of H is a clique of G; K₉ ⊄ G since K₉ has thickness 3 (classical). ∎

**Lemma 2 (edge floor).** Under the edge-necessary condition,
e(H) ≥ E_min(n) := C(n,2) − (6n − 12).
Values: E_min(14..18) = 19, 27, 36, 46, 57. ∎

**Lemma 3 (degree cap; folklore).** In a triangle-free graph, N(v) is independent, so for
any induced subgraph P ∋ v: deg_P(v) ≤ α(P). Hence e(P) ≤ ⌊|P|·α(P)/2⌋, and globally
Δ(H) ≤ α(H) ≤ 8. ∎

**Lemma 4 (matching vs independence; folklore).** In any graph, α ≤ n − ν.
*Proof.* Fix a maximum matching M and an independent set S. Each of the ν edges of M
contains at most one vertex of S, and the n − 2ν unmatched vertices contribute at most
themselves, so |S| ≤ ν + (n − 2ν) = n − ν. ∎ *(Phrasing repaired 2026-08-29 per the
single-shot review, attack 4 — the earlier one-liner omitted the unmatched vertices.)*

## 2. Gallai–Edmonds, specialised to triangle-free H

Let D = D(H) be the set of vertices missed by at least one maximum matching, A = N(D)∖D,
C = V∖(D∪A). The Gallai–Edmonds structure theorem gives (all classical):

- (GE-a) every component of H[D] is factor-critical;
- (GE-b) def(H) = c(H[D]) − |A|, where c(H[D]) = number of components of H[D];
- (GE-c) every maximum matching matches C perfectly (so |C| is even, ν(H[C]) = |C|/2);
- (GE-d) by definition of A: there are no D–C edges, and no edges between distinct
  components of H[D].

Write the **shape** of H as (s, t, (o₁,…,o_t), a, c): s = number of singleton components
of H[D]; t = number of larger components, of orders oᵢ; a = |A|; c = |C|.

**Lemma 5 (component orders).** Each non-singleton component of H[D] has odd order ≥ 5.
*Proof.* Factor-critical graphs have odd order (remove a vertex: perfect matching) and are
connected. Order 3: for every vertex v, the other two must be adjacent (they form the
perfect matching of H−v), so all three pairs are adjacent — K₃, a triangle. Excluded. ∎

**Lemma 6 (order 5 is C₅).** The unique triangle-free factor-critical graph on 5 vertices
is C₅ (α = 2, e = 5).
*Proof.* A factor-critical graph on ≥ 3 vertices is non-bipartite: if the parts were X, Y
with |X| > |Y|, deleting y ∈ Y leaves no perfect matching (Hall on X). Non-bipartite and
triangle-free on 5 vertices ⟹ shortest odd cycle has length 5, i.e., a spanning C₅. Any
chord of a 5-cycle closes a triangle, so no further edges. ∎

**Lemma 7 (independence cap for factor-critical graphs).** A factor-critical graph F on
o ≥ 3 vertices has α(F) ≤ (o − 1)/2.
*Proof.* Suppose S independent, |S| = (o+1)/2. Then |V∖S| = (o−1)/2 ≥ 1; pick u ∉ S. F − u
has a perfect matching M of (o−1)/2 edges, and every vertex of S is covered by M (u ∉ S).
Each M-edge contains at most one S-vertex (S independent), so |S| ≤ (o−1)/2 —
contradiction. ∎

**Lemma 8 (Ramsey floors).** A triangle-free graph on N vertices has α ≥ k whenever
N ≥ R(3,k): α ≥ 2 for N ≥ 3, α ≥ 3 for N ≥ 6, α ≥ 4 for N ≥ 9, α ≥ 5 for N ≥ 14.
(Only these four values are load-bearing for n ≤ 18.) Small-argument conventions used by
the sweep's `ramsey_lb`, stated explicitly per the single-shot review (attack 8):
ramsey_lb(0) = 0, ramsey_lb(1) = ramsey_lb(2) = 1, ramsey_lb(3..5) = 2,
ramsey_lb(6..8) = 3, ramsey_lb(9..13) = 4, ramsey_lb(14..17) = 5 — each elementary
(a nonempty graph has α ≥ 1; a triangle-free graph on ≥ 3 vertices is not complete). ∎

**Lemma 9 (α adds across parts).** α(H) ≥ s + Σᵢ α(Fᵢ) + α(H[C]), where Fᵢ are the
non-singleton D-components.
*Proof.* Singleton D-vertices, maximum independent sets of each Fᵢ, and a maximum
independent set of H[C] span no mutual edges by (GE-d), so their union is independent. ∎

**Lemma 10 (edge location).** Every edge of H lies inside a D-component, or is incident to
A, or lies inside C (GE-d). Hence, using Lemma 3 for parts and Δ(H) ≤ 8 for A:
e(H) ≤ Σᵢ ⌊oᵢ·α(Fᵢ)/2⌋ + 8a + ⌊c·α(H[C])/2⌋,
with the order-5 refinement e(C₅) = 5 (Lemma 6), and α(H[C]) ≤ c/2 (Lemma 4 + GE-c). ∎

## 3. The shape relaxation and its exhaustive check

Collecting Lemmas 0–10, any H arising from a pocket witness at n has a shape
(s, t, (oᵢ), a, c) satisfying the **four master constraints**:

1. **Deficiency:** s + t − a ≥ 20 − n  (Lemma 0 + GE-b).
2. **α-budget:** there exist integers αᵢ ∈ [ramsey_lb(oᵢ), (oᵢ−1)/2] (with o=5 forcing
   αᵢ=2) and α_C ∈ [ramsey_lb(c), c/2] such that s + Σαᵢ + α_C ≤ 8
   (Lemmas 1, 6, 7, 8, 9 + GE-c; the αᵢ, α_C are the true independence numbers of the parts).
3. **Vertex count:** s + Σoᵢ + a + c = n, c even, each oᵢ odd ≥ 5 (Lemma 5, GE-c).
4. **Edge window:** for the same (αᵢ, α_C): Σ e_max(oᵢ, αᵢ) + 8a + ⌊c·α_C/2⌋ ≥ E_min(n),
   where e_max(5,2) = 5 and e_max(o,α) = ⌊oα/2⌋ (Lemmas 2, 3, 10).

The ranges are finite: s ≤ 8 and t ≤ 4 (constraint 2 with αᵢ ≥ 2), a ≤ s + t − (20−n)
(constraint 1), oᵢ ≤ n. **Soundness:** every actual pocket witness H at n induces a shape
and a choice of (αᵢ, α_C) — its true part-independence numbers — passing all four checks;
therefore, if NO shape at n passes, the pocket at n is empty.

`verifier/alpha2_pocket_sweep.py` enumerates every shape and every admissible (αᵢ, α_C)
assignment. Output (banked, `population/alpha2-pocket-sweep.log`):

```
n=14: e(H) >= 19 required; 14 shapes checked;  0 survivor(s)
n=15: e(H) >= 27 required; 28 shapes checked;  0 survivor(s)
n=16: e(H) >= 36 required; 51 shapes checked;  0 survivor(s)
n=17: e(H) >= 46 required; 88 shapes checked;  0 survivor(s)
n=18: e(H) >= 57 required; 139 shapes checked; 1 survivor(s)
    SURVIVOR s=1 t=1 a=0 c=0 orders=[17] alphas=[7] alpha_C=0 emax=59
```

This proves Theorem 1 and the forcing part of Theorem 2's shape. The remainder of
Theorem 2 is finished by hand in §5.

## 4. Hand-verified kill patterns (illustrative; completeness is the sweep's job)

The 320 shapes die by four recurring mechanisms. Worked examples:

- **Vertex count / parity.** n=15, t=3: budget forces s ≤ 2 and all three components C₅
  (Σαᵢ ≥ 6), but s + 15 > 15 already. Or: c odd is impossible (GE-c).
- **Ramsey vs α-budget.** n=14, s=5, a=0, one component of order 9: budget needs
  α(F₁) ≤ 8 − 5 = 3, but R(3,4) = 9 forces α(F₁) ≥ 4.
- **Edge starvation (the main kill).** n=17, s=2, t=1, a=0, c=0, o₁ = 15: budget allows
  α₁ ≤ 6, so e(H) = e(F₁) ≤ ⌊15·6/2⌋ = 45 < 46 = E_min(17). One edge short — the pocket
  at 17 dies by exactly one edge at its densest shape.
- **Deficiency vs |A|.** n=14, t=0, c=0: then s + a = 14 with s ≥ 6 + a, giving s ≥ 10 —
  but s ≤ α(H) ≤ 8.

Full hand case analyses of n = 14 and n = 15 (done first, before the sweep existed)
agreed with the machine on every branch; they are superseded by the sweep and not
duplicated here.

## 5. Finishing Theorem 2 (n = 18)

The sweep leaves only (s,t,a,c) = (1,1,0,0) with o₁ = 17. So H = K₁ ⊔ F, F a
factor-critical triangle-free graph on 17 vertices, and:

- **a = 0, c = 0, s = 1:** the singleton D-vertex has neighbours only in A (GE-d), which
  is empty — it is isolated in H, so G = K₁ ∨ F̄ (the cone over F̄).
- **ν(F) = 8** (factor-critical on 17), so ν(H) = 8 and χ(G) = 18 − 8 = 10 exactly.
- **e(F) ≥ 57:** e(H) = e(F) (all other parts empty), Lemma 2.
- **α(F) = 7:** budget gives α(F) ≤ 8 − s = 7; and e(F) ≥ 57 forces a vertex of degree
  ≥ ⌈2·57/17⌉ = 7, whose neighbourhood is independent (Lemma 3), so α(F) ≥ 7.
- **Δ(F) ≤ 7** (Lemma 3 inside F), hence e(F) ≤ ⌊17·7/2⌋ = 59 (17·7 is odd, so 7-regular
  is impossible and 59 needs degree sequence 7¹⁶6¹).
- **e(G) = 153 − e(F) ∈ {94,95,96}.** At e(F) = 57, e(G) = 96 = 6·18−12: any biplanar
  partition has |E₁| + |E₂| = 96 with |Eᵢ| ≤ 48, forcing |E₁| = |E₂| = 48 = 3·18−6, and a
  planar graph on 18 vertices with exactly 48 edges is a maximal planar triangulation. ∎

**What is NOT proven:** existence or non-existence of such an F, and biplanarity of
K₁ ∨ F̄ for any candidate — that is (Q18), now the entire content of the pocket. Status of
After this file: n = 14–17 EMPTY (PROVEN, externally reviewed); n = 18 OPEN, reduced to
(Q18).

## 6. Notes for P2 / novelty

These queries emerged from the reduction itself and were logged before being run
(recorded as additions to a pre-registered query list):

- F is precisely a **(3,8)-Ramsey graph on 17 vertices** (triangle-free, no independent
  8-set) with ≥ 57 edges. The max edge count of (3,8;17)-graphs is a Ramsey–Turán-type
  quantity; check Radziszowski DS1 tables and McKay's Ramsey-graph archive before any
  enumeration. If max < 57, (Q18) dies by literature/data alone.
- Near-regularity: 2e(F) ≥ 114 with Δ ≤ 7 means degree sequence within 5 of 7-regular
  (e.g. 7¹²6⁵ at e = 57). 7-regular triangle-free graphs on 17 vertices do not exist
  (parity); circulant triangle-free candidates (e.g. C₁₇({±6,±7,±8}), 6-regular, e = 51)
  fall short — the survivors, if any, are non-regular and close to extremal.
- Factor-criticality is FORCED, so a P2 enumeration may restrict to factor-critical F
  (sound), or search the α ≤ 7 window without it (superset, also sound).

## Addendum 2026-08-29 (same day, post-novelty-run): window tightened to e(F) ∈ {57, 58}

The pre-registered novelty search surfaced Ahanjideh–Ekim–Yıldız (J. Comb. Optim.
2024, arXiv:2207.02271) and Banak–Ekim–Taşkın (Discrete Optim. 2023, arXiv:2304.01729):
the latter's exhaustive branch-and-cut proves the maximum size of a triangle-free graph with
Δ ≤ 7 and ν ≤ 8 is **58** (their Table 3, instance (7,8): PreUB 59, LB = UB = 58, gap 0%),
and Z(7) = 9. Hence e(F) = 59 is impossible and Theorem 2's window is e(F) ∈ {57, 58}
(status of the tightening: depends on an IMPORTED machine-verified computation (Banak–Ekim–Taşkın 2023, Table 3) —
independently re-checkable in P2's enumeration). An explicit F attaining 58 inside the
window exists: the C₅-blowup [4,4,3,3,3] (all properties machine-verified;
`suite/q18-cone-c5-44333.json`). So (Q18) is live, with a canonical first SAT target.

## 7. Remark: the hand-sketched lemmas were Gallai–Edmonds fragments

An earlier internal attack plan hand-derived partial structure lemmas (a maximum-matching
/ unmatched-vertex analysis with two explicitly unresolved leak cases). They are exactly
fragments of the Gallai–Edmonds decomposition, and under the full classical theorem both
leaks close by definition — every edge is located by (GE-d), with no case analysis needed.

*[Abridged from the internal research file: process/methodology notes elided;
mathematical content unchanged.]*
