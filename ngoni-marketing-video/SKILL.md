---
name: ngoni-marketing-video
description: Pitch, script and render short square ad videos for a mobile app that drive downloads and subscriptions — real people (licensed stock plus a few AI hero shots), real app screens on a rendered phone, feature-highlight animations, a regional AI voiceover and a trial end card — on a tracked, tiny budget. Use when asked for marketing, promo, ad, TikTok/Reels or subscription videos for an app, a video series, video scripts, or "more videos like the last one".
---

# Ngoni Marketing Video

Make ads that look shot, show the real product, and cost cents. The proven recipe (Dueo, Nov 2026): **licensed stock people + 0–1 AI hero shot + real app captures on a Blender phone + HyperFrames edit with highlights on exact UI elements + regional TTS voiceover + "Try it free for N days" end card.** A stock-only video costs about $0.005 (voice only); a video with one AI hero shot about $0.40.

## Owner Rules (non-negotiable)

1. **Pitch first.** Every new video idea goes to the owner as a short pitch (hook, story, who's on screen, which feature, cost) and waits for approval before any paid call or render.
2. **Square 1:1 only** (1080×1080, 30 fps) unless the owner asks otherwise. No vertical duplicates.
3. **Real app screens only.** Never mock or generate UI. Captures come from the app's native device/integration test runs with demo data.
4. **No real brands on screen** (shops, banks, apps, charities, medical aids) and no real personal data. Paint them out or ask for a recapture.
5. **Claims match the product.** Read the app's AGENTS.md/ARB copy for forbidden claims (e.g. "bank balance", "connects to your bank", advice). Figures in captions and voiceover must equal the figures on the capture.
6. **Budget is the owner's money.** Log every paid call before it runs, one call at a time, no retry loops. See [references/budget.md](references/budget.md).
7. **Nothing is posted, published, DMed or committed** by this workflow unless the owner says so. Nothing posts before the advertised features are live in the stores.
8. **Script home.** If the owner keeps scripts in a notes app (e.g. a Kanso notebook), save one note per video and update it as the video moves (backlog → approved → rendered with path and cost); keep the repo `video-scripts.md` in sync.

## Workflow

1. **Ground truth.** Read the product's AGENTS.md, store listing, ARB/l10n copy, existing `marketing/` work and the capture folder. List which features have clean captures.
2. **Pitch.** Propose 6–9 ideas, each: title, 1-line hook (readable in 2 s), 3–5 beat story, audience segment (solo/families/flatmates/couples…), feature shown, captures needed (have/missing), AI shot yes/no, cost. Recommend a top 3 and an order (dated hooks like payday or Black Friday first). Stop for approval.
3. **Script** each approved video: VO lines (5–7, ~20–27 s total), hook caption, captions per beat, screens with the exact highlights, end card, claims check. Template in [references/script-template.md](references/script-template.md).
4. **Captures.** Use existing captures where they fit; otherwise write ONE consolidated capture request (screen, exact state and demo data, light mode, which video) for whoever runs the device pass. Never drive the simulator yourself if another agent owns it.
5. **People.** Licensed stock first; AI hero shot only for the moment stock can't show. See [references/pipeline.md](references/pipeline.md).
6. **Voice.** One TTS call per video with all lines separated by `<long pause>`, split on silences with `scripts/vo_segments.py`, transcribe to check. Flag lines the transcriber mishears; re-voicing costs ~$0.005.
7. **Edit.** HyperFrames composition per video, highlights placed from boxes measured on the capture. See [references/highlights.md](references/highlights.md).
8. **QA.** `hyperframes check`, contact sheet per cut, loudness −14 LUFS, every on-screen figure equals the capture, no brands, end card present.
9. **Report.** Per video: status, length, cost, file path; total spend and credit left; what changed from the brief and why; lines to check by ear; captures still needed.

## Scripts

| Script | Use |
|---|---|
| `scripts/gemini_tts.py` | One Gemini TTS call (Interactions API). Regional voices from `GET /v1beta/voices?language_code=xx-YY` (free). |
| `scripts/gemini_omni.py` | One Gemini Omni video call (text-to-video). 360p test, then 1080p final. 16:9 or 9:16 only — centre-crop to square. |
| `scripts/gemini_image.py` | One image call (optional first frames / stills). |
| `scripts/vo_segments.py` | Split a one-call VO read on silences and show the words heard in each segment. |
| `scripts/stock_segment.sh` | Cut a graded 1080×1080 segment straight from a stock clip URL with ffmpeg. |
| `scripts/blender_phone_shot.py` | Headless Blender: real capture on a graphite phone, warm light, slow push-in. ~65 s per 4 s shot. |
| `scripts/blender_retexture.py` | Reuse a saved phone .blend with a new capture and length. |

Every paid script reads `GEMINI_API_KEY` from the environment only, never prints it, makes exactly one request and prints one JSON line with usage for the spend log.

## References

- [references/pipeline.md](references/pipeline.md) — tools that worked, tools that didn't, and why.
- [references/budget.md](references/budget.md) — prices, spend log format, caps and reserve.
- [references/highlights.md](references/highlights.md) — the screen-scene data model, rings/spotlights/count-ups, camera rules.
- [references/script-template.md](references/script-template.md) — pitch and script templates.
- `examples/dueo-series/` — the full Dueo batch builder (`build_batch2.py`, `build_series.py`, `targets.py`) and the tool comparison log. App-specific; copy the structure, not the content.
