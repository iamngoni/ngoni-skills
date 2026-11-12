#!/usr/bin/env python3
"""One Gemini TTS call through the Interactions API. Exactly one request: no retries, no loops.

The key is read from the GEMINI_API_KEY environment variable only; it is never printed or written.
Usage: GEMINI_API_KEY=... gemini_tts.py --model gemini-3.8-flash-tts --voice <voice-id> \
         --style "warm, conversational" --out out.wav "text"
Prints one JSON line with the model, voice, http status, seconds, usage and audio duration, or the API error.
"""
import argparse, base64, json, os, sys, time, urllib.error, urllib.request, wave

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--voice", required=True)
ap.add_argument("--style", default="")
ap.add_argument("--out", required=True)
ap.add_argument("text")
a = ap.parse_args()
key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY not set")

content = {"type": "text", "text": a.text}
if a.style:
    content["annotations"] = [{"type": "speech_metadata", "style": a.style}]
body = {"model": a.model, "input": [{"type": "user_input", "content": [content]}],
        "response_format": {"type": "audio"}, "generation_config": {"speech_config": [{"voice": a.voice}]}}
req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions",
                             data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json", "x-goog-api-key": key})
t = time.time()
try:
    with urllib.request.urlopen(req, timeout=300) as r:
        status, data = r.status, json.loads(r.read())
except urllib.error.HTTPError as e:
    err = json.loads(e.read() or b"{}").get("error", {})
    print(json.dumps({"model": a.model, "status": e.code, "error": err.get("status"),
                      "message": (err.get("message") or "")[:400]}))
    sys.exit(1)

audio = None
def walk(o):
    global audio
    if isinstance(o, dict):
        if o.get("type") == "audio" and o.get("data") and audio is None:
            audio = o
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(data)
dur = None
if audio:
    raw = base64.b64decode(audio["data"])
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if raw[:4] == b"RIFF":
        open(a.out, "wb").write(raw)
    else:  # headerless 24 kHz mono s16le
        with wave.open(a.out, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(raw)
    with wave.open(a.out) as w:
        dur = round(w.getnframes() / w.getframerate(), 2)
print(json.dumps({"model": a.model, "voice": a.voice, "status": status, "seconds": round(time.time() - t, 1),
                  "usage": data.get("usage") or data.get("usageMetadata"), "audio_s": dur,
                  "mime": audio.get("mime_type") if audio else None, "out": a.out if audio else None,
                  "keys": list(data.keys())}))
sys.exit(0 if audio else 1)
