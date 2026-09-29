---
name: claude-design-studio
description: Studio rules for brand and visual design work with Claude Design, Claude Code and Higgsfield, distilled from four Claude Design video tutorials (UI Collective, Nate Herk, RoboNuggets, Jack Roberts). Use before building any brand identity, design system, logo, deck, landing page or render set, and whenever the output risks looking like generic AI design.
---

# Claude Design studio rules

Source: `laza/research/claude-design-transcripts.md`. The transcripts are partial auto-captions, so rules only cover what the speakers actually say. Tags like [V2 5:47] point to video and timestamp. V1 is UI Collective "Complete Guide", V2 is Nate Herk "2 Hour Course", V3 is RoboNuggets "25 Tricks", V4 is Jack Roberts "Every Level". Lines marked *(inference)* are our own application, not from the videos.

## 1. Start from a design system, and only one
- Build the design system first. It's "the first thing that I want you guys to do" [V2 5:47]. It's "the starting point when using Claude, or indeed any AI agent" [V3 0:36].
- It costs tokens up front but saves them later, because everything built afterwards inherits the logos, type and colors [V2 5:51].
- "You don't want to go crazy building like five different design systems. Start with one and then iterate" [V2 6:05].
- You don't have to start from scratch. Upload a deck, website or screenshot you like and Claude extracts colors, fonts and components [V3 0:56].
- In Claude Code, a design system can be a custom skill you call every time (e.g. a /duolingo skill) [V3 2:06]. *(inference)* For each client, keep a `<client>-brand` skill with tokens, fonts, logo rules and voice.

## 2. Brief like a design director, with references
- Level 1 prompting ("make me a site for X") gives everyone the same result: "a simple purple gradient unless you provide specific information" [V4 3:07].
- Level 2 means briefing Claude as a design director: a specific brief plus real inspiration [V4 3:39–3:58].
- Sources the videos name: Pinterest, Awwwards, Godly, Mobbin, Landbook [V4 description, 4:24–4:58]. Screenshot what you like and drop it in [V4 4:46–4:51].
- styles.refero.design (transcribed as "styles.refereo.design") is a gallery of 2,000+ real design systems (Mercury, Linear, Apple) in a format Claude can read. Copy one in and modify it [V3 1:08–1:37].
- Don't browse thousands yourself. Give Claude the gallery link and ask it to pick the **three** systems closest to the business [V3 1:38–2:05].
- Mix systems to get something original: font from one, color and motion from another [V3 3:57–4:24].

## 3. Kill the AI tells
- **Fonts.** "The quickest way to spot a design that looks like it was made with AI is by the font." Replace the default. Pick from Fontshare or Fontesk (free), pair heading and text with Fontjoy, then name the fonts in the prompt or upload the font files to the design system [V3 2:47–3:15].
- **Copy.** "If the words in your design look like they were written by AI, you've already lost your audience even if the visuals look perfect." Have Claude study the top five competitors' copy, note the patterns and put them in the design system [V3 3:30–3:55].
- **Color.** Escape the "generic purple slop" [V4 timestamp 3:06]. Use a real palette generator [V4 timestamp 9:26].

## 4. Iterate; never one-shot
- "Iterate until it sings" and the "No-Oneshot Rule" [V4 timestamps 6:19, 7:29]. First drafts are drafts.
- Let Claude's clarifying questions do the brief-writing, since "we're not good at defining everything we want in an initial prompt" [V1 2:28–2:49]. Set the novelty/experimental level on purpose [V1 3:41–3:48] and choose which tweaks to expose (accent color, motion intensity) [V1 3:53–4:29].
- Guardrails trade off against freshness: "if you give AI total freedom it produces really good results… when you start adding guardrails like a design system, the results are not usually as good" [V1 6:13–6:27]. *(inference)* Explore freely first, lock the system second, then push the locked system with references so it doesn't go flat.
- Web layouts drift more than mobile. Check desktop hardest [V1 6:29–6:38].
- Opus's vision lets Claude Design look at its own output to catch breakage [V2 3:31–3:38]. *(inference)* Always visually QA before showing a client.

## 5. Budget the session
- Claude Design has its own usage limit, separate from chat and Code, and it resets weekly [V2 2:05–2:18, 4:31]. Six screens can "burn through a ton of tokens" [V1 5:21–5:32].
- Opus costs more than Sonnet or Haiku, so switch models strategically [V2 3:44–3:50]. *(inference)* Use cheaper models or passes for exploration, and the top model for the final build and visual QA.

## 6. One brand across everything
- Level 4: apply the one system across the whole business: decks and emails on brand, one-shot decks [V4 timestamps 11:17–12:48].
- Export paths: Claude Code, Canva, ZIP or HTML. Deploy through Claude Code to GitHub and Vercel [V2 1:27–1:31, timestamp 1:42:01].

## 7. Generated assets and motion
- Level 5: AI image and video generation (Higgsfield is named) supercharges design. Generate assets inside the flow, e.g. "five logo variations instantly" [V4 description, timestamps 14:57–15:53].
- Level 6: motion, interactive graphics and 3D make sites "feel alive" [V4 timestamps 17:26–18:46]. Launch videos appear in V2 [timestamp 1:09:00].

## Checklist before showing a client
1. Is there one design system (tokens, fonts, logo rules, voice), and is everything built from it?
2. Were references gathered (Pinterest, Awwwards, Godly, Mobbin, Landbook, Refero), and did Claude narrow them to three?
3. Is the font deliberately chosen, not a default, with the files in the system?
4. Is the copy modeled on the top five competitors, not AI phrasing?
5. Did it go through at least two iterations? Nothing one-shot.
6. Was it visually QA'd at desktop and mobile?
7. Are generated assets (logos, renders) proofed for spelling, Arabic and artifacts?
