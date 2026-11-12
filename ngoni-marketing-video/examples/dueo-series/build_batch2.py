"""Batch 2: nine square videos (owner brief 12 Nov 2026). Square 1:1 only.

People: licensed Pexels stock (licenses.md) and Gemini Omni hero shots (assets/ai, centre-cropped from 16:9).
App screens: real device-pass captures only, as
  - Blender phone shots (assets/shots/phone-b2_*.mp4), and
  - flat highlight scenes: the capture moves in its own pixel space (1206x2622), so every ring,
    spotlight, label and count-up is placed from boxes measured on the capture (tools/targets.py).
    Rings only show while the camera is still, which the builder asserts.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "tools"))
from build_series import captions, end_card, HF  # noqa: E402
from targets import T  # noqa: E402

CW, CH = 1206, 2622          # capture size
F = 1080                     # square frame
MOVE = 0.7                   # camera move length (s)

# Screen scenes. poses: (arrive_t, cx, cy, s): capture point (cx, cy) sits at the frame centre at scale s.
# swap: (t, key) crossfades to a second capture in the same place. marks: (in, out, target, kind, label, count)
# count: (from, to, prefix) counts the <cnt> placeholder in the label. foot: a small standing note.
VIDEOS = {
    "black-friday": {
        "title": "Dueo: Black Friday, after payday", "vo": "vo-bf", "end": 19.7, "total": 25.2,
        "shots": [
            ("h1", "video", "assets/ai/H1-1080p.mp4", 0.0, 3.3),
            ("home", "screen", None, 3.3, 6.9),
            ("d1", "video", "assets/stock/D1-s.mp4", 10.2, 3.2),
            ("pi", "phone", "assets/shots/phone-b2_ideas.mp4", 13.4, 2.0),
            ("ideas", "screen", None, 15.4, 4.3),
        ],
        "screens": {
            "home": {"cap": "home", "poses": [(0, 603, 680, 0.95), (1.0, 380, 664, 1.55), (4.2, 603, 640, 1.0)],
                     "marks": [(1.05, 3.5, "home_num", "spot@bottom", "What’s left after commitments: <em>R<cnt></em>", (0, 6600, "")),
                               (4.3, 6.9, "home_plan", "ring@above", "A planning figure, <em>not a bank balance</em>", None)]},
            "ideas": {"cap": "ideas", "poses": [(0, 603, 1150, 0.95)],
                      "marks": [(0.25, 1.9, "ideas_title", "ring@top", "Ideas from <em>your own plan</em>", None),
                                (1.95, 4.3, "ideas_ok", "spot@top", "Nothing moves <em>until you say so</em>", None)]},
        },
        "vo_lines": [("bf1", 0.20, 2.94), ("bf2", 3.45, 1.29), ("bf3", 5.0, 5.02), ("bf4", 10.35, 3.09),
                     ("bf5", 13.75, 5.73), ("bf6", 19.95, 1.97)],
        "caps": [
            ("c1", 0.0, 3.25, "bot", "bot", "Black Friday is <em>2&nbsp;days after payday.</em>", ""),
            ("c4", 10.25, 13.35, "bot", "bot", "Shop with that, <em>not the whole salary.</em>", ""),
            ("c5", 13.45, 15.35, "top", "side", "Not sure? <em>Ask Dueo for ideas.</em>", ""),
        ],
    },
    "just-ask": {
        "title": "Dueo: Just ask", "vo": "vo-ja", "end": 15.6, "total": 21.1,
        "shots": [
            ("h3", "video", "assets/ai/H3-1080p.mp4", 0.0, 2.5),
            ("pa", "phone", "assets/shots/phone-b2_ask.mp4", 2.5, 2.0),
            ("ask", "screen", None, 4.5, 5.4),
            ("pay", "screen", None, 9.9, 5.7),
        ],
        "screens": {
            "ask": {"cap": "ask", "poses": [(0, 603, 600, 0.95), (1.6, 420, 640, 1.45)],
                    "marks": [(0.1, 0.85, "ask_q", "ring", "Ask in <em>your own words</em>", None),
                              (1.65, 5.4, "ask_num", "spot@bottom", "<em>R<cnt></em> left for the trip", (0, 1200, ""))]},
            "pay": {"cap": "pay", "swap": (3.0, "paid"), "poses": [(0, 603, 1000, 0.95)],
                    "marks": [(0.1, 1.3, "pay_msg", "ring@left", "<em>Just say it</em>", None),
                              (1.35, 2.9, "pay_card", "ring@bottom", "It drafts <em>the record</em>", None),
                              (3.35, 5.7, "paid_done", "spot", "Nothing changes <em>until you approve</em>", None)]},
        },
        "vo_lines": [("ja1", 0.25, 2.06), ("ja2", 2.6, 3.3), ("ja3", 6.15, 3.5), ("ja4", 9.95, 2.85),
                     ("ja5", 13.05, 2.31), ("ja6", 15.85, 2.24)],
        "caps": [
            ("c1", 0.0, 2.45, "bot", "bot", "Can we afford <em>the trip in December?</em>", ""),
            ("c2", 2.55, 4.45, "top", "side", "Just ask. <em>It answers from your plan.</em>", ""),
        ],
    },
    "fine-print": {
        "title": "Dueo: The fine print", "vo": "vo-fp", "end": 19.9, "total": 25.3,
        "shots": [
            ("f1", "video", "assets/stock/F1-s.mp4", 0.0, 5.0),
            ("pl", "phone", "assets/shots/phone-b2_lease.mp4", 5.0, 2.0),
            ("lease", "screen", None, 7.0, 7.75),
            ("quote", "screen", None, 14.75, 2.25),
            ("applied", "screen", None, 17.0, 2.9),
        ],
        "screens": {
            "lease": {"cap": "lease", "poses": [(0, 603, 760, 0.95), (3.8, 450, 730, 1.45)],
                      "marks": [(0.1, 1.6, "lease_src", "ring@518,215", "14 pages, <em>read for you</em>", None),
                                (1.85, 3.05, "lease_rise", "ring", "Goes up <em>8% each March</em>", None),
                                (3.85, 7.75, "lease_date", "spot@top", "Last day to give notice: <em>31&nbsp;Dec</em>", None)]},
            "quote": {"cap": "quote", "poses": [(0, 603, 2050, 0.95)],
                      "marks": [(0.1, 2.25, "quote_box", "spot@top", "The exact words <em>from your lease</em>", None)]},
            "applied": {"cap": "applied", "poses": [(0, 603, 760, 0.95)],
                        "marks": [(0.15, 2.9, "applied_toast", "ring", "A reminder <em>before 31&nbsp;Dec</em>", None)],
                        "foot": "Dueo shows the clause for each figure. Not legal advice."},
        },
        "vo_lines": [("fp1", 0.2, 4.61), ("fp2", 5.05, 3.51), ("fp3", 8.85, 5.71), ("fp4", 14.85, 2.03),
                     ("fp5", 17.1, 2.56), ("fp6", 20.15, 1.59)],
        "caps": [
            ("c1", 0.0, 4.95, "bot", "bot", "Your lease says the rent goes up in March. <em>Did you read that far?</em>", ""),
            ("c2", 5.05, 6.95, "top", "side", "Add your lease. <em>Dueo reads it.</em>", ""),
        ],
    },
    "pay-it-off": {
        "title": "Dueo: Pay it off faster", "vo": "vo-po", "end": 21.3, "total": 26.7,
        "shots": [
            ("p1", "video", "assets/stock/P1-s.mp4", 0.0, 4.8),
            ("plan", "screen", None, 4.8, 13.3),
            ("p2", "video", "assets/stock/P2-s.mp4", 18.1, 3.2),
        ],
        "screens": {
            "plan": {"cap": "plan", "swap": (3.6, "extra"),
                     "poses": [(0, 603, 1500, 0.95), (2.6, 603, 940, 0.95), (6.6, 603, 700, 1.1)],
                     "marks": [(0.15, 1.85, "plan_order", "ring", "What you owe, <em>and the rates</em>", None),
                               (2.65, 3.55, "plan_date", "ring@680,168", "<em>Minimums only</em>", None),
                               (4.05, 4.95, "extra_amt", "ring", "<em>+R600</em> a month", None),
                               (5.0, 5.85, "extra_order", "ring", "<em>Smallest</em> first", None),
                               (6.65, 9.9, "extra_date", "spot@top", "Debt-free by <em>November 2027</em>", None),
                               (9.95, 13.3, "extra_less", "ring@top", "<em><cnt> months</em> sooner, less interest", (0, 13, ""))],
                     "foot": "Estimates use the rates you entered. Not financial advice."},
        },
        "vo_lines": [("po1", 0.15, 4.47), ("po2", 4.9, 2.36), ("po3", 7.5, 7.03), ("po4", 14.8, 2.82),
                     ("po5", 17.9, 3.17), ("po6", 21.55, 2.06)],
        "caps": [
            ("c1", 0.0, 4.75, "bot", "bot", "A credit card and a store account. <em>They never seem to shrink.</em>", ""),
            ("c5", 18.15, 21.25, "bot", "bot", "Estimates from your own numbers. <em>Nothing moves.</em>", ""),
        ],
    },
    "money-owed": {
        "title": "Dueo: Money owed", "vo": "vo-mo", "end": 19.1, "total": 24.4,
        "shots": [
            ("m1", "video", "assets/stock/M1-s.mp4", 0.0, 5.1),
            ("po", "phone", "assets/shots/phone-b2_owed.mp4", 5.1, 1.9),
            ("owed", "screen", None, 7.0, 4.05),
            ("remind", "screen", None, 11.05, 8.05),
        ],
        "screens": {
            "owed": {"cap": "owed", "poses": [(0, 603, 970, 0.9)],
                     "marks": [(0.1, 1.6, "owed_list", "ring", "Who, <em>and how much</em>", None),
                               (1.6, 2.9, "owed_card", "ring", "<em>R<cnt></em> still to come back", (0, 4900, "")),
                               (2.9, 4.05, "owed_intro", "ring@380,615", "A record, <em>not a bank balance</em>", None)]},
            "remind": {"cap": "remind", "poses": [(0, 603, 1070, 0.95), (2.6, 603, 1650, 0.95)],
                       "marks": [(0.1, 0.9, "remind_amt", "ring", "", None),
                                 (0.9, 1.85, "remind_late", "ring@700,846", "<em>Noticed</em>", None),
                                 (2.65, 4.4, "remind_msg", "spot@top", "A friendly reminder, <em>drafted for you</em>", None),
                                 (4.4, 6.0, "remind_tone", "ring", "You pick <em>the tone</em>", None),
                                 (6.0, 8.05, "remind_msg", "ring@top", "Dueo never <em>sends anything for you</em>", None)]},
        },
        "vo_lines": [("mo1", 0.2, 4.74), ("mo2", 5.2, 5.68), ("mo3", 11.15, 3.12), ("mo4", 14.5, 4.32),
                     ("mo5", 19.35, 1.66)],
        "caps": [
            ("c1", 0.0, 5.05, "bot", "bot", "You lent a friend R2,200. <em>Where’s that written down?</em>", ""),
            ("c2", 5.15, 6.95, "top", "side", "In Dueo, <em>it’s a record.</em>", ""),
        ],
    },
}
T["plan_order"] = ("plan", 60, 1476, 1146, 1920)

SCR_CSS = """@font-face { font-family: "Bricolage Grotesque"; src: url("assets/fonts/BricolageGrotesque-Variable.ttf") format("truetype"); font-weight: 200 800; }
@font-face { font-family: "Figtree"; src: url("assets/fonts/Figtree-Variable.ttf") format("truetype"); font-weight: 300 900; }
#root { position: absolute; inset: 0; overflow: hidden; background: BG; }
#root .layer { position: absolute; left: 0; top: 0; width: 1206px; height: 2622px; transform-origin: 0 0; }
#root .layer img { position: absolute; inset: 0; width: 1206px; height: 2622px; }
#root .ring { position: absolute; border: 7px solid #F2A65A; border-radius: 30px; opacity: 0; }
#root .ring.spot { box-shadow: 0 0 0 2600px rgba(10, 22, 16, 0.5); }
#root .lab { position: absolute; padding: 18px 30px; border-radius: 999px; background: #1D4B3D; color: #FFFFFF; white-space: nowrap;
  font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 40px; letter-spacing: -0.02em; opacity: 0; }
#root .lab em { font-style: normal; color: #F6C48C; }
#root .lab .cnt { font-variant-numeric: tabular-nums; }
#root .foot { position: absolute; left: 40px; right: 40px; bottom: 28px; text-align: center; font-family: "Figtree", sans-serif;
  font-weight: 600; font-size: 26px; color: #FFFFFF; }
#root .foot span { display: inline-block; padding: 10px 20px; border-radius: 999px; background: rgba(15, 31, 25, 0.78); }
"""
BG = {"ask": "#FDF8FF", "home": "#FDF8FF", "remind": "#FFFFFF", "quote": "#8B928D"}


def pose_xy(cx, cy, s):
    return round(F / 2 - s * cx, 2), round(F / 2 - s * cy, 2)


def check_pose(name, cx, cy, s):
    h = F / 2 / s
    assert cx - h >= -1 and cx + h <= CW + 1, (name, "x out of capture", cx, s)
    assert cy - h >= -1 and cy + h <= CH + 1, (name, "y out of capture", cy, s)


def pose_at(poses, t):
    """The pose held at time t, or None while the camera is moving."""
    held = poses[0]
    for p in poses[1:]:
        if t >= p[0]:
            held = p
        elif t > p[0] - MOVE:
            return None
    return held


def label_width(html):
    txt = re.sub(r"<[^>]+>", "", html).replace("&nbsp;", " ").replace("<cnt>", "0000")
    return int(len(txt) * 21 + 60)


def screen(cid, sc, dur):
    cap = sc["cap"]; poses = sc["poses"]
    for p in poses:
        check_pose(cid, *p[1:])
    els, tl = [], []
    x, y = pose_xy(*poses[0][1:])
    tl.append(f'tl.set("#{cid}-layer", {{x: {x}, y: {y}, scale: {poses[0][3]}}}, 0);')
    for p in poses[1:]:
        x, y = pose_xy(*p[1:])
        tl.append(f'tl.to("#{cid}-layer", {{x: {x}, y: {y}, scale: {p[3]}, duration: {MOVE}, ease: "power3.inOut"}}, {round(p[0] - MOVE, 2)});')
    imgs = f'<img src="assets/screens2/{cap}.png" alt="">'
    if "swap" in sc:
        ts, k2 = sc["swap"]
        imgs += f'<img id="{cid}-swap" src="assets/screens2/{k2}.png" alt="" style="opacity:0">'
        tl.append(f'tl.to("#{cid}-swap", {{opacity: 1, duration: 0.4, ease: "power2.inOut"}}, {ts});')
    counts = []
    for i, (a, b, tgt, kind, html, count) in enumerate(sc["marks"]):
        held = pose_at(poses, a + 0.01)
        held_end = pose_at(poses, b - 0.01)
        assert held and held_end and held == held_end, (cid, tgt, "ring shown while the camera moves")
        assert b <= dur + 1e-6, (cid, tgt)
        ck, x0, y0, x1, y1 = T[tgt]
        active = sc.get("swap") and a >= sc["swap"][0] and sc["swap"][1] or cap
        assert ck == active, (cid, tgt, "target is on", ck, "but screen shows", active)
        _, cx, cy, s = held
        pad = 14
        fx0 = F / 2 + s * (x0 - cx) - pad; fx1 = F / 2 + s * (x1 - cx) + pad
        fy0 = F / 2 + s * (y0 - cy) - pad; fy1 = F / 2 + s * (y1 - cy) + pad
        rid, lid = f"{cid}-r{i}", f"{cid}-l{i}"
        w = label_width(html); lh = 86
        kind, _, side = kind.partition("@")
        lx = min(max((fx0 + fx1) / 2 - w / 2, 36), F - 36 - w)
        if "," in side:
            lx, ly = (float(n) for n in side.split(","))
        elif side == "left":
            lx, ly = fx0 - 22 - w, (fy0 + fy1) / 2 - lh / 2
        elif side == "top":
            ly = 40
        elif side == "bottom":
            ly = F - 40 - lh
        elif side == "above":
            ly = fy0 - 22 - lh
        elif F - 24 - fy1 >= lh + 30:
            ly = fy1 + 22
        elif fy0 - 24 >= lh + 30:
            ly = fy0 - 22 - lh
        else:
            ly = min(fy1 - lh - 20, F - lh - 40)
        if sc.get("foot") and ly + lh > F - 90 and "," not in side:
            ly = F - 96 - lh
        els.append(f'<div class="ring {"spot" if kind == "spot" else ""}" id="{rid}" style="left:{fx0:.1f}px;top:{fy0:.1f}px;width:{fx1 - fx0:.1f}px;height:{fy1 - fy0:.1f}px"></div>')
        inner = html.replace("<cnt>", f'<span class="cnt" id="{lid}-n">{count[2]}{count[0]:,}</span>' if count else "")
        if html:
            assert 0 <= lx and lx + w <= F + 40 and 0 <= ly and ly + lh <= F, (cid, tgt, "label off frame", lx, ly, w)
            els.append(f'<div class="lab" id="{lid}" style="left:{lx:.1f}px;top:{ly:.1f}px">{inner}</div>')
        tl.append(f'tl.fromTo("#{rid}", {{opacity: 0, scale: 1.1}}, {{opacity: 1, scale: 1, duration: 0.45, ease: "expo.out"}}, {a});')
        if html: tl.append(f'tl.fromTo("#{lid}", {{opacity: 0, y: 18}}, {{opacity: 1, y: 0, duration: 0.4, ease: "expo.out"}}, {round(a + 0.12, 2)});')
        if b < dur - 0.05:
            tl.append(f'tl.to({[f"#{rid}"] + ([f"#{lid}"] if html else [])}, {{opacity: 0, duration: 0.22, ease: "power2.in"}}, {round(b - 0.22, 2)});')
        if count:
            c0, c1, pre = count
            counts.append(f'(function(){{ const el = document.getElementById("{lid}-n"); const st = {{v: {c0}}};'
                          f' tl.to(st, {{v: {c1}, duration: {min(1.2, b - a - 0.4):.2f}, ease: "power2.out", onUpdate: () => {{'
                          f' el.textContent = "{pre}" + Math.round(st.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ","); }} }}, {round(a + 0.15, 2)}); }})();')
    foot = f'<div class="foot"><span>{sc["foot"]}</span></div>' if sc.get("foot") else ""
    css = SCR_CSS.replace("BG", BG.get(cap, "#EFF1ED"))
    return ("<template>\n<style>\n" + css + "</style>\n"
            f'<div id="root" data-composition-id="{cid}" data-width="{F}" data-height="{F}" data-layout-allow-overlap>\n'
            f'  <div class="layer" id="{cid}-layer">{imgs}</div>\n  ' + "\n  ".join(els) + f"\n  {foot}\n</div>\n<script>\n"
            "const tl = gsap.timeline({ paused: true });\n" + "\n".join(tl) + "\n" + "\n".join(counts)
            + f'\nwindow.__timelines["{cid}"] = tl;\n</script>\n</template>\n')


def index(v):
    END, TOTAL = v["end"], v["total"]
    rows, subs, cuts = [], [], []
    for sid, kind, src, st, du in v["shots"]:
        cuts.append(st)
        if kind == "screen":
            cid = f"scr-{sid}"
            subs.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" data-duration="{du}" data-track-index="2" data-track-kind="graphics" data-width="{F}" data-height="{F}" style="z-index:2"></div>')
        else:
            cls = "clip shot phone" if kind == "phone" else "clip shot"
            rows.append(f'      <video id="s-{sid}" class="{cls}" src="{src}" muted data-start="{st}" data-duration="{du}" data-track-index="1" style="z-index:1"></video>')
    vo = [f'      <audio id="vo-{n}" class="clip" src="assets/audio/{v["vo"]}/{n}.wav" data-start="{s}" data-duration="{d}" data-track-index="7" data-volume="1"></audio>' for n, s, d in v["vo_lines"]]
    sfx = [f'      <audio id="sfx-{i+1}" class="clip" src="assets/audio/whoosh-short.mp3" data-start="{round(max(0, s - 0.15), 2)}" data-duration="0.57" data-track-index="8" data-volume="0.14"></audio>' for i, s in enumerate(cuts[1:])]
    sfx.append(f'      <audio id="sfx-end" class="clip" src="assets/audio/impact-bass-1.mp3" data-start="{END}" data-duration="2.1" data-track-index="8" data-volume="0.4"></audio>')
    sub = lambda c, kind, st, du, z: (f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{st}" data-duration="{du}" data-track-index="{z}" data-track-kind="{kind}" data-width="{F}" data-height="{F}" style="z-index:{z}"></div>')
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={F}, height={F}" />
    <title>{v["title"]}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {F}px; height: {F}px; overflow: hidden; background: #1A120C; }}
      .shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 50%; }}
      #warm {{ position: absolute; inset: 0; background: linear-gradient(160deg, #7a4a2a 0%, #c8875a 55%, #e9b183 100%); }}
      .phone {{ left: auto; right: 0; width: 640px; object-position: 50% 60%; -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 220px); mask-image: linear-gradient(90deg, transparent 0, #000 220px); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{F}" data-height="{F}" data-fps="30">
      <div id="warm"></div>
      <!-- People: Pexels stock and Gemini Omni hero shots (licenses.md). App screens: real device-pass captures only. -->
{chr(10).join(rows)}
{chr(10).join(subs)}
{sub("captions", "captions", 0, END, 4)}
{sub("end", "graphics", END, round(TOTAL - END, 2), 5)}
      <audio id="music" class="clip" src="assets/audio/bgm.wav" data-start="0" data-media-start="0" data-duration="{TOTAL}" data-track-index="6" data-volume="0.13" data-fade-in="0.3" data-fade-out="2.0"></audio>
{chr(10).join(vo)}
{chr(10).join(sfx)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    only = sys.argv[1:] or list(VIDEOS)
    for slug in only:
        v = VIDEOS[slug]
        root = os.path.join(HERE, f"{slug}-s")
        os.makedirs(os.path.join(root, "compositions"), exist_ok=True)
        link = os.path.join(root, "assets")
        if not os.path.islink(link):
            os.symlink("../assets", link)
        end = 0
        for sid, kind, src, st, du in v["shots"]:
            assert abs(st - end) < 1e-6, (slug, sid, "gap or overlap", end, st)
            end = st + du
            if kind == "screen":
                open(os.path.join(root, "compositions", f"scr-{sid}.html"), "w").write(screen(f"scr-{sid}", v["screens"][sid], du))
            else:
                assert os.path.exists(os.path.join(HERE, src)), src
        assert abs(end - v["end"]) < 1e-6, (slug, "shots end", end, v["end"])
        for n, s, d in v["vo_lines"]:
            assert s + d <= v["total"] - 0.3, (slug, n)
        open(os.path.join(root, "index.html"), "w").write(index(v))
        open(os.path.join(root, "compositions", "captions.html"), "w").write(captions(v, F))
        open(os.path.join(root, "compositions", "end.html"), "w").write(end_card(F))
        json.dump(HF, open(os.path.join(root, "hyperframes.json"), "w"), indent=2)
        json.dump({"id": f"dueo-{slug}-s", "name": f'{v["title"]} (1:1)'}, open(os.path.join(root, "meta.json"), "w"))
        print("built", slug)
