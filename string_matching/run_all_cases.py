from __future__ import annotations

import re
import subprocess
from pathlib import Path

TEXT_SIZES = [100, 200, 500, 1000, 2000, 5000, 10000]
ALGOS = {
    0: "Naive",
    1: "Rabin-Karp",
}

SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "string_matching"
RESULTS = SCRIPT_DIR / "results.txt"

TIME_RE = re.compile(r"Time taken:\s*([0-9.]+)\s*seconds")
MATCHES_RE = re.compile(r"Matches:\s*(\d+)")


def run_one(algo: int, text: str, pattern: str) -> tuple[float, int, str]:
    inp = f"{algo}\n{text}\n{pattern}\n".encode()
    proc = subprocess.run(
        [str(BINARY)],
        input=inp,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    out = proc.stdout.decode("utf-8", errors="replace")

    t = TIME_RE.search(out)
    m = MATCHES_RE.search(out)
    if not t or not m:
        raise RuntimeError(f"Could not parse output:\n{out}")

    return float(t.group(1)), int(m.group(1)), out


def main() -> None:
    if not BINARY.exists():
        raise SystemExit("string_matching binary not found. Compile string_matching.cpp first.")

    with RESULTS.open("w") as f:
        f.write("ILP 11 - Naive String Matching vs Rabin-Karp\n")
        f.write("===========================================\n")

        for n in TEXT_SIZES:
            inp_file = SCRIPT_DIR / f"random_{n}.txt"
            if not inp_file.exists():
                f.write(f"random_{n}.txt: MISSING\n")
                continue

            text, pattern = inp_file.read_text().splitlines()[:2]

            for algo, name in ALGOS.items():
                t, matches, _ = run_one(algo, text, pattern)
                line = f"algo={name}, n={n}, m={len(pattern)}: time={t} seconds, matches={matches}\n"
                print(line.strip())
                f.write(line)

    print(f"\nResults written to {RESULTS}")


if __name__ == "__main__":
    main()
