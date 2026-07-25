import argparse

from perception import viewer
from perception.cli import add_source_arguments, build_source
from perception.pose_estimation import UPPER_BODY_LANDMARKS, PoseEstimator
from perception.wave import WaveDetector


def main() -> None:
    parser = argparse.ArgumentParser(description="Live pose estimation and wave detection in Rerun")
    add_source_arguments(parser)
    parser.add_argument("--full-body", action="store_true", help="Draw all 33 landmarks, not just the upper body")
    args = parser.parse_args()

    keep = None if args.full_body else UPPER_BODY_LANDMARKS
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
