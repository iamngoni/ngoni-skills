# Feature highlights

The owner's favourite part: animations that point at the exact feature on the real screen.

## Principle

Show the capture flat, in its own pixel space (e.g. 1206×2622), and move a virtual camera over it. Every highlight is a box **measured on the capture**, so a ring always lands on the real element at any zoom.

## Data model (see `examples/dueo-series/build_batch2.py`)

```python
# targets.py — boxes in capture pixels, measured once per capture
T = {"home_num": ("home", 112, 588, 612, 740), ...}   # name: (capture, x0, y0, x1, y1)

# per video
"screens": {
  "home": {
    "cap": "home",
    "poses": [(0, 603, 680, 0.95), (1.0, 380, 664, 1.55)],   # (arrive_t, cx, cy, scale): capture point at frame centre
    "swap": (3.0, "paid"),                                     # optional crossfade to a second capture in place
    "marks": [                                                 # (in, out, target, kind, label, count)
      (1.05, 3.5, "home_num", "spot@bottom", "What’s left: <em>R<cnt></em>", (0, 6600, "")),
      (4.3, 6.9, "home_plan", "ring@above", "A planning figure, <em>not a bank balance</em>", None),
    ],
    "foot": "Estimates use the rates you entered. Not financial advice.",
  }
}
```

## Highlight kinds

- **ring** — rounded outline around the box, label placed `@top/@bottom/@left/@above` or at explicit `@x,y`.
- **spot** — dim everything except the box (spotlight), label beside it.
- **count-up** — `<cnt>` in the label animates from→to (use the capture's exact figure).
- **punch-in** — a pose with scale 1.3–1.6 centred on the box before the mark.
- **foot** — small standing note for required qualifiers (not advice, planning figure, estimates).

## Rules

- A ring or spotlight only shows while the camera is **still**; the builder asserts no mark overlaps a camera move (`MOVE` ≈ 0.7 s).
- One idea per mark, 0.8–4 s each, synced to the VO line that names it.
- Labels are short, sentence case, one emphasised phrase (`<em>`), no exclamation marks.
- Every number in a label equals the number on the capture.
- Paint out anything that must not show (real brands, share buttons, toasts) on the image before use, with the surrounding surface colour.
- Check with HyperFrames snapshots at each mark's midpoint.
