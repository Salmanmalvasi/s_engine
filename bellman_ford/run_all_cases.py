from __future__ import annotations

import re
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "bellman_ford"
RESULTS = SCRIPT_DIR / "results.txt"

# Must match generator naming
SIZES = [
    (20, 80),
    (50, 250),
    (100, 700),
    (200, 2000),
    (400, 6000),
]

TIME_RE = re.compile(r"Time taken:\s*([0-9.]+)\s*seconds")
NEG_RE = re.compile(r"Negative cycle detected")
REACH_RE = re.compile(r"Reachable:\s*(\d+)")
SUM_RE = re.compile(r"SumDist:\s*(-?\d+)")


def run_case(inp: bytes) -> tuple[float, bool, int, int, str]:
    proc = subprocess.run(
        [str(BINARY)],
        input=inp,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    out = proc.stdout.decode("utf-8", errors="replace")

    t = TIME_RE.search(out)
    if not t:
        raise RuntimeError(f"Could not parse time:\n{out}")

    neg = bool(NEG_RE.search(out))
    reach = int(REACH_RE.search(out).group(1)) if REACH_RE.search(out) else -1
    sumd = int(SUM_RE.search(out).group(1)) if SUM_RE.search(out) else 0

    return float(t.group(1)), neg, reach, sumd, out


def main() -> None:
    if not BINARY.exists():
        raise SystemExit("bellman_ford binary not found. Compile bellman_ford.cpp first.")

    with RESULTS.open("w") as f:
        f.write("Algorithm: Bellman-Ford (Single Source Shortest Path)\n")
        f.write("ILP 12 - Bellman-Ford Timing Results\n")
        f.write("===================================\n")

        for n, m in SIZES:
            for tag in ("pos", "neg"):
                file_path = SCRIPT_DIR / f"random_{n}_{m}_{tag}.txt"
                if not file_path.exists():
                    f.write(f"{file_path.name}: MISSING\n")
                    continue

                t, neg, reach, sumd, _ = run_case(file_path.read_bytes())
                line = (
                    f"algo=Bellman-Ford, n={n}, m={m}, case={tag}: time={t} seconds, "
                    f"negCycle={1 if neg else 0}, reachable={reach}, sumDist={sumd}\n"
                )
                print(line.strip())
                f.write(line)

    print(f"\nResults written to {RESULTS}")


if __name__ == "__main__":
    main()
