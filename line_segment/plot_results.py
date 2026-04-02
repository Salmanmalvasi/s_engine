import re, os
os.makedirs("charts", exist_ok=True)

data = []
with open("results.txt", "r") as f:
    for line in f:
        m = re.search(r"n=(\d+).*?([\d.]+) seconds", line)
        if m: data.append((int(m.group(1)), float(m.group(2))))

data.sort()
if not data: exit()

with open("results_table.csv", "w") as f:
    f.write("n,Time(s)\n")
    for n, t in data: f.write(f"{n},{t}\n")

w, h = 800, 400
max_n, max_t = max([d[0] for d in data]), max([d[1] for d in data])
if max_t == 0: max_t = 0.001

pts = []
for n, t in data:
    x = 50 + (n / max_n) * 700
    y = 350 - (t / max_t) * 300
    pts.append(f"{x},{y}")

svg = f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" fill="white"/>
<text x="400" y="30" text-anchor="middle" font-size="16" font-family="sans-serif">Line Segment Intersection (O(N) total)</text>
<polyline points="{' '.join(pts)}" fill="none" stroke="blue" stroke-width="2"/>
'''
for n, t in data:
    x = 50 + (n / max_n) * 700 ; y = 350 - (t / max_t) * 300
    svg += f'<circle cx="{x}" cy="{y}" r="4" fill="red"/>\n'
    svg += f'<text x="{x}" y="{y-10}" font-size="10" font-family="sans-serif" text-anchor="middle">{t:.6f}s</text>\n'
svg += '</svg>'

with open("charts/line_segment_timing.svg", "w") as f: f.write(svg)

html = f'''<html><head><title>ILP 14 - Line Segment Intersection</title>
<style>body{{font-family:sans-serif; margin:40px;}} table{{border-collapse:collapse;}} th,td{{border:1px solid #ccc; padding:8px;}}</style>
</head><body>
<h2>Algorithm: Line Segment Intersection</h2>
<p>Complexity: O(1) per check. Checking N independent pairs takes O(N) time.</p>
<img src="line_segment_timing.svg" width="800">
<h3>Data</h3>
<table><tr><th>Number of Pairs (n)</th><th>Time (seconds)</th></tr>
'''
for n, t in data: html += f"<tr><td>{n}</td><td>{t:.6f}</td></tr>"
html += "</table></body></html>"
with open("charts/index.html", "w") as f: f.write(html)
