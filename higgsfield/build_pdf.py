#!/usr/bin/env python3
"""
HIGGSFIELD — Pitch Deck — landscape PDF export (spec section 11).

  python3 build_pdf.py   ->  HIGGSFIELD_Pitch_Deck.pdf

Reads index.html (build_responsive.py output), rebuilds a print HTML from the
desktop deck, then renders it with headless Chrome at 1280x800 landscape, one
deck section per page. Video and live-map pages are dropped, the baked
hero/thanks glow is flattened, all motion and fade opacity is forced static.

The opacity-force list below is a deliberate SUPERSET of the JS FADES list
(it adds .cmp-tile,.plan-tile,.cp-wrap,.cp-img,.cp-name and .mfill so plan
and comparison images print un-faded). Do not trim it down to FADES.

Requires: Pillow (only when real baked slides exist), and a Chrome/Chromium
binary on PATH (chromium, chromium-browser, google-chrome, or CHROME_BIN).
"""

import os
import re
import shutil
import subprocess
import sys

OUT_PDF = "HIGGSFIELD_Pitch_Deck.pdf"
PRINT_HTML = "print.html"
SLIDES = [("img/slides/slide_00.jpg", "img/slides/slide_00_flat.jpg"),
          ("img/slides/slide_21.jpg", "img/slides/slide_21_flat.jpg")]

# Same Google Fonts link as the site (brand token).
GF_HREF = "https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@300;400;600&display=swap"


def flatten(src, out):
    """Replace every pixel within Euclidean color distance < 24 of the corner
    pixel (5,5) with that exact color, killing the baked-in radial glow that
    cannot render flat in print. Saved quality=93, progressive (house style)."""
    from PIL import Image
    img = Image.open(src).convert("RGB")
    base = img.getpixel((5, 5))
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if (r - base[0]) ** 2 + (g - base[1]) ** 2 + (b - base[2]) ** 2 < 24 ** 2:
                px[x, y] = base
    img.save(out, quality=93, progressive=True)


def find_chrome():
    for c in (os.environ.get("CHROME_BIN"), "chromium", "chromium-browser",
              "google-chrome", "google-chrome-stable", "chrome",
              "/opt/pw-browsers/chromium"):
        if c and shutil.which(c):
            return shutil.which(c)
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    sys.exit("no Chrome/Chromium binary found (set CHROME_BIN)")


def main():
    src = open("index.html").read()

    style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    deckm = re.search(r'<main class="desktop-deck">(.*?)</main>', src, re.S)
    deck = deckm.group(1)

    # drop non-printable pages: video + live map
    deck = re.sub(r'<section class="slide media vid".*?</section>', "", deck, flags=re.S)
    deck = re.sub(r'<section class="slide mapsec".*?</section>', "", deck, flags=re.S)

    # flatten baked hero/thanks glow and swap the flattened files in
    # (skipped automatically while the deck ships placeholder SVG art)
    flats = []
    for orig, flat in SLIDES:
        if os.path.isfile(orig) and orig in deck:
            flatten(orig, flat)
            deck = deck.replace(orig, flat)
            flats.append(flat)

    # headless Chrome must paint everything immediately
    deck = deck.replace(' loading="lazy"', "")

    print_css = """
@page{size:1280px 800px;margin:0}
html{scroll-snap-type:none!important;scroll-behavior:auto;background:#0A0F0C}
body{background:#0A0F0C}
.slide{width:1280px!important;height:800px!important;min-height:0!important;page-break-after:always;break-after:page;overflow:hidden;position:relative;transform:none!important;display:flex}
.slide:last-child{page-break-after:auto}
.slide *{animation:none!important}
.flowbg,.bar,.hint,.dot,.prog{display:none!important}
.natwrap,.wrap,.mframe,.mapwrap,.sgrid,.lock,.herofoot,.ty,.tycap,.cmp-tile,.plan-tile,.cp-wrap,.cp-img,.cp-name{opacity:1!important;transform:none!important}
.slide>img,.mfill{opacity:1!important;transform:none!important}
.cmp-tile img,.plan-tile img,.cp-img{box-shadow:none!important;background:transparent!important;border-radius:0!important}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
"""

    html = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="%s" rel="stylesheet">
<style>%s</style><style>%s</style></head>
<body><main class="desktop-deck">%s</main></body></html>""" % (
        GF_HREF, style, print_css, deck)

    open(PRINT_HTML, "w").write(html)

    chrome = find_chrome()
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=30000", "--no-pdf-header-footer",
        "--print-to-pdf=" + OUT_PDF,
        "file://" + os.path.abspath(PRINT_HTML),
    ], check=True)

    os.unlink(PRINT_HTML)
    for flat in flats:
        os.unlink(flat)

    try:
        import fitz
        doc = fitz.open(OUT_PDF)
        print("%s: %d pages, %d KB" % (OUT_PDF, doc.page_count,
                                       os.path.getsize(OUT_PDF) // 1024))
    except ImportError:
        print("%s: %d KB (install PyMuPDF for a page count)"
              % (OUT_PDF, os.path.getsize(OUT_PDF) // 1024))


if __name__ == "__main__":
    main()
