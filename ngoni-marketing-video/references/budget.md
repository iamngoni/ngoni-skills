# Budget

The owner funds generation with prepaid Gemini credit (Dueo started with $5). Treat it as cash.

## Prices seen (Gemini API, Nov 2026, list price)

| Item | Price | Typical per use |
|---|---|---|
| Omni 1.2 Flash video, 360p | ~$0.023/s + thinking tokens | 3 s test ≈ $0.075, 6 s ≈ $0.15 |
| Omni 1.2 Flash video, 720p | ~$0.07/s | — |
| Omni 1.2 Flash video, 1080p | ~$0.104/s + thinking tokens | 3 s ≈ $0.32, 6 s ≈ $0.64 |
| Thinking tokens (billed as text output) | $9 / 1M | +$0.004–0.015 per video call — include it in estimates |
| TTS `gemini-3.8-flash-tts` | — | ≈ $0.005 per 25 s read |
| Image (Nano Banana 2.1, 2K) | — | ≈ $0.05 |
| Listing voices/models, polling results (GET) | free | — |

Actual spend per Dueo video: stock-only $0.005; one AI hero shot $0.39–0.40; the first cinematic ad with three AI shots $1.59.

## Rules

- Agree a cap per video and a total before starting (Dueo batch 2: $0.80 per hero video, $0.30 otherwise, keep $0.80 in reserve).
- **Log before you call.** One row per call, written before it runs; fill in the actual from the response's usage.
- One request at a time; no retry loops. A failed call is reported, not retried silently.
- Stop and report if the next call would break the cap or the reserve.
- Report per video and all-time totals, and credit left, in every update.

## Spend log format (`spend-log.md`)

| # | When | Video | Call | Expected | Result | Actual (from usage) | Running total |
|---|---|---|---|---|---|---|---|
| 1 | 12 Nov | Black Friday | Omni 360p test, 3 s, 16:9 | ≈ $0.075 | HTTP 200, 27 s; tokens … | **$0.076** | $0.076 |
