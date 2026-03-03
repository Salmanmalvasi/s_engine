import subprocess
from pathlib import Path

SIZES = [1000, 5000, 25000, 50000, 100000]
CATEGORIES = ["ascending", "descending", "random"]
BINARY_DIR = Path(__file__).resolve().parent
BINARY = BINARY_DIR / "merge_sort"
OUTPUT_LOG = BINARY_DIR / "results.txt"

if not BINARY.exists():
    raise SystemExit("merge_sort binary not found. Please compile merge_sort.cpp first.")

with OUTPUT_LOG.open("w") as log:
    log.write("Merge sort batch run results\n")
    log.write("===============================\n")
    for category in CATEGORIES:
        for n in SIZES:
            input_file = Path(f"{category}_{n}.txt")
            if not input_file.exists():
                log.write(f"{input_file.name}: MISSING\n")
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
            for line in output.splitlines():
                if line.startswith("Time taken:"):
                    time_taken = line.split(":", 1)[1].strip()
            sample = "".join(output.splitlines()[1:3]) if output else ""
            log.write(f"{input_file.name}: {time_taken} | sample_output: {sample}\n")
            if process.returncode != 0:
                log.write(f"  [non-zero exit: {process.returncode}] stderr: {process.stderr.strip()}\n")

print(f"Execution complete, details written to {OUTPUT_LOG}")
