"""Earth-Moon problem verifier.

Deterministic, network-free, pure. Takes a candidate construction (the JSON
format specified verbatim by the FrontierMath problem statement) and returns
the achieved score plus pass/fail on every structural condition.

Conditions checked (mirroring the problem's acceptance conditions):
  C1  structure: JSON keys present, edges well-formed, E1 and E2 disjoint,
      no self-loops, no duplicate edges, endpoints in [0, N)
  C2  planarity: both (V, E1) and (V, E2) are planar  [linear-time LR test]
  C3  coloring: supplied coloring is proper on G = (V, E1 u E2) and uses at
      most k distinct colors
  C4  optimality: G cannot be properly colored with k-1 colors  [SAT UNSAT]
  C5  (submission mode only) k in [10, 12]

Score = k when C1-C4 pass, else None. Internal/fitness mode omits C5 so the
search can climb through k < 10.

Cost model: C2 is O(n); C4 is a SAT call on n*(k-1) variables and
O(m*(k-1)) clauses -- the dominant cost, reported per instance.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

import networkx as nx
from pysat.solvers import Cadical195


@dataclass
class Verdict:
    ok: bool
    score: int | None  # verified chromatic number, None if any check failed
    checks: dict = field(default_factory=dict)  # name -> (bool, detail)
    cost: dict = field(default_factory=dict)  # timings + instance size

    def summary(self) -> str:
        lines = [f"PASS score={self.score}" if self.ok else "FAIL"]
        for name, (ok, detail) in self.checks.items():
            lines.append(f"  [{'ok' if ok else 'XX'}] {name}: {detail}")
        lines.append(f"  cost: {self.cost}")
        return "\n".join(lines)


def _norm_edges(raw) -> tuple[set[frozenset], str | None]:
    """Normalise an edge list; return (set of undirected edges, error)."""
    out = set()
    for e in raw:
        if not (isinstance(e, (list, tuple)) and len(e) == 2):
            return set(), f"malformed edge {e!r}"
        u, v = e
        if not (isinstance(u, int) and isinstance(v, int)):
            return set(), f"non-integer endpoint in {e!r}"
        if u == v:
            return set(), f"self-loop {e!r}"
        key = frozenset((u, v))
        if key in out:
            return set(), f"duplicate edge {e!r}"
        out.add(key)
    return out, None


def sat_colorable(n: int, edges: list[tuple[int, int]], k: int,
                  clique_hint: list[int] | None = None) -> tuple[bool, list[int] | None]:
    """Exact test: does G admit a proper k-coloring? Returns (bool, witness).

    Symmetry breaking: vertices of a (greedy) clique are pre-assigned
    distinct colors -- sound because clique vertices must all differ and
    colors are interchangeable.
    """
    if k <= 0:
        return (n == 0), []
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    if clique_hint is None:
        clique_hint = _greedy_clique(G)
    if len(clique_hint) > k:
        return False, None  # clique bigger than k colors: immediately UNSAT

    def var(v: int, c: int) -> int:
        return v * k + c + 1

    with Cadical195() as s:
        for v in range(n):
            s.add_clause([var(v, c) for c in range(k)])
        for u, v in edges:
            for c in range(k):
                s.add_clause([-var(u, c), -var(v, c)])
        for i, v in enumerate(clique_hint):
            s.add_clause([var(v, i)])
        sat = s.solve()
        if not sat:
            return False, None
        model = set(l for l in s.get_model() if l > 0)
        col = [next(c for c in range(k) if var(v, c) in model) for v in range(n)]
        return True, col


def _greedy_clique(G: nx.Graph) -> list[int]:
    best: list[int] = []
    for seed in sorted(G.nodes, key=lambda v: -G.degree(v))[:30]:
        clique = [seed]
        cand = set(G.neighbors(seed))
        while cand:
            v = max(cand, key=lambda x: len(cand & set(G.neighbors(x))))
            clique.append(v)
            cand &= set(G.neighbors(v))
        if len(clique) > len(best):
            best = clique
    return best


def verify(sub: dict, submission_mode: bool = False) -> Verdict:
    """Verify a candidate. `sub` is the parsed JSON object."""
    v = Verdict(ok=False, score=None)
    t0 = time.perf_counter()

    # --- C1 structure -----------------------------------------------------
    required = ["num_vertices", "edges_part1", "edges_part2", "coloring",
                "chromatic_number"]
    missing = [key for key in required if key not in sub]
    if missing:
        v.checks["C1-structure"] = (False, f"missing keys {missing}")
        return v
    n = sub["num_vertices"]
    k = sub["chromatic_number"]
    if not (isinstance(n, int) and n > 0 and isinstance(k, int)):
        v.checks["C1-structure"] = (False, "num_vertices/chromatic_number not positive ints")
        return v
    e1, err1 = _norm_edges(sub["edges_part1"])
    e2, err2 = _norm_edges(sub["edges_part2"])
    if err1 or err2:
        v.checks["C1-structure"] = (False, err1 or err2)
        return v
    if e1 & e2:
        v.checks["C1-structure"] = (False, f"E1 and E2 share {len(e1 & e2)} edges")
        return v
    all_ends = {x for e in (e1 | e2) for x in e}
    if all_ends and (min(all_ends) < 0 or max(all_ends) >= n):
        v.checks["C1-structure"] = (False, "endpoint out of range [0, N)")
        return v
    coloring = sub["coloring"]
    if not (isinstance(coloring, list) and len(coloring) == n
            and all(isinstance(c, int) for c in coloring)):
        v.checks["C1-structure"] = (False, "coloring is not a list of N ints")
        return v
    v.checks["C1-structure"] = (True, f"n={n}, |E1|={len(e1)}, |E2|={len(e2)}, k={k}")

    edges1 = [tuple(sorted(e)) for e in sorted(e1, key=sorted)]
    edges2 = [tuple(sorted(e)) for e in sorted(e2, key=sorted)]
    edges = edges1 + edges2

    # --- C5 submission range (checked early, cheap) -----------------------
    if submission_mode:
        ok5 = 10 <= k <= 12
        v.checks["C5-range"] = (ok5, f"k={k} must be in [10,12]")
        if not ok5:
            return v

    # --- C2 planarity -----------------------------------------------------
    t = time.perf_counter()
    for name, es in (("E1", edges1), ("E2", edges2)):
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(es)
        planar, _ = nx.check_planarity(G, counterexample=False)
        if not planar:
            v.checks["C2-planarity"] = (False, f"({name}) is not planar")
            return v
    v.checks["C2-planarity"] = (True, "both parts planar")
    v.cost["planarity_s"] = round(time.perf_counter() - t, 4)

    # --- C3 proper coloring with <= k colors ------------------------------
    bad = [(u, w) for u, w in edges if coloring[u] == coloring[w]]
    ncolors = len(set(coloring))
    if bad:
        v.checks["C3-coloring"] = (False, f"{len(bad)} monochromatic edges, e.g. {bad[0]}")
        return v
    if ncolors > k:
        v.checks["C3-coloring"] = (False, f"coloring uses {ncolors} > k = {k} colors")
        return v
    v.checks["C3-coloring"] = (True, f"proper, uses {ncolors} colors <= k = {k}")

    # --- C4 no (k-1)-coloring --------------------------------------------
    t = time.perf_counter()
    colorable, _ = sat_colorable(n, edges, k - 1)
    v.cost["sat_s"] = round(time.perf_counter() - t, 4)
    if colorable:
        v.checks["C4-lower-bound"] = (False, f"G IS ({k - 1})-colorable: chromatic number < k")
        return v
    v.checks["C4-lower-bound"] = (True, f"({k - 1})-coloring UNSAT")

    v.cost["total_s"] = round(time.perf_counter() - t0, 4)
    v.cost["n"] = n
    v.cost["m"] = len(edges)
    v.ok = True
    v.score = k
    return v


def verify_file(path: str, submission_mode: bool = False) -> Verdict:
    with open(path) as f:
        return verify(json.load(f), submission_mode=submission_mode)


if __name__ == "__main__":
    import sys
    mode = "--submission" in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith("-")]
    for p in paths:
        print(p)
        print(verify_file(p, submission_mode=mode).summary())
