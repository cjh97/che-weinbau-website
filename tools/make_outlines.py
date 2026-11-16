"""Build simplified country outlines (Natural Earth 1:50m, public domain) for the zoomed map views.
Output: tools/map_outlines.json  {map: {ADM0_A3: "svg path d"}} in each map's svg units."""
import json, sys
src, out = sys.argv[1], sys.argv[2]
MAPS = {"eu": (-12, 56, (-16, 31, 26, 60)), "ca": (-126, 43, (-128, 30, -112, 45)), "il": (31, 35, (29.5, 27.5, 39.5, 36.5))}
A3 = {"DEU": "DE", "FRA": "FR", "LUX": "LU", "CHE": "CH", "AUT": "AT", "ITA": "IT", "SVN": "SI", "HRV": "HR", "CZE": "CZ", "PRT": "PT", "USA": "US", "ISR": "IL"}

def clip(ring, x0, y0, x1, y1):            # Sutherland–Hodgman against a rectangle
    def cut(pts, inside, inter):
        res = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia: res.append(inter(a, b))
                res.append(b)
            elif ia: res.append(inter(a, b))
        return res
    def ix(x): return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]))
    def iy(y): return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y)
    p = ring
    for inside, inter in [(lambda q: q[0] >= x0, ix(x0)), (lambda q: q[0] <= x1, ix(x1)), (lambda q: q[1] >= y0, iy(y0)), (lambda q: q[1] <= y1, iy(y1))]:
        if not p: break
        p = cut(p, inside, inter)
    return p

def rdp(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True; stack = [(0, len(pts) - 1)]
    while stack:
        s, e = stack.pop(); ax, ay = pts[s]; bx, by = pts[e]; dx, dy = bx - ax, by - ay; L = (dx * dx + dy * dy) ** .5 or 1e-9
        best, bi = -1, -1
        for i in range(s + 1, e):
            d = abs(dy * (pts[i][0] - ax) - dx * (pts[i][1] - ay)) / L
            if d > best: best, bi = d, i
        if best > tol: keep[bi] = True; stack += [(s, bi), (bi, e)]
    return [p for p, k in zip(pts, keep) if k]

data = json.load(open(src)); res = {}
for m, (lon0, lat0, (bx0, by0, bx1, by1)) in MAPS.items():
    res[m] = {}
    for f in data["features"]:
        a3 = f["properties"]["ADM0_A3"]; g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        d = ""
        for poly in polys:
            for ring in poly[:1]:                                   # outer rings only (lakes not needed at this scale)
                r = clip([tuple(q) for q in ring], bx0, by0, bx1, by1)
                if len(r) < 3: continue
                pts = [((x - lon0) * 20 + 5, (lat0 - y) * 20 + 5) for x, y in r]
                if pts[0] == pts[-1]: pts = pts[:-1]
                k = max(range(len(pts)), key=lambda n: (pts[n][0] - pts[0][0]) ** 2 + (pts[n][1] - pts[0][1]) ** 2)
                pts = rdp(pts[:k + 1], 0.3) + rdp(pts[k:] + [pts[0]], 0.3)[1:-1]   # closed ring: simplify the two halves
                if len(pts) < 3: continue
                xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                if max(xs) - min(xs) < 0.8 and max(ys) - min(ys) < 0.8: continue   # specks
                d += "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
        if d: res[m][A3.get(a3, a3)] = d
json.dump(res, open(out, "w"), separators=(",", ":"))
print({m: (len(v), sum(len(s) for s in v.values())) for m, v in res.items()})
