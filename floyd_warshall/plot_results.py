from __future__ import annotations
from pathlib import Path
import re

SCRIPT_DIR   = Path(__file__).resolve().parent
RESULTS_PATH = SCRIPT_DIR / "results.txt"
OUTPUT_DIR   = SCRIPT_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

LINE_RE = re.compile(
    r"algo=Floyd-Warshall, n=(\d+), m=(\d+), case=(pos|neg): time=([0-9.e\-]+) seconds, "
    r"negCycle=(\d), reachablePairs=(\-?\d+), sumDist=(\-?\d+)"
)

rows = []
if RESULTS_PATH.exists():
    for line in RESULTS_PATH.read_text().splitlines():
        m = LINE_RE.search(line)
        if not m: continue
        rows.append({"n":int(m.group(1)),"m":int(m.group(2)),"case":m.group(3),
                     "time":float(m.group(4)),"neg":int(m.group(5)),
                     "reachablePairs":int(m.group(6)),"sumDist":int(m.group(7))})

csv_path = SCRIPT_DIR / "results_table.csv"
with csv_path.open("w") as f:
    f.write("algo,n,m,case,time_seconds,negCycle,reachablePairs,sumDist\n")
    for r in rows:
        f.write(f"Floyd-Warshall,{r['n']},{r['m']},{r['case']},{r['time']},{r['neg']},{r['reachablePairs']},{r['sumDist']}\n")

SVG_T = '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><style>.axis{{stroke:#555;stroke-width:1}}.grid{{stroke:#d0d0d0;stroke-width:.7}}.lbl{{font:12px system-ui,sans-serif;fill:#222}}</style><rect width="100%" height="100%" fill="#fff"/>{c}</svg>'

def norm(v,lo,hi,L):
    return L/2 if hi==lo else (v-lo)/(hi-lo)*L

def build_svg(title, series, fname):
    if not series: return
    W,H,MG = 900,520,80
    PW,PH = W-MG*2, H-MG*2
    axs=[x for s in series.values() for x,_ in s]
    ays=[y for s in series.values() for _,y in s]
    x0,x1 = min(axs),max(axs)
    y0,y1 = 0.0,max(ays)
    c=[]
    c.append(f'<text x="{W/2}" y="30" text-anchor="middle" class="lbl" font-size="17">{title}</text>')
    c.append(f'<line class="axis" x1="{MG}" y1="{H-MG}" x2="{W-MG}" y2="{H-MG}"/>')
    c.append(f'<line class="axis" x1="{MG}" y1="{MG}" x2="{MG}" y2="{H-MG}"/>')
    c.append(f'<text x="{W/2}" y="{H-20}" text-anchor="middle" class="lbl">Vertices (n)</text>')
    c.append(f'<text x="20" y="{H/2}" text-anchor="middle" transform="rotate(-90 20,{H/2})" class="lbl">Time (s)</text>')
    for s in range(5):
        r=s/4
        xp=MG+r*PW; xl=round(x0+r*(x1-x0))
        c.append(f'<line class="grid" x1="{xp}" y1="{MG}" x2="{xp}" y2="{H-MG}"/>')
        c.append(f'<text x="{xp}" y="{H-MG+18}" text-anchor="middle" class="lbl">{xl}</text>')
        yp=MG+r*PH; yl=y1-r*(y1-y0)
        c.append(f'<line class="grid" x1="{MG}" y1="{yp}" x2="{W-MG}" y2="{yp}"/>')
        c.append(f'<text x="{MG-8}" y="{yp+4}" text-anchor="end" class="lbl">{yl:.6f}</text>')
    clrs={"pos":"#1f77b4","neg":"#d62728"}; leg_y=MG-20; leg_x=MG
    for idx,key in enumerate(["pos","neg"]):
        if key not in series: continue
        col=clrs[key]
        pts=" ".join(f"{MG+norm(n,x0,x1,PW)},{H-MG-norm(t,y0,y1,PH)}" for n,t in series[key])
        c.append(f'<polyline fill="none" stroke="{col}" stroke-width="2" points="{pts}"/>')
        for n,t in series[key]:
            xp=MG+norm(n,x0,x1,PW); yp=H-MG-norm(t,y0,y1,PH)
            c.append(f'<circle cx="{xp}" cy="{yp}" r="4" fill="{col}"/>')
        lx=leg_x+idx*170; lbl="No Neg Cycle" if key=="pos" else "Neg Cycle"
        c.append(f'<rect x="{lx}" y="{leg_y}" width="14" height="14" fill="{col}"/>')
        c.append(f'<text x="{lx+20}" y="{leg_y+12}" class="lbl">{lbl}</text>')
    (OUTPUT_DIR/fname).write_text(SVG_T.format(w=W,h=H,c="".join(c)))

pos=sorted([(r["n"],r["time"]) for r in rows if r["case"]=="pos"])
neg=sorted([(r["n"],r["time"]) for r in rows if r["case"]=="neg"])
build_svg("Floyd–Warshall Timing O(n³) — with/without Negative Cycle",{"pos":pos,"neg":neg},"floyd_warshall_timing.svg")

lines=[
 "<!DOCTYPE html>","<html lang='en'>","<head>","<meta charset='UTF-8'>",
 "<title>ILP 13 - Floyd-Warshall</title>",
 "<style>body{font-family:system-ui,sans-serif;margin:2rem;background:#f4f4f4}"
 "section{margin-bottom:2rem;background:#fff;padding:1rem;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,.08)}"
 "table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:8px 14px;text-align:right}"
 "th{background:#f0f0f0}td:first-child,th:first-child{text-align:left}</style>",
 "</head>","<body>",
 "<h1>ILP 13 — Floyd–Warshall</h1>",
 "<p><strong>Algorithm:</strong> Floyd–Warshall (All-Pairs Shortest Paths) | Complexity: O(n³)</p>",
 "<section><h2>Timing Graph</h2>",
 '<object type="image/svg+xml" data="floyd_warshall_timing.svg" width="900" height="520"></object>',
 '<p><a href="floyd_warshall_timing.svg" target="_blank">Open chart</a></p></section>',
 "<section><h2>Data Table</h2><table>",
 "<tr><th>case</th><th>n</th><th>m</th><th>time (s)</th><th>negCycle</th><th>reachablePairs</th><th>sumDist</th></tr>",
]
for r in sorted(rows, key=lambda r:(r["n"],r["case"])):
    lines.append(f"<tr><td>{r['case']}</td><td>{r['n']}</td><td>{r['m']}</td><td>{r['time']:.6f}</td><td>{r['neg']}</td><td>{r['reachablePairs']}</td><td>{r['sumDist']}</td></tr>")
lines+=["</table></section>","</body>","</html>"]
(OUTPUT_DIR/"index.html").write_text("\n".join(lines))

print(f"CSV: {csv_path}")
print(f"Report: {OUTPUT_DIR/'index.html'}")
