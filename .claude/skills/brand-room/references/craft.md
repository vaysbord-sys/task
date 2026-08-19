# Craft — Art Direction and the Build Spec

Load this whenever you're building. The idea earns the meeting; this is what makes the page look like it came from someone who already has the job.

**Contents**
1. [Typography](#1-typography)
2. [Color](#2-color)
3. [Grid, space, composition](#3-grid-space-composition)
4. [Motion](#4-motion)
5. [Imagery and art direction](#5-imagery-and-art-direction)
6. [Copy voice](#6-copy-voice)
7. [The build spec](#7-the-build-spec)
8. [Delivery](#8-delivery)
9. [Pre-ship checklist](#9-pre-ship-checklist)

---

## 1. Typography

Type is the loudest signal of craft level. Amateur pages are almost always identifiable by type alone.

- **One family, occasionally two.** A single strong grotesk or a grotesk + a display/serif pairing where the second family does exactly one job. Three families is a tell.
- **A real scale, not arbitrary sizes.** Pick a ratio and hold it. A workable display-led scale: `12 / 14 / 16 / 20 / 28 / 40 / 64 / 96 / 140`. Clamp the top sizes so the hero never breaks on a phone: `font-size: clamp(2.75rem, 9vw, 8.5rem)`.
- **Set display type tight.** Big type needs negative tracking (`letter-spacing: -0.03em` at 64px+) and tight leading (`line-height: 0.92–1.0`). Body wants `1.45–1.6` and a measure of **60–75 characters** (`max-width: 34em`).
- **Eyebrows and labels**: 11–12px, uppercase, `letter-spacing: 0.12em`, weight 600, in a muted token. These do more for perceived rigor than any effect.
- **Weight contrast beats size contrast.** 800 next to 400 at the same size reads more designed than two sizes of the same weight.
- **Numbers matter in sport.** Tabular figures (`font-variant-numeric: tabular-nums`) for scores, stats, dates, and countdowns. Big numerals set as display objects are a free art-direction move.
- Google Fonts is the only allowed remote asset in an Artifact. Safe, high-craft picks: **Inter Tight, Archivo / Archivo Expanded, Anton, Bebas Neue, Space Grotesk, Instrument Serif, Sora, Barlow Condensed**. Always give a real fallback stack, and prefer a system-font build if the piece must work offline.

## 2. Color

- **A ground, a commitment, and a whisper.** One dominant neutral (usually near-black or paper-white), one saturated color the idea owns, and one muted support. That's it.
- Define every color as a **token on `:root`**, never inline. Tokens make a page look systematized even to a viewer who never opens dev tools — because the consistency is visible.
- **Near-black, not black** (`#0A0A0B`–`#111`), **paper, not white** (`#FAFAF8`). Pure `#000`/`#fff` flattens depth on OLED phones.
- Text tokens by role: primary / secondary (~62% opacity) / tertiary (~38%). Body copy at full white on black is fatiguing; the 62% step is where editorial pages get their calm.
- **Borders at 6–10% opacity.** Anything heavier turns a layout into a spreadsheet.
- If the target brand has equity colors, **use them and don't correct them.** Bring craft to their palette; that's the entire pitch.
- Theme handling for Artifacts: full palette on bare `:root`, dark overrides under both `@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])` **and** `:root[data-theme="dark"]`, and an explicit `background` on `body`. A deliberate single-look design may skip dark mode, but must then paint both background and text explicitly.

## 3. Grid, space, composition

- **A 12-column grid with a generous gutter**, and content that deliberately breaks it once or twice (a full-bleed image, a headline that runs past the margin). The break only reads as intentional if the grid is obvious everywhere else.
- **A spacing scale**: `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 160`. Section padding on the large end. Crowded sections are the most common amateur tell after type.
- **Vertical rhythm is pacing.** Alternate section heights and densities: hero (full viewport) → tight argument → wide visual → dense system grid → quiet close. Uniform section heights read as a template.
- **One focal point per screen.** If two things compete, the viewer picks neither.
- **Anchor the first viewport.** Idea + line visible with no scroll, on a 390px-wide phone. Test it at that width first, not last.
- **Asymmetry over centering** for editorial confidence; centered layouts are for moments of ceremony (the line, the close).

## 4. Motion

- **One easing curve for the whole page.** `cubic-bezier(.16,1,.3,1)` for entrances, `cubic-bezier(.4,0,.2,1)` for state changes. Durations: 150–250ms for UI, 400–700ms for entrances. Longer than that and it feels like a screensaver.
- **Reveal on scroll, once, subtly**: 12–20px translate + opacity, staggered 40–80ms between siblings. IntersectionObserver, `unobserve` after firing.
- **Never animate what the eye needs to read.** Headlines can arrive; body copy should just be there.
- Honor `@media (prefers-reduced-motion: reduce)` by collapsing everything to opacity or nothing.
- One signature motion moment is worth ten small ones — a counter that counts, a wordmark that assembles, a card stack that deals. Pick one and make it perfect.

## 5. Imagery and art direction

- **No stock photography.** It is the single fastest way to look like a template. If a real asset isn't available, build the visual: type-driven compositions, gradient/noise fields, SVG diagrams, CSS-drawn geometry, duotone treatments.
- Where generated key art is appropriate, the **Higgsfield MCP tools** are available in this environment (`generate_image` / `generate_image_batch`) — art-direct the prompt properly (lens, light, grade, composition, wardrobe) rather than typing a description. Keep a consistent grade across every image in the piece; inconsistency reads worse than fewer images.
- **Treat all imagery through one grade.** A single duotone, grain overlay, or contrast curve applied uniformly makes mixed sources look authored. A grain layer (`feTurbulence` SVG at 2–4% opacity, `mix-blend-mode: overlay`) unifies almost anything.
- **Crop hard.** Wide establishing shots read as slideshow; tight crops read as art direction.
- Never fake logos of real brands in a way that implies endorsement, never fabricate athlete quotes or performance data, and label conceptual work as conceptual.
- **Rights reality:** for spec work aimed at a league or brand, avoid unlicensed player likenesses in a way that implies official use. Silhouettes, typography, equipment, crowd, and city imagery carry the idea without the problem — and demonstrating that awareness is itself a hiring signal.

## 6. Copy voice

- **Say it flat.** Write the sentence a confident person says out loud. Then cut its first three words.
- Headlines: 3–7 words. Subheads: one sentence, under 20 words. Body: two to four sentences per block, maximum.
- **No brand-voice mush.** Ban: *elevate, unlock, redefine, seamless, immersive, storytelling, passionate, journey, empower, next-level.*
- Specificity is the whole game: *"Week 4, 9:30am ET, in a Munich bar"* beats *"global fans everywhere."*
- Labels do work: naming a section "The System" or "Week One" instead of "Approach" tells the reader you think in operations.
- **The applicant's name appears once**, in a small footer, with one way to reply. No bio paragraph, no skills list, no "let's connect."

## 7. The build spec

Default deliverable: **one self-contained HTML file** that opens anywhere.

- No build step, no framework, no CDN scripts, no external stylesheets. Inline all CSS and JS; embed assets as data URIs. Google Fonts is the only permitted remote (with a fallback stack).
- Semantic structure: `header / main / section / footer`, one `h1`, headings in order.
- Responsive by construction: relative units, flexbox/grid, `max-width: 100%` on media, `clamp()` for type. Wide tables/diagrams scroll inside their own `overflow-x: auto` container — the body must **never** scroll horizontally.
- Performance: no layout shift, images compressed and dimensioned, no blocking work before first paint, JS measured in tens of lines not hundreds.
- Accessibility: 4.5:1 contrast on body text, visible focus states, `alt` text, `prefers-reduced-motion` respected.
- Keep the whole page under ~16MB including embedded assets so it can be published as an Artifact.
- **Print/PDF path:** if the piece may be sent as a file, add a small `@media print` block so a browser "Save as PDF" produces something respectable. Decks especially.

## 8. Delivery

Three routes, in order of preference:

1. **Artifact** — write the HTML file, then publish with the `Artifact` tool for a private shareable URL. Load the `artifact-design` skill before writing if the piece is being built as an artifact; it calibrates design investment and carries the theming and CSP rules. This is the fastest path to "here's a link."
2. **Vercel** — the `Vercel` MCP (`deploy_to_vercel`) puts it on a real URL when the piece deserves a domain of its own (a named campaign microsite reads better than a generic link).
3. **File in the repo** — commit the HTML to the repo and push, so the piece is versioned and can be reworked later.

Always give the user the actual link or path, plus the pitch note that carries it.

## 9. Pre-ship checklist

Run this before handing anything over. Answer honestly; each "no" is a task.

- [ ] Screenshot the first viewport at 390px wide. Muted, at thumbnail size, does it say **the idea**?
- [ ] Is there exactly one idea on the page, or did two survive?
- [ ] Read every headline out loud. Any that a real person wouldn't say?
- [ ] One type family (or a deliberate two), a real scale, tight display tracking?
- [ ] Three colors, all tokenized, target brand's equity respected?
- [ ] One easing curve, reduced-motion handled?
- [ ] Is there a **system** section proving the idea flexes (club, market, format, language)?
- [ ] Is there an **operating** beat — how it would actually be made and run?
- [ ] Conceptual/unaffiliated status stated, no fabricated metrics, no implied endorsement?
- [ ] Loads instantly, no horizontal scroll, footer has one way to reply?
- [ ] Would the hiring manager forward this to their boss? If not — what single change fixes that?
