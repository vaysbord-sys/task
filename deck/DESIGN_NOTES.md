# Vaysbord Portfolio — Design Notes

Deck source: `vaysbord-deck.html` → rendered to `Maxim-Vaysbord-Portfolio-2025.pdf`
(19 slides, 16:9, Chromium print-to-PDF).

## Skills sourced & applied

Pulled from the open agent-skills ecosystem (`npx skills`, vercel-labs/skills) and
read directly from source:

- **Taste Skill** — `npx skills add leonxlnx/taste-skill` (github.com/leonxlnx/taste-skill).
  "Anti-slop" frontend/design rules.
- **Emil Kowalski's skill** — `npx skills add emilkowalski/skill` (github.com/emilkowalski/skill).
  Design-engineering philosophy (taste as differentiator, cohesion, unseen details).
- **Impeccable** (impeccable.style) — closed/paid plugin, not on public GitHub,
  so it could not be installed or read here. Flagged, not applied.

## Changes made (v1 → v2), each tied to a rule

| Rule applied | v1 problem | v2 fix |
|---|---|---|
| Eyebrow restraint (≤1 per 3 sections) | Red kicker on every slide | Kickers only on dividers + 2 structural slides; headlines carry |
| One accent, locked | Red **and** gold | Single locked accent (`#E8452E`) across all 19 slides |
| Shape consistency lock | Pill tags mixed with sharp frames | All sharp (radius 0); pills replaced by mono `·`-separated meta |
| Layout-repetition / zigzag cap (≤2 consecutive splits) | ~8 near-identical text-left/frames-right splits | 6 rotating families: statement, frame-grid, hero-frame, split, three-col, quote |
| Content density (no hairline-per-row) | 11-row hairline media list | Grouped into 3 labelled clusters |
| Body type off Inter | Inter body | Geist body; Space Grotesk display; Geist Mono meta |
| Copy self-audit / no em-dash flourish | Em-dashes in prose | Replaced with commas / `·` in prose & captions |
| Honest captioned image zones (not fake screenshots) | — | Kept; each zone labelled with the exact asset that belongs there |
| Cohesion (Emil) | — | One spacing scale, one caption style, consistent chrome |

## For your own environment

To install these skills into a coding agent (Claude Code, Cursor, Codex, etc.):

```
npx skills add emilkowalski/skill
npx skills add leonxlnx/taste-skill
```

## Still open

The deck's image zones are placeholders — the original Google Slides visuals
did not come through the export. Drop real artwork into the captioned frames
(or share the assets and they can be placed and re-rendered).
