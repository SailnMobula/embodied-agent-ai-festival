import argparse

import numpy as np
from PIL import Image

from perception import annotate, viewer
from perception.cli import add_source_arguments, build_source
from perception.pose_estimation import UPPER_BODY_LANDMARKS, PoseEstimator
from perception.wave import WaveDetector


def render_image(path: str, out: str, keep: tuple[int, ...] | None) -> None:
    rgb = np.array(Image.open(path).convert("RGB"))
    pose = PoseEstimator().estimate(rgb, timestamp_seconds=0.0)
    if pose is None:
        raise SystemExit(f"No person found in {path}")
    annotate.save(annotate.draw_pose(rgb, pose, keep), out)
    print(f"saved {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Live pose estimation and wave detection in Rerun")
    add_source_arguments(parser)
    parser.add_argument("--full-body", action="store_true", help="Draw all 33 landmarks, not just the upper body")
    parser.add_argument("--image", help="Run on one image instead of a live source")
    parser.add_argument("--out", help="With --image, save an annotated PNG instead of opening Rerun")
    args = parser.parse_args()

    keep = None if args.full_body else UPPER_BODY_LANDMARKS

    if args.image and args.out:
        render_image(args.image, args.out, keep)
        return

    estimator = PoseEstimator()
    wave_detector = WaveDetector()
    viewer.init("pose")
    viewer.enable_pose_skeleton(keep)

    with build_source(args) as source:
        for frame in source.frames():
            viewer.log_image(frame.color_rgb)

            pose = estimator.estimate(frame.color_rgb, frame.timestamp)
            if pose is None:
                viewer.clear_pose()
                continue

            height, width = frame.color_rgb.shape[:2]
            viewer.log_pose(pose, width, height, keep)

            state = wave_detector.update(frame.timestamp, pose.landmarks)
            viewer.log_status(describe(state), alert=state.is_waving)


def describe(state) -> str:
    if state.is_waving:
        return f"WAVE  x_norm={state.x_norm:.2f}"
    if state.wrist_raised:
        return f"arm raised  ({state.oscillations} swings)"
    return "no wave"


if __name__ == "__main__":
    main()
