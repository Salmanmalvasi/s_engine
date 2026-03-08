from __future__ import annotations
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SIZES = [(20, 120), (30, 250), (40, 500), (60, 1200), (80, 2000)]
random.seed(42)

def gen_graph(n, m, neg_cycle):
    edges, used = [], set()
    for i in range(n):
        u, v, w = i, (i + 1) % n, random.randint(1, 9)
        edges.append((u, v, w)); used.add((u, v))
    def rand_w():
        return random.randint(-5, 15) if neg_cycle else random.randint(0, 15)
    while len(edges) < m:
        u, v = random.randrange(n), random.randrange(n)
        if u == v or (u, v) in used: continue
        used.add((u, v)); edges.append((u, v, rand_w()))
    if neg_cycle and n >= 3:
        edges += [(0,1,1),(1,2,1),(2,0,-5)]
    return edges[:m]

def write_case(n, m, tag):
    edges = gen_graph(n, m, tag == "neg")
    out = SCRIPT_DIR / f"random_{n}_{m}_{tag}.txt"
    with out.open("w") as f:
        f.write(f"{n} {len(edges)}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")

for n, m in SIZES:
    write_case(n, m, "pos")
    write_case(n, m, "neg")
print(f"Generated {len(SIZES)*2} input files in {SCRIPT_DIR}")
