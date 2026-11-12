#!/usr/bin/env python3
"""Print speech segments of a VO read (silences >= MIN s at -38 dB) with the words Whisper heard in each.
Usage: vo_segments.py full.wav transcript.json [min_silence]"""
import json, re, subprocess, sys
wav, tj = sys.argv[1], sys.argv[2]; mn = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
err = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", f"silencedetect=noise=-38dB:d={mn}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout)
sil = list(zip(st, en + [dur] * (len(st) - len(en))))
segs, cur = [], 0.0
for a, b in sil:
    if a - cur > 0.05: segs.append((cur, a))
    cur = b
if dur - cur > 0.05: segs.append((cur, dur))
d = json.load(open(tj)); words = d if isinstance(d, list) else d.get("words", [])
for i, (a, b) in enumerate(segs):
    ws = [w.get("text", w.get("word")) for w in words if a - 0.15 <= (w["start"] + w["end"]) / 2 <= b + 0.15]
    print(f"{i:2d} {a:6.2f}-{b:6.2f} ({b-a:4.2f}s) {' '.join(ws)}")
