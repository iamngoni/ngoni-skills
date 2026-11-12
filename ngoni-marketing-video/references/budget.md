# Budget

Generation is usually paid from prepaid API credit. Treat it as the owner's cash.

## Prices seen (Gemini API, Nov 2026, list price — re-check before use)

| Item | Price | Typical per use |
|---|---|---|
| Omni 1.2 Flash video, 360p | ~$0.023/s + thinking tokens | 3 s test ≈ $0.075; 6 s ≈ $0.15 |
| Omni 1.2 Flash video, 720p | ~$0.07/s | — |
| Omni 1.2 Flash video, 1080p | ~$0.104/s + thinking tokens | 3 s ≈ $0.32; 6 s ≈ $0.64 |
| Thinking tokens (billed as text output) | $9 / 1M | +$0.004–0.015 per video call; include it in estimates |
| TTS (`gemini-3.8-flash-tts`) | — | ≈ $0.005 per 25 s read |
| Image (Nano Banana 2.1, 2K) | — | ≈ $0.05 |
| Listing voices or models, polling results (GET) | free | — |

Rule of thumb: a stock-only video costs its voiceover (under a cent), and each AI hero shot adds about $0.40 (a test take plus the final).

## Rules

- Agree on a total, a per-video cap and a reserve before starting. If the owner hasn't set them, propose them.
- **Log before you call.** Write one row per call before it runs, then fill in the actual cost from the response's usage.
- Make one request at a time, with no retry loops. Report a failed call; don't silently retry it.
- Stop and report if the next call would break the cap or the reserve.
- Give the per-video total, the all-time total and the credit left in every update. Remind the owner that the log uses list prices and that the billing page shows what was actually charged.

## Spend log format (`spend-log.md`)

| # | When | Video | Call | Expected | Result | Actual (from usage) | Running total |
|---|---|---|---|---|---|---|---|
| 1 | 12 Nov | Launch teaser | Omni 360p test, 3 s, 16:9 | ≈ $0.075 | HTTP 200, 27 s; tokens … | **$0.076** | $0.076 |
