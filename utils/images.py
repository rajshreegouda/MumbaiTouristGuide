"""Real photos come from Wikipedia / Wikimedia Commons (free licences, attribution shown in footer).
Images are cached in assets/images so the app works offline after the first download."""
import re
from pathlib import Path
import requests

IMG_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"
API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "MumbaiTouristGuide/1.0 (student project; streamlit)"}
_tried = set()


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _query(**params):
    p = {"action": "query", "format": "json", "redirects": 1, **params}
    return requests.get(API, params=p, headers=HEADERS, timeout=8).json().get("query", {})


def _first_page(q):
    pages = q.get("pages", {})
    return next(iter(pages.values())) if pages else {}


def download_for(name, wiki_title):
    """Download a photo for a place. Returns saved filename or ''."""
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    titles = [t for t in (wiki_title, name) if t]
    for t in titles:
        try:
            page = _first_page(_query(titles=t, prop="pageimages", pithumbsize=1100))
            src = page.get("thumbnail", {}).get("source")
            if not src:  # fall back to search
                hits = _query(list="search", srsearch=t + " Mumbai", srlimit=1).get("search", [])
                if hits:
                    page = _first_page(_query(titles=hits[0]["title"], prop="pageimages", pithumbsize=1100))
                    src = page.get("thumbnail", {}).get("source")
            if src:
                data = requests.get(src, headers=HEADERS, timeout=15).content
                fn = slug(name) + ".jpg"
                (IMG_DIR / fn).write_bytes(data)
                return fn
        except Exception:
            continue
    return ""


def wiki_summary(wiki_title, sentences=4):
    try:
        page = _first_page(_query(titles=wiki_title, prop="extracts", exintro=1, explaintext=1, exsentences=sentences))
        return page.get("extract", "")
    except Exception:
        return ""


def resolve(place, allow_fetch=False):
    """Return a local path / URL usable by st.image, or None."""
    img = (place.get("image") or "").strip()
    if img.startswith("http"):
        return img
    if img and (IMG_DIR / img).exists():
        return str(IMG_DIR / img)
    fn = slug(place["name"]) + ".jpg"
    if (IMG_DIR / fn).exists():
        return str(IMG_DIR / fn)
    if allow_fetch and place["name"] not in _tried:
        _tried.add(place["name"])
        got = download_for(place["name"], place.get("wiki_title"))
        if got:
            return str(IMG_DIR / got)
    return None
