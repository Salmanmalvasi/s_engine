from pathlib import Path
import re

RESULTS_PATH = Path("results.txt")
OUTPUT_DIR = Path("charts")
OUTPUT_DIR.mkdir(exist_ok=True)

pattern = re.compile(r"^(ascending|descending|random)_(\d+)\.txt: ([0-9.]+) seconds")

data = {"ascending": [], "descending": [], "random": []}

for line in RESULTS_PATH.read_text().splitlines():
    match = pattern.match(line)
    if not match:
        continue
    category, size, time_str = match.groups()
    data[category].append((int(size), float(time_str)))

COLORS = {"ascending": "#1f77b4", "descending": "#ff7f0e", "random": "#2ca02c"}

SVG_TEMPLATE = """<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\">
  <style>
    .axis {{ stroke: #555; stroke-width: 1; }}
    .grid {{ stroke: #ccc; stroke-width: 0.5; }}
    .label {{ font: 12px sans-serif; fill: #333; }}
  </style>
  <rect width=\"100%\" height=\"100%\" fill=\"#fff\" />
  {content}
</svg>"""


def normalize(value, min_value, max_value, length):
    if max_value - min_value == 0:
        return length / 2
    return (value - min_value) / (max_value - min_value) * length


def build_svg(title, dataset_map, filename):
    width, height = 900, 500
    margin = 60
    plot_width = width - margin * 2
    plot_height = height - margin * 2

    sizes = [size for entries in dataset_map.values() for size, _ in entries]
    times = [time for entries in dataset_map.values() for _, time in entries]
    if not sizes or not times:
        return

    x_min, x_max = min(sizes), max(sizes)
    y_min, y_max = min(times), max(times)

    content = []
    content.append(f"  <text x=\"{width/2}\" y=\"30\" text-anchor=\"middle\" class=\"label\" font-size=\"18\">{title}</text>")
    content.append(f"  <line class=\"axis\" x1=\"{margin}\" y1=\"{height-margin}\" x2=\"{width-margin}\" y2=\"{height-margin}\" />")
    content.append(f"  <line class=\"axis\" x1=\"{margin}\" y1=\"{margin}\" x2=\"{margin}\" y2=\"{height-margin}\" />")
    content.append(f"  <text x=\"{width/2}\" y=\"{height-20}\" text-anchor=\"middle\" class=\"label\">Input size</text>")
    content.append(f"  <text x=\"20\" y=\"{height/2}\" text-anchor=\"middle\" transform=\"rotate(-90 20,{height/2})\" class=\"label\">Time (s)</text>")

    for step in range(5):
        ratio = step / 4
        x = margin + ratio * plot_width
        label = round(x_min + ratio * (x_max - x_min))
        content.append(f"  <line class=\"grid\" x1=\"{x}\" y1=\"{margin}\" x2=\"{x}\" y2=\"{height-margin}\" />")
        content.append(f"  <text x=\"{x}\" y=\"{height-margin+20}\" text-anchor=\"middle\" class=\"label\">{label}</text>")
        y = margin + ratio * plot_height
        label = round(y_max - ratio * (y_max - y_min), 5)
        content.append(f"  <line class=\"grid\" x1=\"{margin}\" y1=\"{y}\" x2=\"{width-margin}\" y2=\"{y}\" />")
        content.append(f"  <text x=\"{margin-10}\" y=\"{y+4}\" text-anchor=\"end\" class=\"label\">{label}</text>")

    legend_y = margin / 2
    legend_x = width - margin - 20
    legend_items = []

    for idx, (label, entries) in enumerate(dataset_map.items()):
        if not entries:
            continue
        poly = []
        for size, time in entries:
            x = margin + normalize(size, x_min, x_max, plot_width)
            y = height - margin - normalize(time, y_min, y_max, plot_height)
            poly.append(f"{x},{y}")
        points = " ".join(poly)
        color = COLORS.get(label, "#000")
        content.append(f"  <polyline fill=\"none\" stroke=\"{color}\" stroke-width=\"2\" points=\"{points}\" />")
        legend_items.append((label.capitalize(), color))

    for i, (label, color) in enumerate(legend_items):
        lx = legend_x
        ly = legend_y + i * 20
        content.append(f"  <line x1=\"{lx}\" y1=\"{ly}\" x2=\"{lx+30}\" y2=\"{ly}\" stroke=\"{color}\" stroke-width=\"3\" />")
        content.append(f"  <text x=\"{lx+35}\" y=\"{ly+4}\" class=\"label\">{label}</text>")

    svg = SVG_TEMPLATE.format(width=width, height=height, content="\n".join(content))
    (OUTPUT_DIR / filename).write_text(svg)


for category, entries in data.items():
    if not entries:
        continue
    entries.sort()
    build_svg(f"Merge Sort Timing - {category.capitalize()} Inputs", {category: entries}, f"{category}_timing.svg")

combined_map = {k: sorted(v) for k, v in data.items() if v}
if combined_map:
    build_svg("Merge Sort Timing Comparison", combined_map, "combined_timing.svg")

print(f"Charts written to {OUTPUT_DIR.resolve()}")
