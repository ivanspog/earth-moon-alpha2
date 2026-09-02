"""Cube-and-conquer wrapper for the lex-off audits (P-005 hardening).

Why: without the lex symmetry constraints the monolithic no-sym runs blow
past 12 h (the n=18 sibling audit did). Split on K edge variables: the
2^K sign patterns partition the FULL assignment space, so
  - every cube UNSAT  =>  the base instance is UNSAT (soundness is
    trivial: cube i only ADDS unit clauses to the audited encoding);
  - any cube SAT      =>  solve() itself re-verifies the partition
    (planarity of both parts, disjointness) before reporting.
Each cube runs in a FRESH process (memory hygiene after two OOM kills)
and banks its verdict to population/cube-audit-<name>/cube-<i>.json, so
a kill loses at most one cube.

Cube variable selection (deterministic, documented): greedily pick the
edge contained in the most K5 subgraphs, subject to sharing no endpoint
with an already-picked edge (vertex-disjoint => the cubes split globally
different regions), always excluding edge index 0 (pinned to part 1 by
the part-swap unit clause, which no-sym mode keeps — sound by the swap
argument).

Usage:
  # one cube (spawned by run_cube_audit.py):
  .venv/bin/python verifier/biplanar_sat_cube.py --weights 3,3,5,3,5 \
      --cube-bits 7 --cube-index 42
  # print the chosen cube edges and exit:
  .venv/bin/python verifier/biplanar_sat_cube.py --weights 3,3,5,3,5 \
      --cube-bits 7 --show
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from biplanar_sat import k5_subgraphs  # noqa: E402
from biplanar_sat_prop import solve  # noqa: E402
from c5_inflation_attack import inflate_c5  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")


def cube_edges(n, edges, bits):
    """Deterministic: top `bits` edges by K5-membership count, greedily
    vertex-disjoint, edge 0 excluded."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    count = {e: 0 for e in edges}
    for c in k5_subgraphs(n, adj):
        cs = sorted(c)
        for i, u in enumerate(cs):
            for v in cs[i + 1:]:
                count[(u, v)] += 1
    ranked = sorted(edges[1:], key=lambda e: (-count[e], e))
    picked, used = [], set()
    for e in ranked:
        if used & set(e):
            continue
        picked.append(e)
        used |= set(e)
        if len(picked) == bits:
            break
    return picked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--cube-bits", type=int, default=7)
    ap.add_argument("--cube-index", type=int)
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--with-sym", action="store_true",
                    help="keep lex symmetry breaking (default OFF: this "
                         "tool exists for the no-sym audits)")
    args = ap.parse_args()

    w = [int(t) for t in args.weights.split(",")]
    n, edges = inflate_c5(w)
    edges = sorted(tuple(sorted(e)) for e in edges)
    eidx = {e: i for i, e in enumerate(edges)}
    cvars = cube_edges(n, edges, args.cube_bits)
    assert len(cvars) == args.cube_bits, \
        f"only {len(cvars)} disjoint cube edges available"
    if args.show:
        print(json.dumps({"n": n, "m": len(edges), "cube_bits": args.cube_bits,
                          "cube_edges": [list(e) for e in cvars]}))
        return
    assert args.cube_index is not None and \
        0 <= args.cube_index < 2 ** args.cube_bits
    units = []
    for b, e in enumerate(cvars):
        lit = eidx[e] + 1
        units.append(lit if (args.cube_index >> b) & 1 else -lit)

    base = "c5_" + "_".join(map(str, w)) + \
        ("" if args.with_sym else "_nosym") + f"_cube{args.cube_index:03d}"
    autos = None
    if args.with_sym:
        from biplanar_sat import inflation_automorphisms
        autos = inflation_automorphisms(w)
    outdir = os.path.join(ROOT, "population",
                          "cube-audit-c5_" + "_".join(map(str, w)) +
                          ("" if args.with_sym else "_nosym"))
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    verdict, dt = solve(n, edges, base, autos=autos, extra_units=units)
    with open(os.path.join(outdir, f"cube-{args.cube_index:03d}.json"),
              "w") as f:
        json.dump({"cube_index": args.cube_index, "cube_bits": args.cube_bits,
                   "cube_edges": [list(e) for e in cvars], "units": units,
                   "verdict": verdict, "wall_s": round(dt, 1),
                   "total_s": round(time.time() - t0, 1)}, f)
    print(f"[cube {args.cube_index}] {verdict} in {dt:.1f}s", flush=True)


if __name__ == "__main__":
    main()
