"""Export docs/slides.html to a 16:9 PDF, one slide per page (headless Chromium via Playwright; see render_slides.py for setup).
Run:  LD_LIBRARY_PATH=$CONDA_PREFIX/lib python scripts/export_slides_pdf.py [--out docs/slides.pdf]"""
from __future__ import annotations
import argparse, pathlib
from playwright.sync_api import sync_playwright

W, H = 1440, 810

def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--src", default="docs/slides.html"); ap.add_argument("--out", default="docs/slides.pdf")
    a = ap.parse_args()
    body = pathlib.Path(a.src).read_text(encoding="utf-8")
    html = ("<!doctype html><html><head><meta charset='utf-8'></head><body>" + body +
            f"<style>html{{scroll-behavior:auto!important;scroll-snap-type:none!important}} .slide{{height:{H}px;min-height:0;overflow:hidden;border:0;page-break-after:always;break-after:page}} .nav,.prog{{display:none!important}} @page{{size:{W}px {H}px;margin:0}}</style></body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(html, wait_until="networkidle"); pg.emulate_media(media="screen"); pg.wait_for_timeout(300)
        pg.pdf(path=a.out, width=f"{W}px", height=f"{H}px", print_background=True, prefer_css_page_size=True)
        b.close()
    print("wrote", a.out, pathlib.Path(a.out).stat().st_size // 1024, "KB")

if __name__ == "__main__":
    main()
