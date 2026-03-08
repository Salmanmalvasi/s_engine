from __future__ import annotations
import re, subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BINARY = SCRIPT_DIR / "floyd_warshall"
RESULTS = SCRIPT_DIR / "results.txt"
SIZES = [(20,120),(30,250),(40,500),(60,1200),(80,2000)]

TIME_RE = re.compile(r"Time taken:\s*([0-9.]+)\s*seconds")
NEG_RE  = re.compile(r"Negative cycle detected")
RP_RE   = re.compile(r"ReachablePairs:\s*(\d+)")
SUM_RE  = re.compile(r"SumDist:\s*(-?\d+)")

def run_case(inp):
    proc = subprocess.run([str(BINARY)], input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out  = proc.stdout.decode("utf-8", errors="replace")
    t    = TIME_RE.search(out)
    if not t: raise RuntimeError(f"No time in output:\n{out}")
    neg  = bool(NEG_RE.search(out))
    rp   = int(RP_RE.search(out).group(1))  if RP_RE.search(out)  else -1
    sumd = int(SUM_RE.search(out).group(1)) if SUM_RE.search(out) else 0
    return float(t.group(1)), neg, rp, sumd

if not BINARY.exists():
    raise SystemExit("floyd_warshall binary not found.")

with RESULTS.open("w") as f:
    f.write("Algorithm: Floyd-Warshall (All-Pairs Shortest Paths)\n")
    f.write("ILP 13 - Floyd-Warshall Timing Results\n")
    f.write("=====================================\n")
    for n, m in SIZES:
        for tag in ("pos","neg"):
            path = SCRIPT_DIR / f"random_{n}_{m}_{tag}.txt"
            if not path.exists():
                f.write(f"{path.name}: MISSING\n"); continue
            t, neg, rp, sumd = run_case(path.read_bytes())
            line = (f"algo=Floyd-Warshall, n={n}, m={m}, case={tag}: time={t} seconds, "
                    f"negCycle={1 if neg else 0}, reachablePairs={rp}, sumDist={sumd}\n")
            print(line.strip()); f.write(line)

print(f"\nResults written to {RESULTS}")
