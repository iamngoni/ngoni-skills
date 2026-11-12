#!/usr/bin/env python3
"""Subscription series: writes one HyperFrames project per video and aspect ratio:
  series/<slug>-v/ (1080x1920) and series/<slug>-s/ (1080x1080), each with assets -> ../assets.
Edit VIDEOS below, run `python3 build_series.py`, then render each project (see README in renders/)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
TRIAL = "Try it free for 3 days"
FINE = "3-day free trial for new subscribers. Then billed by the App Store or Google Play until you cancel."

# shots: (id, src, start, dur, kind)  src "stock/X" gets -v/-s; "shots/phone-X" is a Blender shot of a real capture
# vo: (file under assets/audio/<vo dir>/, start, dur)
# caps: (id, in, out, 9:16 position, 1:1 position, html, note)
VIDEOS = {
    "money-back": {
        "title": "Dueo: Money back", "vo": "vo-mb", "end": 21.9, "total": 27.4,
        "shots": [
            ("a1", "stock/A1", 0.0, 2.95, "people"),        # Pexels 6967638
            ("a2", "stock/A2", 2.95, 2.35, "people"),       # Pexels 6136985
            ("p1", "shots/phone-mb_found", 5.3, 5.0, "phone"),
            ("a3", "stock/A3", 10.3, 2.6, "people"),        # Pexels 6967638
            ("p2", "shots/phone-mb_draft", 12.9, 3.5, "phone"),
            ("p3", "shots/phone-mb_rises", 16.4, 3.2, "phone"),
            ("a4", "stock/A4", 19.6, 2.3, "people"),        # Pexels 6918635
        ],
        "vo_lines": [("m1", 0.25, 2.65), ("m2", 3.05, 5.10), ("m3", 8.3, 4.57), ("m4", 13.0, 2.46),
                     ("m5", 16.5, 2.02), ("m6", 19.75, 1.76), ("m7", 22.4, 2.07)],
        "caps": [
            ("c1", 0.0, 2.9, "bot", "bot", "You’re probably paying for things <em>you forgot about.</em>", ""),
            ("c2", 2.95, 5.25, "bot", "bot", "Dueo checks the statements and emails <em>you share…</em>", ""),
            ("c3", 5.35, 10.25, "top", "side", "Dueo found <em>R1,787&nbsp;a&nbsp;year.</em>", "Plus R329 back, counted separately."),
            ("c4", 10.35, 12.85, "bot", "bot", "Insurance that isn’t in your plan. <em>An order charged twice.</em>", ""),
            ("c5", 12.95, 16.35, "top", "side", "It writes the cancel message. <em>You send it.</em>", "Nothing is cancelled for you."),
            ("c6", 16.45, 19.55, "top", "side", "And it spots <em>the bills that went up.</em>", ""),
            ("c7", 19.65, 21.85, "bot", "bot", "Money back, <em>without the admin.</em>", ""),
        ],
    },
    "payday-plan": {
        "title": "Dueo: Payday plan", "vo": "vo-pp", "end": 18.0, "total": 23.5,
        "shots": [
            ("b1", "stock/B1", 0.0, 1.7, "people"),         # Pexels 5593003
            ("b2", "stock/B2", 1.7, 2.7, "people"),         # Pexels 8655149
            ("p1", "shots/phone-pp_plan", 4.4, 5.4, "phone"),
            ("p2", "shots/phone-pp_added", 9.8, 2.4, "phone"),
            ("p3", "shots/phone-pp_left", 12.2, 4.0, "phone"),
            ("b3", "stock/B3", 16.2, 1.8, "people"),        # Pexels 5894542
        ],
        "vo_lines": [("p1", 0.2, 1.36), ("p2", 1.85, 2.40), ("p3", 4.5, 4.92), ("p4", 9.9, 2.20),
                     ("p5", 12.3, 3.88), ("p6", 16.4, 1.20), ("p7", 18.4, 1.85)],
        "caps": [
            ("c1", 0.0, 1.65, "bot", "bot", "It’s payday.", ""),
            ("c2", 1.75, 4.35, "bot", "bot", "Here’s your whole month, <em>in one tap.</em>", ""),
            ("c3", 4.45, 9.75, "top", "side", "Bills due before next payday. Goals. <em>What’s left.</em>", "Planning figures, not a bank balance."),
            ("c4", 9.85, 12.15, "top", "side", "Check it, and <em>confirm once.</em>", ""),
            ("c5", 12.25, 16.15, "top", "side", "Ideas for what’s left. <em>Nothing moves until you say so.</em>", ""),
            ("c6", 16.25, 17.95, "bot", "bot", "Payday, <em>sorted.</em>", ""),
        ],
    },
    "no-typing": {
        "title": "Dueo: A month with no typing", "vo": "vo-nt", "end": 19.7, "total": 25.2,
        "shots": [
            ("c1", "stock/C1", 0.0, 3.9, "people"),         # Pexels 7128597
            ("p1", "shots/phone-nt_week", 3.9, 5.0, "phone"),
            ("c2", "stock/C2", 8.9, 1.7, "people"),         # Pexels 5100063
            ("p2", "shots/phone-nt_scan", 10.6, 2.0, "phone"),
            ("p3", "shots/phone-nt_done", 12.6, 4.7, "phone"),
            ("c3", "stock/C3", 17.3, 2.4, "people"),        # Pexels 7227064
        ],
        "vo_lines": [("n1", 0.15, 3.62), ("n2", 4.05, 4.62), ("n3", 9.0, 2.28), ("n4", 12.75, 2.28),
                     ("n5", 15.15, 2.10), ("n6", 17.45, 2.07), ("n7", 20.2, 2.03)],
        "caps": [
            ("c1", 0.0, 3.85, "bot", "bot", "Who has time to type in <em>every bill?</em>", ""),
            ("c2", 4.0, 8.85, "top", "side", "Bank emails and statements <em>mark your bills paid.</em>", "Only what you share with Dueo."),
            ("c3", 8.95, 10.55, "bot", "bot", "Snap a receipt…", ""),
            ("c3b", 10.65, 12.55, "top", "side", "…and it <em>reads that too.</em>", ""),
            ("c4", 12.7, 15.0, "top", "side", "Once a week, <em>a&nbsp;30‑second review.</em>", ""),
            ("c5", 15.1, 17.25, "top", "side", "You confirm, <em>and you’re done.</em>", ""),
            ("c6", 17.35, 19.65, "bot", "bot", "A month of money, <em>without the typing.</em>", ""),
        ],
    },
}

CAP_CSS = """@font-face { font-family: "Bricolage Grotesque"; src: url("assets/fonts/BricolageGrotesque-Variable.ttf") format("truetype"); font-weight: 200 800; }
@font-face { font-family: "Figtree"; src: url("assets/fonts/Figtree-Variable.ttf") format("truetype"); font-weight: 300 900; }
#root { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
#root .g { position: absolute; inset: 0; opacity: 0; }
#root .scrim { position: absolute; left: 0; right: 0; }
#root .cap { position: absolute; left: 88px; right: 88px; }
#root .t { font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 88px; line-height: 1.0; letter-spacing: -0.035em; color: #FFFFFF; text-shadow: 0 2px 24px rgba(18,11,6,0.35); }
#root .t em { font-style: normal; color: #F6C48C; }
#root .n { margin-top: 24px; font-family: "Figtree", sans-serif; font-weight: 500; font-size: 36px; color: #F3E6D8; }
#root .v-top .scrim { top: 0; height: 44%; background: linear-gradient(180deg, rgba(18,11,6,0.62) 0%, rgba(18,11,6,0.36) 55%, rgba(18,11,6,0) 100%); }
#root .v-top .cap { top: 200px; }
#root .v-bot .scrim { bottom: 0; height: 40%; background: linear-gradient(0deg, rgba(18,11,6,0.66) 0%, rgba(18,11,6,0.38) 55%, rgba(18,11,6,0) 100%); }
#root .v-bot .cap { bottom: 250px; }
@media (min-aspect-ratio: 9/10) {
  #root .t { font-size: 64px; }
  #root .n { font-size: 28px; margin-top: 14px; }
  #root .scrim, #root .cap { top: auto; bottom: auto; height: auto; }
  #root .s-bot .scrim { left: 0; right: 0; top: auto; bottom: 0; height: 46%; background: linear-gradient(0deg, rgba(18,11,6,0.66) 0%, rgba(18,11,6,0.36) 60%, rgba(18,11,6,0) 100%); }
  #root .s-bot .cap { left: 64px; right: 64px; top: auto; bottom: 64px; }
  #root .s-side .scrim { left: 0; top: 0; bottom: 0; height: 100%; width: 62%; background: linear-gradient(90deg, rgba(18,11,6,0.55) 0%, rgba(18,11,6,0.3) 70%, rgba(18,11,6,0) 100%); }
  #root .s-side .cap { left: 64px; right: auto; top: 80px; width: 450px; }
}
"""


def captions(v, h):
    groups, tl = [], []
    for cid, a, b, vp, sp, html, note in v["caps"]:
        n = f'<div class="n">{note}</div>' if note else ""
        groups.append(f'  <div class="g v-{vp} s-{sp}" id="{cid}"><div class="scrim"></div>'
                      f'<div class="cap"><div class="t">{html}</div>{n}</div></div>')
        if a == 0:
            tl.append(f'tl.fromTo("#{cid}", {{opacity: 1}}, {{opacity: 1, duration: 0.01}}, 0)'
                      f'.fromTo("#{cid} .t", {{scale: 1.04}}, {{scale: 1, duration: 0.6, ease: "expo.out"}}, 0);')
        else:
            tl.append(f'tl.fromTo("#{cid}", {{opacity: 0}}, {{opacity: 1, duration: 0.3, ease: "power2.out"}}, {a})'
                      f'.fromTo("#{cid} .cap", {{y: 30}}, {{y: 0, duration: 0.45, ease: "expo.out"}}, {a});')
        tl.append(f'tl.to("#{cid}", {{opacity: 0, duration: 0.2, ease: "power2.in"}}, {round(b - 0.2, 2)});')
    return ("<template>\n<style>\n" + CAP_CSS + "</style>\n"
            f'<div id="root" data-composition-id="captions" data-width="1080" data-height="{h}" data-layout-allow-overlap>\n'
            + "\n".join(groups) + "\n</div>\n<script>\nconst tl = gsap.timeline({ paused: true });\n"
            + "\n".join(tl) + '\nwindow.__timelines["captions"] = tl;\n</script>\n</template>\n')


def end_card(h):
    return f"""<template>
<style>
@font-face {{ font-family: "Bricolage Grotesque"; src: url("assets/fonts/BricolageGrotesque-Variable.ttf") format("truetype"); font-weight: 200 800; }}
@font-face {{ font-family: "Figtree"; src: url("assets/fonts/Figtree-Variable.ttf") format("truetype"); font-weight: 300 900; }}
#root {{ position: absolute; inset: 0; overflow: hidden; background: #EEF1EC; font-family: "Figtree", sans-serif; color: #0F1F19; }}
#root .wrap {{ position: absolute; left: 96px; right: 96px; top: 0; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }}
#root .mark {{ width: 200px; height: 200px; }}
#root .word {{ margin-top: 20px; font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 170px; line-height: 1; letter-spacing: -0.045em; color: #1D4B3D; }}
#root .claim {{ margin-top: 30px; font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 64px; letter-spacing: -0.03em; }}
#root .trial {{ margin-top: 26px; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: 52px; letter-spacing: -0.02em; color: #1D4B3D; }}
#root .cta {{ margin-top: 56px; padding: 30px 64px; border-radius: 999px; background: #1D4B3D; color: #FFFFFF; font-size: 50px; font-weight: 700; }}
#root .stores {{ margin-top: 34px; font-size: 42px; font-weight: 500; color: #4A5A53; }}
#root .stores b {{ color: #0F1F19; font-weight: 700; }}
#root .fine {{ margin-top: 40px; max-width: 760px; font-size: 26px; line-height: 1.35; color: #5F6E67; }}
@media (min-aspect-ratio: 9/10) {{ #root .mark {{ width: 130px; height: 130px; }} #root .word {{ font-size: 116px; }} #root .claim {{ font-size: 50px; margin-top: 16px; }} #root .trial {{ font-size: 42px; margin-top: 16px; }} #root .cta {{ margin-top: 32px; font-size: 42px; padding: 22px 52px; }} #root .stores {{ margin-top: 20px; font-size: 36px; }} #root .fine {{ margin-top: 24px; font-size: 22px; max-width: 820px; }} }}
</style>
<div id="root" data-composition-id="end" data-width="1080" data-height="{h}">
  <div class="wrap">
    <img class="mark" id="en-mark" src="assets/brand/brand_mark.png" alt="Dueo">
    <div class="word" id="en-word">Dueo</div>
    <div class="claim" id="en-claim">Money plans, made together.</div>
    <div class="trial" id="en-trial">{TRIAL}</div>
    <div class="cta" id="en-cta">Download Dueo</div>
    <div class="stores" id="en-stores"><b>App Store</b> · <b>Google Play</b> · dueo.space</div>
    <div class="fine" id="en-fine">{FINE}</div>
  </div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.from("#en-mark", {{ y: 40, scale: 0.8, opacity: 0, duration: 0.6, ease: "expo.out" }}, 0)
  .from("#en-word", {{ y: 40, opacity: 0, duration: 0.5, ease: "expo.out" }}, 0.12)
  .from("#en-claim", {{ y: 30, opacity: 0, duration: 0.45, ease: "expo.out" }}, 0.3)
  .from("#en-trial", {{ y: 24, opacity: 0, duration: 0.45, ease: "expo.out" }}, 0.42)
  .from("#en-cta", {{ y: 30, opacity: 0, duration: 0.45, ease: "expo.out" }}, 0.55)
  .from("#en-stores", {{ y: 20, opacity: 0, duration: 0.4, ease: "expo.out" }}, 0.7)
  .from("#en-fine", {{ opacity: 0, duration: 0.4, ease: "power2.out" }}, 0.85);
window.__timelines["end"] = tl;
</script>
</template>
"""


def index(v, h, suf):
    END, TOTAL = v["end"], v["total"]
    vids = []
    for sid, src, st, du, kind in v["shots"]:
        path = f"assets/{src}-{suf}.mp4" if src.startswith("stock/") else f"assets/{src}.mp4"
        cls = "clip shot phone" if kind == "phone" else "clip shot"
        vids.append(f'      <video id="s-{sid}" class="{cls}" src="{path}" muted data-start="{st}" data-duration="{du}" data-track-index="1" style="z-index:1"></video>')
    vo = [f'      <audio id="vo-{n}" class="clip" src="assets/audio/{v["vo"]}/{n}.wav" data-start="{s}" data-duration="{d}" data-track-index="7" data-volume="1"></audio>' for n, s, d in v["vo_lines"]]
    p_starts = [st for _, _, st, _, k in v["shots"] if k == "phone"]
    sfx = [f'      <audio id="sfx-{i+1}" class="clip" src="assets/audio/whoosh-short.mp3" data-start="{round(max(0, s - 0.15), 2)}" data-duration="0.57" data-track-index="8" data-volume="0.16"></audio>' for i, s in enumerate(p_starts)]
    sfx.append(f'      <audio id="sfx-{len(p_starts)+1}" class="clip" src="assets/audio/impact-bass-1.mp3" data-start="{END}" data-duration="2.1" data-track-index="8" data-volume="0.4"></audio>')
    sub = lambda c, kind, st, du, z: (f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{st}" data-duration="{du}" data-track-index="{z}" data-track-kind="{kind}" data-width="1080" data-height="{h}" style="z-index:{z}"></div>')
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height={h}" />
    <title>{v["title"]}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: {h}px; overflow: hidden; background: #1A120C; }}
      .shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 50%; }}
      #warm {{ position: absolute; inset: 0; background: linear-gradient(160deg, #7a4a2a 0%, #c8875a 55%, #e9b183 100%); }}
      @media (min-aspect-ratio: 9/10) {{ .phone {{ left: auto; right: 0; width: 640px; object-position: 50% 60%; -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 220px); mask-image: linear-gradient(90deg, transparent 0, #000 220px); }} }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="{h}" data-fps="30">
      <div id="warm"></div>
      <!-- People: licensed Pexels stock (series/licenses.md). App screens: Blender phone shots of real device-pass captures only. -->
{chr(10).join(vids)}
{sub("captions", "captions", 0, END, 4)}
{sub("end", "graphics", END, round(TOTAL - END, 2), 5)}
      <audio id="music" class="clip" src="assets/audio/bgm.wav" data-start="0" data-media-start="0" data-duration="{TOTAL}" data-track-index="6" data-volume="0.14" data-fade-in="0.3" data-fade-out="2.0"></audio>
{chr(10).join(vo)}
{chr(10).join(sfx)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


HF = json.load(open(os.path.join(HERE, "..", "cinematic", "hyperframes.json")))
HF.pop("registryItems", None)
if __name__ == "__main__":
    for slug, v in VIDEOS.items():
        for suf, h in (("v", 1920), ("s", 1080)):
            root = os.path.join(HERE, f"{slug}-{suf}")
            os.makedirs(os.path.join(root, "compositions"), exist_ok=True)
            link = os.path.join(root, "assets")
            if not os.path.islink(link):
                os.symlink("../assets", link)
            open(os.path.join(root, "index.html"), "w").write(index(v, h, suf))
            open(os.path.join(root, "compositions", "captions.html"), "w").write(captions(v, h))
            open(os.path.join(root, "compositions", "end.html"), "w").write(end_card(h))
            json.dump(HF, open(os.path.join(root, "hyperframes.json"), "w"), indent=2)
            json.dump({"id": f"dueo-{slug}-{suf}", "name": f'{v["title"]} ({"9:16" if suf == "v" else "1:1"})'},
                      open(os.path.join(root, "meta.json"), "w"))
        # sanity: shots and VO stay inside their windows
        for sid, src, st, du, kind in v["shots"]:
            assert st + du <= v["end"] + 1e-6, (slug, sid)
        for n, s, d in v["vo_lines"]:
            assert s + d <= v["total"] - 0.3, (slug, n)
    print("built", ", ".join(VIDEOS))
