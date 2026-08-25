#!/usr/bin/env python3
"""
HIGGSFIELD — Pitch Deck (scroll-deck website template)

Single-scroll pitch-deck website generator, built to the Scroll-Deck Website
Design System & Build Spec (reference build: YONEX Venice).

  python3 build_responsive.py   ->  index.html  (one self-contained file,
                                     two parallel decks: desktop + mobile)

HOW TO USE THIS TEMPLATE
  Every value in the "BRAND TOKENS" block below is a placeholder to swap.
  Everything under "FIXED SYSTEM" (CSS physics, JS, thresholds, curves) must
  stay byte-identical per the spec: the 0.32 fade divisor,
  cubic-bezier(.16,1,.3,1), luminance >148, probes 42 / 0.4 / 0.5,
  .55s/.3s/.12s timings, top:22px, z-index 50/60, the 720px breakpoint,
  100svh sizing, snap rules, the radius/shadow/tracking ladders.

  PLACEHOLDER_ART=True inlines labeled SVG stand-ins for every image so the
  template previews without assets. Set it to False once real files exist at
  the img/ paths listed in tokens.json / README.md.

Copy rule: no em-dash in copy; keep &rsquo; and &middot;.
"""

import re
from urllib.parse import quote

# ============================================================================
# BRAND TOKENS  (all placeholders — swap per brand, see spec section 1)
# ============================================================================

PLACEHOLDER_ART = True          # False once real assets exist under img/

BRAND_NAME    = "HIGGSFIELD"
PROJECT_NAME  = "Pitch Deck"
PARTNER_NAME  = "[PARTNER / CO-BRAND]"          # placeholder partner lockup
PAGE_TITLE    = "Higgsfield · Pitch Deck"

# --- Fonts (display face + label/body face) ---------------------------------
# Display: condensed heavy all-caps grotesque, single weight, always uppercase.
# Label/body: workhorse sans at 300/400/600.
GF_HREF        = "https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@300;400;600&display=swap"
DISPLAY_STACK  = "'Anton',Impact,sans-serif"
LAB_STACK      = "Inter,-apple-system,sans-serif"   # --lab var (labels)
BODY_STACK     = "Inter,sans-serif"                 # literal stack (body, 300)

# --- Accent + derived siblings (re-derive both at matching lightness) -------
GREEN          = "#A3E635"    # primary accent (placeholder acid green)
GREEN_ONDARK   = "#B7F34D"    # brighter sibling, legibility on deep grounds
GREEN_ONLIGHT  = "#4D7C0F"    # darker sibling, used only under .dk

# --- Ink --------------------------------------------------------------------
INK            = "#EDF3EE"    # default body text (light green-white)
HEADLINE_INK   = "#f4f3ee"    # warm paper white for display headers
DARK_INK       = "#15110c"    # dark-scheme base ink (under .dk)

# --- The dark family (spec: "navy family", here charcoal-green) -------------
INTRO_BG       = "#12211A"    # brand ground: every non-concept native section
                              #   (luminance must stay <= 148; this is ~29)
MB_NAVY        = "#070B08"    # mobile body base (near-black)
PAGE_BASE      = "#0A0F0C"    # html/body fallback + flow-gradient end stop
FLOW_MID       = "#141D17"    # flow-gradient mid stop
FLOW_BRIGHT    = "#1E2B22"    # flow-gradient bright stop
PH_TILE_1      = "#101812"    # placeholder fill behind loading images
PH_TILE_2      = "#0C120E"    # media-frame placeholder fill
SCRIM_INK      = "rgba(6,12,8"          # summary-scrim ink (r,g,b prefix)
GLOW_RGB       = "183,243,77"           # mobile glow tint (GREEN_ONDARK rgb)
MB_TINT_RGB    = "112,168,128"          # mobile body radial tint (sage)
CURSOR_CORE    = "#d9ffb3"    # cursor dot core
CURSOR_MID     = "#a3e635"    # cursor dot mid
CURSOR_GLOW    = "rgba(163,230,53,.5)"  # cursor dot glow

# --- Concepts (the three pitch pillars) -------------------------------------
# Each key needs: MCONCEPT, REF_BG/REF_FG, REF_META, DETAILS, CONCEPT_NAME,
# REF_ORDER, a body string, a TOC row and a SUMTILES row.
CONCEPTS = ["engine", "studio", "network"]          # order = SUMTILES order

CONCEPT_NAME = {
    "engine":  "ENGINE",      # placeholder: pillar 01 name
    "studio":  "STUDIO",      # placeholder: pillar 02 name
    "network": "NETWORK",     # placeholder: pillar 03 name
}

# key -> (backgroundHex, isDarkText). Light bg => dk True.
MCONCEPT = {
    "engine":  ("#122A1C", False),   # deep green ground, light text
    "studio":  ("#EFEAE0", True),    # bone ground, dark text
    "network": ("#E3E7E1", True),    # pale sage ground, dark text
}

# Desktop reference walls: split fg/bg.
REF_BG = {"engine": "#122A1C", "studio": "#EFEAE0", "network": "#E3E7E1"}
REF_FG = {"engine": "#f4f3ee", "studio": "#2a2620", "network": "#101a12"}

DETAILS = {"engine": 5, "studio": 5, "network": 5}   # keep the "/ 5"
                                                     # comparison denominator
                                                     # in sync if changed

# Per-concept reference-wall sub-line (r-line) + refs heading.
REF_META = {
    "engine":  ("References", "Placeholder r-line. One sentence on what this reference wall establishes for Pillar 01."),
    "studio":  ("References", "Placeholder r-line. One sentence on what this reference wall establishes for Pillar 02."),
    "network": ("References", "Placeholder r-line. One sentence on what this reference wall establishes for Pillar 03."),
}

# Hand-tuned tile permutation per concept (12 tiles, neighbour contrast).
REF_ORDER = {
    "engine":  [1, 7, 4, 10, 2, 8, 5, 11, 3, 9, 6, 12],
    "studio":  [2, 9, 5, 12, 1, 7, 4, 10, 6, 11, 3, 8],
    "network": [3, 10, 6, 12, 2, 8, 1, 9, 5, 11, 4, 7],
}

# Concept overview taglines + body copy (placeholders, no em-dashes).
TAGLINE = {
    "engine":  "Placeholder tagline · one line on Pillar 01",
    "studio":  "Placeholder tagline · one line on Pillar 02",
    "network": "Placeholder tagline · one line on Pillar 03",
}
ENGINE_B  = ("Placeholder overview body for Pillar 01. Two to four sentences on the core thesis, "
             "what it is, why it wins, and the proof behind it. Replace in build_responsive.py, "
             "keep it under roughly 70 words so the 780px reading column breathes.")
STUDIO_B  = ("Placeholder overview body for Pillar 02. Two to four sentences on the product surface, "
             "the workflow it unlocks, and who it serves. Replace in build_responsive.py, "
             "keep it under roughly 70 words so the 780px reading column breathes.")
NETWORK_B = ("Placeholder overview body for Pillar 03. Two to four sentences on distribution, "
             "community, and the compounding loop. Replace in build_responsive.py, "
             "keep it under roughly 70 words so the 780px reading column breathes.")
BODY = {"engine": ENGINE_B, "studio": STUDIO_B, "network": NETWORK_B}

# Facts pair on every concept cover (two key/value slots).
FACTS = [("Focus",  "Placeholder fact value 01"),
         ("Status", "Placeholder fact value 02 · 2026")]

# --- Nav (text-only, ~5 items so the mobile bar fits one line) --------------
NAV = [("Intro", "intro"), ("Engine", "engine"), ("Studio", "studio"),
       ("Network", "network"), ("Summary", "summary")]

# --- TOC rows: (key, number, name, right-tag) -------------------------------
TOC = [("engine",  "01", CONCEPT_NAME["engine"],  "Placeholder tag · Pillar 01"),
       ("studio",  "02", CONCEPT_NAME["studio"],  "Placeholder tag · Pillar 02"),
       ("network", "03", CONCEPT_NAME["network"], "Placeholder tag · Pillar 03")]
TOC_TITLE = "THREE PILLARS"          # placeholder deck-structure title

# --- Location / map (iframe keyed off lat/long coords, NOT an address query)
MAP_EB     = "Location"
MAP_TITLE  = "Higgsfield HQ"                                   # placeholder
MAP_ADDR   = "Placeholder Street &nbsp;&middot;&nbsp; San Francisco, CA"
MAP_COORDS = "37.7749,-122.4194"                               # placeholder
MAP_IFRAME_TITLE = "Higgsfield HQ"
MAP_SRC = "https://maps.google.com/maps?q=" + MAP_COORDS + "&z=16&hl=en&output=embed"

# --- Exploration (context grid) ---------------------------------------------
# NOTE (spec parity): the eyebrow + heading are hardcoded literals inside the
# two builders (d_explore / explore_m), not constants. Edit them there.
EXP_PARA = ("Placeholder exploration paragraph. Four to six sentences of market and culture "
            "context that set up the three pillars, replace in build_responsive.py. This block "
            "is the only long-form paragraph in the intro group, so use it to frame the "
            "problem, the moment, and why this team. Keep sentences short. No em-dashes, "
            "use a period or the &middot; connector instead.")
EXP_TILES = [  # 6 tiles: (image slot N, label, one-line desc)
    (1, "Placeholder label 01", "Placeholder one-line description for context tile 01."),
    (2, "Placeholder label 02", "Placeholder one-line description for context tile 02."),
    (3, "Placeholder label 03", "Placeholder one-line description for context tile 03."),
    (4, "Placeholder label 04", "Placeholder one-line description for context tile 04."),
    (5, "Placeholder label 05", "Placeholder one-line description for context tile 05."),
    (6, "Placeholder label 06", "Placeholder one-line description for context tile 06."),
]

# --- The Plans (the ONE live summary page) + comparison ---------------------
PLANS_EB    = "Next"
PLANS_TITLE = "THE ROADMAP"          # placeholder for "The Plans"
SUMTILES = [  # (key, caption) — fixes concept order everywhere
    ("engine",  CONCEPT_NAME["engine"]  + " &middot; Roadmap"),
    ("studio",  CONCEPT_NAME["studio"]  + " &middot; Roadmap"),
    ("network", CONCEPT_NAME["network"] + " &middot; Roadmap"),
]

HERO_SUB   = "Placeholder hero sub-line &middot; one sentence under the wordmark"
THANKS_TXT = "Thank you"

# --- Asset path convention (spec section 10.1) ------------------------------
P_SLIDE   = "img/slides/slide_%02d.jpg"          # baked hero/thanks
P_RENDER  = "img/renders/%s/d%d.jpg"             # concept details
P_VIDEO   = "img/vids/%s.mp4"                    # H.264 8-bit yuv420p 1920w
P_PLAN    = "img/plans/%s.png"                   # PNG on white, ~1400px
P_REF     = "img/m/refs/%s/r%02d.jpg"            # 12 per concept
P_EXP     = "img/m/exp/exp%d.jpg"                # 6 tiles
P_LOGO    = "img/logo.png"
P_PARTNER = "img/partner.png"

# ============================================================================
# helpers
# ============================================================================

def _rgb(hexs):
    h = hexs.lstrip("#")
    return "%d,%d,%d" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

INK_RGB      = _rgb(INK)
DARK_INK_RGB = _rgb(DARK_INK)
GREEN_RGB    = _rgb(GREEN)


def ph(path, label, w, h, bg, fg, big=None):
    """Placeholder art: labeled inline SVG data URI standing in for `path`.

    When PLACEHOLDER_ART is False the real asset path ships instead. The SVG
    names the asset slot so every image placeholder documents itself.
    """
    if not PLACEHOLDER_ART:
        return path
    fs1 = max(int(h * 0.05), 22)
    fs2 = max(int(h * 0.028), 13)
    head = ("<text x='50%%' y='40%%' fill='%s' fill-opacity='.95' font-family='Arial Black,Arial'"
            " font-size='%d' letter-spacing='6' text-anchor='middle'>%s</text>"
            % (fg, int(fs1 * 1.7), big)) if big else ""
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d'>"
           "<rect width='%d' height='%d' fill='%s'/>"
           "<rect x='8' y='8' width='%d' height='%d' fill='none' stroke='%s' stroke-opacity='.3' stroke-width='2'/>"
           "%s"
           "<text x='50%%' y='%s' fill='%s' fill-opacity='.85' font-family='Arial' font-size='%d'"
           " letter-spacing='3' text-anchor='middle'>%s</text>"
           "<text x='50%%' y='%s' fill='%s' fill-opacity='.5' font-family='monospace' font-size='%d'"
           " text-anchor='middle'>%s</text></svg>"
           % (w, h, w, h, bg, w - 16, h - 16, fg, head,
              "58%" if big else "48%", fg, fs1, label,
              "68%" if big else "58%", fg, fs2, path))
    return "data:image/svg+xml;utf8," + quote(svg, safe="")


def slide_bg(n):
    """bg_of(): with real assets, sample pixel (5,5) of slide_NN.jpg; in
    placeholder mode the baked slides ground on INTRO_BG."""
    if PLACEHOLDER_ART:
        return INTRO_BG
    from PIL import Image
    img = Image.open(P_SLIDE % n).convert("RGB")
    return "#%02x%02x%02x" % img.getpixel((5, 5))


def a_hero():
    return ph(P_SLIDE % 0, "BAKED HERO SLIDE · " + PROJECT_NAME, 2880, 1800,
              INTRO_BG, GREEN, big=BRAND_NAME)

def a_thanks():
    return ph(P_SLIDE % 21, "BAKED CLOSING SLIDE", 2880, 1800,
              INTRO_BG, GREEN, big="THANK YOU")

def a_detail(k, i):
    return ph(P_RENDER % (k, i), "%s · DETAIL %02d" % (CONCEPT_NAME[k], i),
              1600, 893, MCONCEPT[k][0], REF_FG[k])

def a_ref(k, n):
    return ph(P_REF % (k, n), "REF %02d" % n, 730, 548, MCONCEPT[k][0], REF_FG[k])

def a_exp(n):
    return ph(P_EXP % n, "CONTEXT %02d" % n, 794, 336, FLOW_MID, GREEN)

def a_plan(k):
    return ph(P_PLAN % k, "%s · ROADMAP (PNG on white)" % CONCEPT_NAME[k],
              1400, 1000, "#ffffff", "#22301f")

def a_logo():
    return ph(P_LOGO, "", 600, 160, INTRO_BG, HEADLINE_INK, big=BRAND_NAME)

def a_partner():
    return ph(P_PARTNER, PARTNER_NAME, 300, 80, INTRO_BG, HEADLINE_INK)

# ============================================================================
# DESKTOP BUILDERS  (one <section> per page; order in list = scroll order)
# ============================================================================

def dslide_img(src, bg, key=None):
    k = ' data-key="%s"' % key if key else ""
    return ('<section class="slide" style="background:%s" data-bg="%s"%s>'
            '<img src="%s" alt=""></section>' % (bg, bg, k, src))

def d_hero():
    return dslide_img(a_hero(), slide_bg(0), key="intro")

def d_thanks():
    return dslide_img(a_thanks(), slide_bg(21))

def d_map():
    return ('<section class="slide mapsec" data-bg="%s">'
            '<div class="mapwrap">'
            '<div class="maphead"><div class="mapeb">%s</div>'
            '<div class="maptitle">%s</div></div>'
            '<div class="mapframe"><iframe src="%s" title="%s" loading="lazy" '
            'referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
            '<div class="mapcap"><span class="mdot"></span>'
            '<span class="addr">%s</span></div>'
            '</div></section>'
            % (INTRO_BG, MAP_EB, MAP_TITLE, MAP_SRC, MAP_IFRAME_TITLE, MAP_ADDR))

def d_explore():
    tiles = "".join(
        '<div class="etile"><div class="ei"><img src="%s" alt="" loading="lazy"></div>'
        '<div class="el">%s</div><div class="ed">%s</div></div>'
        % (a_exp(n), lab, desc) for n, lab, desc in EXP_TILES)
    # eyebrow + heading are hardcoded literals here by design (spec parity)
    return ('<section class="slide nat explore" data-bg="%s">'
            '<div class="natwrap">'
            '<div class="eb">Market Context</div>'
            '<h2 class="ex-h gh">Exploration</h2>'
            '<p class="ex-para">%s</p>'
            '<div class="egrid">%s</div>'
            '</div></section>' % (INTRO_BG, EXP_PARA, tiles))

def d_toc():
    rows = "".join(
        '<button class="li" data-key="%s"><span class="ln">%s</span>'
        '<span class="lname gh">%s</span><span class="ltag">%s</span></button>'
        % (k, num, name, tag) for k, num, name, tag in TOC)
    return ('<section class="slide nat" style="background:%s" data-bg="%s">'
            '<div class="natwrap">'
            '<div class="eb tg">Table of Content</div>'
            '<h2 class="gh">%s</h2>'
            '<div class="dtoc">%s</div>'
            '</div></section>' % (INTRO_BG, INTRO_BG, TOC_TITLE, rows))

def d_overview(k, pos):
    bg, dk = MCONCEPT[k]
    darkc = " dk" if dk else ""
    facts = "".join('<div><span class="fk">%s</span><span class="fv">%s</span></div>'
                    % (fk, fv) for fk, fv in FACTS)
    return ('<section class="slide nat cover%s" style="background:%s" data-bg="%s" data-key="%s">'
            '<div class="natwrap cov-wrap">'
            '<div class="eb">[ %02d / %02d ] &nbsp;Pillar</div>'
            '<h2 class="cov-h gh">%s</h2>'
            '<div class="cov-tag">%s</div>'
            '<p class="cov-body">%s</p>'
            '<div class="cov-facts">%s</div>'
            '</div></section>'
            % (darkc, bg, bg, k, pos + 1, len(CONCEPTS), CONCEPT_NAME[k],
               TAGLINE[k], BODY[k], facts))

def d_refs(k):
    bg, fg = REF_BG[k], REF_FG[k]
    head, line = REF_META[k]
    tiles = "".join('<button class="ref-tile"><img src="%s" alt="" loading="lazy"></button>'
                    % a_ref(k, n) for n in REF_ORDER[k])
    return ('<section class="slide nat refs" style="background:%s;--rfg:%s" data-bg="%s">'
            '<div class="natwrap">'
            '<div class="r-head"><div class="eb">%s</div>'
            '<h3 class="gh">%s</h3>'
            '<div class="r-line">%s</div></div>'
            '<div class="dgrid">%s</div>'
            '</div></section>' % (bg, fg, bg, head, CONCEPT_NAME[k], line, tiles))

def d_video(k):
    bg, _ = MCONCEPT[k]
    label = "%s &middot; Film" % CONCEPT_NAME[k]
    if PLACEHOLDER_ART:
        inner = ('<img class="mfill" src="%s" alt="">'
                 % ph(P_VIDEO % k, "%s · FILM (H.264 yuv420p · 1920w · +faststart)"
                      % CONCEPT_NAME[k], 1920, 1080, bg, REF_FG[k]))
    else:
        inner = ('<video class="mfill mvid" src="%s" muted loop playsinline '
                 'preload="metadata"></video>' % (P_VIDEO % k))
    return ('<section class="slide media vid" style="background:%s" data-bg="%s">'
            '<div class="mframe">%s</div><span class="rlabel">%s</span></section>'
            % (bg, bg, inner, label))

def d_plan(k):
    return ('<section class="slide nat conceptplan dk" style="background:#fff" data-bg="#ffffff">'
            '<div class="natwrap cp-wrap">'
            '<img class="cp-img" src="%s" alt="">'
            '<div class="cp-name">%s &middot; Roadmap</div>'
            '</div></section>' % (a_plan(k), CONCEPT_NAME[k]))

def d_details(k):
    bg, _ = MCONCEPT[k]
    out = []
    for i in range(1, DETAILS[k] + 1):
        out.append('<section class="slide media detail" style="background:%s" data-bg="%s">'
                   '<div class="mframe"><img class="mfill" src="%s" alt="" loading="lazy"></div>'
                   '<span class="rlabel">%s &middot; Detail %02d</span></section>'
                   % (bg, bg, a_detail(k, i), CONCEPT_NAME[k], i))
    return out

def d_plans():
    tiles = "".join('<figure class="plan-tile"><img src="%s" alt="" loading="lazy">'
                    '<figcaption>%s</figcaption></figure>'
                    % (a_plan(k), cap) for k, cap in SUMTILES)
    return ('<section class="slide nat" style="background:%s" data-bg="%s" data-key="summary">'
            '<div class="natwrap">'
            '<div class="eb">%s</div><h2 class="gh">%s</h2>'
            '<div class="plan-grid">%s</div>'
            '</div></section>' % (INTRO_BG, INTRO_BG, PLANS_EB, PLANS_TITLE, tiles))

def d_compare(n):
    tiles = "".join('<figure class="cmp-tile"><img src="%s" alt="" loading="lazy">'
                    '<figcaption>%s</figcaption></figure>'
                    % (a_detail(k, n), CONCEPT_NAME[k]) for k, _ in SUMTILES)
    return ('<section class="slide nat compare" style="background:%s" data-bg="%s">'
            '<div class="natwrap">'
            '<div class="eb">Comparison &middot; [ %d / 5 ]</div>'
            '<h2 class="gh">View %02d</h2>'
            '<div class="cmp-grid">%s</div>'
            '</div></section>' % (INTRO_BG, INTRO_BG, n, n, tiles))

# ============================================================================
# MOBILE BUILDERS  (free scroll; sections transparent, body bg eases)
# ============================================================================

def hero():
    return ('<section class="m hero glow" data-bg="%s" data-key="intro" id="m-intro">'
            '<div class="lock"><img class="mlogo" src="%s" alt="%s">'
            '<div class="sub">%s</div></div>'
            '<div class="herofoot"><img class="lourdes" src="%s" alt="%s">'
            '<span class="scap">Scroll &darr;</span></div>'
            '</section>' % (INTRO_BG, a_logo(), BRAND_NAME, HERO_SUB,
                            a_partner(), PARTNER_NAME))

def mapsec():
    return ('<section class="m mapsec glow" data-bg="%s">'
            '<div class="mapwrap">'
            '<div class="maphead"><div class="eb">%s</div>'
            '<div class="maptitle">%s</div></div>'
            '<div class="mapframe"><iframe src="%s" title="%s" loading="lazy" '
            'referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
            '<div class="mapcap"><span class="mdot"></span>'
            '<span class="addr">%s</span></div>'
            '</div></section>'
            % (INTRO_BG, MAP_EB, MAP_TITLE, MAP_SRC, MAP_IFRAME_TITLE, MAP_ADDR))

def explore_m():
    tiles = "".join(
        '<div class="etile"><div class="ei"><img src="%s" alt="" loading="lazy"></div>'
        '<div class="el">%s</div><div class="ed">%s</div></div>'
        % (a_exp(n), lab, desc) for n, lab, desc in EXP_TILES)
    # eyebrow + heading hardcoded literals (spec parity with d_explore)
    return ('<section class="m explore glow" data-bg="%s">'
            '<div class="wrap">'
            '<div class="eb">Market Context</div>'
            '<h2 class="ex-h">Exploration</h2>'
            '<p class="ex-para">%s</p>'
            '<div class="egrid">%s</div>'
            '</div></section>' % (INTRO_BG, EXP_PARA, tiles))

def toc_m():
    rows = "".join(
        '<button class="li" data-key="%s"><span class="ln">%s</span>'
        '<span class="lname">%s</span></button>'
        % (k, num, name) for k, num, name, _tag in TOC)
    return ('<section class="m glow" data-bg="%s">'
            '<div class="wrap">'
            '<div class="eb tg">Table of Content</div>'
            '<h2>%s</h2>'
            '<div class="toc">%s</div>'
            '</div></section>' % (INTRO_BG, TOC_TITLE, rows))

def overview(k, pos):
    bg, dk = MCONCEPT[k]
    darkc = " dk" if dk else ""
    facts = "".join('<div><span class="fk">%s</span><span class="fv">%s</span></div>'
                    % (fk, fv) for fk, fv in FACTS)
    return ('<section class="m%s" data-bg="%s" data-key="%s" id="m-%s">'
            '<div class="wrap">'
            '<div class="eb">%s &middot; [ %02d / %02d ]</div>'
            '<h2>%s</h2>'
            '<div class="tag">%s</div>'
            '<p class="body">%s</p>'
            '<div class="facts">%s</div>'
            '</div></section>'
            % (darkc, bg, k, k, CONCEPT_NAME[k], pos + 1, len(CONCEPTS),
               CONCEPT_NAME[k], TAGLINE[k], BODY[k], facts))

def refs(k):
    bg, fg = REF_BG[k], REF_FG[k]
    head, line = REF_META[k]
    dk = " dk" if MCONCEPT[k][1] else ""
    tiles = "".join('<button class="tile"><img src="%s" alt="" loading="lazy"></button>'
                    % a_ref(k, n) for n in REF_ORDER[k])
    return ('<section class="m refs%s" data-bg="%s" style="--rfg:%s">'
            '<div class="wrap">'
            '<div class="r-head"><div class="eb">%s</div>'
            '<h3>%s</h3><div class="r-line">%s</div></div>'
            '<div class="grid">%s</div>'
            '</div></section>' % (dk, bg, fg, head, CONCEPT_NAME[k], line, tiles))

def mvideo(k):
    bg, _ = MCONCEPT[k]
    label = "%s &middot; Film" % CONCEPT_NAME[k]
    if PLACEHOLDER_ART:
        inner = ('<img class="mfill" src="%s" alt="">'
                 % ph(P_VIDEO % k, "%s · FILM" % CONCEPT_NAME[k], 1080, 1920,
                      bg, REF_FG[k]))
    else:
        inner = ('<video class="mfill mvid" src="%s" muted loop playsinline '
                 'preload="metadata"></video>' % (P_VIDEO % k))
    return ('<section class="m media vid" data-bg="%s">'
            '<div class="mframe">%s</div><span class="rlabel">%s</span></section>'
            % (bg, inner, label))

def mplan(k):
    return ('<section class="m conceptplan glow dk" data-bg="#ffffff">'
            '<div class="cp-wrap">'
            '<img class="cp-img" src="%s" alt="">'
            '<div class="cp-name">%s &middot; Roadmap</div>'
            '</div></section>' % (a_plan(k), CONCEPT_NAME[k]))

def details(k):
    bg, _ = MCONCEPT[k]
    out = []
    for i in range(1, DETAILS[k] + 1):
        out.append('<section class="m media" data-bg="%s">'
                   '<div class="mframe"><img class="mfill" src="%s" alt="" loading="lazy"></div>'
                   '<span class="rlabel">%s &middot; Detail %02d</span></section>'
                   % (bg, a_detail(k, i), CONCEPT_NAME[k], i))
    return out

def plans_m():
    tiles = "".join('<figure class="plan-tile"><img src="%s" alt="" loading="lazy">'
                    '<figcaption>%s</figcaption></figure>'
                    % (a_plan(k), cap) for k, cap in SUMTILES)
    return ('<section class="m plans glow" data-bg="%s" data-key="summary">'
            '<div class="wrap">'
            '<div class="eb">%s</div><h2>%s</h2>'
            '<div class="plan-grid">%s</div>'
            '</div></section>' % (INTRO_BG, PLANS_EB, PLANS_TITLE, tiles))

def mcompare(n):
    tiles = "".join('<figure class="cmp-tile"><img src="%s" alt="" loading="lazy">'
                    '<figcaption>%s</figcaption></figure>'
                    % (a_detail(k, n), CONCEPT_NAME[k]) for k, _ in SUMTILES)
    return ('<section class="m compare glow" data-bg="%s">'
            '<div class="wrap">'
            '<div class="eb">Comparison &middot; [ %d / 5 ]</div>'
            '<h2>View %02d</h2>'
            '<div class="cmp-grid">%s</div>'
            '</div></section>' % (INTRO_BG, n, n, tiles))

def thanks():
    return ('<section class="m thanks glow" data-bg="%s">'
            '<div class="ty">%s</div></section>' % (INTRO_BG, THANKS_TXT))

# ============================================================================
# ASSEMBLY  (order in list = DOM order = scroll order; both decks identical
# inventory; dead builders — render pages, a "Three Concepts" grid, a mobile
# goal section — are intentionally NOT wired, per spec)
# ============================================================================

desktop_secs = [d_hero(), d_map(), d_explore(), d_toc()]
for _i, _k in enumerate(CONCEPTS):
    desktop_secs += [d_overview(_k, _i), d_refs(_k), d_video(_k), d_plan(_k)]
    desktop_secs += d_details(_k)
desktop_secs += [d_plans()]
desktop_secs += [d_compare(n) for n in range(1, 6)]
desktop_secs += [d_thanks()]
desktop = "\n".join(desktop_secs)

mobile_secs = [hero(), mapsec(), explore_m(), toc_m()]
for _i, _k in enumerate(CONCEPTS):
    mobile_secs += [overview(_k, _i), refs(_k), mvideo(_k), mplan(_k)]
    mobile_secs += details(_k)
mobile_secs += [plans_m()]
mobile_secs += [mcompare(n) for n in range(1, 6)]
mobile_secs += [thanks()]
mobile = "\n".join(mobile_secs)

nav_html = "".join('<a data-key="%s">%s</a>' % (k, lab) for lab, k in NAV)

# ============================================================================
# FIXED SYSTEM CSS  (spec sections 2-7; only @TOKENS@ swap per brand)
# ============================================================================

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--green:@GREEN@;--ink:@INK@;--bar:72px;--lab:@LAB@}
html{scroll-snap-type:y mandatory;scroll-behavior:smooth;background:@BASE@;-webkit-text-size-adjust:100%}
body{background:@BASE@;color:var(--ink);font-family:@LAB@;font-weight:300;overflow-x:clip}
a{text-decoration:none;color:inherit}
button{background:none;border:0;color:inherit;font:inherit}
img{display:block}
figure{margin:0}
.flowbg{position:fixed;inset:0;z-index:-1;background:radial-gradient(120% 80% at 50% 34%,@FLOWB@ 0%,@FLOWM@ 46%,@BASE@ 100%)}
.prog{position:fixed;top:0;left:0;height:3px;width:0;background:var(--green);z-index:60;transition:width .12s linear}
.bar{position:fixed;top:22px;left:50%;transform:translateX(-50%);z-index:50;display:flex;gap:0;align-items:center;padding:0;background:none}
.bar a{font:300 10px/1 var(--lab);letter-spacing:.24em;color:rgba(246,249,253,.6);text-transform:uppercase;padding:9px 18px;transition:color .3s ease,opacity .3s ease;cursor:pointer;white-space:nowrap}
.bar a:hover{color:#fff}
.bar a.active{color:var(--green)}
.bar.dark a{color:rgba(14,20,30,.5)}
.bar.dark a:hover{color:#0b1220}
.bar.dark a.active{color:var(--green)}
.hint{position:fixed;left:50%;bottom:18px;transform:translate(-50%,0);z-index:40;font:400 10px/1 var(--lab);letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.55);animation:bob 2.4s ease-in-out infinite;pointer-events:none}
@keyframes bob{0%,100%{transform:translate(-50%,0)}50%{transform:translate(-50%,6px)}}
.mobile-deck{display:none}
.slide{height:100svh;scroll-snap-align:start;scroll-snap-stop:always;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}
.slide>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;will-change:opacity}
.slide.nat{padding:78px 6vw 44px}
.natwrap{width:100%;max-width:1200px;opacity:0;position:relative;z-index:2}
.slide.media{padding:0}
.mframe{width:100%;height:100%;border-radius:0;overflow:hidden;background:@PH2@;opacity:0;will-change:opacity;position:relative}
.mfill{width:100%;height:100%;object-fit:cover;object-position:center}
img.mfill{cursor:zoom-in}
.rlabel{position:absolute;right:36px;bottom:32px;z-index:3;font:400 12px/1 var(--lab);letter-spacing:.14em;color:#fff;text-transform:uppercase;opacity:.92;text-shadow:0 1px 10px rgba(0,0,0,.5);pointer-events:none}
.nat .eb{font:400 13px/1 var(--lab);letter-spacing:.2em;color:var(--green);text-transform:uppercase;margin-bottom:16px}
.tg,.eb.tg{color:@GREEND@!important}
.nat h2{font:400 clamp(40px,5vw,70px)/.98 @DISPLAY@;color:#f4f3ee;text-transform:uppercase}
.gh{position:relative;display:inline-block}
.gh::after{content:attr(data-t);position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;color:transparent;background:radial-gradient(150px 150px at var(--hx,50%) var(--hy,50%),rgba(@GREENRGB@,.98),rgba(@GREENRGB@,0) 62%);-webkit-background-clip:text;background-clip:text;opacity:0;transition:opacity .3s ease}
.gh:hover::after{opacity:1}
.cov-wrap{max-width:1200px}
.cov-h{font:400 clamp(50px,7vw,108px)/.95 @DISPLAY@;color:#f4f3ee;text-transform:uppercase;margin:6px 0 0}
.cov-tag{font:400 clamp(15px,1.4vw,21px)/1.2 var(--lab);letter-spacing:.05em;color:var(--green);text-transform:uppercase;margin:18px 0 22px}
.cov-body{font:300 clamp(14px,1.05vw,17px)/1.62 @BODYSTACK@;color:@INK@;max-width:780px;margin:0 0 34px}
.cov-facts{display:flex;gap:56px}
.cov-facts>div{display:flex;flex-direction:column;gap:8px}
.fk{font:400 11px/1 var(--lab);letter-spacing:.14em;text-transform:uppercase;color:rgba(@INKRGB@,.5)}
.fv{font:300 13px/1.3 var(--lab);letter-spacing:.03em;color:rgba(@INKRGB@,.85)}
.slide.nat.dk h2,.slide.nat.dk h3,.slide.nat.dk .cov-h{color:@DARKINK@}
.slide.nat.dk .cov-body{color:rgba(@DARKINKRGB@,.82)}
.slide.nat.dk .cov-tag{color:@GREENL@}
.slide.nat.dk .fk{color:rgba(@DARKINKRGB@,.5)}
.slide.nat.dk .fv{color:rgba(@DARKINKRGB@,.85)}
.slide.nat.dk .r-line{color:rgba(@DARKINKRGB@,.55)}
.slide.nat.dk .cp-name{color:rgba(@DARKINKRGB@,.82)}
.slide.refs .natwrap{max-width:1320px;height:100%;display:flex;flex-direction:column}
.r-head{flex:0 0 auto;margin-bottom:16px}
.r-head .eb{margin-bottom:0}
.r-head h3{font:400 clamp(28px,3.2vw,46px)/1 @DISPLAY@;text-transform:uppercase;color:var(--rfg,#f4f3ee);margin:6px 0}
.r-line{font:400 12px/1.3 var(--lab);letter-spacing:.06em;color:var(--rfg,#f4f3ee);opacity:.66}
.dgrid{flex:1 1 auto;min-height:0;display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:1fr;gap:12px}
.ref-tile{border:0;padding:0;border-radius:10px;overflow:hidden;cursor:zoom-in;position:relative;background:@PH1@;transition:transform .5s cubic-bezier(.16,1,.3,1),box-shadow .5s}
.ref-tile img{width:100%;height:100%;object-fit:cover}
.ref-tile:hover{transform:scale(1.045);z-index:6;box-shadow:0 18px 50px rgba(0,0,0,.45)}
.ref-tile.zoomed{transform:scale(1.9);z-index:40;box-shadow:0 40px 120px rgba(0,0,0,.6)}
.dtoc{margin-top:26px;border-top:1px solid rgba(255,255,255,.14)}
.dtoc .li{display:grid;grid-template-columns:60px minmax(0,1fr) auto;gap:20px;align-items:center;width:100%;text-align:left;padding:26px 8px;border-bottom:1px solid rgba(255,255,255,.14);cursor:pointer;transition:padding .45s cubic-bezier(.16,1,.3,1),background .45s}
.dtoc .li:hover{padding-left:26px;background:linear-gradient(90deg,rgba(@GREENRGB@,.08),transparent 70%)}
.dtoc .li .ln{font:400 14px/1 var(--lab);letter-spacing:.1em;color:@GREEND@}
.dtoc .li .lname{font:400 clamp(15px,2vw,27px)/1 @DISPLAY@;text-transform:uppercase;color:#e0e0e3}
.dtoc .li .ltag{font:300 13px/1.3 var(--lab);letter-spacing:.04em;color:rgba(@INKRGB@,.55);text-align:right}
.explore{background:@INTRO@}
.ex-h{font:400 clamp(38px,4vw,58px)/1 @DISPLAY@;color:#fff;text-transform:uppercase;margin:4px 0 12px}
.ex-para{font:300 clamp(14px,1.05vw,16px)/1.55 @BODYSTACK@;color:#f2f1ec;max-width:1180px;margin:0 0 30px}
.egrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px 22px}
.etile .ei{aspect-ratio:397/168;border-radius:8px;overflow:hidden;margin-bottom:9px;background:@PH1@}
.etile .ei img{width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.16,1,.3,1);cursor:zoom-in}
.etile:hover .ei img{transform:scale(1.05)}
.etile .el{font:400 12px/1.3 var(--lab);letter-spacing:.16em;color:var(--green);text-transform:uppercase;margin-bottom:7px}
.etile .ed{font:300 14px/1.45 @BODYSTACK@;color:rgba(255,255,255,.9)}
.explore::after{content:'';position:absolute;inset:0;opacity:0;transition:opacity .5s ease;background:radial-gradient(200px 200px at var(--mx,50%) var(--my,50%),rgba(255,255,255,.5),rgba(255,255,255,.1) 42%,transparent 72%);mix-blend-mode:overlay;z-index:1;pointer-events:none}
.explore.reflect::after{opacity:1}
.mapsec{background:@INTRO@}
.mapwrap{width:100%;max-width:1200px;height:100svh;display:flex;flex-direction:column;padding:96px 5.5% 44px;opacity:0}
.maphead{margin-bottom:18px}
.mapeb{font:400 12px/1 var(--lab);letter-spacing:.2em;color:var(--green);text-transform:uppercase}
.maptitle{font:400 clamp(30px,5vw,54px)/.95 @DISPLAY@;color:#f2f1ec;text-transform:uppercase;margin-top:6px}
.mapframe{flex:1 1 auto;min-height:0;border:0;border-radius:12px;overflow:hidden}
.mapframe iframe{width:100%;height:100%;border:0;border-radius:12px}
.mapcap{display:flex;align-items:center;gap:10px;margin-top:16px;font:300 12px/1 var(--lab);letter-spacing:.08em;color:rgba(242,241,236,.8)}
.mdot{width:9px;height:9px;border-radius:50%;background:var(--green);flex:0 0 auto}
.addr{font:400 12px/1 var(--lab);letter-spacing:.05em;color:var(--green)}
.plan-grid{margin-top:22px;display:grid;grid-template-columns:repeat(3,1fr);gap:30px}
.plan-tile{display:flex;flex-direction:column;gap:22px;align-items:center}
.plan-tile img{width:100%;height:auto;border-radius:10px;background:#fff;box-shadow:0 22px 60px rgba(0,0,0,.4);cursor:zoom-in}
.plan-tile figcaption{font:600 clamp(12px,1vw,15px)/1 var(--lab);letter-spacing:.2em;text-transform:uppercase;color:rgba(@INKRGB@,.85);text-align:center}
.cp-wrap{display:flex;flex-direction:column;align-items:center;gap:30px}
.cp-img{height:66vh;width:auto;max-width:88vw;border-radius:10px;background:#fff;box-shadow:0 22px 60px rgba(0,0,0,.4);cursor:zoom-in}
.cp-name{font:600 clamp(12px,1vw,15px)/1 var(--lab);letter-spacing:.2em;text-transform:uppercase;color:rgba(@INKRGB@,.82)}
.compare .natwrap{max-width:1340px}
.cmp-grid{margin-top:24px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;align-items:start}
.cmp-tile{display:flex;flex-direction:column;gap:11px}
.cmp-tile img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:10px;background:@PH1@;box-shadow:0 18px 50px rgba(0,0,0,.4);cursor:zoom-in}
.cmp-tile figcaption{font:600 clamp(11px,.95vw,14px)/1 var(--lab);letter-spacing:.18em;text-transform:uppercase;color:rgba(@INKRGB@,.85);text-align:center}
.lb{position:fixed;inset:0;z-index:9998;display:flex;align-items:center;justify-content:center;background:rgba(5,9,18,.94);backdrop-filter:blur(6px);opacity:0;pointer-events:none;transition:opacity .35s}
.lb.open{opacity:1;pointer-events:auto}
.lb img{max-width:90vw;max-height:88vh;object-fit:contain;border-radius:6px;box-shadow:0 30px 100px rgba(0,0,0,.6);transform:scale(.96);transition:transform .4s cubic-bezier(.16,1,.3,1)}
.lb.open img{transform:scale(1)}
.lb .lbx{position:absolute;top:22px;right:26px;font:400 12px/1 var(--lab);letter-spacing:.2em;color:#fff;text-transform:uppercase;cursor:pointer}
.dot{position:fixed;top:0;left:0;width:13px;height:13px;border-radius:50%;background:radial-gradient(circle,@CURCORE@ 0%,@CURMID@ 55%,rgba(0,0,0,0) 100%);box-shadow:0 0 12px 3px @CURGLOW@;transform:translate(-50%,-50%);pointer-events:none;z-index:10000}
@media (pointer:fine){body{cursor:none}a,button,.ref-tile,.dtoc .li,.etile{cursor:none}}
@media (max-width:720px){
:root{--bar:46px}
html{scroll-snap-type:none;scroll-behavior:auto;overflow-x:clip;max-width:100%}
body{overflow-x:clip;max-width:100%;-webkit-overflow-scrolling:touch;overscroll-behavior:none;cursor:auto;background-color:@MBNAVY@;background-image:radial-gradient(135% 90% at 50% 26%,rgba(@MBTINT@,.13),rgba(@MBTINT@,.04) 42%,transparent 68%);background-attachment:fixed;transition:background-color .55s ease}
.desktop-deck{display:none}
.mobile-deck{display:block}
.flowbg{display:none}
.hint,.dot{display:none}
.gh::after{display:none}
.bar{left:0;right:0;top:0;transform:none;width:100%;border-radius:0;gap:0;padding:15px 12px;justify-content:space-between;flex-wrap:nowrap;overflow:visible;background:none}
.bar a{font:400 9.5px/1 var(--lab);letter-spacing:.04em;padding:4px 2px;white-space:nowrap}
.m,.m.mapsec{background:transparent;position:relative;overflow:hidden}
.m.glow{background-image:radial-gradient(88% 56% at 50% 46%,rgba(@GLOWRGB@,.15),rgba(@GLOWRGB@,.05) 46%,rgba(@GLOWRGB@,0) 76%)}
.m .wrap{padding:56px 20px;opacity:0}
.m .mframe,.m .wrap,.m .sgrid,.m .lock{will-change:opacity}
.eb{font:400 12px/1 var(--lab);letter-spacing:.16em;color:var(--green);text-transform:uppercase;margin-bottom:12px}
.m h2{font:400 clamp(40px,13vw,66px)/.94 @DISPLAY@;letter-spacing:.01em;color:#f4f3ee;text-transform:uppercase}
.tag{font:400 13px/1.3 var(--lab);letter-spacing:.06em;color:var(--green);text-transform:uppercase;margin:14px 0 18px}
.body{font:300 16px/1.65 @BODYSTACK@;color:rgba(@INKRGB@,.88);max-width:34em;letter-spacing:.002em}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px;max-width:420px}
.facts>div{display:flex;flex-direction:column;gap:7px}
.facts .fk{font:400 10px/1 var(--lab);letter-spacing:.14em}
.facts .fv{font:300 12px/1.3 var(--lab);letter-spacing:.03em}
.m.dk h2,.m.dk h3{color:@DARKINK@}
.m.dk .tag{color:@GREENL@}
.m.dk .body{color:rgba(@DARKINKRGB@,.82)}
.m.dk .fk{color:rgba(@DARKINKRGB@,.5)}
.m.dk .fv{color:rgba(@DARKINKRGB@,.85)}
.m.dk .r-line{color:rgba(@DARKINKRGB@,.55)}
.m.dk .cp-name{color:rgba(@DARKINKRGB@,.82)}
.hero{min-height:100svh;display:flex;flex-direction:column;padding:calc(var(--bar) + 24px) 16px 120px}
.lock{margin:auto;text-align:center;width:min(78vw,420px);opacity:0}
.mlogo{width:100%;height:auto}
.sub{font:400 10px/1.6 var(--lab);letter-spacing:.06em;color:rgba(@INKRGB@,.78);text-transform:uppercase;margin-top:12px}
.herofoot{position:absolute;left:16px;right:16px;bottom:34px;display:flex;align-items:center;justify-content:space-between;opacity:0}
.lourdes{height:18px;width:auto}
.scap{font:400 10px/1 var(--lab);letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.6)}
.m.mapsec .mapwrap{height:100svh;max-width:none;padding:calc(var(--bar) + 22px) 16px 30px}
.explore .wrap{padding:56px 18px 40px}
.ex-h{font:400 clamp(34px,12vw,50px)/.98 @DISPLAY@;margin:4px 0 12px}
.ex-para{font:300 14px/1.6 @BODYSTACK@;margin:0 0 26px}
.egrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 12px}
.etile .ei{aspect-ratio:397/220;margin-bottom:8px}
.etile .el{font:400 9.5px/1.2 var(--lab);letter-spacing:.1em;margin-bottom:4px}
.etile .ed{font:300 12px/1.4 @BODYSTACK@}
.toc{margin-top:14px}
.toc .li{display:grid;grid-template-columns:30px 1fr;gap:12px;align-items:center;width:100%;text-align:left;padding:18px 2px;border-top:1px solid rgba(255,255,255,.12);cursor:pointer}
.toc .li .ln{font:400 12px/1 var(--lab);letter-spacing:.08em;color:@GREEND@}
.toc .li .lname{font:400 clamp(13px,4vw,19px)/1 @DISPLAY@;text-transform:uppercase;color:#e0e0e3}
.refs{min-height:100svh;padding:calc(var(--bar) + 6px) 0 0}
.refs .wrap{padding:8px 12px 14px;display:flex;flex-direction:column;gap:18px}
.r-head h3{font:400 clamp(24px,7vw,34px)/.98 @DISPLAY@}
.r-line{font:400 11px/1.3 var(--lab);opacity:.62}
.grid{display:grid;grid-template-columns:repeat(2,1fr);grid-auto-rows:1fr;gap:8px}
.tile{border:0;padding:0;border-radius:8px;overflow:hidden;background:@PH1@;cursor:zoom-in}
.tile img{width:100%;height:100%;object-fit:cover;aspect-ratio:4/3}
.m.media{min-height:100svh;padding:14px;display:flex;align-items:center}
.m.media:not(.vid) .mframe{width:100%;height:auto;max-height:calc(100svh - 28px);border-radius:12px;background:transparent}
.m.media:not(.vid) img.mfill{width:100%;height:auto;object-fit:contain}
.m.media.vid{padding:0}
.m.media.vid .mframe{height:100svh;border-radius:0}
.m .rlabel{right:18px;bottom:26px;font:400 11px/1 var(--lab);letter-spacing:.12em}
.details .wrap{padding:56px 16px 104px}
.details h3{font:400 clamp(26px,8vw,38px)/1 @DISPLAY@;color:#f4f3ee;text-transform:uppercase}
.dstack{display:flex;flex-direction:column;gap:10px;margin-top:16px}
.dstack .dtile{border-radius:8px;overflow:hidden}
.m.conceptplan{min-height:100svh;display:flex;align-items:center}
.m.conceptplan .cp-wrap{width:100%;padding:calc(var(--bar) + 24px) 16px 40px;gap:22px;opacity:0}
.cp-img{width:90%;max-width:440px;height:auto;box-shadow:0 14px 40px rgba(0,0,0,.4)}
.cp-name{font:600 12px/1 var(--lab);letter-spacing:.18em}
.plan-grid{display:block;margin-top:18px}
.plans .plan-tile{margin:0 0 26px;gap:18px}
.plan-tile img{max-width:440px;box-shadow:0 14px 40px rgba(0,0,0,.4)}
.plan-tile figcaption{font:600 13px/1 var(--lab);letter-spacing:.18em}
.compare .cmp-grid{display:flex;flex-direction:column;gap:14px;margin-top:18px}
.cmp-tile img{aspect-ratio:16/9}
.cmp-tile figcaption{font:600 12px/1 var(--lab);letter-spacing:.16em;margin-top:8px}
.sgrid{padding:56px 14px 56px;opacity:0}
.stile{aspect-ratio:16/9;border-radius:10px;overflow:hidden}
.thanks{min-height:100svh;display:flex;align-items:center;justify-content:center;padding:40px 20px}
.ty{font:400 min(21vw,66px)/.95 @DISPLAY@;color:#f4f3ee;text-transform:uppercase;opacity:0}
}
@media (orientation:landscape) and (max-height:560px){
.m .wrap{padding:40px 24px}
.hero{padding-bottom:80px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}
.natwrap,.wrap,.mframe,.mapwrap,.sgrid,.lock,.herofoot,.ty,.tycap,.slide>img{opacity:1!important}
.hint{animation:none}}
"""

TOKENS = {
    "@GREEN@": GREEN, "@GREEND@": GREEN_ONDARK, "@GREENL@": GREEN_ONLIGHT,
    "@GREENRGB@": GREEN_RGB, "@INK@": INK, "@INKRGB@": INK_RGB,
    "@DARKINK@": DARK_INK, "@DARKINKRGB@": DARK_INK_RGB,
    "@INTRO@": INTRO_BG, "@BASE@": PAGE_BASE, "@MBNAVY@": MB_NAVY,
    "@FLOWM@": FLOW_MID, "@FLOWB@": FLOW_BRIGHT,
    "@PH1@": PH_TILE_1, "@PH2@": PH_TILE_2,
    "@GLOWRGB@": GLOW_RGB, "@MBTINT@": MB_TINT_RGB,
    "@CURCORE@": CURSOR_CORE, "@CURMID@": CURSOR_MID, "@CURGLOW@": CURSOR_GLOW,
    "@DISPLAY@": DISPLAY_STACK, "@LAB@": LAB_STACK, "@BODYSTACK@": BODY_STACK,
}
for _t, _v in TOKENS.items():
    CSS = CSS.replace(_t, _v)

# ============================================================================
# FIXED SYSTEM JS  (spec sections 3.7, 5, 6 — keep byte-identical; the FADES
# list and the prefers-reduced-motion block above must stay the same set)
# ============================================================================

JS = r"""
(function(){
'use strict';
var mq=function(){return matchMedia('(max-width:720px)').matches};
function deck(){return document.querySelector(mq()?'.mobile-deck':'.desktop-deck')}
var bar=document.getElementById('bar'),prog=document.getElementById('prog');
var links=[].slice.call(bar.querySelectorAll('a[data-key]'));
var bgEls=[].slice.call(document.querySelectorAll('section[data-bg]'));
var mSecs=[].slice.call(document.querySelectorAll('.mobile-deck section[data-bg]'));

/* ---- unified scroll-driven fade (0.32 divisor is fixed physics) ---- */
var FADES=[].slice.call(document.querySelectorAll('.natwrap, .wrap, .mframe, .mapwrap, .sgrid, .lock, .herofoot, .ty, .tycap, .desktop-deck .slide>img'));
var NF=FADES.length,RECTS=new Array(NF),LASTO=new Array(NF),FVID=new Array(NF);
for(var fi=0;fi<NF;fi++){FVID[fi]=FADES[fi].querySelector?FADES[fi].querySelector('video'):null;}
function fadeAll(){
  var vh=innerHeight,i,r,el,v,o,inO,outO;
  for(i=0;i<NF;i++){RECTS[i]=FADES[i].getBoundingClientRect();}
  for(i=0;i<NF;i++){
    r=RECTS[i];el=FADES[i];v=FVID[i];
    if(r.height===0){if(v&&!v.paused)v.pause();continue;}
    inO=(vh-r.top)/(vh*0.32);outO=r.bottom/(vh*0.32);o=inO<outO?inO:outO;
    o=o<0?0:o>1?1:o;o=+o.toFixed(3);
    if(o!==LASTO[i]){LASTO[i]=o;el.style.opacity=o.toFixed(3);}
    if(v){var iv=(r.bottom>vh*0.12)&&(r.top<vh*0.88);
      if(iv){if(v.paused){var p=v.play();if(p&&p.catch)p.catch(function(){});}}
      else if(!v.paused){v.pause();}}
  }
}

/* ---- mobile body background easing (.55s via CSS transition) ---- */
var curBg=null;
function mBg(){if(!mq())return;var mid=innerHeight*0.5,pick=null,i,r;
  for(i=0;i<mSecs.length;i++){r=mSecs[i].getBoundingClientRect();
    if(r.top<=mid&&r.bottom>=mid){pick=mSecs[i];break;}}
  if(!pick){for(i=0;i<mSecs.length;i++){var rr=mSecs[i].getBoundingClientRect();
    if(rr.bottom>0){pick=mSecs[i];break;}}}
  if(pick){var c=pick.getAttribute('data-bg');
    if(c!==curBg){curBg=c;document.body.style.backgroundColor=c;}}}

/* ---- rAF coalescer ---- */
var uTick=false;function uReq(){if(!uTick){uTick=true;requestAnimationFrame(function(){fadeAll();mBg();uTick=false;});}}
addEventListener('scroll',uReq,{passive:true});addEventListener('resize',uReq);
addEventListener('load',function(){fadeAll();mBg();});fadeAll();mBg();

/* ---- nav theme flip by data-bg luminance (Rec. 709, threshold 148) ---- */
function lum(hex){if(!hex)return 0;
  hex=hex.replace('#','');
  if(hex.length===3)hex=hex.split('').map(function(c){return c+c;}).join('');
  var n=parseInt(hex,16);
  return 0.2126*(n>>16&255)+0.7152*(n>>8&255)+0.0722*(n&255);}
function navTheme(){var probe=42,cur=null,d=deck();
  for(var i=0;i<bgEls.length;i++){if(!d.contains(bgEls[i]))continue;
    var r=bgEls[i].getBoundingClientRect();
    if(r.top<=probe&&r.bottom>=probe)cur=bgEls[i];}
  if(cur)bar.classList.toggle('dark',lum(cur.getAttribute('data-bg'))>148);}
addEventListener('scroll',navTheme,{passive:true});addEventListener('resize',navTheme);navTheme();

/* ---- active nav link (probe innerHeight*0.4) ---- */
function act(){var secs=[].slice.call(deck().querySelectorAll('section[data-key]'));
  var cur='intro',mid=innerHeight*0.4;
  secs.forEach(function(s){var r=s.getBoundingClientRect();if(r.top<=mid)cur=s.dataset.key;});
  links.forEach(function(a){a.classList.toggle('active',a.dataset.key===cur);});}
addEventListener('scroll',act,{passive:true});addEventListener('resize',act);act();

/* ---- programmatic navigation ---- */
function goKey(k){var t=deck().querySelector('section[data-key="'+k+'"]');
  if(t)t.scrollIntoView({behavior:'smooth'});}
links.forEach(function(a){a.addEventListener('click',function(){goKey(a.dataset.key);});});
[].slice.call(document.querySelectorAll('.dtoc .li[data-key], .toc .li[data-key]'))
  .forEach(function(b){b.addEventListener('click',function(){goKey(b.dataset.key);});});

/* ---- progress bar ---- */
addEventListener('scroll',function(){var h=document.body.scrollHeight-innerHeight;
  prog.style.width=(h>0?scrollY/h*100:0)+'%';},{passive:true});

/* ---- lightbox ---- */
var lb=document.createElement('div');lb.className='lb';
lb.innerHTML='<img alt=""><span class="lbx">Close ✕</span>';
document.body.appendChild(lb);
var lbImg=lb.querySelector('img');
function openLB(src){lbImg.src=src;lb.classList.add('open');
  document.documentElement.style.overflow='hidden';}
function closeLB(){lb.classList.remove('open');
  document.documentElement.style.overflow='';}
lb.addEventListener('click',closeLB);
addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('open'))closeLB();});
[].slice.call(document.querySelectorAll('.ref-tile, .det-tile, .sum-tile, img.mfill, .plan-tile img, .cp-img, .cmp-tile img, .stile img, .etile .ei img, .tile'))
  .forEach(function(t){t.addEventListener('click',function(e){
    var im=t.tagName==='IMG'?t:t.querySelector('img');
    if(im){e.stopPropagation();openLB(im.src);}});});

/* ---- reference-tile 3s dwell zoom ---- */
[].slice.call(document.querySelectorAll('.ref-tile')).forEach(function(t){
  var timer=null;
  t.addEventListener('mouseenter',function(){timer=setTimeout(function(){t.classList.add('zoomed');},3000);});
  t.addEventListener('mouseleave',function(){clearTimeout(timer);t.classList.remove('zoomed');});
});

/* ---- keyboard navigation (desktop only) ---- */
addEventListener('keydown',function(e){
  if(mq()||lb.classList.contains('open'))return;
  var keys=['ArrowDown','PageDown',' ','ArrowUp','PageUp','Home','End'];
  if(keys.indexOf(e.key)===-1)return;
  var slides=[].slice.call(document.querySelectorAll('.desktop-deck .slide'));
  if(!slides.length)return;
  e.preventDefault();
  if(e.key==='Home'){slides[0].scrollIntoView({behavior:'smooth'});return;}
  if(e.key==='End'){slides[slides.length-1].scrollIntoView({behavior:'smooth'});return;}
  var cur=0,best=Infinity;
  slides.forEach(function(s,i){var d=Math.abs(s.getBoundingClientRect().top);
    if(d<best){best=d;cur=i;}});
  var next=cur+((e.key==='ArrowUp'||e.key==='PageUp')?-1:1);
  next=next<0?0:next>slides.length-1?slides.length-1:next;
  slides[next].scrollIntoView({behavior:'smooth'});
});

/* ---- header green in-text ripple ---- */
[].slice.call(document.querySelectorAll('.gh')).forEach(function(h){
  h.setAttribute('data-t',h.textContent);
  h.addEventListener('mousemove',function(e){var r=h.getBoundingClientRect();
    h.style.setProperty('--hx',(e.clientX-r.left)+'px');
    h.style.setProperty('--hy',(e.clientY-r.top)+'px');});
});

/* ---- exploration cursor reflection (desktop only) ---- */
var exp=document.querySelector('.desktop-deck .explore');
if(exp){
  exp.addEventListener('mousemove',function(e){var r=exp.getBoundingClientRect();
    exp.style.setProperty('--mx',(e.clientX-r.left)+'px');
    exp.style.setProperty('--my',(e.clientY-r.top)+'px');
    exp.classList.add('reflect');});
  exp.addEventListener('mouseleave',function(){exp.classList.remove('reflect');});
}

/* ---- custom cursor dot (fine pointers only) ---- */
var fine=matchMedia('(pointer:fine)').matches;
if(fine){
  var dot=document.createElement('div');dot.className='dot';document.body.appendChild(dot);
  var dx=0,dy=0,dPend=false;
  addEventListener('mousemove',function(e){dx=e.clientX;dy=e.clientY;
    if(!dPend){dPend=true;requestAnimationFrame(function(){
      dot.style.transform='translate('+dx+'px,'+dy+'px) translate(-50%,-50%)';dPend=false;});}
  },{passive:true});
}

/* ---- IntersectionObserver entrance scaffolding ---- */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(en){
    if(en.isIntersecting)en.target.classList.add('in');});},{threshold:.22});
  [].slice.call(document.querySelectorAll('.slide,.m')).forEach(function(s){io.observe(s);});
}
})();
"""

# ============================================================================
# PAGE SHELL
# ============================================================================

html_out = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="%s" rel="stylesheet">
<style>%s</style>
</head>
<body>
<div class="flowbg"></div>
<div class="prog" id="prog"></div>
<nav class="bar" id="bar">%s</nav>
<main class="desktop-deck">
%s
</main>
<main class="mobile-deck">
%s
</main>
<div class="hint">Scroll &darr;</div>
<script>%s</script>
</body>
</html>
""" % (PAGE_TITLE, GF_HREF, CSS, nav_html, desktop, mobile, JS)

with open("index.html", "w") as f:
    f.write(html_out)

n_desktop = len(re.findall(r'<section class="slide', html_out))
n_mobile = len(re.findall(r'<section class="m[ "]', html_out))
print("index.html written: %d KB, %d desktop sections, %d mobile sections"
      % (len(html_out) // 1024, n_desktop, n_mobile))
