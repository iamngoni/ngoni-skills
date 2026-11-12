# Example: Dueo subscription series (Nov 2026)

Dueo is a money-planning app for iOS and Android, made for South Africa first (ZAR). These are the rules and results from one real project, kept as a worked example. Don't apply them to other projects.

## Project rules (from the owner)

- **Format:** square 1:1 only, 1080×1080, 20–27 s. No vertical cuts.
- **Approval:** every new idea is pitched first and needs the owner's approval before anything is rendered.
- **Script home:** each script is a note in the owner's Kanso notebook (Dueo › Marketing Scripts). `marketing/growth/content/video-scripts.md` in the repo stays in sync.
- **Forbidden claims:** never say "bank balance", "connects to your bank" or "pays for you", and give no financial or tax advice.
  - "Available after commitments" is a planning figure.
  - Required on-screen qualifiers include "Estimates use the rates you entered" and "Not legal advice".
- **Audience:** keep wording neutral, never couples-only. Who's on screen varies: people on their own, families, flatmates and friends, couples.
- **Offers:** no discount codes or sales in ads.
- **End card:**
  - Headline: "Try it free for 3 days".
  - Line: "Download Dueo · App Store · Google Play · dueo.space".
  - Fine print: "3-day free trial for new subscribers. Then billed by the App Store or Google Play until you cancel."
- **Captures:** iOS light mode at 1206×2622, from the app's native integration tests, using demo data.
- **Voice:** Gemini TTS `en-za-csagent-7` (Cape Town English).
- **Posting:** nothing posts until the release with the advertised features is live in both stores.

## Budget and results

- **Credit:** $5 of prepaid Gemini credit in total, with a reserve of $0.80.
- **Caps:** $0.80 per hero video and $0.30 for the rest.

| Videos | Cost |
|---|---|
| Cinematic couples ad (3 AI shots) | $1.59 |
| Money back, Payday plan, No typing (stock only) | $0.005 each |
| Black Friday, Just ask (1 AI hero shot each) | $0.40 each |
| Fine print, Pay it off, Money owed (stock only) | $0.005 each |

## Hooks that worked

- "It's the 25th. Before you tap anything…" (posted on payday)
- "Black Friday is 2 days after payday. Check one number first."
- "You lent a friend R2,200. Where's that written down?"
- "Can we afford the trip in December?"
- "A credit card and a store account. They never seem to shrink."

## Files

- `build_series.py`: builds a HyperFrames project per video and holds the captions and end card.
- `build_batch2.py`: the shot lists, screen scenes, highlight marks, voiceover timing and captions for each video.
- `targets.py`: highlight boxes measured on each capture.
- `tool-log.md`: every tool tried and what happened.
