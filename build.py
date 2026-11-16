#!/usr/bin/env python3
"""Static site generator for che-weinbau.com.

    python build.py            -> builds the site into _site/
    python build.py --preview  -> same, but links point to .../index.html (for file previews)

Content lives in content.py; styles in static/css/site.css; behaviour in static/js/site.js.
Only the Python standard library is needed.
"""
import datetime as dt
import html
import json
import pathlib
import re
import shutil
import sys
from html.parser import HTMLParser

import content as C

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "_site"
PREVIEW = "--preview" in sys.argv
TODAY = dt.date.today()
IMG_DIR = ROOT / "assets" / "img"

e = html.escape


def t(v, lang):
    """Pick the language variant of a value (plain strings pass through)."""
    return v[lang] if isinstance(v, dict) else v


# ------------------------------------------------------------------ linking
class Ctx:
    def __init__(self, path, lang, key):
        self.path, self.lang, self.key = path, lang, key
        self.prefix = "../" * path.count("/")

    def href(self, target_path):
        p = self.prefix + target_path
        if PREVIEW:
            p += "index.html"
        return p or "./"

    def page(self, key, lang=None):
        return self.href(C.PAGES[key][lang or self.lang])

    def asset(self, p):
        if p.endswith((".css", ".js")):   # version by content, so browsers never show a stale script
            import hashlib
            p += "?v=" + hashlib.md5((ROOT / p).read_bytes()).hexdigest()[:8]
        return self.prefix + p


def img(ctx, name, alt="", cls="", sizes="100vw", eager=False):
    src = ctx.asset(f"assets/img/{name}")
    srcset = ""
    if (IMG_DIR / "thumbs" / name).exists():
        srcset = f' srcset="{ctx.asset("assets/img/thumbs/" + name)} 800w, {src} 2000w" sizes="{sizes}"'
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{src}"{srcset} alt="{e(alt)}"{c} {load}>'


# ------------------------------------------------------------------ icons
ICONS = {
    "grape": '<circle cx="12" cy="9" r="2.3"/><circle cx="8.5" cy="12" r="2.3"/><circle cx="15.5" cy="12" r="2.3"/><circle cx="12" cy="15" r="2.3"/><circle cx="10" cy="18.5" r="2"/><circle cx="14" cy="18.5" r="2"/><path d="M12 6.7V3m0 0c1.5 0 3 .8 4 2"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.4-3 7.7-7 9-4-1.3-7-4.6-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "leaf": '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19l7-7"/>',
    "speed": '<path d="M4 15a8 8 0 1116 0"/><path d="M12 15l4-5"/><circle cx="12" cy="15" r="1.3"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a1 1 0 01-1 1A16 16 0 014 5a1 1 0 011-1"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-12a7 7 0 0114 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "Facebook": '<path d="M14 8h3V4h-3a4 4 0 00-4 4v3H7v4h3v7h4v-7h3l1-4h-4V8z"/>',
    "Instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/>',
    "YouTube": '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10 9.5v5l4.5-2.5z"/>',
}


def icon(name, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ------------------------------------------------------------------ analytics
def analytics():
    """Plausible: cookieless, no personal data stored -> no consent banner needed."""
    if not C.PLAUSIBLE_DOMAIN or PREVIEW:
        return ""
    return (f'<script async src="{C.PLAUSIBLE_SCRIPT}"></script>\n'
            '<script>window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},'
            'plausible.init=plausible.init||function(i){plausible.o=i||{}};plausible.init()</script>')


# ------------------------------------------------------------------ layout
def layout(ctx, title, description, body, hero_img=None):
    body_class = "" if 'class="hero' in body else "solid-header"
    lang = ctx.lang
    other = "en" if lang == "de" else "de"
    canonical = f"{C.SITE_URL}/{ctx.path}"
    alt_links = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{C.SITE_URL}/{C.PAGES[ctx.key][l]}">' for l in ("de", "en")
    ) + f'<link rel="alternate" hreflang="x-default" href="{C.SITE_URL}/{C.PAGES[ctx.key]["de"]}">'
    nav = "".join(
        f'<li><a href="{ctx.page(k)}"{" aria-current=page" if k == ctx.key else ""}>{e(t(C.NAV_LABELS[k], lang))}</a></li>'
        for k in C.NAV
    )
    og_img = f"{C.SITE_URL}/assets/img/{hero_img or 'hero-mosel.jpg'}"
    full_title = title if "CH engineering" in title else f"{title} | CH engineering"
    org = {
        "@context": "https://schema.org", "@type": "Organization", "name": C.COMPANY["name"],
        "url": C.SITE_URL, "email": C.COMPANY["email"], "telephone": C.COMPANY["phone"],
        "logo": f"{C.SITE_URL}/assets/img/logo-white.png",
        "address": {"@type": "PostalAddress", "streetAddress": C.COMPANY["street"],
                    "postalCode": "54536", "addressLocality": "Kröv", "addressCountry": "DE"},
        "sameAs": list(C.COMPANY["social"].values()),
    }
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
{alt_links}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{og_img}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{'de_DE' if lang == 'de' else 'en_US'}">
<meta name="theme-color" content="#16181a">
<link rel="icon" href="{ctx.asset('assets/favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{ctx.asset('static/css/site.css')}">
{analytics()}
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
</head>
<body class="{body_class}">
<a class="skip" href="#main">{e(t(C.UI['skip'], lang))}</a>
<header class="site-header" data-header>
  <div class="wrap header-inner">
    <a class="brand" href="{ctx.page('home')}" aria-label="CH engineering – {e(t(C.NAV_LABELS['home'], lang))}">
      <img src="{ctx.asset('assets/img/logo-white.png')}" alt="CH engineering" width="180" height="46">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Hauptnavigation">
      <ul>{nav}</ul>
      <a class="lang" href="{ctx.page(ctx.key, other)}" hreflang="{other}" lang="{other}">{other.upper()}<span class="sr"> – {e(t(C.UI['lang_switch'], lang))}</span></a>
    </nav>
    <button class="nav-toggle" aria-controls="main-nav" aria-expanded="false" data-nav-toggle>
      <span></span><span></span><span class="sr">{e(t(C.UI['menu'], lang))}</span>
    </button>
  </div>
</header>
<main id="main">
{body}
</main>
{footer(ctx)}
<div class="lightbox" data-lightbox hidden><button class="lb-close" aria-label="{e(t(C.UI['close'], lang))}">×</button><button class="lb-prev" aria-label="‹">‹</button><img alt=""><button class="lb-next" aria-label="›">›</button></div>
<script src="{ctx.asset('static/js/site.js')}" defer></script>
</body>
</html>
"""


def footer(ctx):
    lang, co = ctx.lang, C.COMPANY
    social = "".join(
        f'<a href="{u}" rel="noopener" aria-label="{n}">{icon(n)}</a>' for n, u in co["social"].items()
    )
    links = "".join(f'<li><a href="{ctx.page(k)}">{e(t(C.NAV_LABELS[k], lang))}</a></li>' for k in C.NAV)
    hours = "<br>".join(e(h) for h in t(C.UI["hours_text"], lang))
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="{ctx.asset('assets/img/logo-white.png')}" alt="CH engineering" width="180" height="46" loading="lazy">
      <p>{e(t(C.UI['footer_claim'], lang))}</p>
      <div class="social" aria-label="{e(t(C.UI['follow'], lang))}">{social}</div>
    </div>
    <div>
      <h2>{e(t(C.UI['hq'], lang))}</h2>
      <p>{e(co['name'])}<br>{e(co['street'])}<br>{e(co['zip_city'])}</p>
      <p><a href="tel:{co['phone'].replace(' ', '')}">{e(co['phone_display'])}</a><br>
      <a href="mailto:{co['email']}">{e(co['email'])}</a></p>
    </div>
    <div>
      <h2>{e(t(C.UI['production'], lang))}</h2>
      <p>{e(co['name'])}<br>{e(co['production']['street'])}<br>{e(co['production']['zip_city'])}</p>
      <p><a href="tel:{co['production']['phone'].replace(' ', '')}">{e(co['production']['phone_display'])}</a></p>
      <h2 class="footer-sub">{e(t(C.UI['hours'], lang))}</h2>
      <p>{hours}</p>
    </div>
    <div>
      <h2>CH engineering</h2>
      <ul class="footer-links">{links}</ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© {TODAY.year} {e(co['name'])}. {e(t(C.UI['copyright'], lang))}</span>
    <span><a href="{ctx.page('imprint')}">{e(t(C.NAV_LABELS['imprint'], lang))}</a> · <a href="{ctx.page('privacy')}">{e(t(C.NAV_LABELS['privacy'], lang))}</a></span>
  </div>
</footer>"""


# ------------------------------------------------------------------ building blocks
def paras(items):
    return "".join(f"<p>{e(p)}</p>" for p in items)


# ------------------------------------------------------------------ shared page components
# Every page is built from the same few blocks so the site looks consistent:
#   hero → statement → split sections (photo + text) → cards / data → gallery → CTA

def hero(ctx, image, title, *, home=False, top="", actions="", sub=None, stats=None):
    alt = title
    bar = ""
    if stats:
        items = "".join(f'<div class="figure"><strong>{e(s["value"])}</strong><span>{e(t(s["label"], ctx.lang))}</span></div>' for s in stats)
        bar = f'<div class="figures-bar"><div class="wrap figures-grid">{items}</div></div>'
    return f"""<section class="hero{' hero-home' if home else ''}{' hero-figures' if stats else ''}">
  {img(ctx, image, alt, 'hero-img', eager=True)}
  <div class="wrap hero-content">
    {top}
    <h1>{e(title)}</h1>
    {f'<p class="hero-sub">{e(sub)}</p>' if sub else ''}
    {f'<div class="hero-actions">{actions}</div>' if actions else ''}
  </div>
  {bar}
</section>"""


def page_hero(ctx, d, title=None):
    sub = d.get("subtitle") or d.get("lead")
    return hero(ctx, d["hero_img"], title or t(d["title"], ctx.lang), sub=t(sub, ctx.lang) if sub else None, stats=d.get("stats"))


def figures(ctx, image, stats):
    """Full-width photo with the key figures across the bottom (spec-sheet style)."""
    items = "".join(f'<div class="figure"><strong>{e(s["value"])}</strong><span>{e(t(s["label"], ctx.lang))}</span></div>' for s in stats)
    return f"""<section class="figures">
  {img(ctx, image, '', 'figures-img')}
  <div class="figures-bar"><div class="wrap figures-grid">{items}</div></div>
</section>"""


def statement(text, extra=""):
    return f"""<section class="statement">
  <div class="wrap"><p class="statement-text">{e(text)}</p>{extra}</div>
</section>"""


def split(ctx, image, title, body_html, *, rev=False, studio=False, caption=None, label=None, media=None, grey=False):
    title_alt = title.replace("\n", " ")
    media_html = media or img(ctx, image, caption or title_alt, sizes="(min-width: 900px) 50vw, 100vw")
    cap = f'<figcaption>{e(caption)}</figcaption>' if caption else ""
    lab = f'<p class="label">{e(label)}</p>' if label else ""
    cls = "split" + (" split-rev" if rev else "") + (" split-grey" if grey else "")
    return f"""<section class="{cls}">
  <figure class="split-media{' studio' if studio else ''}{' split-media-grid' if media else ''}">{media_html}{cap}</figure>
  <div class="split-body">{lab}<h2>{e(title).replace(chr(10), '<br>')}</h2>{body_html}</div>
</section>"""


def section(title, inner, *, grey=False, link=None):
    head = f'<div class="section-head"><h2>{e(title)}</h2>{link or ""}</div>' if title else ""
    return f"""<section class="section{' section-grey' if grey else ''}">
  <div class="wrap">{head}{inner}</div>
</section>"""


MAPS = {"eu": ("tools/map_eu.txt", -12, 56), "ca": ("tools/map_us.txt", -126, 43), "il": ("tools/map_il.txt", 31, 35)}  # grid file, lon0, lat0 (0.5° grid)


def _map_svg(ctx, which):
    """Inline SVG: muted dot geography, accent markers, thin leader lines to labels."""
    fn, lon0, lat0 = MAPS[which]
    rows = (ROOT / fn).read_text().strip().split("|")
    grid = ["".join(("1" if m[0] == "#" else "0") * int(m[1:]) for m in re.findall(r"[#.]\d+", r)) for r in rows]
    W, H = len(grid[0]) * 10, len(grid) * 10
    dots = "".join(f"M{x*10+5} {y*10+5}h0" for y, r in enumerate(grid) for x, c in enumerate(r) if c == "1")
    marks = ""
    for i, loc in enumerate(C.LOCATIONS):
        if loc["map"] != which:
            continue
        x = (loc["lon"] - lon0) / 0.5 * 10 + 5
        y = (lat0 - loc["lat"]) / 0.5 * 10 + 5
        lx, ly = loc["lx"], loc["ly"]
        label = e(t(loc["label"], ctx.lang))
        anchor = loc.get("anchor") or ("end" if lx < x - 20 else ("start" if lx > x + 20 else "middle"))
        story = " has-story" if loc.get("story") else ""
        tag = f' role="button" tabindex="0" aria-label="{label}"' if story else ""
        marks += (f'<g class="mk{story}{" mk-home" if loc.get("home") else ""}" data-loc="{i}"{tag}>'
                  f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{lx}" y2="{ly + (6 if ly > y else -4)}"/>'
                  f'<circle class="mk-hit" cx="{x:.0f}" cy="{y:.0f}" r="22"/><circle class="mk-dot" cx="{x:.0f}" cy="{y:.0f}" r="{8 if loc.get("home") else 6.5}"/>'
                  f'<text x="{lx}" y="{ly}" text-anchor="{anchor}">{label}</text></g>')
    return (f'<svg class="map-svg map-{which}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(t(C.HOME["map_title"], ctx.lang))}">'
            f'<path class="geo" d="{dots}"/>{marks}</svg>')


def _leaf(x, y, rot):
    return f'<ellipse class="leaf" cx="{x}" cy="{y}" rx="8" ry="4.5" transform="rotate({rot} {x} {y})"/>'


def _grapes(x, y):
    pts = [(-5, 0), (0, 0), (5, 0), (-2.5, 4.6), (2.5, 4.6), (0, 9.2)]
    return "".join(f'<circle class="grape" cx="{x+dx}" cy="{y+dy}" r="2.7"/>' for dx, dy in pts)


def _vine_front(x, y):
    """One vine seen along the row: post, leaves up the canopy, two grape clusters."""
    out = f'<path class="post" d="M{x} {y}V{y-88}"/>'
    for i, (dx, dy, r) in enumerate([(-9, -24, -30), (9, -32, 30), (-10, -44, -20), (10, -54, 25), (-9, -64, -35), (9, -74, 35), (-4, -84, -60), (6, -90, 60)]):
        out += _leaf(x + dx, y + dy, r)
    return out + _grapes(x - 7, y - 40) + _grapes(x + 8, y - 22)


def _vine_row_side():
    """Trellis row seen from the side, repeating every 240 units so it can scroll past endlessly.
    Returns (posts + wire + leaves, grapes) as two layers; grapes are clipped to the part not yet harvested."""
    base = '<path class="post" d="M-1500 -30H1500"/>'
    grapes = ""
    for x in range(-1440, 1480, 40):
        i = (x // 40) % 6
        if i % 2 == 0:
            base += f'<path class="post" d="M{x} 0V-40"/>'
        base += _leaf(x + 8, -34 - (i % 3) * 4, 20 + i * 11) + _leaf(x + 24, -27 - (i % 2) * 6, -30 - i * 9)
        if i % 2:
            grapes += _grapes(x + 14, -22)
    return base, grapes


def slope_story(ctx):
    """Scroll scene. 1) side view: ground tilts 0 → 75 %. 2) view turns 90°: terrace cross-section,
    the MSH in one lane with its head over the row. 3) outline of a conventional straddle harvester for comparison."""
    lang = ctx.lang
    labels = t(C.HOME["slope_labels"], lang)
    flats = [(-930, 510), (-670, 360), (-410, 210), (-150, 60), (110, -90), (370, -240), (630, -390)]
    prof = "M-1200 510" + "".join(f"H{x}V{y}" for x, y in flats) + "H1200"
    vines = "".join(_vine_front(x + 45, y) for x, y in flats if x != -150)
    vine_head = _vine_front(-105, 60)
    row_base, row_grapes = _vine_row_side()
    feat_imgs = ["grapes-1.jpg", "msh-g02.jpg", "msh-g06.jpg", "msh-row.jpg"]
    stations = "".join(
        f'<article class="station" data-station><div class="station-img">{img(ctx, feat_imgs[i], t(f["title"], lang), sizes="380px")}</div>'
        f'<div><h3>{e(t(f["title"], lang))}</h3><p>{e(t(f["text"], lang))}</p></div></article>'
        for i, f in enumerate(C.HOME["features"]))
    return f"""<section class="slope-story" data-slope data-labels="{e('|'.join(labels))}">
  <div class="slope-sticky">
    <div class="wrap"><h2>{e(t(C.HOME['slope_title'], lang))}</h2></div>
    <canvas class="slope-canvas" data-scene aria-hidden="true"></canvas>
    <div class="wrap slope-read"><strong data-slope-num>1</strong><span data-slope-label>{e(labels[3])}</span></div>
    <div class="slope-photo" data-slope-photo>
      {img(ctx, 'msh-row.jpg', t(C.HOME['benefits_title'], lang), 'slope-photo-img')}
      <div class="wrap slope-photo-text"><h2>{e(t(C.HOME['benefits_title'], lang))}</h2></div>
    </div>
  </div>
</section>"""


def quality(ctx):
    """Photo that opens up to full width while scrolling, headline on it, the four benefits as a quiet row below."""
    h, lang = C.HOME, ctx.lang
    items = "".join(f'<div class="benefit"><h3>{e(t(f["title"], lang))}</h3><p>{e(t(f["text"], lang))}</p></div>' for f in h["features"])
    return f"""<section class="expand">
  <div class="wrap benefits">{items}</div>
  <div class="wrap benefits-more"><a class="text-link" href="{ctx.page('msh')}">{e(t(h['short_link'], lang))}</a></div>
</section>"""


def world_map(ctx):
    lang = ctx.lang
    stories = ""
    first = True
    for i, loc in enumerate(C.LOCATIONS):
        st = loc.get("story")
        if not st:
            continue
        pic = f'<div class="story-img">{img(ctx, st["img"], t(st["title"], lang), sizes="(min-width: 900px) 25vw, 100vw")}</div>' if st.get("img") else ""
        link = f'<a class="text-link" href="{st["link"]}" rel="noopener">{e(t(C.UI["read_source"], lang))}</a>' if st.get("link") else ""
        stories += (f'<article class="story{"" if pic else " story-noimg"}" data-story="{i}"{"" if first else " hidden"}>{pic}'
                    f'<div class="story-text"><h3>{e(t(st["title"], lang))}</h3><p>{e(t(st["text"], lang))}</p>{link}</div></article>')
        first = False
    ca = "Kalifornien, USA" if lang == "de" else "California, USA"
    il = "Israel" if lang == "de" else "Israel"
    return f"""<section class="section worldmap">
  <div class="wrap">
    <div class="worldmap-head"><h2>{e(t(C.HOME['map_title'], lang))}</h2><p>{e(t(C.HOME['map_text'], lang))}</p></div>
    <div class="worldmap-grid">
      <div class="insets">
        <figure class="inset">{_map_svg(ctx, 'ca')}<figcaption>{ca}</figcaption></figure>
        <figure class="inset">{_map_svg(ctx, 'il')}<figcaption>{il}</figcaption></figure>
      </div>
      <div class="map-eu-wrap">{_map_svg(ctx, 'eu')}</div>
    </div>
    <div class="stories">{stories}</div>
  </div>
</section>"""


def cards(ctx, items):
    """items: (image, title, text, href or None)"""
    out = ""
    for image, title, text, href in items:
        tag, attr = ("a", f' href="{href}"') if href else ("div", "")
        out += f"""<{tag} class="card"{attr}>
  <div class="card-media">{img(ctx, image, title, sizes='(min-width: 900px) 25vw, 100vw')}</div>
  <h3>{e(title)}</h3><p>{e(text)}</p>
</{tag}>"""
    return f'<div class="cards cards-{len(items)}">{out}</div>'


def spec_rows(ctx, rows):
    return "".join(f"<tr><th scope=row>{e(t(k, ctx.lang))}</th><td>{e(t(v, ctx.lang))}</td></tr>" for k, v in rows)


def gallery(ctx, names, alt):
    items = "".join(
        f'<a href="{ctx.asset("assets/img/" + n)}" class="g-item" data-lb>{img(ctx, n, alt, sizes="(min-width: 900px) 33vw, 50vw")}</a>'
        for n in names
    )
    lead = " gallery-lead" if (len(names) + 3) % 3 == 0 else ""
    return f'<div class="gallery{lead}">{items}</div>'


def cta_band(ctx, title, text):
    lang = ctx.lang
    return f"""<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>{e(title)}</h2><p>{e(text)}</p></div>
    <div class="cta-actions">
      <a class="btn btn-dark" href="{ctx.page('contact')}">{e(t(C.UI['contact_cta'], lang))}</a>
      <a class="btn btn-outline" href="tel:{C.COMPANY['phone'].replace(' ', '')}">{icon('phone')} {e(C.COMPANY['phone_display'])}</a>
    </div>
  </div>
</section>"""


def fmt_date(iso, lang):
    d = dt.date.fromisoformat(iso)
    if lang == "de":
        months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        return f"{d.day}. {months[d.month - 1]} {d.year}"
    return d.strftime("%B %-d, %Y")


def news_card(ctx, n, full=True):
    lang = ctx.lang
    title = t(n["title"], lang)
    text = t(n.get("body") or n["summary"], lang)
    media = (f'<div class="news-media{" contain" if n.get("fit") == "contain" else ""}">{img(ctx, n["img"], "", sizes="(min-width: 900px) 33vw, 100vw")}</div>'
             if n.get("img") and ((IMG_DIR / n["img"]).exists() or not (IMG_DIR / ".fetched").exists())
             else '<div class="news-media news-media-empty">' + icon("grape", "icon big") + "</div>")
    link = ""
    if n.get("link"):
        label = t(C.UI["read_source"], lang) if n.get("summary") else n["source"]
        link = f'<a class="news-link" href="{n["link"]}" rel="noopener">{e(label)} {icon("ext")}</a>'
    src = f'<span class="news-source">{e(t(C.UI["source"], lang))}: {e(n["source"])}</span>' if n.get("summary") and n.get("source") else ""
    return f"""<article class="news-card">
  {media}
  <div class="news-body">
    <time datetime="{n['date']}">{fmt_date(n['date'], lang)}</time>
    <h3>{e(title)}</h3>
    <p>{e(text if full else text[:180].rsplit(' ', 1)[0] + ' …' if len(text) > 180 else text)}</p>
    <div class="news-foot">{src}{link}</div>
  </div>
</article>"""


# ------------------------------------------------------------------ pages
def home(ctx):
    h, lang = C.HOME, ctx.lang
    events = ""
    for ev in C.EVENTS:
        if dt.date.fromisoformat(ev["end"]) >= TODAY:
            events += f"""<a class="event" data-event-end="{ev['end']}" href="{ev['url']}" rel="noopener">
  <strong>{e(t(ev['title'], lang))}</strong><span class="event-text">{e(t(ev.get('short', ev['text']), lang))}</span></a>"""
    feat_imgs = ["grapes-1.jpg", "msh-g02.jpg", "msh-g06.jpg", "msh-row.jpg"]
    feats = cards(ctx, [(feat_imgs[i], t(f["title"], lang), t(f["text"], lang), None) for i, f in enumerate(h["features"])])
    models = "".join(
        f"""<a class="model" href="{ctx.page(p['page'])}">
  {img(ctx, p['img'], t(p['title'], lang), sizes='(min-width: 900px) 33vw, 100vw')}
  <div class="model-text"><h3>{e(t(p['title'], lang))}</h3><p>{e(t(p['text'], lang))}</p><span class="model-more">{e(t(C.UI['learn_more'], lang))}</span></div>
</a>""" for p in h["products"])
    s1, s2 = h["split1"], h["split2"]
    more = f'<a class="text-link" href="{ctx.page("msh")}">{e(t(C.UI["learn_more"], lang))}</a>'
    actions = (f'<a class="btn btn-light" href="{ctx.page("msh")}">{e(t(C.UI["learn_more"], lang))}</a>'
               f'<a class="btn btn-outline-light" href="{ctx.page("contact")}">{e(t(C.UI["contact_cta"], lang))}</a>')
    caption = ("Leseergebnis des Steillagen-Vollernters, direkt aus dem Sammelbehälter." if lang == "de"
               else "Harvest result of the Steep Slope Harvester, straight from the collecting bin.")
    body = f"""{hero(ctx, 'hero-mosel.jpg', t(h['hero_title'], lang), home=True, top=events, actions=actions, stats=h['stats'])}
{slope_story(ctx)}
{quality(ctx)}
{section(t(h['products_title'], lang), f'<div class="models">{models}</div>')}
{world_map(ctx)}
{split(ctx, 'msh-studio-ut125.jpg', t(h['story_title'], lang), f"<p>{e(t(h['story'], lang))}</p>", rev=True, studio=True)}
{cta_band(ctx, t(h['cta_title'], lang), t(h['cta_text'], lang))}"""
    return layout(ctx, t(h["title"], lang), t(h["description"], lang), body)


def msh(ctx):
    m, lang = C.MSH, ctx.lang
    secs = "".join(split(ctx, s['img'], t(s['title'], lang), paras(t(s['text'], lang)), rev=bool(i % 2), studio=True)
                   for i, s in enumerate(m["sections"]))
    alt = "Leseergebnis" if lang == "de" else "Harvest result"
    grid = "".join(f'<a href="{ctx.asset("assets/img/" + n)}" class="q-item" data-lb>{img(ctx, n, alt, sizes="(min-width: 900px) 16vw, 33vw")}</a>' for n in m["quality_imgs"])
    specs = f"""<div class="specs-wrap"><table class="specs"><tbody>{spec_rows(ctx, m['specs'])}</tbody></table>
<p class="fine">{e(t(m['specs_foot'], lang))}<br>{e(t(C.UI['specs_note'], lang))}</p></div>"""
    body = f"""{page_hero(ctx, m)}
{secs}
{split(ctx, None, t(m['quality_title'], lang), f"<p>{e(t(m['quality_text'], lang))}</p>", media=f'<div class="q-grid">{grid}</div>', grey=True)}
{section(t(m['specs_title'], lang), specs)}
{section(t(C.UI['gallery'], lang), gallery(ctx, m['gallery'], t(m['title'], lang)), grey=True)}
{cta_band(ctx, t(C.HOME['cta_title'], lang), t(C.HOME['cta_text'], lang))}"""
    return layout(ctx, t(m["title"], lang), t(m["description"], lang), body, m["hero_img"])


def ut125(ctx):
    u, lang = C.UT125, ctx.lang
    feats = "".join(split(ctx, f['img'], t(f['title'], lang), f"<p>{e(t(f['text'], lang))}</p>", rev=not bool(i % 2), label=t(f['kicker'], lang))
                    for i, f in enumerate(u["features"]))
    groups = "".join(
        f'<div class="spec-group"><h3>{e(t(g, lang))}</h3><table class="specs"><tbody>{spec_rows(ctx, rows)}</tbody></table></div>'
        for g, rows in u["spec_groups"])
    specs = f'<div class="spec-groups">{groups}</div><p class="fine">{e(t(u["specs_foot"], lang))}<br>{e(t(C.UI["specs_note"], lang))}</p>'
    body = f"""{page_hero(ctx, u)}
{split(ctx, 'ut125-side.jpg', t(u['built_title'], lang), f"<p>{e(t(u['lead'], lang))}</p><p>{e(t(u['intro'], lang))}</p>")}
{feats}
{section(t(u['specs_title'], lang), specs, grey=True)}
{section(t(C.UI['gallery'], lang), gallery(ctx, u['gallery'], t(u['title'], lang)))}
{cta_band(ctx, t(u['cta_title'], lang), t(C.HOME['cta_text'], lang))}"""
    return layout(ctx, t(u["title"], lang), t(u["description"], lang), body, u["hero_img"])


def keller(ctx):
    k, lang = C.KELLER, ctx.lang
    mods = "".join(
        f'<div class="module"><h3>{e(t(m["title"], lang))}</h3><p>{e(t(m["text"], lang))}</p></div>'
        for m in k["modules"])
    body = f"""{page_hero(ctx, k)}
{split(ctx, 'keller-2.jpg', t(k['system_title'], lang), f"<p>{e(t(k['intro'], lang))}</p><div class='modules'>{mods}</div>")}
{split(ctx, 'keller-3.jpg', t(k['custom_title'], lang), f"<p>{e(t(k['cta'], lang))}</p>", rev=True, grey=True)}
{cta_band(ctx, t(k['cta_title'], lang), t(k['cta_text'], lang))}"""
    return layout(ctx, t(k["title"], lang), t(k["description"], lang), body, k["hero_img"])


def news_page(ctx):
    n, lang = C.NEWS_PAGE, ctx.lang
    cards_html = "".join(news_card(ctx, x) for x in C.NEWS)
    body = f"""{page_hero(ctx, n)}
{section(None, f'<div class="news-grid">{cards_html}</div>')}"""
    return layout(ctx, t(n["title"], lang), t(n["description"], lang), body, n["hero_img"])


def contact(ctx):
    c, lang, co = C.CONTACT_PAGE, ctx.lang, C.COMPANY
    maps = "https://www.google.com/maps/search/?api=1&query="
    hours = "<br>".join(e(h) for h in t(C.UI["hours_text"], lang))
    p = co["production"]
    hq = f"""<p class="contact-line">{icon('pin')}<span>{e(co['name'])}<br>{e(co['street'])}<br>{e(co['zip_city'])}</span></p>
<p class="contact-line">{icon('phone')}<a href="tel:{co['phone'].replace(' ', '')}">{e(co['phone_display'])}</a></p>
<p class="contact-line">{icon('mail')}<a href="mailto:{co['email']}">{e(co['email'])}</a></p>
<p class="contact-line">{icon('clock')}<span>{hours}</span></p>
<div class="contact-actions"><a class="btn btn-dark" href="mailto:{co['email']}">{e(co['email'])}</a>
<a class="btn btn-outline" href="{maps}{e(co['name'] + ', ' + co['street'] + ', ' + co['zip_city'])}" rel="noopener">{e(t(C.UI['route'], lang))}</a></div>"""
    prod = f"""<p class="contact-line">{icon('pin')}<span>{e(co['name'])}<br>{e(p['street'])}<br>{e(p['zip_city'])}</span></p>
<p class="contact-line">{icon('phone')}<a href="tel:{p['phone'].replace(' ', '')}">{e(p['phone_display'])}</a></p>
<div class="contact-actions"><a class="btn btn-outline" href="{maps}{e(p['street'] + ', ' + p['zip_city'])}" rel="noopener">{e(t(C.UI['route'], lang))}</a></div>"""
    body = f"""{page_hero(ctx, c)}
{split(ctx, 'hero-mosel.jpg', t(C.UI['hq'], lang) + ' Kröv', hq)}
{split(ctx, 'ut125-hof.jpg', t(C.UI['production'], lang) + ' Wintrich', prod, rev=True)}"""
    return layout(ctx, t(c["title"], lang), t(c["description"], lang), body, c["hero_img"])


def imprint(ctx):
    lang, co = ctx.lang, C.COMPANY
    md = "<br>".join(e(m) for m in co["managing_directors"])
    if lang == "de":
        body = f"""<h1>Impressum</h1>
<p>Angaben gemäß § 5 DDG</p>
<p><strong>{e(co['name'])}</strong><br>{e(co['street'])}<br>54536 Kröv/Mosel<br>Deutschland</p>
<p>Telefon: <a href="tel:{co['phone'].replace(' ', '')}">{e(co['phone_display'])}</a><br>E-Mail: <a href="mailto:{co['email']}">{e(co['email'])}</a></p>
<h2>Geschäftsführung</h2><p>{md}</p>
<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: {e(co['vat_id'])}</p>"""
    else:
        body = f"""<h1>Imprint</h1>
<p>Information pursuant to § 5 DDG (German Digital Services Act)</p>
<p><strong>{e(co['name'])}</strong><br>{e(co['street'])}<br>54536 Kröv/Mosel<br>Germany</p>
<p>Phone: <a href="tel:{co['phone'].replace(' ', '')}">{e(co['phone_display'])}</a><br>Email: <a href="mailto:{co['email']}">{e(co['email'])}</a></p>
<h2>Managing directors</h2><p>{md}</p>
<h2>VAT ID</h2><p>VAT identification number pursuant to § 27a UStG: {e(co['vat_id'])}</p>"""
    title = t(C.NAV_LABELS["imprint"], lang)
    return layout(ctx, title, title + " – " + co["name"], f'<section class="section legal"><div class="wrap narrow prose">{body}</div></section>')


# --- privacy policy: imported from the old site's HTML, sanitised
class Sanitizer(HTMLParser):
    KEEP = {"p", "br", "strong", "b", "em", "i", "ul", "ol", "li", "a", "h2", "h3", "h4"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.depth_skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.depth_skip += 1
        if self.depth_skip or tag not in self.KEEP:
            return
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href.startswith(("http", "mailto:")):
                self.out.append(f'<a href="{e(href)}" rel="noopener">')
                return
            self.out.append("<a>")
            return
        self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.depth_skip -= 1
        if not self.depth_skip and tag in self.KEEP and tag != "br":
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.depth_skip:
            self.out.append(e(data))


def privacy_html():
    f = ROOT / "tools" / "_import" / "datenschutz.html"
    custom = ROOT / "legal" / "datenschutz.html"
    if custom.exists():  # an edited version takes precedence
        return custom.read_text()
    if not f.exists():
        return "<p>Die Datenschutzerklärung wird aus der bisherigen Website übernommen.</p>"
    raw = f.read_text(errors="ignore")
    m = re.search(r'data-elementor-type="wp-page".*?>(.*)<footer', raw, re.S) or re.search(r"<article.*?>(.*?)</article>", raw, re.S)
    s = Sanitizer()
    s.feed(m.group(1) if m else raw)
    out = "".join(s.out)
    out = re.sub(r"<p>\s*</p>", "", out)
    out = re.sub(r"^\s*(<h[1-4]>)?\s*Datenschutzerklärung\s*(</h[1-4]>)?", "", out, count=1)
    return out


PRIVACY_ADDENDUM = """
<h2>Hosting dieser Website</h2>
<p>Diese Website wird über GitHub Pages bereitgestellt (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Beim Aufruf der Website verarbeitet GitHub technisch notwendige Verbindungsdaten, insbesondere die IP-Adresse, um die Seiten auszuliefern und die Sicherheit des Dienstes zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; unser berechtigtes Interesse liegt in einer sicheren und zuverlässigen Bereitstellung der Website. GitHub ist unter dem EU-US Data Privacy Framework zertifiziert. Weitere Informationen: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub-Datenschutzerklärung</a>.</p>
<h2>Webanalyse mit Plausible Analytics</h2>
<p>Wir nutzen den Webanalysedienst Plausible Analytics (Plausible Insights OÜ, Västriku tn 2, 50403 Tartu, Estland). Die Daten werden ausschließlich auf Servern in der EU verarbeitet. Plausible verwendet keine Cookies und speichert keine Informationen auf Ihrem Endgerät. Es werden keine personenbezogenen Daten gespeichert: Die IP-Adresse wird nur kurzzeitig zur Bildung einer täglich wechselnden, anonymen Kennung genutzt und nicht gespeichert. Erfasst werden u. a. aufgerufene Seiten, Verweisquelle, Land, Gerätetyp, Browser und Betriebssystem in aggregierter Form. Eine Wiedererkennung von Besuchern über mehrere Tage oder Websites hinweg ist nicht möglich.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; unser berechtigtes Interesse liegt in der statistischen Auswertung der Nutzung, um unser Angebot zu verbessern. Weitere Informationen: <a href="https://plausible.io/data-policy" rel="noopener">plausible.io/data-policy</a>.</p>
<h2>Cookies auf dieser Website</h2>
<p>Diese Website setzt keine Cookies und bindet keine Inhalte von Drittanbietern (z. B. Schriftarten, Karten oder Videos) ein. Links zu sozialen Netzwerken sind einfache Verweise; Daten werden erst übertragen, wenn Sie einen solchen Link anklicken.</p>
"""


def privacy(ctx):
    lang = ctx.lang
    note = ""
    if lang == "en":
        note = '<p class="note">This privacy policy is provided in German. The German version is legally binding.</p>'
    body = f"""<section class="section legal"><div class="wrap narrow prose" lang="de">
<h1>{'Datenschutzerklärung' if lang == 'de' else 'Privacy policy'}</h1>{note}
{privacy_html()}
{PRIVACY_ADDENDUM}
</div></section>"""
    title = t(C.NAV_LABELS["privacy"], lang)
    return layout(ctx, title, title + " – " + C.COMPANY["name"], body)


def redirect_page(target_rel, target_abs):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Weiterleitung</title>
<link rel="canonical" href="{target_abs}"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={target_rel}"></head>
<body><a href="{target_rel}">{target_abs}</a></body></html>"""


# ------------------------------------------------------------------ main
RENDER = {"home": home, "msh": msh, "ut125": ut125, "keller": keller, "news": news_page,
          "contact": contact, "imprint": imprint, "privacy": privacy}


def write(path, html_text):
    target = OUT / path / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html_text)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for d in ("static", "assets"):
        if (ROOT / d).exists():
            shutil.copytree(ROOT / d, OUT / d, ignore=shutil.ignore_patterns(".fetched"))
    urls = []
    for key, paths in C.PAGES.items():
        for lang, path in paths.items():
            write(path, RENDER[key](Ctx(path, lang, key)))
            urls.append(f"{C.SITE_URL}/{path}")
    for old, (key, lang) in C.REDIRECTS.items():
        ctx = Ctx(old, lang, key)
        write(old, redirect_page(ctx.page(key), f"{C.SITE_URL}/{C.PAGES[key][lang]}"))
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {C.SITE_URL}/sitemap.xml\n")
    (OUT / "404.html").write_text(redirect_page("/", C.SITE_URL + "/"))
    if (ROOT / "CNAME").exists():
        shutil.copy(ROOT / "CNAME", OUT / "CNAME")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(urls)} pages + {len(C.REDIRECTS)} redirects into {OUT}")


if __name__ == "__main__":
    main()
