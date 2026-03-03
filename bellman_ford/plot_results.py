from __future__ import annotations

from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_PATH = SCRIPT_DIR / "results.txt"
OUTPUT_DIR = SCRIPT_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

LINE_RE = re.compile(
    r"algo=Bellman-Ford, n=(\d+), m=(\d+), case=(pos|neg): time=([0-9.e\-]+) seconds, negCycle=(\d), reachable=(\-?\d+), sumDist=(\-?\d+)"
)

rows: list[dict] = []
if RESULTS_PATH.exists():
    for line in RESULTS_PATH.read_text().splitlines():
        m = LINE_RE.search(line)
        if not m:
            continue
        rows.append(
            {
                "n": int(m.group(1)),
                "m": int(m.group(2)),
                "case": m.group(3),
                "time": float(m.group(4)),
                "neg": int(m.group(5)),
                "reachable": int(m.group(6)),
                "sumDist": int(m.group(7)),
            }
        )

# CSV
csv_path = SCRIPT_DIR / "results_table.csv"
with csv_path.open("w") as f:
    f.write("n,m,case,time_seconds,negCycle,reachable,sumDist\n")
    for r in rows:
        f.write(
            f"{r['n']},{r['m']},{r['case']},{r['time']},{r['neg']},{r['reachable']},{r['sumDist']}\n"
        )

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


def build_svg_two_series(title: str, series: dict[str, list[tuple[int, float]]], filename: str) -> None:
    if not series:
        return

    width, height = 900, 520
    margin = 80
    plot_width = width - margin * 2
    plot_height = height - margin * 2

    all_x = [x for s in series.values() for (x, _) in s]
    all_y = [y for s in series.values() for (_, y) in s]
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = 0.0, max(all_y)

    content: list[str] = []
    content.append(
        f'<text x="{width/2}" y="30" text-anchor="middle" class="label" font-size="18">{title}</text>'
    )
    content.append(
        f'<line class="axis" x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" />'
    )
    content.append(
        f'<line class="axis" x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" />'
    )

    content.append(
        f'<text x="{width/2}" y="{height-20}" text-anchor="middle" class="label">Number of vertices (n)</text>'
    )
    content.append(
        f'<text x="20" y="{height/2}" text-anchor="middle" transform="rotate(-90 20,{height/2})" class="label">Time (s)</text>'
    )

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

    colors = {"pos": "#1f77b4", "neg": "#d62728"}
    legend_y = margin - 20
    legend_x = margin

    for idx, key in enumerate(["pos", "neg"]):
        if key not in series:
            continue
        color = colors[key]
        pts = []
        for n, t in series[key]:
            x = margin + normalize(n, x_min, x_max, plot_width)
            y = height - margin - normalize(t, y_min, y_max, plot_height)
            pts.append(f"{x},{y}")

        content.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{" ".join(pts)}" />'
        )
        for n, t in series[key]:
            x = margin + normalize(n, x_min, x_max, plot_width)
            y = height - margin - normalize(t, y_min, y_max, plot_height)
            content.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}" />')

        lx = legend_x + idx * 170
        label = "No Neg Cycle" if key == "pos" else "Neg Cycle"
        content.append(f'<rect x="{lx}" y="{legend_y}" width="14" height="14" fill="{color}" />')
        content.append(
            f'<text x="{lx+20}" y="{legend_y+12}" class="label">{label}</text>'
        )

    svg = SVG_TEMPLATE.format(width=width, height=height, content="\n  ".join(content))
    (OUTPUT_DIR / filename).write_text(svg)


# Build series: pos and neg plotted vs n
pos = [(r["n"], r["time"]) for r in rows if r["case"] == "pos"]
neg = [(r["n"], r["time"]) for r in rows if r["case"] == "neg"]
pos.sort()
neg.sort()

build_svg_two_series(
    "Bellman–Ford Timing (O(VE)) — with/without Negative Cycle",
    {"pos": pos, "neg": neg},
    "bellman_ford_timing.svg",
)

# HTML viewer
html: list[str] = [
    "<!DOCTYPE html>",
    "<html lang=\"en\">",
    "<head>",
    "  <meta charset=\"UTF-8\">",
    "  <title>ILP 12 - Bellman-Ford</title>",
    "  <style>",
    "    body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; background: #f4f4f4; }",
    "    section { margin-bottom: 2rem; background: #fff; padding: 1rem; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,.08); }",
    "    table { border-collapse: collapse; margin-top: 1rem; width: 100%; }",
    "    th, td { border: 1px solid #ccc; padding: 8px 14px; text-align: right; }",
    "    th { background: #f0f0f0; }",
    "    td:first-child, th:first-child { text-align: left; }",
    "  </style>",
    "</head>",
    "<body>",
    "  <h1>ILP 12 — Bellman–Ford</h1>",
    "  <p><strong>Algorithm:</strong> Bellman–Ford (Single Source Shortest Path)</p>",
    "  <section>",
    "    <h2>Timing Graph</h2>",
    "    <object type=\"image/svg+xml\" data=\"bellman_ford_timing.svg\" width=\"900\" height=\"520\"></object>",
    "    <p><a href=\"bellman_ford_timing.svg\" target=\"_blank\">Open chart</a></p>",
    "  </section>",
    "  <section>",
    "    <h2>Data Table</h2>",
    "    <table>",
    "      <tr><th>case</th><th>n</th><th>m</th><th>time (s)</th><th>negCycle</th><th>reachable</th><th>sumDist</th></tr>",
]

for r in sorted(rows, key=lambda r: (r["n"], r["case"])):
    html.append(
        f"      <tr><td>{r['case']}</td><td>{r['n']}</td><td>{r['m']}</td><td>{r['time']:.6f}</td><td>{r['neg']}</td><td>{r['reachable']}</td><td>{r['sumDist']}</td></tr>"
    )

html += [
    "    </table>",
    "  </section>",
    "</body>",
    "</html>",
]

(OUTPUT_DIR / "index.html").write_text("\n".join(html))

print(f"CSV table: {csv_path}")
print(f"Charts and viewer: {OUTPUT_DIR / 'index.html'}")
