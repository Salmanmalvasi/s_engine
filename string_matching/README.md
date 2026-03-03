# ILP 11 — Naive String Matching & Rabin–Karp

This folder contains a complete assignment-style setup:

- C++ program implementing:
  - **Naive String Matching**
  - **Rabin–Karp Algorithm** (rolling hash)
- Random test-case generator
- Runner to benchmark both algorithms and log results
- Plotter to generate SVG charts + an HTML report

## Input format (for the C++ program)

The executable reads:

```
algo
text
pattern
```

- `algo = 0` → Naive
- `algo = 1` → Rabin–Karp
- `text` and `pattern` must not contain spaces

## Output format

- `Matches: <count>`
- `Positions: ...` (only if matches exist)
- `Time taken: <seconds> seconds`

## Files

- `string_matching.cpp` — implementations + timing
- `random_inputs.py` — generates `random_<n>.txt`
- `run_all_cases.py` — runs both algos for each input, writes `results.txt`
- `plot_results.py` — creates `charts/*.svg`, `charts/index.html`, and `results_table.csv`

## Notes on complexity

- Naive matching worst case: $O(nm)$
- Rabin–Karp expected: $O(n + m)$ (worst-case $O(nm)$ if many collisions; we verify matches to be safe)

