# ILP 12 — Bellman–Ford Algorithm

This folder contains a complete assignment-style setup:

- C++ implementation of **Bellman–Ford** for single-source shortest paths.
- Detects **negative-weight cycle reachable from the source**.
- Random input generator that creates graphs *with and without* a negative cycle.
- Runner that benchmarks and stores results in a file.
- Plotter that generates SVG charts + an HTML report.

## Input format

```
n m src
u1 v1 w1
u2 v2 w2
...
um vm wm
```

- Directed edges `u -> v` with weight `w`.
- Nodes are numbered `0..n-1`.

## Output format

- `Negative cycle detected ...` OR `No negative cycle detected`
- `Reachable: <count>`
- `SumDist: <sum of finite distances>` (used as a quick verification/checksum)
- `Time taken: <seconds> seconds`

## Complexity

Bellman–Ford runtime: $O(VE)$

## Files

- `bellman_ford.cpp` — implementation
- `random_inputs.py` — generates `random_<n>_<m>_pos.txt` and `random_<n>_<m>_neg.txt`
- `run_all_cases.py` — runs all cases and writes `results.txt`
- `plot_results.py` — produces charts + `results_table.csv`
- `charts/index.html` — report viewer
