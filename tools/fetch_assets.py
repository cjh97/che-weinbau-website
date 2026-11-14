"""One-time import of images (and the privacy-policy page) from the old WordPress site.

Runs inside GitHub Actions (see .github/workflows/deploy.yml). Downloads each image
listed in tools/assets.json, resizes it to max 2000px, saves an optimised JPEG/PNG to
assets/img/, plus an 800px thumbnail in assets/img/thumbs/.
"""
import io
import json
import pathlib
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((ROOT / "tools" / "assets.json").read_text())
out = ROOT / "assets" / "img"
thumbs = out / "thumbs"
imp = ROOT / "tools" / "_import"
for d in (out, thumbs, imp):
    d.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (asset import for che-weinbau.com rebuild)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


failed = []
for name, src in cfg["images"].items():
    url = cfg["base"] + src
    try:
        im = Image.open(io.BytesIO(get(url)))
        im.load()
        target = out / name
        if name.endswith(".png"):
            im = im.convert("RGBA")
            im.thumbnail((1200, 1200))
            im.save(target, optimize=True)
            continue
        im = im.convert("RGB")
        big = im.copy()
        big.thumbnail((2000, 2000))
        big.save(target, "JPEG", quality=82, optimize=True, progressive=True)
        small = im.copy()
        small.thumbnail((800, 800))
        small.save(thumbs / name, "JPEG", quality=78, optimize=True, progressive=True)
        print("ok", name)
    except Exception as e:  # keep going, report at the end
        failed.append(f"{name} <- {url}: {e}")

for name, url in cfg.get("pages", {}).items():
    try:
        (imp / name).write_bytes(get(url))
        print("ok", name)
    except Exception as e:
        failed.append(f"{name} <- {url}: {e}")

(out / ".fetched").write_text("\n".join(failed) or "all ok\n")
if failed:
    print("FAILED:\n" + "\n".join(failed), file=sys.stderr)
