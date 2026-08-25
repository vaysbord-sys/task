# HIGGSFIELD · Pitch Deck — Scroll-Deck Website Template

A single-scroll pitch-deck website built to the **Scroll-Deck Website Design
System & Build Spec** (reference build: YONEX Venice). One self-contained
`index.html` carries two complete parallel decks — `<main class="desktop-deck">`
(mandatory vertical scroll-snap, one slide per gesture) and
`<main class="mobile-deck">` (free scroll, eased per-section background) —
and CSS alone decides which renders, switching at `max-width:720px`.

Every piece of copy, color, and imagery in this build is a **placeholder**.
The system machinery (fade physics, nav luminance flip, snap, lightbox,
cursor dot, PDF export) is final and must not be re-tuned.

## Files

| File | What it is |
|---|---|
| `build_responsive.py` | Generator. Brand tokens up top (all placeholders), fixed-system CSS/JS below. Run `python3 build_responsive.py` → `index.html`. |
| `index.html` | Generated output. One file, both decks, inline SVG placeholder art. |
| `build_pdf.py` | Landscape PDF export (1280×800, one section per page, video + map dropped, motion neutralized). Needs Chrome/Chromium. |
| `tokens.json` | The spec section-1 design-tokens object, filled with this template's placeholder values. |

## Swapping in real content

1. **Copy + colors + fonts** live in the `BRAND TOKENS` block at the top of
   `build_responsive.py` (mirrored in `tokens.json`). Swap hexes, names,
   taglines, bodies, TOC rows, facts, map coordinates, exploration tiles.
   - Re-derive `GREEN_ONDARK` / `GREEN_ONLIGHT` at matching lightness when
     changing the accent; never invent unrelated hues.
   - `INTRO_BG` must keep Rec-709 luminance ≤ 148 so the nav stays light-text.
   - Each concept's `dk` flag must match its ground: light background → `True`.
   - The exploration eyebrow ("Market Context") and heading ("Exploration")
     are hardcoded literals inside `d_explore()` / `explore_m()` — edit the
     builders, not constants (spec parity).
   - Copy rule: no em-dashes; keep `&rsquo;` and `&middot;`.

2. **Assets**: set `PLACEHOLDER_ART = False` and supply files at these paths
   (spec section 10):

   ```
   img/slides/slide_00.jpg          baked hero    (2880px wide, progressive JPEG q93)
   img/slides/slide_21.jpg          baked closing (2880px wide)
   img/renders/{concept}/d1..d5.jpg detail renders (1600×893)
   img/vids/{concept}.mp4           H.264 8-bit yuv420p, 1920-wide, +faststart — never HEVC/10-bit
   img/plans/{concept}.png          roadmap/plan line art on white, ~1400px (PyMuPDF from PDF)
   img/m/refs/{concept}/r01..r12.jpg  reference tiles (~730–840px)
   img/m/exp/exp1..exp6.jpg         exploration tiles (660–794px)
   img/logo.png  img/partner.png    brand + partner lockups
   ```

   Concepts (placeholder pillar keys): `engine`, `studio`, `network`.
   With real slides in place, `slide_bg()` samples pixel (5,5) of each baked
   JPG so the letterbox color matches the image edge and feeds nav contrast.

3. **Build and check**: `python3 build_responsive.py`, open `index.html`,
   resize across 720px, confirm the nav flips dark over the light STUDIO /
   NETWORK / plan sections, videos autoplay/pause on scroll, lightbox opens.

4. **PDF**: `python3 build_pdf.py` → `HIGGSFIELD_Pitch_Deck.pdf`.

## Page order (both decks, fixed skeleton)

```
hero (data-key=intro) → map → exploration → toc
  per pillar (engine, studio, network):
    overview → references → film → roadmap → details ×5
roadmap summary (data-key=summary) → comparison View 01..05 → thank you
```

If `DETAILS` per concept changes from 5, update both the comparison loop
range and the `[ n / 5 ]` denominator.

## Fixed physics — do not change

Fade divisor `0.32`; `cubic-bezier(.16,1,.3,1)`; luminance formula + `>148`
threshold; probes 42px / `innerHeight*0.4` / `innerHeight*0.5`;
`.55s`/`.3s`/`.12s` timings; nav `top:22px`, z-index 50/60; breakpoint 720px;
`100svh` slides; snap `y mandatory` + `scroll-snap-stop:always` (desktop only);
the radius (0/6/8/10/12), shadow (18/50 · 22/60 · 30/100 · 40/120) and
tracking (`.24em` → 0) ladders. The JS `FADES` list and the
`prefers-reduced-motion` opacity block are the same selector set — keep them
in sync; the PDF opacity-force list is a deliberate superset — never trim it.
