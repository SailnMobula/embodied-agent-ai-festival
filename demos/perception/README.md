# Perception demos

Live RealSense D455 perception for the workshop's Station 2, shown in **Rerun**: one viewer that
holds the camera image, the 2D overlays and the 3D point cloud together.

Five live demos, each a single command:

| Command | Shows | Model |
| --- | --- | --- |
| `python detect.py` | Bounding boxes around people | YOLO11n |
| `python segment.py` | Pixel-exact masks | YOLO11n-seg |
| `python pose.py` | Skeleton + live wave detection | MediaPipe Pose |
| `python depth.py` | The 3D point cloud — how the robot sees | RealSense depth |
| `python fuse.py` | Detections placed into the 3D cloud | YOLO11n + depth |

Plus `footage.py` for pretty pre-rendered stills (zero-shot, prompt-driven — not realtime).

## Setup

Managed with [uv](https://docs.astral.sh/uv/). Python **3.12** is pinned (PyTorch and MediaPipe
have no 3.14 wheels yet).

```bash
uv sync                       # create the env and install everything
curl -L -o models/pose_landmarker_lite.task \
  https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task
```

The YOLO weights download themselves on first run. Run everything with `uv run`:

```bash
uv run detect.py
```

## Running the camera

**The RealSense on macOS is the fragile part.** Live USB capture needs `sudo` and is unreliable
(a known librealsense-on-Apple-Silicon issue). Two ways to de-risk the talk:

**Rehearse on the webcam** — no depth, but detection, segmentation and pose all work:

```bash
uv run detect.py --webcam 0
uv run pose.py --webcam 0
```

**Record once, play back live** — the robust path for `depth.py` and `fuse.py`, which need depth.
The Python binding segfaults on enumeration on this Mac, but the C tool `rs-record` (from
`brew install librealsense`) does not. Record a clip, then play it back:

```bash
rs-record -f scene.bag        # Ctrl-C to stop
uv run depth.py --bag scene.bag
uv run fuse.py --bag scene.bag
```

Live RealSense is the default (no flag) and works on Linux / the robot, but **not on this Mac** —
`pyrealsense2` segfaults enumerating the device. On macOS, use `--webcam` or `--bag`.

## Suggested run order on stage

1. `detect.py` — "the robot finds people." Boxes.
2. `segment.py` — "not just where, but exactly which pixels." Masks.
3. `pose.py` — "down to the joints." Upper-body skeleton (arms and hands, no legs — pass
   `--full-body` for all 33 landmarks). Wave at the camera → the status log flips to `WAVE`. This
   is the exact signal the robot's wave-back reacts to.
4. `depth.py` — spin the point cloud. "This is how the robot sees — in 3D, not a flat picture."
5. `fuse.py` — "and it knows *where in the room* each person is." Labels floating in the cloud.

## Footage (optional, heavy)

`footage.py` reuses the zero-shot GroundingDINO + SAM pipeline from `projects/rausch`: name what
you want with a text prompt and get high-quality masks. Too slow for live, so run it on stills or
on a recorded `.bag` — good for slides.

```bash
uv run --extra footage footage.py photo.jpg --prompt "person. robot. box."
uv run --extra footage footage.py --bag scene.bag --stride 15 --limit 20 --prompt "person."
```

Prompts are lowercase phrases, each ending in a period. Weights (~3 GB) download on first use;
they are shared with `projects/rausch` if you have run that.

## Tests

```bash
uv run pytest
```

`test_wave.py` and `test_geometry.py` cover the pure logic — the wave rule and the pinhole
maths — with no camera and no models. The `smoke_*.py` scripts exercise the model wrappers and
every Rerun call against a sample image, writing an `.rrd` you can open in Rerun to eyeball the
overlays.

## What runs where

- `perception/sources.py` — the camera abstraction. `RealSenseSource` (live or `.bag`) and
  `WebcamSource`, behind one `FrameSource` interface, so the demos never know which is plugged in.
- `perception/geometry.py` — pinhole maths: deprojection to a point cloud, lifting a box into 3D.
- `perception/wave.py` — the wave rule. Reports `x_norm`, matching the robot's `last_wave` signal.
- `perception/{detection,segmentation,pose_estimation,zeroshot}.py` — thin model wrappers, each
  returning plain data.
- `perception/viewer.py` — every Rerun call lives here; nothing else imports `rerun`.
