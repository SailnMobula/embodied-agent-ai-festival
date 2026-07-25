import sys

import numpy as np
from PIL import Image

from perception import viewer
from perception.pose_estimation import PoseEstimator, skeleton_connections
from perception.sources import estimated_intrinsics


def load_sample() -> np.ndarray:
    from ultralytics.utils import ASSETS

    return np.array(Image.open(ASSETS / "bus.jpg").convert("RGB"))


def main(path: str) -> None:
    print(f"skeleton connections: {len(skeleton_connections())}")

    rgb = load_sample()
    height, width = rgb.shape[:2]

    pose = PoseEstimator().estimate(rgb, timestamp_seconds=0.0)
    if pose is None:
        print("no pose found in sample")
        return
    print(f"landmarks: {len(pose.landmarks)}")

    viewer.init("smoke-pose", spawn=False, save_path=path)
    viewer.enable_pose_skeleton()
    viewer.log_camera(estimated_intrinsics(width, height))
    viewer.log_image(rgb)
    viewer.log_pose(pose, width, height)
    print(f"saved {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "smoke_pose.rrd")
