---
name: ngoni-marketing-video
description: Pitch, script and render short ad videos for any app or product — real people (licensed stock plus a few AI hero shots), the real product UI on a rendered device, feature-highlight animations, an AI voiceover and an end card with the offer — on a tracked, small budget. Use when asked for marketing, promo, ad, launch, TikTok/Reels/Shorts or subscription videos, a video series, video scripts, or "more videos like the last one".
---

# Ngoni Marketing Video

Make ads that look shot, show the real product, and cost cents. The recipe:

> **licensed stock people + 0–1 AI hero shot per video + real product captures on a rendered device + a HyperFrames edit with highlights on exact UI elements + an AI voiceover + an end card with the offer.**

A stock-only video costs about the price of its voiceover, a fraction of a cent. One AI hero shot adds about $0.40. Tools, prices and limits are in [references/pipeline.md](references/pipeline.md) and [references/budget.md](references/budget.md).

## Before Starting: Get the Project's Brief

Every project has its own rules. Find them first; ask only for what you can't find.

1. **Read the project.** Look at its AGENTS.md/README, store listing, website copy, localisation strings, any existing `marketing/` folder and the brand assets (colours, fonts, logo). Note any product claims the project forbids.
2. **Ask the owner's preferences. Never assume them.** If a rules file from an earlier batch exists (step 3), reuse it and confirm only what's missing or what might have changed. Otherwise ask the questions below, using the agent's question tool if it has one. Ask in one round, offer the options, and allow "other". Each option shows a short trade-off, never a pre-picked answer, because the right choice differs by product.

   | Preference | Options to offer |
   |---|---|
   | **Aspect ratio(s)** | 9:16 vertical (TikTok, Reels, Shorts native) · 1:1 square (feed and cross-platform, looks more "designed") · 4:5 (Instagram and Facebook feed) · 16:9 (YouTube, web) · several cuts from one edit (more QA per video) |
   | **Length** | 6–10 s bumper · 15–20 s · 20–30 s story · 30–60 s explainer |
   | **Look** | cinematic (real people, AI hero shots) · product-first (screens and motion graphics) · founder/UGC style · mix |
   | **People on screen** | stock only · stock plus AI hero shots · AI only · none |
   | **Voice** | AI voiceover (which accent and language) · on-screen text only · the owner's own recorded voice |
   | **Audience** | segments, region and language, and who should appear on screen |
   | **Offer and end card** | free trial (length) · price · plain download · waitlist, plus store badges, domain and required fine print |
   | **Budget** | total, per-video cap and reserve |
   | **Captures** | where the real UI comes from (test runs, staging app, design files) and who takes them |
   | **Script home** | the repo, a notes app or a doc |
   | **Approval and posting** | pitch-first or go ahead · when posting is allowed · who posts |

   Say which preferences you inferred from the project, and let the owner correct them.
3. **Write the answers down** as the project's video rules, next to the scripts: a "00 rules" note or `marketing/VIDEO_RULES.md`. Later batches start from that file. When the owner changes a preference mid-project (for example "square only from now on"), update the file straight away. See `examples/dueo-series/README.md` for a filled-in set.

## Always (any project)

- **Spend only with consent.** Pitch each idea (hook, story, who's on screen, feature, cost) and wait for approval before any paid call or render, unless the owner chose "go ahead" within a budget.
- **Show the real product.** Never generate or mock product UI, and never let AI footage show readable fake screens.
- **Use no real third-party brands or personal data** on screen. Paint them out with the surrounding colour, or recapture with demo data.
- **Match claims to the product.** Every number in captions, voiceover and highlights must equal the number on the capture. Keep required qualifiers on screen, such as "estimate" or "not advice".
- **Treat money as the owner's.** Log every paid call before it runs. Make one call at a time, with no retry loops. Stop and report before you break the cap or the reserve.
- **Publish nothing yourself.** Don't post, DM or commit marketing assets unless the owner says so.

## Workflow

1. **Ground truth.** Check which features have clean captures and which claims are allowed.
2. **Pitch** 6–9 ideas using [references/script-template.md](references/script-template.md). Recommend a top 3 and an order, with dated or seasonal hooks first. Stop for approval, unless the owner chose go-ahead; in that case, make the top 3 within budget and report.
3. **Script** each approved video: 5–7 voiceover lines, the hook caption, captions per beat, the screens with their highlights, the end card and a claims check.
4. **Captures.** Reuse what exists. Otherwise write one consolidated capture request (screen, exact state and demo data, theme, which video) for whoever owns the devices.
5. **People.** Use licensed stock first. Add an AI hero shot only for a moment stock can't show.
6. **Voice.** Make one TTS call per video with all lines in it, split it on the silences (`scripts/vo_segments.py`), and transcribe it to check. Flag misheard words, especially names and accents.
7. **Edit** in HyperFrames, placing highlights from boxes measured on the capture ([references/highlights.md](references/highlights.md)).
8. **QA.**
   - `hyperframes check` passes.
   - Make a contact sheet per cut.
   - Loudness is −14 LUFS.
   - Every figure matches its capture.
   - No brands are visible.
   - The end card is present.
9. **Report** per video: status, length, cost and path. Include the total spend and credit left, any changes from the brief, lines to check by ear, and captures still needed. Update the script entries.

## Scripts

| Script | Use |
|---|---|
| `scripts/gemini_tts.py` | One Gemini TTS call. List regional voices for free with `GET /v1beta/voices?language_code=xx-YY`. |
| `scripts/gemini_omni.py` | One Gemini Omni text-to-video call: a 360p test take, then the 1080p final. Output is 16:9 or 9:16, so crop for square. |
| `scripts/gemini_image.py` | One image call, for first frames or stills. |
| `scripts/vo_segments.py` | Splits a one-call voiceover read on its silences and shows the words heard in each segment. |
| `scripts/stock_segment.sh` | Cuts a graded segment from a stock clip URL in any aspect, without downloading the whole clip. |
| `scripts/blender_phone_shot.py` | Headless Blender: puts a real capture on a phone with soft light and a slow push-in. |
| `scripts/blender_retexture.py` | Reuses a saved phone .blend with a new capture and length. |

Each paid script reads `GEMINI_API_KEY` from the environment only, never prints it, makes exactly one request, and prints one JSON line with usage for the spend log. The model names and prices were current in Nov 2026; check them before you use them.

## References

- [references/pipeline.md](references/pipeline.md): the tools that worked, the ones that didn't, and why.
- [references/budget.md](references/budget.md): prices, the spend-log format, caps and reserve.
- [references/highlights.md](references/highlights.md): the screen-scene data model, highlight kinds and camera rules.
- [references/script-template.md](references/script-template.md): pitch and script templates, plus hook patterns.
- `examples/dueo-series/`: one real project, Dueo (a money-planning app in South Africa). It holds that project's rules, its batch builder and its tool log. Copy the structure, not the content.
