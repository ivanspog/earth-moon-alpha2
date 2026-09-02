"""Machine check of the odd-cycle-inflation chromatic-number formula

    chi(C_{2k+1}[w]) = max(omega, ceil(n/k)),  omega = max adjacent sum

used to repair the gap Gemini's review found in P-004 (the old proof
assumed the lower bound ceil(n/k) is tight).

Per instance the check is logically complete without any SAT chi search:
  upper bound: the explicit arc coloring is verified to be a PROPER
    coloring with exactly max(omega, ceil(n/k)) colors;
  lower bound: alpha and omega are computed EXACTLY (networkx exact
    algorithms on n <= ~36), and chi >= max(omega, ceil(n/alpha)) is a
    trivial theorem. Equality follows when alpha = k and omega = max
    adjacent sum, both of which are asserted per instance.
On tiny instances (n <= 15) an end-to-end SAT cross-check of chi is kept.

Usage: .venv/bin/python verifier/chi_inflation_check.py
"""
from __future__ import annotations

import itertools
import math
import os
import random
import sys

from pysat.solvers import Cadical195

sys.path.insert(0, os.path.dirname(__file__))


def inflate(L, w):
    n = sum(w)
    bag = []
    for i, x in enumerate(w):
        bag += [i] * x
    edges = [(u, v) for u in range(n) for v in range(u + 1, n)
             if bag[u] == bag[v] or (bag[u] - bag[v]) % L in (1, L - 1)]
    return n, edges


def colorable(n, edges, t):
    s = Cadical195()
    var = lambda v, c: v * t + c + 1
    for v in range(n):
        s.add_clause([var(v, c) for c in range(t)])
    for u, v in edges:
        for c in range(t):
            s.add_clause([-var(u, c), -var(v, c)])
    res = s.solve()
    s.delete()
    return res


def chi_exact(n, edges, lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if colorable(n, edges, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def arc_coloring(L, w, T):
    """Constructive T-coloring per the repair lemma: bag i gets the arc
    [a_i, a_i+w_i) mod T; gaps g_i >= 0 with sum = kT - n and
    g_i <= T - w_i - w_{i+1}. Returns coloring or None."""
    k = (L - 1) // 2
    n = sum(w)
    need = k * T - n
    if need < 0:
        return None
    caps = [T - w[i] - w[(i + 1) % L] for i in range(L)]
    if any(c < 0 for c in caps) or sum(caps) < need:
        return None
    g = []
    rem = need
    for c in caps:
        take = min(c, rem)
        g.append(take)
        rem -= take
    col, a = [], 0
    for i in range(L):
        col += [(a + j) % T for j in range(w[i])]
        a += w[i] + g[i]
    return col


def formula(L, w):
    k = (L - 1) // 2
    n = sum(w)
    om = max(w[i] + w[(i + 1) % L] for i in range(L))
    return max(om, math.ceil(n / k))


def check(L, w):
    import networkx as nx
    n, edges = inflate(L, w)
    k = (L - 1) // 2
    f = formula(L, w)
    # upper bound: constructive coloring must be proper with <= f colors
    col = arc_coloring(L, w, f)
    assert col is not None, (L, w, "arc coloring infeasible")
    assert len(set(col)) <= f, (L, w, "too many colors")
    for u, v in edges:
        assert col[u] != col[v], (L, w, "arc coloring improper", u, v)
    # lower bound: exact alpha and omega
    g = nx.Graph(edges)
    g.add_nodes_from(range(n))
    alpha = len(max(nx.find_cliques(nx.complement(g)), key=len))
    omega = len(max(nx.find_cliques(g), key=len))
    assert alpha == k, (L, w, "alpha != k", alpha)
    assert omega == max(w[i] + w[(i + 1) % L] for i in range(L)), (L, w, omega)
    lb = max(omega, math.ceil(n / alpha))
    assert lb == f, (L, w, lb, f)
    # tiny instances: independent end-to-end SAT cross-check
    if n <= 15:
        c = chi_exact(n, edges, 2, f)
        assert c == f, (L, w, "SAT chi mismatch", c, f)
    return True, f, f


def dihedral_canon(w):
    L = len(w)
    best = None
    for s in range(L):
        for d in (1, -1):
            cand = tuple(w[(s + d * j) % L] for j in range(L))
            if best is None or cand < best:
                best = cand
    return best


def sweep(L, wmax, exhaustive=True, samples=0, seed=0):
    seen = set()
    bad = 0
    vecs = (itertools.product(range(1, wmax + 1), repeat=L) if exhaustive
            else (tuple(random.Random(seed + i).choices(range(1, wmax + 1), k=L))
                  for i in range(samples)))
    tested = 0
    for w in vecs:
        cw = dihedral_canon(w)
        if cw in seen:
            continue
        seen.add(cw)
        ok, c, f = check(L, cw)
        tested += 1
        if not ok:
            bad += 1
            print(f"  MISMATCH L={L} w={cw}: chi={c} formula={f}", flush=True)
    print(f"L={L} wmax={wmax}: {tested} classes tested, {bad} mismatches",
          flush=True)
    return bad


def main():
    total = 0
    total += sweep(5, 7)                 # exhaustive, 7^5 pre-dedup
    total += sweep(7, 4)                 # exhaustive, 4^7 pre-dedup
    total += sweep(7, 7, exhaustive=False, samples=4000)
    total += sweep(9, 3)                 # exhaustive, 3^9 pre-dedup
    total += sweep(9, 5, exhaustive=False, samples=3000)
    total += sweep(11, 4, exhaustive=False, samples=2000)
    total += sweep(13, 3, exhaustive=False, samples=1000)
    print("TOTAL MISMATCHES:", total, flush=True)


if __name__ == "__main__":
    main()
