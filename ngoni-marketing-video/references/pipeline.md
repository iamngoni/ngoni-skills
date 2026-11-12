# Pipeline

Proven on Dueo (Nov 2026, Apple silicon Mac, 24 GB). Times are wall clock.

## 1. People: licensed stock first

- **Pexels** (Pexels License, no attribution, commercial use). `curl` on www.pexels.com gets 403 — open clip pages with a web fetch, take the author and the `videos.pexels.com/video-files/<id>/<id>-<variant>.mp4` URL, then cut only the seconds you need with `scripts/stock_segment.sh` (no full download).
- Record every clip in `licenses.md`: id, author, URL, seconds used.
- Vet for: candid, no watermark, no visible brands, audience fit (region, age, household type). Phones in stock face the people or are black — don't composite screens onto them; cut to the Blender phone instead.
- Backups: Mixkit (thin on African households). Avoid Coverr and stock aggregators that mix in AI or watermarked clips. HeyGen stock search: mood boards only (low-res, unclear licence).
- Vary who's on screen across a series: people on their own, families, flatmates/friends, couples.

## 2. AI hero shots: only the moment stock can't show

- **Gemini Omni 1.2 Flash** (`gemini-omni-1.2-flash`, Interactions API; Veo 3.1 Preview was retired 22 Oct 2026). Text-to-video, 3–6 s.
- Always a **360p test take** (~$0.07–0.15), look at it, then **one 1080p final** (~$0.33–0.64). No retries without telling the owner.
- No 1:1 output: generate 16:9 and centre-crop to 1080×1080.
- Prompt: who (region, age, relationship), where (real local setting), the single action, light, "plain walls, no lettering, no logos". Generated phones can show glowing fake UI — blur/darken that region or cut away before the phone is readable.
- Typical spend: one hero shot per lead video, $0.40 all-in.

## 3. App screens: real captures on a rendered phone

- Captures come from the app's native integration tests (iOS, light mode, full resolution, demo data). Remove test-only banners (e.g. "You're offline") by filling with the surrounding surface colour — never alter content.
- **Phone shots:** `scripts/blender_phone_shot.py` (Blender 5.x headless, EEVEE, Standard view transform so UI colours stay exact). `scripts/blender_retexture.py` swaps the capture in a saved .blend. Blender MCP needs `BLENDER_PATH` set and an open Blender with the add-on; headless scripts are more repeatable.
- **Flat highlight scenes:** the capture itself, full frame, with camera moves and highlights (see highlights.md). These carry the feature explanation.

## 4. Voice

- **Gemini TTS** (`gemini-3.8-flash-tts`) with a regional Extended Voice Library voice. List voices free: `GET /v1beta/voices?language_code=en-ZA`. Dueo uses `en-za-csagent-7` (Cape Town English, warm, conversational).
- One call per video: all lines in one input separated by `<long pause>`, then split with `scripts/vo_segments.py` against a Whisper transcript. ~$0.005 per video.
- Expect the transcriber to mishear accents and brand names ("Dueo" → "Duo", "bill" → "bull"). Flag them for the owner to check by ear; re-voice one video for ~$0.005.
- Fallbacks: Kokoro (`npx hyperframes tts`, free, neutral American), macOS `say` (no regional voices).

## 5. Music and sound

- HeyGen music catalog via `media-use resolve --type bgm` (free with sign-in) or a quiet piano/guitar bed. No lyrics under VO. Duck under voice.

## 6. Edit, QA and output

- **HyperFrames** for the edit (seek-safe renders, brand system, check/snapshot QA, per-line audio placement). ~20 s per 30 s render. Remotion is faster for single UI shots but flat.
- Output: 1080×1080, 30 fps, H.264, loudnorm to −14 LUFS. Contact sheet PNG per cut.
- End card on every video: trial line ("Try it free for 3 days"), "Download <App> · App Store · Google Play · <domain>", fine print ("N-day free trial for new subscribers. Then billed by the App Store or Google Play until you cancel.").
- Captions burned in (most people watch muted); hook readable at frame 0, inside the middle 80%.

## Didn't work (Nov 2026)

- Gemini free tier: 429 limit 0 for image/video/music; needs prepaid credit (402 when depleted).
- "Imagen 2.6" doesn't exist; Imagen 4 retired — Nano Banana 2.1 replaces it.
- codex-imagegen: tool unavailable in session.
- HeyGen generation and voices: need a paid HyperFrames plan.
