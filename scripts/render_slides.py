"""Render docs/slides.html to PNGs with headless Chromium (Playwright) so the deck can be checked without a desktop browser.
Setup (once, no root needed):  pip install playwright && python -m playwright install chromium
                               conda install -c conda-forge alsa-lib libgbm   # the two shared libs the bundled Chromium needs here
Run:  LD_LIBRARY_PATH=$CONDA_PREFIX/lib python scripts/render_slides.py [--out out_dir] [--slides 1,4,12]"""
from __future__ import annotations
import argparse, pathlib
from playwright.sync_api import sync_playwright

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="docs/slides.html"); ap.add_argument("--out", default="logs/slides")
    ap.add_argument("--slides", default="", help="comma-separated 1-based slide numbers; default all")
    ap.add_argument("--width", type=int, default=1440); ap.add_argument("--height", type=int, default=810)
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    body = pathlib.Path(a.src).read_text(encoding="utf-8")
    html = ("<!doctype html><html><head><meta charset='utf-8'></head><body>" + body +
            "<style>html{scroll-behavior:auto!important;scroll-snap-type:none!important}</style></body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": a.width, "height": a.height})
        pg.set_content(html, wait_until="networkidle")
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        want = [int(x) for x in a.slides.split(",") if x] or list(range(1, n + 1))
        for i in want:
            pg.evaluate(f"window.scrollTo(0, document.querySelectorAll('.slide')[{i-1}].offsetTop)")
            pg.wait_for_timeout(250); pg.screenshot(path=str(out / f"slide_{i:02d}.png"))
        b.close()
    print(f"rendered {len(want)} of {n} slides to {out}/")

if __name__ == "__main__":
    main()
