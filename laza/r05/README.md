# LAZA · Round 05 · Palette usage slide

One editable slide (native shapes, no images) for the Logo × packaging Round 05
deck, meant to sit at 13 / 14, between "Secondary type" and "Overview".

- `LAZA_R05_palette_slide.pptx`: the slide
- `LAZA_R05_palette_slide_preview.png`: LibreOffice render for review
- `build_palette_slide.py`: regenerates the slide (`python3 build_palette_slide.py`, needs `python-pptx`)
- Google Slides copy in Drive: "LAZA · Palette usage slide · Round 05 insert"

## Insert into the deck

1. Open "LAZA · Logo × Packaging · Round 05" in Google Slides.
2. File → Import slides → pick the insert file from Drive (or upload the .pptx). Leave "Keep original theme" unchecked.
3. Drag it to position 13.
4. Edit → Find and replace `/ 13` with `/ 14` to renumber the other footers.

## Palette

| Color | Share | HEX | RGB | CMYK (FOGRA39) | Role |
|---|---|---|---|---|---|
| LAZA blue | 60% | #A6B7D5 | 166 183 213 | 40 24 8 0 | Field: box body, bags, sleeves, signage |
| LAZA white | 25% | #EEEDE7 | 238 237 231 | 8 6 10 0 | Breathing space, logo on blue, lids, labels |
| LAZA yellow | 10% | #EEE1A9 | 238 225 169 | 9 10 42 0 | Accent: logo, seals, stickers, one per face |
| Navy | 5% | #1F2A44 | 31 42 68 | 90 60 0 78 | Small functional text only |

Contrast (WCAG 2.x): navy on blue 7.0:1, on yellow 10.8:1, on white 12.2:1. White on blue
1.7:1 and yellow on blue 1.5:1, so large type only. Yellow on white 1.1:1, never.

## How the CMYK was made

Rounds 02–04 used the naive RGB→CMYK formula, which puts black into pastels (blue came out
22 14 0 16). These values are profiled instead: Fogra's FOGRA39L characterization data
(ISO 12647-2, coated art paper, from Ubuntu's `icc-profiles-free`), profiled with ArgyllCMS
`colprof -qm -kp 0 0.4 0.95 1 1 -l330 -L98`, and converted from sRGB with relative colorimetric
intent. Round-trip error after rounding is ΔE76 ≤ 1.5. Blue, yellow and white separate with no K.

Still to do before print: confirm the stock (re-separate for FOGRA52 / PSO Uncoated if the box
is uncoated board), pick Pantone matches from a physical guide, and sign off a printed proof.

## Open points for next session

- Fonts are Helvetica (headings) and IBM Plex Mono (labels), the house style from the
  September LAZA decks. If Round 05 uses other fonts, restyle the text boxes to match.
- The 60/25/10/5 split is a proposal (60-30-10 rule, with navy taken out of the white
  share). Confirm it with Maxim.
