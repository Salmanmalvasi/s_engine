from __future__ import annotations

from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_PATH = SCRIPT_DIR / "results.txt"
OUTPUT_DIR = SCRIPT_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

LINE_RE = re.compile(
    r"algo=(.+?), n=(\d+), m=(\d+): time=([0-9.e\-]+) seconds, matches=(\d+)"
)

series: dict[str, list[tuple[int, float, int, int]]] = {}
# algo -> list of (n, time, m, matches)

if RESULTS_PATH.exists():
    for line in RESULTS_PATH.read_text().splitlines():
        m = LINE_RE.search(line)
        if not m:
            continue
        algo = m.group(1).strip()
        n = int(m.group(2))
        pat_len = int(m.group(3))
        time_s = float(m.group(4))
        matches = int(m.group(5))
        series.setdefault(algo, []).append((n, time_s, pat_len, matches))

for k in series:
    series[k].sort(key=lambda x: x[0])

# CSV
csv_path = SCRIPT_DIR / "results_table.csv"
with csv_path.open("w") as f:
    f.write("algo,n,m,time_seconds,matches\n")
    for algo, rows in series.items():
        for n, t, mlen, matches in rows:
            f.write(f"{algo},{n},{mlen},{t},{matches}\n")

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


def build_svg_multi(title: str, series_data: dict[str, list[tuple[int, float]]], filename: str) -> None:
    if not series_data:
        return

    width, height = 900, 520
    margin = 80
    plot_width = width - margin * 2
    plot_height = height - margin * 2

    all_x = [n for rows in series_data.values() for (n, _) in rows]
    all_y = [t for rows in series_data.values() for (_, t) in rows]

    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = 0.0, max(all_y)

    palette = [
        ("#1f77b4", "Naive"),
        ("#d62728", "Rabin-Karp"),
        ("#2ca02c", "Other"),
        ("#9467bd", "Other2"),
    ]

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
        f'<text x="{width/2}" y="{height-20}" text-anchor="middle" class="label">Text length (n)</text>'
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

    # draw each series
    legend_y = margin - 20
    legend_x = margin

    for idx, (name, rows) in enumerate(series_data.items()):
        color = palette[idx % len(palette)][0]

        pts = []
        for n, t in rows:
            x = margin + normalize(n, x_min, x_max, plot_width)
            y = height - margin - normalize(t, y_min, y_max, plot_height)
            pts.append(f"{x},{y}")

        content.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{" ".join(pts)}" />'
        )
        for n, t in rows:
            x = margin + normalize(n, x_min, x_max, plot_width)
            y = height - margin - normalize(t, y_min, y_max, plot_height)
            content.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}" />')

        # legend
        lx = legend_x + idx * 160
        content.append(f'<rect x="{lx}" y="{legend_y}" width="14" height="14" fill="{color}" />')
        content.append(
            f'<text x="{lx+20}" y="{legend_y+12}" class="label">{name}</text>'
        )

    svg = SVG_TEMPLATE.format(width=width, height=height, content="\n  ".join(content))
    (OUTPUT_DIR / filename).write_text(svg)


# Build per-algorithm chart + combined chart
for algo, rows in series.items():
    build_svg_multi(
        f"{algo} String Matching Timing",
        {algo: [(n, t) for (n, t, _, _) in rows]},
        f"{algo.lower().replace(' ', '_')}_timing.svg",
    )

build_svg_multi(
    "Naive vs Rabin-Karp (String Matching)",
    {algo: [(n, t) for (n, t, _, _) in rows] for (algo, rows) in series.items()},
    "combined_timing.svg",
)

# HTML viewer
html = [
    "<!DOCTYPE html>",
    "<html lang=\"en\">",
    "<head>",
    "  <meta charset=\"UTF-8\">",
    "  <title>ILP 11 - String Matching Charts</title>",
    "  <style>",
    "    body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; background: #f4f4f4; }",
    "    section { margin-bottom: 2rem; background: #fff; padding: 1rem; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,.08); }",
    "    table { border-collapse: collapse; margin-top: 1rem; width: 100%; }",
    "    th, td { border: 1px solid #ccc; padding: 8px 14px; text-align: right; }",
    "    th { background: #f0f0f0; text-align: right; }",
    "    td:first-child, th:first-child { text-align: left; }",
    "  </style>",
    "</head>",
    "<body>",
    "  <h1>ILP 11 — Naive String Matching & Rabin–Karp</h1>",
    "  <section>",
    "    <h2>Combined Timing Graph</h2>",
    "    <object type=\"image/svg+xml\" data=\"combined_timing.svg\" width=\"900\" height=\"520\"></object>",
    "    <p><a href=\"combined_timing.svg\" target=\"_blank\">Open combined chart</a></p>",
    "  </section>",
]

for algo in series.keys():
    fname = f"{algo.lower().replace(' ', '_')}_timing.svg"
    html += [
        "  <section>",
        f"    <h2>{algo}</h2>",
        f"    <object type=\"image/svg+xml\" data=\"{fname}\" width=\"900\" height=\"520\"></object>",
        f"    <p><a href=\"{fname}\" target=\"_blank\">Open chart</a></p>",
        "  </section>",
    ]

html += [
    "  <section>",
    "    <h2>Data Table</h2>",
    "    <table>",
    "      <tr><th>Algorithm</th><th>n</th><th>m</th><th>time (s)</th><th>matches</th></tr>",
]

for algo, rows in series.items():
    for n, t, mlen, matches in rows:
        html.append(
            f"      <tr><td>{algo}</td><td>{n}</td><td>{mlen}</td><td>{t:.6f}</td><td>{matches}</td></tr>"
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
