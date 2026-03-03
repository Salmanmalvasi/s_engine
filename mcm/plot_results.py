from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_PATH = SCRIPT_DIR / "results.txt"
OUTPUT_DIR = SCRIPT_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

pattern = re.compile(r"n=(\d+): time=([0-9.e\-]+) seconds")

data = []
for line in RESULTS_PATH.read_text().splitlines():
    match = pattern.search(line)
    if match:
        n = int(match.group(1))
        time_str = match.group(2)
        time_val = float(time_str)
        data.append((n, time_val))

data.sort()

# Write data table as CSV
csv_path = SCRIPT_DIR / "results_table.csv"
with csv_path.open("w") as f:
    f.write("n,time_seconds\n")
    for n, t in data:
        f.write(f"{n},{t}\n")

# Generate SVG graph
SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <style>
    .axis {{ stroke: #555; stroke-width: 1; }}
    .grid {{ stroke: #ccc; stroke-width: 0.5; }}
    .label {{ font: 12px sans-serif; fill: #333; }}
  </style>
  <rect width="100%" height="100%" fill="#fff" />
  {content}
</svg>"""

def normalize(value, min_value, max_value, length):
    if max_value - min_value == 0:
        return length / 2
    return (value - min_value) / (max_value - min_value) * length

def build_svg(title, entries, filename):
    width, height = 900, 500
    margin = 80
    plot_width = width - margin * 2
    plot_height = height - margin * 2

    if not entries:
        return

    sizes = [e[0] for e in entries]
    times = [e[1] for e in entries]

    x_min, x_max = min(sizes), max(sizes)
    y_min, y_max = 0, max(times)

    content = []
    content.append(f'  <text x="{width/2}" y="30" text-anchor="middle" class="label" font-size="18">{title}</text>')
    content.append(f'  <line class="axis" x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" />')
    content.append(f'  <line class="axis" x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" />')
    content.append(f'  <text x="{width/2}" y="{height-20}" text-anchor="middle" class="label">n (number of matrices + 1)</text>')
    content.append(f'  <text x="20" y="{height/2}" text-anchor="middle" transform="rotate(-90 20,{height/2})" class="label">Time (s)</text>')

    for step in range(5):
        ratio = step / 4
        x = margin + ratio * plot_width
        label = round(x_min + ratio * (x_max - x_min))
        content.append(f'  <line class="grid" x1="{x}" y1="{margin}" x2="{x}" y2="{height-margin}" />')
        content.append(f'  <text x="{x}" y="{height-margin+20}" text-anchor="middle" class="label">{label}</text>')
        y = margin + ratio * plot_height
        label_val = y_max - ratio * (y_max - y_min)
        content.append(f'  <line class="grid" x1="{margin}" y1="{y}" x2="{width-margin}" y2="{y}" />')
        content.append(f'  <text x="{margin-10}" y="{y+4}" text-anchor="end" class="label">{label_val:.2e}</text>')

    poly = []
    for n, time in entries:
        x = margin + normalize(n, x_min, x_max, plot_width)
        y = height - margin - normalize(time, y_min, y_max, plot_height)
        poly.append(f"{x},{y}")
    points = " ".join(poly)
    content.append(f'  <polyline fill="none" stroke="#1f77b4" stroke-width="2" points="{points}" />')
    for n, time in entries:
        x = margin + normalize(n, x_min, x_max, plot_width)
        y = height - margin - normalize(time, y_min, y_max, plot_height)
        content.append(f'  <circle cx="{x}" cy="{y}" r="4" fill="#1f77b4" />')

    svg = SVG_TEMPLATE.format(width=width, height=height, content="\n".join(content))
    (OUTPUT_DIR / filename).write_text(svg)

build_svg("MCM Time Complexity (Random Inputs)", data, "mcm_timing.svg")

# Create HTML viewer
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MCM Charts</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; background: #f4f4f4; }
    h1 { margin-bottom: 0.5rem; }
    section { margin-bottom: 2rem; background: #ffffff; padding: 1rem; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,.08); }
    table { border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 8px 16px; text-align: right; }
    th { background: #f0f0f0; }
  </style>
</head>
<body>
  <h1>Matrix Chain Multiplication Timing</h1>
  <section>
    <h2>Timing Graph</h2>
    <object type="image/svg+xml" data="mcm_timing.svg" width="900" height="500"></object>
    <p><a href="mcm_timing.svg" target="_blank">Open chart in new tab</a></p>
  </section>
  <section>
    <h2>Data Table</h2>
    <table>
      <tr><th>n</th><th>Time (seconds)</th></tr>
"""
for n, t in data:
    html_content += f"      <tr><td>{n}</td><td>{t:.2e}</td></tr>\n"
html_content += """    </table>
  </section>
</body>
</html>
"""
(OUTPUT_DIR / "index.html").write_text(html_content)

print(f"CSV table: {csv_path}")
print(f"Charts and viewer: {OUTPUT_DIR / 'index.html'}")
