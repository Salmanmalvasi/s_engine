import os, subprocess, re

print("Compiling line_segment.cpp...")
os.system("clang++ -std=c++17 -O2 line_segment.cpp -o line_segment")

sizes = [1000, 5000, 10000, 20000, 50000]
results = []
print("Running benchmarks...\n")

for n in sizes:
    filename = f"random_{n}.txt"
    if not os.path.exists(filename): continue
    # Note: executing as ./line_segment filename
    out = subprocess.check_output(f"./line_segment {filename}", shell=True).decode()
    print(out.strip()) 
    
    # Parse the nanoseconds output
    time_match = re.search(r"Time Taken \(ns\)\s+:\s+(\d+)", out)
    if time_match:
        ns = float(time_match.group(1))
        t_sec = ns / 1e9 # Convert to seconds for the graph
        results.append((n, t_sec))

with open("results.txt", "w") as f:
    f.write("Algorithm: Line Segment Intersection\n")
    for n, t in results:
        f.write(f"algo=Line-Segment, n={n}, case=random: {t:.6f} seconds\n")
