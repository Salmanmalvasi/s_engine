import re, os
os.makedirs("charts", exist_ok=True)

data = []
with open("results.txt", "r") as f:
    for line in f:
        m = re.search(r"n=(\d+).*?([\d.]+) seconds", line)
        if m: data.append((int(m.group(1)), float(m.group(2))))

data.sort()
if not data: exit()

# Save CSV
with open("results_table.csv", "w") as f:
    f.write("n,Time(s)\n")
    for n, t in data: f.write(f"{n},{t}\n")

# SVG Settings
w, h = 850, 500
margin_l, margin_r, margin_t, margin_b = 90, 40, 60, 70
plot_w = w - margin_l - margin_r
plot_h = h - margin_t - margin_b

max_n = max([d[0] for d in data])
max_t = max([d[1] for d in data]) if max([d[1] for d in data]) > 0 else 0.0001
max_t *= 1.1 # 10% headroom

svg = f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="background-color:white;">\n'
svg += f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-family="sans-serif" font-weight="bold">Line Segment Intersection Time Complexity</text>\n'

# Draw Grid and Ticks
num_ticks = 5
for i in range(num_ticks + 1):
    # Y-axis (Time)
    y_val = max_t * (i / num_ticks)
    y_pos = h - margin_b - (i / num_ticks) * plot_h
    svg += f'<line x1="{margin_l}" y1="{y_pos}" x2="{w-margin_r}" y2="{y_pos}" stroke="#e0e0e0" stroke-width="1"/>\n'
    svg += f'<text x="{margin_l-10}" y="{y_pos+4}" text-anchor="end" font-size="12" font-family="sans-serif">{y_val:.6f}</text>\n'
    
    # X-axis (N sizes)
    x_val = max_n * (i / num_ticks)
    x_pos = margin_l + (i / num_ticks) * plot_w
    svg += f'<line x1="{x_pos}" y1="{margin_t}" x2="{x_pos}" y2="{h-margin_b}" stroke="#e0e0e0" stroke-width="1"/>\n'
    svg += f'<text x="{x_pos}" y="{h-margin_b+20}" text-anchor="middle" font-size="12" font-family="sans-serif">{int(x_val)}</text>\n'

# Draw X and Y Axes
svg += f'<line x1="{margin_l}" y1="{h-margin_b}" x2="{w-margin_r}" y2="{h-margin_b}" stroke="black" stroke-width="2"/>\n' # X-axis
svg += f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{h-margin_b}" stroke="black" stroke-width="2"/>\n' # Y-axis

# Axis Labels
svg += f'<text x="{w/2}" y="{h-15}" text-anchor="middle" font-size="16" font-family="sans-serif" font-weight="bold">Number of Pairs (N)</text>\n'
svg += f'<text x="20" y="{h/2}" transform="rotate(-90 20,{h/2})" text-anchor="middle" font-size="16" font-family="sans-serif" font-weight="bold">Time (seconds)</text>\n'

# Plot Data Points and Line
pts = []
for n, t in data:
    x = margin_l + (n / max_n) * plot_w
    y = h - margin_b - (t / max_t) * plot_h
    pts.append(f"{x},{y}")

svg += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#2196F3" stroke-width="3"/>\n'

for n, t in data:
    x = margin_l + (n / max_n) * plot_w
    y = h - margin_b - (t / max_t) * plot_h
    svg += f'<circle cx="{x}" cy="{y}" r="5" fill="#f44336"/>\n'
    svg += f'<text x="{x}" y="{y-12}" font-size="12" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#333">{t:.6f}s</text>\n'

svg += '</svg>'

with open("charts/line_segment_timing.svg", "w") as f: f.write(svg)

# HTML Wrapper
html = f'''<html><head><title>ILP 14 - Line Segment Intersection</title>
<style>body{{font-family:sans-serif; margin:40px;}} table{{border-collapse:collapse; width: 600px; margin-top: 20px;}} th,td{{border:1px solid #ddd; padding:12px; text-align: left;}} th{{background-color: #f2f2f2;}}</style>
</head><body>
<h2>Algorithm: Line Segment Intersection</h2>
<p>Complexity: O(1) per check. Checking N independent pairs takes <b>O(N)</b> time.</p>
<img src="line_segment_timing.svg" width="850">
<h3>Data Table</h3>
<table><tr><th>Number of Pairs (N)</th><th>Time taken (seconds)</th></tr>
'''
for n, t in data: html += f"<tr><td>{n}</td><td>{t:.6f}</td></tr>"
html += "</table></body></html>"
with open("charts/index.html", "w") as f: f.write(html)
print("Updated charts with proper axes generated in charts/")
