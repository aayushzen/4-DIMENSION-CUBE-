# Tesseract

A rotating 4D hypercube (tesseract), rendered in pygame. One `main.py` file, no platform-specific code — runs the same way on a laptop, in Replit, or on a phone in Pydroid 3.

## What it is

A tesseract has 16 corners living in 4D space (x, y, z, w) instead of the usual 3. Each frame the corners get rotated through a few different planes — some purely in 4D (xw, yw, zw), some in normal 3D (xz, yz) so the shape doesn't just look like a flat spinning square.

![Aayush REPL Banner](assets/REPL.jpg)

After rotating, the points get projected down in two steps:
1. The w-axis collapses into 3D — anything far along w shrinks or grows, which is what actually sells the "4D" look.
2. Normal z-axis perspective turns that 3D into the 2D points drawn on screen.

Blue edges and white corners sit on one side of the w-axis; purple edges and cyan corners sit on the other. That's the visual cue for "this part of the shape is on the far side of the 4th dimension."


## Setup

```
pip install pygame
python main.py
```

## Controls

| Action | Effect |
|---|---|
| Click/tap + drag | Rotate manually |
| Click/tap (no drag) | Pause / resume |
| Arrow keys | Nudge rotation |
| Esc | Quit |
