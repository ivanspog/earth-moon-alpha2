#!/usr/bin/env python3
r"""alpha2_pocket_sweep.py — exhaustive shape sweep for the alpha=2 pocket (C-h3, P1).

Question (C-h3): does a biplanar G with alpha(G) <= 2 and chi(G) >= 10 exist on
n in {14..18} vertices?

Setup: H = complement(G) is triangle-free (alpha(G) <= 2), and chi(G) = n - nu(H)
(color classes are singletons or H-edges), so chi >= 10 iff nu(H) <= n - 10 iff
deficiency def(H) = n - 2 nu(H) >= 20 - n.

Gallai-Edmonds decomposition of H: D = vertices missed by some maximum matching,
A = N(D) \ D, C = rest. Components of H[D] are factor-critical; def = c(D) - |A|;
H[C] has a perfect matching; there are NO D-C edges and no edges between distinct
components of H[D].

Triangle-free specialisations (proved in proofs/P-006):
  - factor-critical triangle-free components have order 1 or odd order >= 5;
  - the unique one of order 5 is C5 (alpha = 2, e = 5);
  - factor-critical on o >= 3 vertices has alpha <= (o-1)/2;
  - triangle-free => deg(v) <= alpha (neighbourhoods are independent), applied
    per part: e(part) <= floor(|part| * alpha(part) / 2);
  - Ramsey lower bounds: o >= R(3,k) => alpha >= k, with
    R(3,2..9) = 3, 6, 9, 14, 18, 23, 28, 36.

Shape = (s singleton D-components, t big D-components with odd orders o_i >= 5,
a = |A|, c = |C|). Necessary conditions checked exhaustively:

  (1) deficiency:  s + t - a >= 20 - n
  (2) alpha budget: s + sum(alpha_i) + alpha_C <= 8
      [biplanar G has no K9 (IMP-11) => omega(G) = alpha(H) <= 8; independent
       sets add across D-components and C since those parts span no mutual edges]
      with alpha_i in [ramsey_lb(o_i), (o_i-1)//2] (order 5 forces exactly 2),
      alpha_C in [ramsey_lb(c), c//2] (c even, H[C] perfectly matched).
  (3) vertex count: s + sum(o_i) + a + c = n, c even
  (4) edge window: e(H) >= binom(n,2) - (6n-12)   [biplanar => e(G) <= 6n-12]
      e(H) <= sum(e_max(o_i, alpha_i)) + 8a + floor(c*alpha_C/2)
      [every H-edge lies in a D-component, is incident to A (deg <= alpha(H) <= 8),
       or lies inside C]

A shape passing all four is a SURVIVOR: it is the P2 enumeration frontier.
Infeasibility of every shape at some n proves the pocket empty at that n
(the sweep is a sound relaxation: every real H induces a shape it covers).

No external inputs. Provenance: prints git commit + SHA-256 of this file.
"""

import hashlib
import subprocess
from itertools import product
from pathlib import Path

R3 = {2: 3, 3: 6, 4: 9, 5: 14, 6: 18, 7: 23, 8: 28, 9: 36}


def ramsey_lb(nverts: int) -> int:
    """Least possible independence number of a triangle-free graph on nverts vertices."""
    if nverts <= 0:
        return 0
    return max([1] + [k for k, r in R3.items() if r <= nverts])


def comp_alpha_range(o: int):
    if o == 5:
        return (2, 2)  # unique component: C5
    return (ramsey_lb(o), (o - 1) // 2)


def comp_emax(o: int, alpha: int) -> int:
    if o == 5:
        return 5  # C5 exactly
    return (o * alpha) // 2


def orders_iter(t: int, budget: int, lo: int = 5):
    """Non-decreasing tuples of t odd orders >= 5 with sum <= budget."""
    if t == 0:
        yield ()
        return
    o = lo
    while o * t <= budget:  # smallest remaining assignment must still fit
        for rest in orders_iter(t - 1, budget - o, o):
            yield (o,) + rest
        o += 2


def feasible(n, s, t, a, c, orders, emin):
    """Return (feasible?, best (emax, alphas, alpha_C)) for this shape."""
    if c == 0:
        ac_lo, ac_hi = 0, 0
    else:
        ac_lo, ac_hi = ramsey_lb(c), c // 2
        if ac_lo > ac_hi:
            return False, None
    ranges = [comp_alpha_range(o) for o in orders]
    if any(lo > hi for lo, hi in ranges):
        return False, None
    best = None
    for alphas in product(*[range(lo, hi + 1) for lo, hi in ranges]):
        for ac in range(ac_lo, ac_hi + 1):
            if s + sum(alphas) + ac > 8:  # alpha budget (2)
                continue
            emax = sum(comp_emax(o, al) for o, al in zip(orders, alphas)) \
                + 8 * a + (c * ac) // 2
            if emax >= emin:  # edge window (4)
                cand = (emax, alphas, ac)
                if best is None or cand > best:
                    best = cand
    return (best is not None), best


def sweep(n):
    dmin = 20 - n
    emin = n * (n - 1) // 2 - (6 * n - 12)
    survivors, checked = [], 0
    for t in range(0, 5):          # s + 2t <= 8 => t <= 4
        for s in range(0, 9):      # s <= alpha(H) <= 8
            amax = s + t - dmin    # deficiency (1)
            if amax < 0:
                continue
            for a in range(0, amax + 1):
                rem = n - s - a
                if rem < 0:
                    continue
                for orders in orders_iter(t, rem):
                    c = rem - sum(orders)
                    if c < 0 or c % 2:  # (3)
                        continue
                    checked += 1
                    ok, best = feasible(n, s, t, a, c, orders, emin)
                    if ok:
                        survivors.append((s, t, a, c, orders, best))
    return survivors, checked, emin


def main():
    here = Path(__file__).resolve()
    sha = hashlib.sha256(here.read_bytes()).hexdigest()
    try:
        git = subprocess.run(["git", "-C", str(here.parent.parent), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        git = "unavailable"
    print(f"# alpha2_pocket_sweep — git {git}")
    print(f"# script sha256 {sha}")
    print(f"# R(3,k) table: {R3}")
    print()
    any_survivor = False
    for n in range(14, 19):
        survivors, checked, emin = sweep(n)
        print(f"n={n}: e(H) >= {emin} required; {checked} shapes checked; "
              f"{len(survivors)} survivor(s)")
        for (s, t, a, c, orders, best) in survivors:
            any_survivor = True
            emax, alphas, ac = best
            print(f"    SURVIVOR s={s} t={t} a={a} c={c} orders={list(orders)} "
                  f"alphas={list(alphas)} alpha_C={ac} emax={emax}")
    print()
    print("VERDICT: pocket shapes exist only where survivors are listed above; "
          "every n with 0 survivors is EMPTY (no biplanar G with alpha<=2, chi>=10).")
    if not any_survivor:
        print("ALL FIVE n EMPTY.")


if __name__ == "__main__":
    main()
