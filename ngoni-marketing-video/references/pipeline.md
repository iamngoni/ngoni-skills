# Pipeline

First proven on a mobile app series (Nov 2026, Apple silicon Mac, 24 GB). Model names and prices change; re-check them before each project.

## 1. People: licensed stock first

- **Pexels** (Pexels License, no attribution needed, commercial use allowed).
  - `curl` gets a 403 on www.pexels.com, so open clip pages with a web fetch instead.
  - Take the author and the `videos.pexels.com/video-files/<id>/<id>-<variant>.mp4` URL.
  - Cut only the seconds you need with `scripts/stock_segment.sh`; never download the whole clip.
- Record every clip in `licenses.md`: id, author, URL and the seconds used.
- Vet each clip:
  - candid, with no watermark and no visible brands;
  - fits the audience: region, age, household type.
- Phones in stock footage usually face the person or show black screens. Don't composite UI onto them; cut to the rendered device instead.
- Backups:
  - **Mixkit** (thinner on some regions).
  - **Avoid** aggregators that mix in AI-made or watermarked clips.
  - **HeyGen stock search** is for mood boards only: low resolution, unclear licence.
- Across a series, vary who's on screen so every audience segment sees themselves.

## 2. AI hero shots: only for the moment stock can't show

- **Model:** Gemini Omni (`gemini-omni-1.2-flash`, Interactions API), text-to-video, 3–6 s. It replaced Veo 3.1 Preview in Oct 2026.
- **Test take:** always make a 360p test first (~$0.07–0.15) and look at it.
- **Final:** then make one 1080p final (~$0.33–0.64). Don't retry without telling the owner.
- **Aspect:** output is 16:9 or 9:16 only. For square or another aspect, crop around the subject.
- **Prompt:** cover who (region, age, relationship), where (a real local setting), the single action, and the light. Add "plain walls, no lettering, no logos".
- Generated phones and laptops show glowing fake UI. Blur or darken that area, or cut away before it's readable.

## 3. Product screens: real captures on a rendered device

- **Source:** captures come from the product itself, from integration or UI test runs, a staging build, or exports from the design system, all with demo data.
- **Clean-up:**
  - Remove test-only overlays by filling them with the surrounding surface colour. Never alter the content.
  - Paint out third-party brands, share buttons and toasts the same way.
- **Device shots:**
  - `scripts/blender_phone_shot.py` uses Blender 5.x headless with EEVEE. Its Standard view transform keeps UI colours exact.
  - `scripts/blender_retexture.py` swaps the capture in a saved .blend.
  - For a laptop or tablet, adapt the device mesh and screen aspect.
  - Blender MCP needs `BLENDER_PATH` set and Blender open with the add-on; headless scripts are more repeatable.
- **Flat highlight scenes:** the capture itself, full frame, with camera moves and highlights (see highlights.md). These scenes carry the feature explanation.

## 4. Voice

- **Model:** Gemini TTS (`gemini-3.8-flash-tts`), with a voice from the Extended Voice Library that matches the audience's accent.
  - List voices for free: `GET /v1beta/voices?language_code=<xx-YY>`.
- **One call per video:** put all lines in one input, separated by `<long pause>`. Split the audio with `scripts/vo_segments.py` against a Whisper transcript. Costs about $0.005 per video.
- **Expect mishearings:** transcribers trip on accents and product names. Flag those lines for the owner to check by ear; re-voicing a whole video costs about $0.005.
- **Fallbacks:**
  - Kokoro (`npx hyperframes tts`): free, neutral American.
  - macOS `say`: few regional voices.
  - For a hero cut, a human voice artist is still worth it.

## 5. Music and sound

- Use the HeyGen music catalog via `media-use resolve --type bgm` (free with sign-in), or a quiet instrumental bed.
- No lyrics under a voiceover, and duck the music beneath the voice.

## 6. Edit, QA and output

- **Edit in HyperFrames.** It gives seek-safe renders, check and snapshot QA, and per-line audio placement. A 30 s video renders in about 20 s. Remotion is faster for a single UI shot but looks flat.
- **Output:** the agreed aspect(s), 30 fps, H.264, loudness normalised to −14 LUFS, plus a contact-sheet PNG per cut.
- **Captions:** burned in, because most people watch muted. The hook must be readable at frame 0, inside the middle 80% of the frame.
- **End card:** the offer (trial, price or download), store badges or the domain, and any fine print the stores or the law require for that offer.

## Didn't work (Nov 2026)

- **Gemini free tier:** returns 429 with limit 0 for image, video and music. It needs prepaid credit, and returns 402 when the credit runs out.
- **Imagen:** Imagen 4 was retired; Nano Banana 2.1 replaces it.
- **Codex image generation:** the tool wasn't available in the session.
- **HeyGen generation and voices:** need a paid HyperFrames plan.

See `examples/dueo-series/tool-log.md` for the full comparison.
