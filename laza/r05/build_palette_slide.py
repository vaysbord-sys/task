"""LAZA · Logo × packaging · Round 05 — palette usage slide (slide 13 of 14).

Builds a one-slide, fully editable .pptx (native shapes and text, no images)
to import into the Round 05 deck: Google Slides → File → Import slides.

CMYK values come from Fogra's FOGRA39L characterization data (ISO 12647-2,
coated paper), profiled with ArgyllCMS (black start 40%, TAC 330%) and converted
from sRGB with relative colorimetric intent. See README.md.

    python3 build_palette_slide.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

OUT = Path(__file__).with_name("LAZA_R05_palette_slide.pptx")

SANS = "Helvetica"
MONO = "IBM Plex Mono"
FOOTER = "LAZA · Logo × packaging · Round 05"
PAGE = "13 / 14"

NAVY = "1F2A44"
INK_SOFT = "5D6475"  # navy at ~70% on LAZA white, for secondary text
HAIRLINE = "C5C6C6"  # navy at ~20% on LAZA white, outlines the white swatch
BG = "EEEDE7"

PALETTE = [
    dict(
        name="LAZA blue", hex="A6B7D5", rgb=(166, 183, 213), cmyk=(40, 24, 8, 0), share=60,
        role="The field. Box body, bags, cup sleeves, shop signage.",
        never="Tints, gradients, other blues.",
    ),
    dict(
        name="LAZA white", hex="EEEDE7", rgb=(238, 237, 231), cmyk=(8, 6, 10, 0), share=25,
        role="Breathing space. Logo on blue, lids, labels, inner panels.",
        never="Pure #FFFFFF in brand artwork.",
    ),
    dict(
        name="LAZA yellow", hex="EEE1A9", rgb=(238, 225, 169), cmyk=(9, 10, 42, 0), share=10,
        role="The accent. Logo, seals, stickers, ribbons. One per face.",
        never="Body text, or yellow on white.",
    ),
    dict(
        name="Navy", hex="1F2A44", rgb=(31, 42, 68), cmyk=(90, 60, 0, 78), share=5,
        role="Function only. Ingredients, address, legal, barcodes.",
        never="The logo or large areas.",
    ),
]


def luminance(hex_):
    def chan(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (int(hex_[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast(fg, bg):
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


# (foreground, background, label, verdict)
PAIRS = [
    (NAVY, "A6B7D5", "Navy on blue", "any size"),
    (NAVY, "EEE1A9", "Navy on yellow", "any size"),
    (NAVY, "EEEDE7", "Navy on white", "any size"),
    ("EEEDE7", "A6B7D5", "White on blue", "large type only"),
    ("EEE1A9", "A6B7D5", "Yellow on blue", "large type only"),
    ("EEE1A9", "EEEDE7", "Yellow on white", "never"),
]


def rgb(hex_):
    return RGBColor.from_string(hex_)


def rect(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    if line:
        shp.line.color.rgb = rgb(line)
        shp.line.width = Pt(0.75)
    else:
        shp.line.fill.background()
    # Drop the theme style reference so no default shadow or outline is applied.
    shp._element.remove(shp._element.find(qn("p:style")))
    return shp


def text(slide, x, y, w, h, runs, size, color=NAVY, font=SANS, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, tracking=0, line_spacing=None,
         shape=None):
    """Add a text box. `runs` is a string, or a list of lines, each a string or
    a list of (text, overrides) runs."""
    box = shape or slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", 0)
    lines = runs if isinstance(runs, list) else [runs]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        parts = line if isinstance(line, list) else [(line, {})]
        for txt, o in parts:
            r = p.add_run()
            r.text = txt
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.color.rgb = rgb(o.get("color", color))
            spc = o.get("tracking", tracking)
            if spc:
                r._r.get_or_add_rPr().set("spc", str(int(spc)))
    return box


def eyebrow(slide, x, y, w, label, color=NAVY):
    # House eyebrow: mono, caps, +0.14em tracking (11pt → 154 hundredths of a pt).
    return text(slide, x, y, w, Inches(0.25), label, 11, color=color, font=MONO,
                tracking=154)


def build():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = rgb(BG)

    L = Inches(0.6)
    W = prs.slide_width - 2 * L

    # Header
    eyebrow(slide, L, Inches(0.5), W, "COLOR PALETTE · USAGE RULES")
    text(slide, L, Inches(0.82), W, Inches(0.6),
         "Blue leads, white breathes, yellow accents.", 32, bold=True, tracking=-60)
    text(slide, L, Inches(1.42), W, Inches(0.3),
         "Shares are by visible area on any packaging face, page or screen.",
         14, color=INK_SOFT)

    # Proportion bar
    bar_y, bar_h = Inches(1.95), Inches(0.5)
    x = L
    for i, c in enumerate(PALETTE):
        seg_w = W * c["share"] // 100 if i < len(PALETTE) - 1 else L + W - x
        seg = rect(slide, x, bar_y, seg_w, bar_h, c["hex"],
                   line=HAIRLINE if c["hex"] == BG else None)
        label_color = BG if c["hex"] == NAVY else NAVY
        tf = seg.text_frame
        tf.margin_left, tf.margin_right = Inches(0.12), Inches(0.04)
        tf.margin_top = tf.margin_bottom = 0
        text(slide, 0, 0, 0, 0, f"{c['share']}%", 15, color=label_color, bold=True,
             anchor=MSO_ANCHOR.MIDDLE, shape=seg)
        tf.margin_left = Inches(0.12)
        x += seg_w

    # Swatch cards
    gap = Inches(0.25)
    col_w = (W - 3 * gap) // 4
    top = Inches(2.75)
    for i, c in enumerate(PALETTE):
        cx = L + i * (col_w + gap)
        rect(slide, cx, top, col_w, Inches(0.9), c["hex"],
             line=HAIRLINE if c["hex"] == BG else None)

        y = top + Inches(1.02)
        text(slide, cx, y, col_w, Inches(0.3), c["name"], 16, bold=True)
        text(slide, cx, y, col_w, Inches(0.3), f"{c['share']}%", 16, bold=True,
             align=PP_ALIGN.RIGHT)

        y += Inches(0.4)
        r, g, b = c["rgb"]
        cy, m, ye, k = c["cmyk"]
        specs = [
            [("HEX   ", {"color": INK_SOFT}), (f"#{c['hex']}", {})],
            [("RGB   ", {"color": INK_SOFT}), (f"{r} {g} {b}", {})],
            [("CMYK  ", {"color": INK_SOFT}), (f"{cy} {m} {ye} {k}", {})],
        ]
        text(slide, cx, y, col_w, Inches(0.62), specs, 10.5, font=MONO,
             line_spacing=1.15)

        y += Inches(0.72)
        rect(slide, cx, y, col_w, Emu(9525), HAIRLINE)  # 0.75pt rule
        y += Inches(0.1)
        text(slide, cx, y, col_w, Inches(0.5), c["role"], 11.5, line_spacing=1.1)
        y += Inches(0.52)
        text(slide, cx, y, col_w, Inches(0.42),
             [[("Never: ", {"bold": True}), (c["never"], {"color": INK_SOFT})]],
             11, line_spacing=1.1)

    # Pairings
    py = Inches(5.95)
    eyebrow(slide, L, py, W, "PAIRINGS · WCAG CONTRAST")
    py += Inches(0.34)
    pgap = Inches(0.15)
    chip_w = (W - 5 * pgap) // 6
    sq = Inches(0.5)
    for i, (fg, bgc, label, verdict) in enumerate(PAIRS):
        px = L + i * (chip_w + pgap)
        chip = rect(slide, px, py, sq, sq, bgc, line=HAIRLINE if bgc == BG else None)
        text(slide, 0, 0, 0, 0, "Aa", 14, color=fg, bold=True, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE, shape=chip)
        tx = px + sq + Inches(0.1)
        ratio = contrast(fg, bgc)
        text(slide, tx, py - Inches(0.01), chip_w - sq - Inches(0.1), Inches(0.52),
             [[(label, {"bold": True})],
              [(f"{ratio:.1f}:1", {"color": INK_SOFT})],
              [(verdict, {"color": INK_SOFT})]],
             10, line_spacing=1.1)

    # Footer
    fy = Inches(7.02)
    text(slide, L, fy, Inches(4), Inches(0.22), FOOTER, 9, color=INK_SOFT, font=MONO)
    text(slide, L + Inches(4), fy, W - Inches(5), Inches(0.22),
         "CMYK: FOGRA39 coated, relative colorimetric. Match Pantone and sign off a "
         "printed proof.", 9, color=INK_SOFT, font=MONO, align=PP_ALIGN.CENTER)
    text(slide, L + W - Inches(1), fy, Inches(1), Inches(0.22), PAGE, 9,
         color=INK_SOFT, font=MONO, align=PP_ALIGN.RIGHT)

    pairs_note = "; ".join(
        f"{label.lower()} {contrast(fg, b):.1f}:1" for fg, b, label, _ in PAIRS)
    slide.notes_slide.notes_text_frame.text = (
        "Palette usage rules. Proportions by visible area: LAZA blue 60%, LAZA white "
        "25%, LAZA yellow 10%, navy 5% (small functional text only). CMYK converted "
        "from sRGB via a FOGRA39 profile (ISO 12647-2 coated, relative colorimetric); "
        "on uncoated board re-separate for FOGRA52 / PSO Uncoated. Contrast (WCAG): "
        f"{pairs_note}."
    )

    # Keep only the blank layout so the file stays small and imports cleanly.
    layouts = prs.slide_master.slide_layouts
    for layout in list(layouts):
        if layout is not slide.slide_layout:
            layouts.remove(layout)
    # Template leftovers: thumbnail and printer settings.
    pkg = prs.part.package
    for rId, rel in list(pkg._rels.items()):
        if rel.reltype == RT.THUMBNAIL:
            pkg._rels.pop(rId)
    for rId, rel in list(prs.part.rels.items()):
        if rel.reltype == RT.PRINTER_SETTINGS:
            prs.part.drop_rel(rId)

    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    for fg, b, label, _ in PAIRS:
        print(f"{label:16s} {contrast(fg, b):5.2f}:1")
    print(build())
