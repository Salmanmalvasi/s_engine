from __future__ import annotations

import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# Bellman-Ford runs in O(n*m), so keep sizes moderate.
# We'll vary number of nodes and generate a sparse-ish directed graph.
SIZES = [
    (20, 80),
    (50, 250),
    (100, 700),
    (200, 2000),
    (400, 6000),
]

random.seed(42)


def gen_graph(n: int, m: int, neg_cycle: bool = False):
    src = 0
    edges: list[tuple[int, int, int]] = []

    # Ensure connectivity-ish from src with a random chain
    for i in range(n - 1):
        w = random.randint(1, 9)
        edges.append((i, i + 1, w))

    remaining = max(0, m - (n - 1))

    used = set((u, v) for u, v, _ in edges)

    for _ in range(remaining):
        u = random.randrange(n)
        v = random.randrange(n)
        if u == v:
            continue
        if (u, v) in used:
            continue
        used.add((u, v))
        # For the "pos" (no-negative-cycle) datasets we force non-negative weights.
        # This guarantees there is no negative cycle anywhere in the graph.
        if neg_cycle:
            w = random.randint(-5, 15)
        else:
            w = random.randint(0, 15)
        edges.append((u, v, w))

    # Optionally inject a small reachable negative cycle (0->1->2->0)
    if neg_cycle and n >= 3:
        edges.append((0, 1, 1))
        edges.append((1, 2, 1))
        edges.append((2, 0, -5))  # cycle weight -3

    # Trim to m edges if we exceeded
    edges = edges[:m]

    return src, edges


def write_case(n: int, m: int, neg: bool):
    src, edges = gen_graph(n, m, neg_cycle=neg)
    tag = "neg" if neg else "pos"
    out = SCRIPT_DIR / f"random_{n}_{m}_{tag}.txt"
    with out.open("w") as f:
        f.write(f"{n} {len(edges)} {src}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")


def main() -> None:
    for n, m in SIZES:
        write_case(n, m, neg=False)
        # add one negative-cycle case too (useful for report)
        write_case(n, m, neg=True)

    print(f"Generated {len(SIZES) * 2} input files in {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
