# Run sheet — perception demos (webcam)

MacBook webcam only, no RealSense. Four demos, in order. Each opens its own Rerun window.

**Stop each demo with `Ctrl-C` before starting the next** — only one program can hold the webcam
at a time.

Ignore the console lines about `re_analytics`, `GL version`, `XNNPACK`, `Feedback manager`,
`NORM_RECT`. They are harmless startup noise.

```bash
cd demos/perception
```

## 1. Detection — YOLO, live

```bash
uv run detect.py --webcam 0
```

Live boxes around people, dozens of frames a second. Stand in view, move around, step out and back.
"The robot finds people in real time."

## 2. Detection — GroundingDINO, snap a photo and prompt it

```bash
uv run --extra footage footage.py --webcam 0 --prompt "person. laptop. cup. bottle. chair."
```

Grabs one frame from the webcam and runs the text prompt over it: boxes plus masks for whatever you
named. Edit the prompt to name anything in the room (lowercase, each phrase ends in a period).
"Instead of a fixed list of classes, I ask for what I want in words." Runs in a few seconds, not
realtime — that is why it takes a single photo.

## 3. Segmentation — YOLO-seg, live

```bash
uv run segment.py --webcam 0
```

Same live feed, but pixel-exact masks instead of boxes. "Not just where someone is, but exactly
which pixels are them."

## 4. Pose — upper body, live, with wave detection

```bash
uv run pose.py --webcam 0
```

Upper-body skeleton (arms and hands). Wave at the camera and the status log flips to `WAVE`.
"The robot does not detect waving — it detects joints, and a rule we wrote turns wrist-above-shoulder
plus side-to-side motion into a wave."

## Before the talk

Run each command once so the models are cached and the webcam permission prompt is already
answered. Step 2 installs `transformers` on first use (cached afterwards).
