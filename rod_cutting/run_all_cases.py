import subprocess
from pathlib import Path

SIZES = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "rod_cutting"
OUTPUT_LOG = SCRIPT_DIR / "results.txt"

if not BINARY.exists():
    raise SystemExit("rod_cutting binary not found. Please compile rod_cutting.cpp first.")

results = []

with OUTPUT_LOG.open("w") as log:
    log.write("Rod Cutting Timing Results\n")
    log.write("==========================\n")
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
        revenue = "N/A"
        
        for line in output.splitlines():
            if line.startswith("Time taken:"):
                time_taken = line.split(":", 1)[1].strip()
            if line.startswith("Maximum Revenue:"):
                revenue = line.split(":", 1)[1].strip()
        
        log.write(f"n={n}: time={time_taken}\n")
        print(f"n={n}: time={time_taken}, revenue={revenue}")
        results.append((n, time_taken))

print(f"\nResults written to {OUTPUT_LOG.resolve()}")
