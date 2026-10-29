# LAZA handoff

Live deck (edit this one, never make a new deck):
https://docs.google.com/presentation/d/1RgtY-Q0Y83rfE3hzOzUkbpnrA4g5qKhaJEkTIgmO7cY/edit

## Round 06 state (Oct 29, 2026)

Deck order: 01 cover · 02 color palette · 03–06 logos (flat vector | volume) · 07 secondary type.

- Main color is **Pale Lazurite #9EB4D6** (RGB 158 180 214, CMYK FOGRA39 44 25 8 0). Shares: blue 60 / white #EEEDE7 25 / yellow #EEE1A9 10 / navy #1F2A44 5.
- Four logos kept: 01 current direction (bigger ledge on L), 02 connected (smooth LA–ZA join), 03 stacked (built from logo 1 letters), 04 round (more space at marked joins). Other five logos removed.
- Vectors: `r05/logos/*.svg` (white and navy), PNGs for slides. Volume renders are Higgsfield jobs referenced in `r05/build_r06_deck.py`.
- Package recolored to Pale Lazurite, no logo: Higgsfield job 2d4e5691-6d5d-4bd3-9823-22b0a8267d20 (not yet on a slide).

## Open

1. Hoodie character (full length, light grey background, Pale Lazurite hoodie, no logo) and Pale Lazurite cup: waiting for the source photos as files. Then one mockup slide: hoodie + cup + box, layout like the user's three-column moodboard.
2. Apply logos to hoodie, cup, box after the user picks.
3. Hand-finish the chosen vector in Illustrator; match Pantone on press.

## Pipeline notes

- Sandbox network blocks Google image URLs and Higgsfield CDN; the Higgsfield `sandbox_exec` can fetch both. Local files reach Higgsfield via a push to this repo and `media_import_url` on the raw.githubusercontent.com URL.
- Slides `createImage` accepts raw.githubusercontent.com and Higgsfield CDN URLs.
