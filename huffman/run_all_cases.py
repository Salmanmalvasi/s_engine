import subprocess
from pathlib import Path

SIZES = [10, 50, 100, 500, 1000, 5000, 10000]
SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "huffman"
OUTPUT_LOG = SCRIPT_DIR / "results.txt"

if not BINARY.exists():
    raise SystemExit("huffman binary not found. Please compile huffman.cpp first.")

results = []

with OUTPUT_LOG.open("w") as log:
    log.write("Huffman Coding Timing Results\n")
    log.write("==============================\n")
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
        num_symbols = "N/A"
        
        # Extract some sample codes for display
        codes_sample = []
        for line in output.splitlines():
            if line.startswith("Time taken:"):
                time_taken = line.split(":", 1)[1].strip()
            if line.startswith("Number of symbols:"):
                num_symbols = line.split(":", 1)[1].strip()
            if " : " in line and not line.startswith("Time") and not line.startswith("Number"):
                codes_sample.append(line)
        
        log.write(f"n={n}: time={time_taken}\n")
        sample_str = ", ".join(codes_sample[:3]) if codes_sample else "N/A"
        print(f"n={n}: time={time_taken}, sample_codes=[{sample_str}...]")
        results.append((n, time_taken))

print(f"\nResults written to {OUTPUT_LOG.resolve()}")
