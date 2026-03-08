# ILP 13 — Floyd–Warshall

C++ implementation of Floyd–Warshall (All-Pairs Shortest Paths).

## Input

```
n m
u v w  (m lines)
```

## Output

- Algorithm name
- Negative cycle detected / not
- ReachablePairs, SumDist, Time taken

## Complexity

O(n³)

## Run

```zsh
clang++ -std=c++17 -O2 floyd_warshall.cpp -o floyd_warshall
python3 random_inputs.py
python3 run_all_cases.py
python3 plot_results.py
```

Open `charts/index.html` in your browser.
