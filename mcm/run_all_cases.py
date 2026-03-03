import subprocess
from pathlib import Path
import re

SIZES = [5, 10, 15, 20, 25, 30, 40, 50]
SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "mcm"
OUTPUT_LOG = SCRIPT_DIR / "results.txt"

if not BINARY.exists():
    raise SystemExit("mcm binary not found. Please compile mcm.cpp first.")

results = []

with OUTPUT_LOG.open("w") as log:
    log.write("MCM Timing Results\n")
    log.write("==================\n")
    for n in SIZES:
        input_file = SCRIPT_DIR / f"random_{n}.txt"
        if not input_file.exists():
            log.write(f"random_{n}.txt: MISSING\n")
            continue
        process = subprocess.run(
            [str(BINARY)],
            stdin=input_file.open(),
            capture_output=True,
            text=True,
            check=False,
        )
        output = process.stdout.strip()
        time_taken = "N/A"
        min_cost = "N/A"
        for line in output.splitlines():
            if line.startswith("Time taken:"):
                time_taken = line.split(":", 1)[1].strip()
            if line.startswith("Minimum Cost:"):
                min_cost = line.split(":", 1)[1].strip()
        log.write(f"n={n}: time={time_taken}, min_cost={min_cost}\n")
        results.append((n, time_taken, min_cost))

print(f"Results written to {OUTPUT_LOG.resolve()}")
