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
uv run --extra footage footage.py --webcam 0 --prompt "person. laptop. cup. bottle"
```

Grabs one frame from the webcam and draws boxes for whatever you named in the prompt. Edit the
prompt to name anything in the room, separated by periods. "Instead of a fixed list of classes, I
ask for what I want in words." Runs in a few seconds, not realtime, so it takes a single photo.
Opens just the picture with boxes, no 3D view. Add `--mask` if you ever want SAM outlines too.

## 3. Segmentation — SAM, snap a photo and outline it

```bash
uv run --extra footage footage.py --webcam 0 --prompt "person" --mask
```

Same snapshot as demo 2, but now SAM traces the exact outline of what GroundingDINO found, not just
a box. "Point at it by name, and it cuts out the exact pixels." A few seconds, not realtime.

## 4. Pose — arm and fingers, live, with wave detection

```bash
uv run pose.py --webcam 0
```

The arm from the body model, the fingers from the hand model, drawn together. Wave at the camera
and the status log flips to `WAVE`. "The robot does not detect waving, it detects joints, and a
rule we wrote turns wrist-above-shoulder plus side-to-side motion into a wave."

## 5. Depth Anything — 3D from a single photo

```bash
uv run --extra footage depth_anything.py --webcam 0
```

Takes one webcam photo and a model guesses the distance of every pixel, with no depth camera. Rerun
shows the coloured depth map and a 3D point cloud you can orbit. "One flat photo in, a 3D scene out."
The depth is relative, not measured in metres, but the shape of the room is real.

## Before the talk

Run each command once so the models are cached and the webcam permission prompt is already
answered. Step 2 installs `transformers` on first use (cached afterwards).
