#!/usr/bin/env python3
"""One Gemini Omni video call (Interactions API). Exactly one request: no retries, no loops.

The key is read from the GEMINI_API_KEY environment variable only; it is never printed or written.
Usage: GEMINI_API_KEY=... gemini_omni.py --resolution 360p --duration 6 --aspect 9:16 --out g2.mp4 "prompt"
Prints one JSON line with status, seconds, usage (if reported) and the saved path, or the API error.
"""
import argparse, base64, json, os, sys, time, urllib.error, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="gemini-omni-1.2-flash")
ap.add_argument("--resolution", required=True, choices=["360p", "720p", "1080p"])
ap.add_argument("--duration", type=int, required=True)
ap.add_argument("--aspect", default="9:16")
ap.add_argument("--out", required=True)
ap.add_argument("prompt")
a = ap.parse_args()
key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY not set")
B = "https://generativelanguage.googleapis.com/v1beta"

body = {"model": a.model, "input": a.prompt,
        "response_format": {"type": "video", "aspect_ratio": a.aspect, "duration": f"{a.duration}s",
                            "resolution": a.resolution, "delivery": "uri"}}
t = time.time()
def call(url, data=None, raw=False):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                                 method="POST" if data else "GET",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=900) as r:
        b = r.read()
        return b if raw else json.loads(b)
try:
    d = call(f"{B}/interactions", body)
except urllib.error.HTTPError as e:
    err = json.loads(e.read() or b"{}").get("error", {})
    print(json.dumps({"status": e.code, "error": err.get("status"), "message": (err.get("message") or "")[:400]}))
    sys.exit(1)

# The single paid call is done. Everything below only reads its result (GETs are free).
found = {}
def walk(o):
    if isinstance(o, dict):
        if o.get("type") == "video" and not found:
            found.update(o)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(d)
meta = {"status": d.get("status"), "id": d.get("id"), "usage": d.get("usage"), "keys": list(d.keys())}
saved = None
if found.get("data"):
    open(a.out, "wb").write(base64.b64decode(found["data"])); saved = a.out
elif found.get("uri") or found.get("file_uri"):
    uri = found.get("uri") or found.get("file_uri")
    fid = uri.rstrip("/").split("files/")[-1].split(":")[0].split("?")[0]
    for _ in range(120):  # poll the file state (free GETs)
        f = call(f"{B}/files/{fid}")
        if f.get("state") == "ACTIVE": break
        if f.get("state") == "FAILED": meta["file_state"] = "FAILED"; break
        time.sleep(5)
    if meta.get("file_state") != "FAILED":
        open(a.out, "wb").write(call(f"{B}/files/{fid}:download?alt=media", raw=True)); saved = a.out
else:
    meta["video_part"] = {k: (v if k != "data" else "...") for k, v in found.items()}
meta.update({"seconds": round(time.time() - t, 1), "out": saved})
print(json.dumps(meta)[:2000])
sys.exit(0 if saved else 1)
