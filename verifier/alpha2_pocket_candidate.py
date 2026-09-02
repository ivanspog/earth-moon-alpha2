#!/usr/bin/env python3
"""alpha2_pocket_candidate.py — build and property-check the (Q18) candidate (C-h3).

F = full blowup C5[4,4,3,3,3]: classes V0..V4 on the 5-cycle, edges between
consecutive classes (blowup of C5 by independent sets). Claimed: triangle-free,
alpha(F) = 7, Delta(F) = 7, e(F) = 58, nu(F) = 8, factor-critical.

G0 = K1 v complement(F) on 18 vertices (apex = vertex 17). Claimed: alpha(G0) <= 2,
omega(G0) = 8 (no K9), e(G0) = 95 <= 96 = 6*18-12, chi(G0) = 10 = 18 - nu(F).

Everything checked exactly (itertools / brute force; n is tiny). No solver.
Writes the candidate graph to suite/q18-cone-c5-44333.json in GT-3 format minus
the biplanar partition (edges_part1 = all edges, edges_part2 = [] placeholder,
coloring = the exact 10-coloring found here) — NOT a submission; a SAT target.
"""

import hashlib
import json
import subprocess
from itertools import combinations
from pathlib import Path

SIZES = [4, 4, 3, 3, 3]


def build():
    cls, v = [], 0
    for s in SIZES:
        cls.append(list(range(v, v + s)))
        v += s
    n = v  # 17
    F = set()
    for i in range(5):
        for a in cls[i]:
            for b in cls[(i + 1) % 5]:
                F.add((min(a, b), max(a, b)))
    return n, cls, F


def max_independent(n, adj, cap=None):
    best = 0
    order = sorted(range(n), key=lambda x: -len(adj[x]))

    def grow(cand, cur):
        nonlocal best
        if cur > best:
            best = cur
        if not cand or (cap and best >= cap and cur + len(cand) <= best):
            return
        if cur + len(cand) <= best:
            return
        v = cand[0]
        grow([u for u in cand[1:] if u not in adj[v]], cur + 1)  # take v
        grow(cand[1:], cur)                                      # skip v
    grow(order, 0)
    return best


def max_matching(n, edges):
    # exact maximum-cardinality matching via networkx blossom algorithm
    # (a plain augmenting DFS is WRONG on non-bipartite graphs: misses blossoms)
    import networkx as nx
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(edges)
    return len(nx.max_weight_matching(g, maxcardinality=True))


def has_perfect_matching(n, edges, removed):
    verts = [v for v in range(n) if v != removed]
    sub = [(a, b) for (a, b) in edges if a != removed and b != removed]
    idx = {v: i for i, v in enumerate(verts)}
    return max_matching(len(verts), [(idx[a], idx[b]) for a, b in sub]) == len(verts) // 2


def greedy_chromatic_exact(n, adj, k):
    """Is the graph k-colorable? exact backtracking (n=18, fine)."""
    colors = [-1] * n
    order = sorted(range(n), key=lambda x: -len(adj[x]))

    def bt(i):
        if i == n:
            return True
        v = order[i]
        used = {colors[u] for u in adj[v] if colors[u] >= 0}
        for c in range(k):
            if c not in used:
                colors[v] = c
                if bt(i + 1):
                    return True
                colors[v] = -1
            if c > max([colors[u] for u in order[:i]] + [-1]):
                break  # symmetry: first use of a fresh color
        return False
    return (bt(0), colors)


def main():
    n, cls, F = build()
    assert n == 17
    adjF = {i: set() for i in range(n)}
    for a, b in F:
        adjF[a].add(b)
        adjF[b].add(a)

    checks = {}
    checks["e(F) == 58"] = (len(F) == 58)
    checks["Delta(F) == 7"] = (max(len(adjF[v]) for v in range(n)) == 7)
    checks["delta(F) == 6"] = (min(len(adjF[v]) for v in range(n)) == 6)
    tri = any(c in adjF[a] and c in adjF[b]
              for a, b in F for c in range(n))
    checks["F triangle-free"] = (not tri)
    checks["alpha(F) == 7"] = (max_independent(n, adjF) == 7)
    checks["nu(F) == 8"] = (max_matching(n, list(F)) == 8)
    checks["F factor-critical"] = all(has_perfect_matching(n, list(F), v) for v in range(n))

    # G0 = K1 v complement(F), apex vertex 17
    N = 18
    comp = [(a, b) for a, b in combinations(range(17), 2) if (a, b) not in F]
    G = comp + [(v, 17) for v in range(17)]
    adjG = {i: set() for i in range(N)}
    for a, b in G:
        adjG[a].add(b)
        adjG[b].add(a)
    checks["e(G0) == 95 (<= 96)"] = (len(G) == 95)
    # alpha(G0) <= 2: no independent triple = H = complement(G0) triangle-free
    checks["alpha(G0) <= 2"] = (max_independent(N, adjG, cap=3) <= 2)
    # omega(G0) = alpha(complement) : check no K9 = independent 9-set in complement
    adjH = {i: set() for i in range(N)}
    for a, b in combinations(range(N), 2):
        if b not in adjG[a]:
            adjH[a].add(b)
            adjH[b].add(a)
    checks["omega(G0) == 8 (no K9)"] = (max_independent(N, adjH) == 8)
    ok9, col10 = greedy_chromatic_exact(N, adjG, 10)
    checks["chi(G0) <= 10 (10-coloring found)"] = ok9
    ok_less, _ = greedy_chromatic_exact(N, adjG, 9)
    checks["chi(G0) >= 10 (9-coloring UNSAT by backtracking)"] = (not ok_less)

    here = Path(__file__).resolve()
    sha = hashlib.sha256(here.read_bytes()).hexdigest()
    try:
        git = subprocess.run(["git", "-C", str(here.parent.parent), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        git = "unavailable"
    print(f"# alpha2_pocket_candidate — git {git}")
    print(f"# script sha256 {sha}")
    allpass = True
    for k, v in checks.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
        allpass &= bool(v)
    print("ALL CHECKS PASS" if allpass else "CHECK FAILURE — do not use candidate")

    if allpass:
        out = {
            "comment": "C-h3 (Q18) candidate G0 = K1 v complement(C5-blowup[4,4,3,3,3]); "
                       "NOT a submission — biplanar partition unknown (SAT target). "
                       "chi = 10 verified exactly (9-coloring refuted by backtracking). "
                       "edges_part1/edges_part2 hold all-edges/empty so that "
                       "biplanar_sat_prop.py --json consumes this file directly.",
            "num_vertices": N,
            "edges_all": sorted([list(e) for e in G]),
            "edges_part1": sorted([list(e) for e in G]),
            "edges_part2": [],
            "coloring_10": col10,
            "chromatic_number": 10,
            "apex": 17,
            "F_classes": [c for c in cls],
        }
        p = here.parent.parent / "suite" / "q18-cone-c5-44333.json"
        p.write_text(json.dumps(out, indent=1))
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
