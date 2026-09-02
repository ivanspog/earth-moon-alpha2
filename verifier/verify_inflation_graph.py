"""Independent verification of the encoded input graphs (council P-005
round-1, Sol point 1: 'the encoded input graph is not auditable').

Reconstructs C5[w] from the DEFINITION by a separate code path and checks
inflate_c5's output against it edge-for-edge, plus structural properties
and the automorphism generators actually used by the SAT runs:

  - n = sum(w); vertex set = {0..n-1}; simple, no loops/dupes;
  - bag i = consecutive block of w[i] vertices, a clique;
  - all cross edges between consecutive bags (mod 5), no other edges;
  - m = sum C(w_i,2) + sum w_i*w_{i+1};
  - every generator from inflation_automorphisms(w) is a bijection on
    vertices mapping the edge set ONTO itself (i.e. is an automorphism);
    generator count = sum(w_i - 1) + #(weight-preserving dihedral maps).

Usage: .venv/bin/python verifier/verify_inflation_graph.py
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from biplanar_sat import inflation_automorphisms  # noqa: E402
from c5_inflation_attack import inflate_c5  # noqa: E402


def reference_inflation(w):
    """Definition-direct reconstruction, independent of inflate_c5."""
    L = len(w)
    n = sum(w)
    starts = [sum(w[:i]) for i in range(L)]
    bags = [list(range(starts[i], starts[i] + w[i])) for i in range(L)]
    E = set()
    for b in bags:
        E |= {tuple(sorted(p)) for p in itertools.combinations(b, 2)}
    for i in range(L):
        for u in bags[i]:
            for v in bags[(i + 1) % L]:
                E.add(tuple(sorted((u, v))))
    return n, E, bags


def check(w):
    n_ref, E_ref, bags = reference_inflation(w)
    n, edges = inflate_c5(w)
    E = {tuple(sorted(e)) for e in edges}
    assert n == n_ref, (n, n_ref)
    assert len(edges) == len(E), "duplicate edges"
    assert all(0 <= u < n and 0 <= v < n and u != v for u, v in E)
    assert E == E_ref, ("edge set mismatch",
                        sorted(E ^ E_ref)[:10])
    m_formula = sum(x * (x - 1) // 2 for x in w) + \
        sum(w[i] * w[(i + 1) % len(w)] for i in range(len(w)))
    assert len(E) == m_formula, (len(E), m_formula)

    gens = inflation_automorphisms(w)
    for g in gens:
        assert sorted(g) == list(range(n)) and \
            sorted(g.values()) == list(range(n)), "not a bijection on [n]"
        img = {tuple(sorted((g[u], g[v]))) for u, v in E}
        assert img == E, "generator is NOT an automorphism"
    n_transp = sum(x - 1 for x in w)
    L = len(w)
    n_dihedral = sum(1 for t in range(L) for d in (1, -1)
                     if (t, d) != (0, 1)
                     and all(w[(d * i + t) % L] == w[i] for i in range(L)))
    assert len(gens) == n_transp + n_dihedral, \
        (len(gens), n_transp, n_dihedral)
    print(f"C5{w}: n={n} m={len(E)} PASS "
          f"(edge set == definition; {len(gens)} generators = "
          f"{n_transp} transpositions + {n_dihedral} dihedral, "
          f"all verified automorphisms)")


if __name__ == "__main__":
    for w in ([3, 3, 5, 3, 5], [3, 4, 4, 3, 5], [3, 4, 4, 4, 4],
              [3, 3, 5, 3, 4], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3]):
        check(w)
    print("ALL GRAPHS VERIFIED against the definition.")
