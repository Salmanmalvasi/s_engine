from __future__ import annotations

import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# Text sizes to benchmark.
# Note: naive is O(n*m), so we keep sizes moderate.
TEXT_SIZES = [100, 200, 500, 1000, 2000, 5000, 10000]

random.seed(42)
ALPHABET = "abcd"  # small alphabet increases repeats (more realistic for matching)


def rand_string(n: int) -> str:
    return "".join(random.choice(ALPHABET) for _ in range(n))


def build_case(n_text: int) -> tuple[str, str]:
    text = rand_string(n_text)

    # pattern length: ~1% of text, clamped
    m = max(4, min(64, n_text // 100))

    # ensure at least one match by copying a substring from the text
    start = random.randint(0, n_text - m)
    pattern = text[start : start + m]

    # sometimes mutate pattern slightly (still usually has matches, but not always)
    if random.random() < 0.25:
        idx = random.randrange(m)
        new_char = random.choice([c for c in ALPHABET if c != pattern[idx]])
        pattern = pattern[:idx] + new_char + pattern[idx + 1 :]

    return text, pattern


def main() -> None:
    for n in TEXT_SIZES:
        text, pattern = build_case(n)
        out = SCRIPT_DIR / f"random_{n}.txt"
        with out.open("w") as f:
            # runner will prepend algo id
            f.write(text + "\n")
            f.write(pattern + "\n")

    print(f"Generated {len(TEXT_SIZES)} input files in {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
