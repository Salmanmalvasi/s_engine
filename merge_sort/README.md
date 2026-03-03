# Merge Sort Assignment

This folder contains the C++ merge sort implementation and Python scripts to generate input files for best, worst, and average case scenarios.

## Files
- `merge_sort.cpp` - Reads `n` and `n` integers from `stdin`, runs merge sort, and reports the sorting time plus the first 10 sorted values.
- `ascending_inputs.py` - Generates ascending input files (`ascending_1000.txt`, ..., `ascending_100000.txt`).
- `descending_inputs.py` - Generates descending input files (`descending_1000.txt`, ..., `descending_100000.txt`).
- `random_inputs.py` - Generates random input files (`random_1000.txt`, ..., `random_100000.txt`).

## How to run
1. Generate the desired input files (adjust `SIZES` in the Python scripts if needed):
   ```bash
   python3 ascending_inputs.py
   python3 descending_inputs.py
   python3 random_inputs.py
   ```
   Each script writes the corresponding input files in the same folder.

2. Compile `merge_sort.cpp` with clang++ or g++:
   ```bash
   clang++ -std=c++17 -O2 merge_sort.cpp -o merge_sort
   ```

3. Run the program using one of the generated files:
   ```bash
   ./merge_sort < random_1000.txt
   ```
   Repeat with other files (`random_5000.txt`, `ascending_25000.txt`, etc.) and note the reported time.

4. You can record the time taken for each input size and plot `input size vs time` in Excel.

## Recording and Visualizing Results

- Use `run_all_cases.py` to execute the compiled binary on every generated input, and it will write out timings and samples into `results.txt`:
   ```bash
   python3 run_all_cases.py
   ```
- Then run `plot_results.py` to create four SVG charts (ascending, descending, random, and combined) under the `charts/` folder:
   ```bash
   python3 plot_results.py
   ```
- You now have four ready-made graphs (`charts/ascending_timing.svg`, `charts/descending_timing.svg`, `charts/random_timing.svg`, and `charts/combined_timing.svg`) that you can open or embed in your report to compare the input scenarios. If double-clicking the SVGs isn’t convenient, open `charts/index.html` in a browser—each chart is embedded there along with links to view them full-screen or save as PNG.
