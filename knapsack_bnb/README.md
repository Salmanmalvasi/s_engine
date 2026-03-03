# ILP 10 — 0/1 Knapsack using Branch and Bound (Binary Tree)

This folder contains a complete “assignment-style” setup:

- C++ implementation of **0/1 Knapsack** using **Branch and Bound**.
- Random test-case generator.
- Benchmark runner that records timings.
- Plotter that generates an SVG graph + an HTML report.

## Input format

Each test file is:

```
n W
w1 v1
w2 v2
...
wn vn
```

Where:
- `n` = number of items
- `W` = knapsack capacity
- `wi` = weight of item `i`
- `vi` = value of item `i`

## Output format

The program prints:
- `Maximum Profit: <ans>`
- `Time taken: <seconds> seconds`

## What “binary tree” means here

At each level `i` (item `i`), the algorithm branches into two children:

- **Include** item `i`
- **Exclude** item `i`

A **best-first search** (priority queue by bound) explores the most promising nodes first.
The **bound** is computed using the **fractional knapsack** upper bound.

## How to run

1. Compile
2. Generate inputs
3. Run benchmarks (writes `results.txt`)
4. Plot charts (writes `charts/index.html`)

