from __future__ import annotations

from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_PATH = SCRIPT_DIR / "results.txt"
OUTPUT_DIR = SCRIPT_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

pattern = re.compile(r"n=(\d+): time=([0-9.e\-]+) seconds")

data: list[tuple[int, float]] = []
if RESULTS_PATH.exists():
    for line in RESULTS_PATH.read_text().splitlines():
        m = pattern.search(line)
        if m:
            data.append((int(m.group(1)), float(m.group(2))))

data.sort(key=lambda x: x[0])

csv_path = SCRIPT_DIR / "results_table.csv"
with csv_path.open("w") as f:
    f.write("n,time_seconds\n")
    for n, t in data:
        f.write(f"{n},{t}\n")

SVG_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <style>
    .axis {{ stroke: #555; stroke-width: 1; }}
    .grid {{ stroke: #d0d0d0; stroke-width: 0.7; }}
    .label {{ font: 12px system-ui, -apple-system, Segoe UI, sans-serif; fill: #222; }}
  </style>
  <rect width="100%" height="100%" fill="#fff" />
  {content}
</svg>
""".strip()


def normalize(value: float, min_value: float, max_value: float, length: float) -> float:
    if max_value - min_value == 0:
        return length / 2
    return (value - min_value) / (max_value - min_value) * length


def build_svg(title: str, entries: list[tuple[int, float]], filename: str) -> None:
    if not entries:
        return

    width, height = 900, 500
    margin = 80
    plot_width = width - margin * 2
    plot_height = height - margin * 2

    xs = [e[0] for e in entries]
    ys = [e[1] for e in entries]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = 0.0, max(ys)

    content: list[str] = []

    content.append(
        f'<text x="{width/2}" y="30" text-anchor="middle" class="label" font-size="18">{title}</text>'
    )
    # axes
    content.append(
        f'<line class="axis" x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" />'
    )
    content.append(
        f'<line class="axis" x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" />'
    )

    content.append(
        f'<text x="{width/2}" y="{height-20}" text-anchor="middle" class="label">Number of items (n)</text>'
    )
    content.append(
        f'<text x="20" y="{height/2}" text-anchor="middle" transform="rotate(-90 20,{height/2})" class="label">Time (s)</text>'
    )

    # grid + ticks
    for step in range(5):
        ratio = step / 4
        x = margin + ratio * plot_width
        x_label = round(x_min + ratio * (x_max - x_min))
        content.append(
            f'<line class="grid" x1="{x}" y1="{margin}" x2="{x}" y2="{height-margin}" />'
        )
        content.append(
            f'<text x="{x}" y="{height-margin+20}" text-anchor="middle" class="label">{x_label}</text>'
        )

        y = margin + ratio * plot_height
        y_label = y_max - ratio * (y_max - y_min)
        content.append(
            f'<line class="grid" x1="{margin}" y1="{y}" x2="{width-margin}" y2="{y}" />'
        )
        content.append(
            f'<text x="{margin-10}" y="{y+4}" text-anchor="end" class="label">{y_label:.6f}</text>'
        )

    # polyline points
    pts = []
    for n, t in entries:
        x = margin + normalize(n, x_min, x_max, plot_width)
        y = height - margin - normalize(t, y_min, y_max, plot_height)
        pts.append(f"{x},{y}")

    content.append(
        f'<polyline fill="none" stroke="#1f77b4" stroke-width="2" points="{" ".join(pts)}" />'
    )

    for n, t in entries:
        x = margin + normalize(n, x_min, x_max, plot_width)
        y = height - margin - normalize(t, y_min, y_max, plot_height)
        content.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#1f77b4" />')

    svg = SVG_TEMPLATE.format(width=width, height=height, content="\n  ".join(content))
    (OUTPUT_DIR / filename).write_text(svg)


build_svg(
    "0/1 Knapsack - Branch and Bound (Binary Decision Tree)",
    data,
    "knapsack_bnb_timing.svg",
)

# HTML viewer
html = [
    "<!DOCTYPE html>",
    "<html lang=\"en\">",
    "<head>",
    "  <meta charset=\"UTF-8\">",
    "  <title>Knapsack BnB Charts</title>",
    "  <style>",
    "    body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; background: #f4f4f4; }",
    "    section { margin-bottom: 2rem; background: #fff; padding: 1rem; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,.08); }",
    "    table { border-collapse: collapse; margin-top: 1rem; }",
    "    th, td { border: 1px solid #ccc; padding: 8px 14px; text-align: right; }",
    "    th { background: #f0f0f0; }",
    "  </style>",
    "</head>",
    "<body>",
    "  <h1>0/1 Knapsack (Branch and Bound)</h1>",
    "  <section>",
    "    <h2>Timing Graph</h2>",
    "    <object type=\"image/svg+xml\" data=\"knapsack_bnb_timing.svg\" width=\"900\" height=\"500\"></object>",
    "    <p><a href=\"knapsack_bnb_timing.svg\" target=\"_blank\">Open chart in new tab</a></p>",
    "  </section>",
    "  <section>",
    "    <h2>Data Table</h2>",
    "    <table>",
    "      <tr><th>n</th><th>time (s)</th></tr>",
]

for n, t in data:
    html.append(f"      <tr><td>{n}</td><td>{t:.6f}</td></tr>")

html += [
    "    </table>",
    "  </section>",
    "</body>",
    "</html>",
]

(OUTPUT_DIR / "index.html").write_text("\n".join(html))

print(f"CSV table: {csv_path}")
print(f"Charts and viewer: {OUTPUT_DIR / 'index.html'}")
