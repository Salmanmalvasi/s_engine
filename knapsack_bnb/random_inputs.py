from __future__ import annotations

import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# Keep sizes moderate: BnB can blow up exponentially on worst cases.
SIZES = [5, 10, 15, 20, 25, 30, 35, 40]

random.seed(42)


def generate_case(n: int) -> tuple[int, int, list[tuple[int, int]]]:
    # weights in [1..100], values in [1..200]
    items = [(random.randint(1, 100), random.randint(1, 200)) for _ in range(n)]

    total_w = sum(w for w, _ in items)
    # capacity ~ 35% to 60% of total weight (typical knapsack hardness)
    W = int(total_w * random.uniform(0.35, 0.60))
    W = max(1, W)

    return n, W, items


def main() -> None:
    for n in SIZES:
        n, W, items = generate_case(n)
        out = SCRIPT_DIR / f"random_{n}.txt"
        with out.open("w") as f:
            f.write(f"{n} {W}\n")
            for w, v in items:
                f.write(f"{w} {v}\n")

    print(f"Generated {len(SIZES)} input files in {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
