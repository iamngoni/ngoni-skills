#!/usr/bin/env python3
"""Generate one image with a Gemini image model (Nano Banana family) via the REST API.

The key is read from the GEMINI_API_KEY environment variable only; it is never printed or written.
Usage: GEMINI_API_KEY=... gemini_image.py --model gemini-nano-banana-2.1 --aspect 9:16 \
         --out assets/stills/s1.png [--ref ref1.png ...] "prompt"
Prints one JSON line: model, seconds, http status, usage metadata, out path (or the API error).
"""
import argparse, base64, json, mimetypes, os, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--aspect", default="9:16")
ap.add_argument("--out", required=True)
ap.add_argument("--ref", action="append", default=[])
ap.add_argument("prompt")
a = ap.parse_args()

key = os.environ.get("GEMINI_API_KEY")
if not key:
    sys.exit("GEMINI_API_KEY not set")

parts = []
for r in a.ref:
    mt = mimetypes.guess_type(r)[0] or "image/png"
    parts.append({"inlineData": {"mimeType": mt, "data": base64.b64encode(open(r, "rb").read()).decode()}})
parts.append({"text": a.prompt})
body = {
    "contents": [{"role": "user", "parts": parts}],
    "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": a.aspect}},
}
url = f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent"
req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json", "x-goog-api-key": key})
t = time.time()
try:
    with urllib.request.urlopen(req, timeout=300) as r:
        status, data = r.status, json.loads(r.read())
except urllib.error.HTTPError as e:
    err = json.loads(e.read() or b"{}").get("error", {})
    print(json.dumps({"model": a.model, "status": e.code, "seconds": round(time.time() - t, 1),
                      "error": err.get("status"), "message": (err.get("message") or "")[:400]}))
    sys.exit(1)

saved = None
for c in data.get("candidates", []):
    for p in c.get("content", {}).get("parts", []):
        d = p.get("inlineData") or p.get("inline_data")
        if d and d.get("data"):
            os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
            open(a.out, "wb").write(base64.b64decode(d["data"])); saved = a.out; break
    if saved: break
print(json.dumps({"model": a.model, "status": status, "seconds": round(time.time() - t, 1),
                  "usage": data.get("usageMetadata"), "out": saved,
                  "finish": [c.get("finishReason") for c in data.get("candidates", [])]}))
sys.exit(0 if saved else 1)
