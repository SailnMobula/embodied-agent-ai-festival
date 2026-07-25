import argparse

import numpy as np
from PIL import Image

from perception import annotate, viewer
from perception.cli import add_source_arguments, build_source
from perception.hands import HandEstimator
from perception.pose_estimation import ARM_LANDMARKS, PoseEstimator
from perception.wave import WaveDetector


def draw_arm_and_fingers(rgb, pose, hands):
    annotated = rgb if pose is None else annotate.draw_pose(rgb, pose, ARM_LANDMARKS)
    return annotate.draw_hands(annotated, hands)


def render_image(path: str, out: str) -> None:
    rgb = np.array(Image.open(path).convert("RGB"))
    pose = PoseEstimator().estimate(rgb, timestamp_seconds=0.0)
    hands = HandEstimator().estimate(rgb, timestamp_seconds=0.0)
    if pose is None and not hands:
        raise SystemExit(f"No arm or hand found in {path}")
    annotate.save(draw_arm_and_fingers(rgb, pose, hands), out)
    print(f"saved {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Live arm and finger tracking with wave detection in Rerun")
    add_source_arguments(parser)
    parser.add_argument("--image", help="Run on one image instead of a live source")
    parser.add_argument("--out", help="With --image, save an annotated PNG instead of opening Rerun")
    args = parser.parse_args()

    if args.image and args.out:
        render_image(args.image, args.out)
        return

    pose_estimator = PoseEstimator()
    hand_estimator = HandEstimator()
    wave_detector = WaveDetector()
    viewer.init("pose")

    with build_source(args) as source:
        for frame in source.frames():
            pose = pose_estimator.estimate(frame.color_rgb, frame.timestamp)
            hands = hand_estimator.estimate(frame.color_rgb, frame.timestamp)
            viewer.log_image(draw_arm_and_fingers(frame.color_rgb, pose, hands))

            if pose is not None:
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
