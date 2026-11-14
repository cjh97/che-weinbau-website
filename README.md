# che-weinbau.com

Website of CH engineering GmbH: static, bilingual (DE/EN), no cookies.

## How it works

| What | Where |
|---|---|
| All texts, specs, news, contact data | `content.py` |
| Page templates & HTML generation | `build.py` |
| Styles | `static/css/site.css` |
| Small scripts (menu, lightbox, analytics events) | `static/js/site.js` |
| Photos | `assets/img/` (thumbnails in `assets/img/thumbs/`) |
| Privacy policy (imported from the old site) | `tools/_import/datenschutz.html`, override with `legal/datenschutz.html` |
| Deploy | `.github/workflows/deploy.yml` → GitHub Pages |

Every push to `main` builds the site (`python build.py` → `_site/`) and publishes it to GitHub Pages.
On the very first run, the workflow also copies the photos from the old WordPress site (`tools/assets.json`).

### Common changes

- **News:** add an entry at the top of `NEWS` in `content.py` (image goes into `assets/img/`).
- **Trade-fair banner:** edit `EVENTS` in `content.py`. Banners hide themselves after their end date.
- **Specs:** `MSH["specs"]` and `UT125["spec_groups"]` in `content.py`.
- **Analytics:** Plausible (`PLAUSIBLE_DOMAIN` in `content.py`). Phone/email clicks are tracked as the `Contact` event.

### Local preview

```
python build.py --preview   # links end in index.html so it works from files
```

Old WordPress URLs (e.g. `/andreoli-ut-110/`, `/en/home/`, old news posts) redirect to the new pages (`REDIRECTS` in `content.py`).
