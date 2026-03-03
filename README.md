# s_engine — DSA / ILP Assignment Engine (C++ + Python Benchmarks)

This repo contains a set of **assignment-style implementations** for common DSA / ILP lab problems.
Each assignment folder includes:

- C++ implementation (with timing)
- Random input generator (Python)
- Runner to execute all cases and log results (Python)
- Plotter to generate **SVG graphs** + **HTML report** (Python, no external deps)

## Included ILPs (so far)

- `merge_sort/` — Merge Sort benchmarking
- `mcm/` — Matrix Chain Multiplication
- `lcs/` — Longest Common Subsequence
- `huffman/` — Huffman Coding
- `rod_cutting/` — Rod Cutting DP
- `knapsack_bnb/` — 0/1 Knapsack (Branch & Bound, binary decision tree)
- `string_matching/` — Naive vs Rabin–Karp
- `bellman_ford/` — Bellman–Ford (with/without negative cycle)

## Quick start

Most folders follow the same workflow:

1. Compile the C++ file (example)
2. Generate random inputs
3. Run all benchmark cases
4. Plot results

Example (Bellman–Ford):

```zsh
cd bellman_ford
clang++ -std=c++17 -O2 bellman_ford.cpp -o bellman_ford
python3 random_inputs.py
python3 run_all_cases.py
python3 plot_results.py
```

Then open:
- `bellman_ford/charts/index.html`

## Notes

- These benchmarks are micro-timings; results will vary by machine and OS.
- Python scripts are dependency-free (no matplotlib) so they work on most lab machines.

## License

Add a license if you plan to share publicly (MIT is a common choice).
