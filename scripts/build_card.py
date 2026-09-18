#!/usr/bin/env python3
"""Regenerate assets/now.svg — a 9:16 status card with live GitHub activity.

Run locally:   python3 scripts/build_card.py
In Actions:    GITHUB_TOKEN is read from the environment for higher rate limits.
"""
import os, json, math, random, datetime, urllib.request, urllib.error
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = os.environ.get("GH_USER", "varadshajith")
OUT  = os.path.join(ROOT, "assets", "now.svg")
F800 = os.path.join(ROOT, "assets", "inter-800.woff2")
F600 = os.path.join(ROOT, "assets", "inter-600.woff2")

W, H   = 480, 853
INK    = "#0A0C0F"
MUTED  = "#98A0AB"
FAINT  = "#AAB2BC"
HAIR   = "#E8EBEF"
BG     = "#FCFCFD"
ACCENT = "#E8590C"
MONO   = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
M      = 40

# ---------------------------------------------------------------- live data
def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-card"},
    )
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def ago(dt, now):
    s = (now - dt).total_seconds()
    if s < 3600:   return f"{int(s//60)} min ago"
    if s < 86400:  return f"{int(s//3600)} hours ago"
    d = int(s // 86400)
    if d == 1:     return "yesterday"
    if d < 7:      return f"{d} days ago"
    if d < 60:     return f"{d//7} weeks ago"
    return f"{d//30} months ago"

def activity():
    """Returns (last_push_repo, last_push_when, commits_7d, repos_7d)."""
    now = datetime.datetime.now(datetime.timezone.utc)
    try:
        ev = api(f"/users/{USER}/events/public?per_page=100")
        if not isinstance(ev, list):
            raise ValueError("unexpected payload")
    except Exception as e:
        print(f"  ! activity fetch failed ({e}); using placeholders")
        return ("—", "no data", 0, 0)

    push = [e for e in ev if e.get("type") == "PushEvent"]
    if not push:
        return ("—", "no recent pushes", 0, 0)

    def when(e):
        return datetime.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00"))

    latest = push[0]
    repo   = latest["repo"]["name"].split("/")[-1]
    week   = [e for e in push if (now - when(e)).days < 7]
    n      = sum(len(e["payload"].get("commits", [])) for e in week)
    repos  = len({e["repo"]["name"] for e in week})
    return (repo, ago(when(latest), now), n, repos)

# ---------------------------------------------------------------- typography
_cache = {}
def _font(path):
    if path not in _cache:
        f = TTFont(path); f.flavor = None
        _cache[path] = (f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _cache[path]

def typeset(fontpath, text, size, x, y, fill, tracking=0.0, begin=None):
    gs, cmap, upem = _font(fontpath)
    s = size / upem
    cx, parts = 0.0, []
    for ch in text:
        if ch == " ":
            cx += gs[cmap[ord("n")]].width * s * 0.58 + tracking
            continue
        gn = cmap.get(ord(ch))
        if gn is None:
            continue
        pen = SVGPathPen(gs); gs[gn].draw(pen); d = pen.getCommands()
        if d:
            parts.append(f'<path transform="translate({cx:.2f},0) scale({s:.5f},{-s:.5f})" d="{d}"/>')
        cx += gs[gn].width * s + tracking
    anim, op = "", "1"
    if begin is not None:
        op = "0"
        anim = (f'<animate attributeName="opacity" values="0;1" dur="0.5s" begin="{begin}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 9;0 0" '
                f'dur="0.6s" begin="{begin}s" fill="freeze" additive="sum"/>')
    return f'<g transform="translate({x},{y})" fill="{fill}" opacity="{op}">{anim}{"".join(parts)}</g>'

def mono(x, y, text, size, fill, tracking=0.0, anchor="start", begin=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    op, an = "1", ""
    if begin is not None:
        op = "0"
        an = f'<animate attributeName="opacity" values="0;1" dur="0.5s" begin="{begin}s" fill="freeze"/>'
    return (f'<text x="{x}" y="{y}"{a} font-family="{MONO}" font-size="{size}" '
            f'letter-spacing="{tracking}" fill="{fill}" opacity="{op}">{text}{an}</text>')

# ---------------------------------------------------------------- field
def field_lines(n=80):
    random.seed(11)
    def theta(x, y):
        return 1.15 * math.sin(0.0090 * y + 0.5) + 0.60 * math.cos(0.0075 * x + 1.9)
    out = []
    for _ in range(n):
        x, y = random.uniform(-30, W + 20), random.uniform(-40, H + 40)
        pts = [(x, y)]
        for _ in range(170):
            a = theta(x, y)
            x += math.cos(a) * 4.0
            y += math.sin(a) * 4.0 * 0.9
            if x < -40 or x > W + 40 or y < -60 or y > H + 60:
                break
            pts.append((x, y))
        if len(pts) > 18:
            out.append(pts)
    return out

def topath(pts):
    px, py = round(pts[0][0]), round(pts[0][1])
    d = f"M{px} {py}"
    for x, y in pts[2::2]:
        qx, qy = round(x), round(y)
        if qx == px and qy == py:
            continue
        d += f" {qx} {qy}"
        px, py = qx, qy
    return d

# ---------------------------------------------------------------- build
def main():
    cfg  = json.load(open(os.path.join(ROOT, "card.json")))
    repo, when, n7, r7 = activity()
    today = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)
    datestr = today.strftime("%d %b %Y").upper()

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Current status card for {USER}">',
         f'<title>Now — updated {datestr}</title>',
         f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>',
         f'<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
         f'<g clip-path="url(#c)" fill="none" stroke="{INK}" stroke-width="1" '
         f'stroke-opacity="0.07" stroke-linecap="round">']
    for i, p in enumerate(field_lines()):
        dash = 240 + (i * 53) % 320
        o.append(f'<path d="{topath(p)}" stroke-dasharray="{dash} {dash}">'
                 f'<animate attributeName="stroke-dashoffset" values="{dash*2};0" '
                 f'dur="{30 + (i%7)*3}s" repeatCount="indefinite"/></path>')
    o.append("</g>")
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{HAIR}"/>')
    o.append('<g clip-path="url(#c)">')

    # header
    o.append(f'<circle cx="{M+4}" cy="60" r="4.5" fill="{ACCENT}">'
             f'<animate attributeName="opacity" values="1;0.25;1" dur="2.6s" repeatCount="indefinite"/></circle>')
    o.append(mono(M + 20, 65, "NOW", 11.5, INK, 3.4))
    o.append(mono(W - M, 65, datestr, 11.5, FAINT, 1.6, "end"))
    o.append(f'<line x1="{M}" y1="86" x2="{W-M}" y2="86" stroke="{HAIR}"/>')

    # statement
    y = 150
    for i, line in enumerate(cfg["statement"]):
        o.append(typeset(F800, line, 34, M, y, INK, -0.9, begin=round(0.15 + i * 0.12, 2)))
        y += 42

    # live strip
    ly = y + 34
    o.append(f'<line x1="{M}" y1="{ly-24}" x2="{W-M}" y2="{ly-24}" stroke="{HAIR}"/>')
    o.append(mono(M, ly, "LAST PUSH", 9.5, FAINT, 2.6, begin=0.5))
    o.append(typeset(F600, repo, 16, M, ly + 24, INK, -0.2, begin=0.5))
    o.append(mono(M, ly + 42, when, 11, MUTED, 0, begin=0.55))
    o.append(mono(W - M, ly, "LAST 7 DAYS", 9.5, FAINT, 2.6, "end", begin=0.5))
    o.append(typeset(F600, f"{n7} commits", 16, W - M - 92, ly + 24, INK, -0.2, begin=0.5))
    o.append(mono(W - M, ly + 42, f"{r7} repos", 11, MUTED, 0, "end", begin=0.55))
    o.append(f'<line x1="{M}" y1="{ly+64}" x2="{W-M}" y2="{ly+64}" stroke="{HAIR}"/>')

    # focus rows
    y = ly + 106
    for i, row in enumerate(cfg["focus"]):
        b = round(0.66 + i * 0.13, 2)
        o.append(mono(M, y, row["label"], 9.5, FAINT, 2.6, begin=b))
        o.append(typeset(F600, row["name"], 21, M, y + 30, INK, -0.3, begin=b))
        for j, ln in enumerate(row["lines"]):
            o.append(mono(M, y + 52 + j * 16, ln, 11.5, MUTED, 0, begin=round(b + 0.05, 2)))
        if i < len(cfg["focus"]) - 1:
            o.append(f'<line x1="{M}" y1="{y+92}" x2="{W-M}" y2="{y+92}" stroke="{HAIR}"/>')
        y += 118

    # stack + footer
    o.append(f'<line x1="{M}" y1="{H-104}" x2="{W-M}" y2="{H-104}" stroke="{HAIR}"/>')
    o.append(mono(M, H - 80, cfg["stack"], 9, FAINT, 1.6, begin=1.05))
    o.append(f'<line x1="{M}" y1="{H-62}" x2="{W-M}" y2="{H-62}" stroke="{HAIR}"/>')
    o.append(mono(M, H - 38, cfg["location"], 10.5, FAINT, 1.8))
    o.append(mono(W - M, H - 38, cfg["cohort"], 10.5, FAINT, 1.8, "end"))
    o.append("</g></svg>")

    svg = "\n".join(o)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(svg)
    print(f"wrote {OUT}  ({len(svg)//1024} KB)")
    print(f"  last push : {repo} — {when}")
    print(f"  last 7d   : {n7} commits / {r7} repos")

if __name__ == "__main__":
    main()
