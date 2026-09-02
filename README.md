# earth-moon-alpha2

Small-order results on the **Earth–Moon problem** (the chromatic number of
biplanar / thickness-2 graphs, open since Ringel 1959; known bounds 9 ≤ χ ≤ 12):
the **independence-number-2 route** — proofs, SAT certificates, verification
scripts, and run logs.

This is a research record, not a paper. Every claim below carries its honest
verification status. Nothing here has been peer-reviewed.

## Claims

| # | Statement | Status |
|---|-----------|--------|
| P-003 | Every biplanar graph G with α(G) ≤ 2 has n ≤ 19; at n = 19, α ≤ 2 forces χ ≥ 10 automatically | Proven (elementary; adversarially reviewed, two external rounds) |
| P-004 | Odd-cycle inflations with χ ≥ 10 not excluded by K₉/edge counts collapse to exactly 4 graphs: C₇⊠K₄, C₅[3,4,4,4,4] (non-biplanar, Kirchweger–Scheucher–Szeider 2023), C₅[3,3,5,3,5], C₅[3,4,4,3,5] | Proven (lemmas + exhaustive enumeration, machine-checked; adversarially reviewed; the χ-exactness lemma is classical — Gao–Zhu 1996 / Niessen–Kind 2000, attributed not claimed) |
| P-005 | C₅[3,3,5,3,5] and C₅[3,4,4,3,5] (n=19) are **not biplanar** ⟹ among all odd-cycle inflations only C₇⊠K₄ remains open | Machine-proven (SAT, planarity propagator; controls both directions incl. independent replication of the KSS 2023 kill; a symmetry-free certificate-validated audit is in progress) |
| P-006 | No biplanar graph with α ≤ 2 and χ ≥ 10 exists on **14–17 vertices**; on 18 vertices any such graph is forced to be K₁ ∨ F̄ with F triangle-free factor-critical, 17 vertices, α(F)=7, Δ(F) ≤ 7, 57 ≤ e(F) ≤ 58 | Proven (Gallai–Edmonds + Ramsey + counting; finite shape sweep machine-checked; one external adversarial review: SOUND) |
| G₀ | The canonical n=18 candidate G₀ = K₁ ∨ complement(C₅-blowup[4,4,3,3,3]) is 10-chromatic (exactly, machine-verified) and **not biplanar** | χ = 10: machine-verified. Non-biplanarity: SAT UNSAT with symmetry breaking (13.3h, 1.95M certificate-validated clauses); symmetry-free confirmation run in progress |

Consequence of the table: with KSS 2023 (n ≤ 13 for all graphs), the α ≤ 2 route
to a 10-chromatic biplanar graph reduces to (a) the residual non-blowup part of
the 18-vertex window above, and (b) the classical 19-vertex question
(Gethner–Sulanke). The edge window at n=18 lands exactly on the published open
case (Δ, ν) = (7, 8) of Ahanjideh–Ekim–Yıldız (J. Comb. Optim. 2024), whose
value 58 was computed by Banak–Ekim–Taşkın (Discrete Optim. 2023).

## Verify it yourself

Requires Python ≥ 3.12 with `networkx`, `python-sat`, `numpy`.

```
# P-006 shape sweep (finite case check; seconds)
python verifier/alpha2_pocket_sweep.py

# G0 candidate properties incl. exact chi=10 (minutes)
python verifier/alpha2_pocket_candidate.py

# P-004 enumeration + chi exactness check (minutes)
python verifier/enumerate_c5_candidates.py
python verifier/chi_inflation_check.py

# P-005 / G0 SAT runs (hours-days; logs of our runs are in logs/)
python verifier/biplanar_sat_prop.py --weights 3,3,5,3,5
python verifier/biplanar_sat_prop.py --json suite/q18-cone-c5-44333.json

# Sanity: the verifier accepts Sulanke's classical chi=9 graph
python verifier/verify.py suite/sulanke.json
```

Every SAT run validates each learned planarity clause as a literal K₅/K₃,₃
subdivision certificate before use (`is_kuratowski_subdivision` in
`verifier/biplanar_sat_prop.py`). Run logs in `logs/` carry git-commit and
input-SHA provenance headers.

## Provenance — read this before judging

This work was produced by an **AI research framework** (long-horizon AI research
sessions with machine verification of every claim, adversarial cross-model
review rounds, and documented literature searches), directed and overseen by a
human who is not a professional mathematician. It is not a one-shot chatbot
output, but AI-produced mathematics warrants extra scrutiny — that is why the
verification scripts and full logs are published. The proof files are exported
from the internal research repository with light edits: internal
cross-references and per-model attribution notes were removed for this public
snapshot (the private record retains full idea-level attribution), and one
process section is abridged and marked as such; the mathematical content is
unchanged. "External adversarial review" in the proof files means adversarial
cross-model AI review rounds — useful hygiene, not peer review.

Novelty caveat, stated honestly: documented searches (zbMATH Open, arXiv,
Semantic Scholar forward citations, OEIS) found none of the above in the
literature, but MathSciNet was not searched and two relevant paywalled texts
(Gethner 2018; Gethner–Sulanke 2009) were not read at source. Some of this may
be known, or easy enough that nobody wrote it down. Corrections are welcome
and will be recorded.

## Contact

Ivan Spogreev — ivanspog@gmail.com

License: TBD (all rights reserved until a license is chosen).
