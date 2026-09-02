"""P-004 enumeration, committed form (was 'code in session transcript').

Enumerate all C5 inflation weight vectors w (positive ints, sum 19) with
every adjacent sum w_i + w_{i+1} <= 8 (K9 exclusion, IMP-11) and edge
count <= 6*19-12 = 102 (IMP-1), up to the dihedral symmetry of C5.
P-004 claims exactly three classes survive:
  [3,4,4,4,4] (99 edges), [3,3,5,3,5] (98), [3,4,4,3,5] (98).

Also reports, for transparency, any vector passing the adjacent-sum
filter but failing the edge bound (there should be a count for the log),
and re-checks chi >= 10 via the Exactness Lemma chi = max(omega, ceil(n/k)).
"""
import itertools
import math

L, N, K = 5, 19, 2
CAP = 6 * N - 12


def edges(w):
    return sum(x * (x - 1) // 2 for x in w) + \
        sum(w[i] * w[(i + 1) % L] for i in range(L))


def canon(w):
    forms = []
    for d in (1, -1):
        for t in range(L):
            forms.append(tuple(w[(d * i + t) % L] for i in range(L)))
    return min(forms)


def main():
    seen_ok, seen_edge_fail = set(), set()
    for w in itertools.product(range(1, 9), repeat=L):
        if sum(w) != N:
            continue
        if any(w[i] + w[(i + 1) % L] > 8 for i in range(L)):
            continue
        c = canon(w)
        omega = max(w[i] + w[(i + 1) % L] for i in range(L))
        chi = max(omega, math.ceil(N / K))
        assert chi >= 10, (w, chi)  # ceil(19/2)=10 and omega<=8: always 10
        (seen_ok if edges(w) <= CAP else seen_edge_fail).add(c)
    print(f"adjacent-sum-feasible classes: {len(seen_ok | seen_edge_fail)}")
    print(f"edge-bound failures: {sorted(seen_edge_fail)}")
    print(f"SURVIVORS ({len(seen_ok)}):")
    for c in sorted(seen_ok):
        print(f"  C5{list(c)}  edges={edges(c)}  omega="
              f"{max(c[i] + c[(i + 1) % L] for i in range(L))}")
    expect = {canon((3, 4, 4, 4, 4)), canon((3, 3, 5, 3, 5)),
              canon((3, 4, 4, 3, 5))}
    assert seen_ok == expect, ("P-004 ENUMERATION MISMATCH", seen_ok)
    print("MATCHES P-004: exactly the three claimed classes.")


if __name__ == "__main__":
    main()
