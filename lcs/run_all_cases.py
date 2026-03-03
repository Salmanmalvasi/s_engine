import subprocess
from pathlib import Path
import re

SIZES = [100, 500, 1000, 2000, 3000, 5000]
SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "lcs"
OUTPUT_LOG = SCRIPT_DIR / "results.txt"

if not BINARY.exists():
    raise SystemExit("lcs binary not found. Please compile lcs.cpp first.")

results = []

with OUTPUT_LOG.open("w") as log:
    log.write("LCS Timing Results\n")
    log.write("==================\n")
    for n in SIZES:
        input_file = SCRIPT_DIR / f"random_{n}.txt"
        if not input_file.exists():
            log.write(f"random_{n}.txt: MISSING\n")
            print(f"random_{n}.txt: MISSING")
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
        lcs_length = "N/A"
        lcs_string = "N/A"
        for line in output.splitlines():
            if line.startswith("Time taken:"):
                time_taken = line.split(":", 1)[1].strip()
            if line.startswith("LCS Length:"):
                lcs_length = line.split(":", 1)[1].strip()
            if line.startswith("LCS String:"):
                lcs_string = line.split(":", 1)[1].strip()
        log.write(f"n={n}: time={time_taken}, lcs_length={lcs_length}\n")
        print(f"n={n}: time={time_taken}, lcs_length={lcs_length}, lcs_string={lcs_string[:50] if len(lcs_string) > 50 else lcs_string}...")
        results.append((n, time_taken, lcs_length))

print(f"\nResults written to {OUTPUT_LOG.resolve()}")
