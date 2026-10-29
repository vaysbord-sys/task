"""Batch requests that turn the Round 05 deck into Round 06 in place.

Writes r06_requests.json for Google Slides presentations.batchUpdate:
color slide rebuilt on Pale Lazurite, four logo slides (vector + volume),
unexplored logo slides removed.

    python3 build_r06_deck.py
"""

import json
from pathlib import Path

EMU = 914400
NAVY, SOFT, BG = "1F2A44", "5D6475", "EEEDE7"
BLUE, YELLOW = "9EB4D6", "EEE1A9"
FONT = "Inter"
FOOTER = "LAZA · Logo × packaging · Round 06"
TOTAL = 7

GH = "https://raw.githubusercontent.com/vaysbord-sys/task/26f012b/laza/r05/logos/"
HF = "https://d8j0ntlcm91z4.cloudfront.net/user_2xojXnccJM2OM83CuOEuH3U88is/"

LOGOS = [
    dict(key="l1", label="CURRENT DIRECTION",
         title="Current direction: a bigger ledge on the L",
         note="Ledge at the top left of the L enlarged. Everything else unchanged.",
         vec=("laza-logo-01-current-direction-white.png", 2585, 2400),
         vol=(HF + "hf_20261027_150739_22fde3b5-7748-4902-b367-d6293b80918a.png", 1, 1)),
    dict(key="l2", label="CONNECTED",
         title="Connected: LA and ZA melt into one shape",
         note="The bumpy notch between A and Z is now one smooth join; the baseline flows across.",
         vec=("laza-logo-02-connected-white.png", 2461, 2400),
         vol=(HF + "hf_20261027_150943_53091f8f-7d19-45d6-b670-7c4103774314.png", 1, 1)),
    dict(key="l3", label="STACKED",
         title="Stacked: logo 1's exact letters, LA over ZA",
         note="Built from the current-direction letters at the same scale, so proportions match.",
         vec=("laza-logo-03-stacked-white.png", 695, 2400),
         vol=(HF + "hf_20261027_150740_23eb2246-9c9d-46e6-857f-2c9ce18450ee.png", 9, 16)),
    dict(key="l4", label="ROUND",
         title="Round: more air where the letters were squeezed",
         note="Gaps opened at the three marked joins: L and A, top of Z and A, foot of Z and A.",
         vec=("laza-logo-04-round-white.png", 2441, 2400),
         vol=(HF + "hf_20261027_150740_53ae57fb-dd86-42d7-a0f8-9755ab592691.png", 1, 1)),
]

PALETTE = [
    ("Pale Lazurite", BLUE, "158 180 214", "44 25 8 0", 60,
     "The field. Boxes, bags, cups, signage, screens.", "Tints, gradients, other blues."),
    ("LAZA white", BG, "238 237 231", "8 6 10 0", 25,
     "The logo on blue. Lids, labels, inner panels.", "Pure #FFFFFF in brand artwork."),
    ("LAZA yellow", YELLOW, "238 225 169", "9 10 42 0", 10,
     "The accent. Seals, stickers, dessert names.", "Body text, or yellow on white."),
    ("Navy", NAVY, "31 42 68", "90 60 0 78", 5,
     "Function only. Ingredients, address, legal.", "The logo or large areas."),
]
PAIRS = [  # fg, bg, label, ratio, verdict
    (NAVY, BLUE, "Navy on blue", "6.8:1", "any size"),
    (NAVY, YELLOW, "Navy on yellow", "10.9:1", "any size"),
    (NAVY, BG, "Navy on white", "12.2:1", "any size"),
    (BG, BLUE, "White on blue", "1.8:1", "large type only"),
    (YELLOW, BLUE, "Yellow on blue", "1.6:1", "large type only"),
    (YELLOW, BG, "Yellow on white", "1.1:1", "never"),
]

reqs = []


def rgb(h):
    return {k: round(int(h[i:i + 2], 16) / 255, 3) for k, i in (("red", 0), ("green", 2), ("blue", 4))}


def props(page, x, y, w, h):
    return {"pageObjectId": page,
            "size": {"width": {"magnitude": int(w * EMU), "unit": "EMU"},
                     "height": {"magnitude": int(h * EMU), "unit": "EMU"}},
            "transform": {"scaleX": 1, "scaleY": 1, "translateX": int(x * EMU),
                          "translateY": int(y * EMU), "unit": "EMU"}}


def rect(oid, page, x, y, w, h, fill):
    reqs.append({"createShape": {"objectId": oid, "shapeType": "RECTANGLE",
                                 "elementProperties": props(page, x, y, w, h)}})
    reqs.append({"updateShapeProperties": {
        "objectId": oid,
        "shapeProperties": {"shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": rgb(fill)}}},
                            "outline": {"propertyState": "NOT_RENDERED"}},
        "fields": "shapeBackgroundFill.solidFill.color,outline.propertyState"}})


def text(oid, page, x, y, w, h, t, size, bold=False, color=NAVY, align="START", anchor="TOP",
         runs=None):
    reqs.append({"createShape": {"objectId": oid, "shapeType": "TEXT_BOX",
                                 "elementProperties": props(page, x, y, w, h)}})
    reqs.append({"insertText": {"objectId": oid, "text": t}})
    reqs.append({"updateTextStyle": {
        "objectId": oid, "textRange": {"type": "ALL"},
        "style": {"fontFamily": FONT, "fontSize": {"magnitude": size, "unit": "PT"}, "bold": bold,
                  "foregroundColor": {"opaqueColor": {"rgbColor": rgb(color)}}},
        "fields": "fontFamily,fontSize,bold,foregroundColor"}})
    for start, end, st in runs or []:
        style, fields = {}, []
        if "bold" in st:
            style["bold"] = st["bold"]; fields.append("bold")
        if "color" in st:
            style["foregroundColor"] = {"opaqueColor": {"rgbColor": rgb(st["color"])}}
            fields.append("foregroundColor")
        reqs.append({"updateTextStyle": {
            "objectId": oid, "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": end},
            "style": style, "fields": ",".join(fields)}})
    if align != "START":
        reqs.append({"updateParagraphStyle": {"objectId": oid, "textRange": {"type": "ALL"},
                                              "style": {"alignment": align}, "fields": "alignment"}})
    if anchor != "TOP":
        reqs.append({"updateShapeProperties": {"objectId": oid, "shapeProperties": {"contentAlignment": anchor},
                                               "fields": "contentAlignment"}})


def image(oid, page, url, bx, by, bw, bh, iw, ih):
    """Fit an iw:ih image inside the box, centered."""
    k = min(bw / iw, bh / ih)
    w, h = iw * k, ih * k
    reqs.append({"createImage": {"objectId": oid, "url": url,
                                 "elementProperties": props(page, bx + (bw - w) / 2, by + (bh - h) / 2, w, h)}})
    return len(reqs) - 1


def slide(oid, index):
    reqs.append({"createSlide": {"objectId": oid, "insertionIndex": index,
                                 "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    reqs.append({"updatePageProperties": {
        "objectId": oid,
        "pageProperties": {"pageBackgroundFill": {"solidFill": {"color": {"rgbColor": rgb(BG)}}}},
        "fields": "pageBackgroundFill.solidFill.color"}})


def footer(page, n):
    text(page + "_ft", page, 0.6, 7.0, 4.5, 0.24, FOOTER, 9)
    text(page + "_pg", page, 11.73, 7.0, 1.0, 0.24, f"{n:02d} / {TOTAL:02d}", 9, align="END")


# 1. Color slide
s = "r6_color"
slide(s, 1)
text(s + "_eb", s, 0.6, 0.45, 8, 0.24, "COLOR PALETTE · USAGE RULES", 9, bold=True)
text(s + "_ti", s, 0.6, 0.72, 12, 0.5, "Pale Lazurite leads, white breathes, yellow accents.", 24, bold=True)
text(s + "_sb", s, 0.6, 1.24, 12, 0.3, "Shares are by visible area on any packaging face, page or screen.", 11, color=SOFT)
W, x = 12.13, 0.6
for i, (name, hx, _, _, share, _, _) in enumerate(PALETTE):
    w = W * share / 100 if i < 3 else 0.6 + W - x
    rect(f"{s}_bar{i}", s, x, 1.68, w, 0.48, hx)
    text(f"{s}_bt{i}", s, x + 0.1, 1.68, max(w - 0.12, 0.4), 0.48, f"{share}%", 12, bold=True,
         color=BG if hx == NAVY else NAVY, anchor="MIDDLE")
    x += w
cw, gap = (W - 3 * 0.25) / 4, 0.25
for i, (name, hx, rgbv, cmyk, share, role, never) in enumerate(PALETTE):
    cx = 0.6 + i * (cw + gap)
    rect(f"{s}_sw{i}", s, cx, 2.42, cw, 0.85, hx)
    if hx == BG:
        reqs.append({"updateShapeProperties": {
            "objectId": f"{s}_sw{i}",
            "shapeProperties": {"outline": {"outlineFill": {"solidFill": {"color": {"rgbColor": rgb("C5C6C6")}}},
                                            "weight": {"magnitude": 0.75, "unit": "PT"}}},
            "fields": "outline.outlineFill.solidFill.color,outline.weight"}})
    text(f"{s}_nm{i}", s, cx, 3.37, cw - 0.6, 0.3, name, 13, bold=True)
    text(f"{s}_pc{i}", s, cx + cw - 0.6, 3.37, 0.6, 0.3, f"{share}%", 13, bold=True, align="END")
    spec = f"HEX   #{hx}\nRGB   {rgbv}\nCMYK  {cmyk}"
    text(f"{s}_sp{i}", s, cx, 3.72, cw, 0.62, spec, 10)
    text(f"{s}_ro{i}", s, cx, 4.42, cw, 0.42, role, 10)
    nv = "Never: " + never
    text(f"{s}_nv{i}", s, cx, 4.88, cw, 0.42, nv, 10, color=SOFT, runs=[(0, 6, {"bold": True, "color": NAVY})])
text(s + "_pe", s, 0.6, 5.5, 8, 0.24, "PAIRINGS · WCAG CONTRAST", 9, bold=True)
pw = (W - 5 * 0.15) / 6
for i, (fg, bgc, label, ratio, verdict) in enumerate(PAIRS):
    px = 0.6 + i * (pw + 0.15)
    rect(f"{s}_pr{i}", s, px, 5.82, 0.5, 0.5, bgc)
    text(f"{s}_pa{i}", s, px, 5.82, 0.5, 0.5, "Aa", 13, bold=True, color=fg, align="CENTER", anchor="MIDDLE")
    t = f"{label}\n{ratio} · {verdict}"
    text(f"{s}_pl{i}", s, px + 0.58, 5.8, pw - 0.58, 0.55, t, 9, color=SOFT,
         runs=[(0, len(label), {"bold": True, "color": NAVY})])
text(s + "_cm", s, 5.2, 7.0, 6.3, 0.24,
     "CMYK: FOGRA39 coated, relative colorimetric. Match Pantone and sign off a printed proof.", 8, color=SOFT)
footer(s, 2)

# 2. Logo slides
for n, L in enumerate(LOGOS):
    s = f"r6_{L['key']}"
    slide(s, 2 + n)
    text(s + "_eb", s, 0.6, 0.45, 8, 0.24, f"0{n + 1} / 04 · {L['label']}", 9, bold=True)
    text(s + "_ti", s, 0.6, 0.72, 12, 0.5, L["title"], 24, bold=True)
    text(s + "_nt", s, 0.6, 1.24, 12, 0.3, L["note"], 11, color=SOFT)
    side, top, gapx = 5.05, 1.72, 0.3
    lx = (13.333 - 2 * side - gapx) / 2
    rx = lx + side + gapx
    rect(s + "_pv", s, lx, top, side, side, BLUE)
    f, iw, ih = L["vec"]
    image(s + "_iv", s, GH + f, lx + 0.55, top + 0.55, side - 1.1, side - 1.1, iw, ih)
    rect(s + "_pw", s, rx, top, side, side, BLUE)
    url, iw, ih = L["vol"]
    image(s + "_iw", s, url, rx, top, side, side, iw, ih)
    text(s + "_lv", s, lx, top + side + 0.08, side, 0.24, "OPTION A · FLAT VECTOR (SVG)", 9, bold=True)
    text(s + "_lw", s, rx, top + side + 0.08, side, 0.24, "OPTION B · VOLUME", 9, bold=True)
    footer(s, 3 + n)

# 3. Remove slides that are replaced or no longer explored; update cover and type slide.
for old in ("p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p14"):
    reqs.append({"deleteObject": {"objectId": old}})
for a, b in (("LAZA · ROUND 05", "LAZA · ROUND 06"),
             ("Nine logos, three type options, one box. October 2026.",
              "Four logos in two finishes, one palette. October 2026."),
             ("LAZA blue", "Pale Lazurite"), ("#A6B7D5", "#9EB4D6"),
             ("Round 05", "Round 06"), ("13 / 14", f"07 / {TOTAL:02d}")):
    reqs.append({"replaceAllText": {"containsText": {"text": a, "matchCase": True}, "replaceText": b}})
reqs.append({"updateShapeProperties": {
    "objectId": "p1_i6",
    "shapeProperties": {"shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": rgb(BLUE)}}}},
    "fields": "shapeBackgroundFill.solidFill.color"}})

out = Path(__file__).parent
cut1 = next(i for i, r in enumerate(reqs) if r.get("createSlide", {}).get("objectId") == "r6_l1")
cut2 = next(i for i, r in enumerate(reqs) if "deleteObject" in r)
for name, part in (("a", reqs[:cut1]), ("b", reqs[cut1:cut2]), ("c", reqs[cut2:])):
    (out / f"r06_req_{name}.json").write_text(json.dumps(part, separators=(",", ":")))
    print(name, len(part), len(json.dumps(part, separators=(",", ":"))))
