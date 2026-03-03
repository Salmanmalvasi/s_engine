from __future__ import annotations

import re
import subprocess
from pathlib import Path

SIZES = [5, 10, 15, 20, 25, 30, 35, 40]
SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "knapsack_bnb"
OUTPUT_LOG = SCRIPT_DIR / "results.txt"

TIME_RE = re.compile(r"Time taken:\s*([0-9.]+)\s*seconds")
PROFIT_RE = re.compile(r"Maximum Profit:\s*(\d+)")


def run_case(input_path: Path) -> tuple[float, int, str]:
    proc = subprocess.run(
        [str(BINARY)],
        input=input_path.read_bytes(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    out = proc.stdout.decode("utf-8", errors="replace")

    t_match = TIME_RE.search(out)
    p_match = PROFIT_RE.search(out)
    if not t_match or not p_match:
        raise RuntimeError(f"Could not parse output for {input_path.name}:\n{out}")

    return float(t_match.group(1)), int(p_match.group(1)), out


def main() -> None:
    if not BINARY.exists():
        raise SystemExit("knapsack_bnb binary not found. Please compile knapsack_bnb.cpp first.")

    with OUTPUT_LOG.open("w") as log:
        log.write("0/1 Knapsack (Branch and Bound - Binary Tree) Timing Results\n")
        log.write("=========================================================\n")

        for n in SIZES:
            input_file = SCRIPT_DIR / f"random_{n}.txt"
            if not input_file.exists():
                log.write(f"random_{n}.txt: MISSING\n")
                continue

            t, profit, _ = run_case(input_file)
            line = f"n={n}: time={t} seconds, profit={profit}\n"
            print(line.strip())
            log.write(line)

    print(f"\nResults written to {OUTPUT_LOG}")


if __name__ == "__main__":
    main()
