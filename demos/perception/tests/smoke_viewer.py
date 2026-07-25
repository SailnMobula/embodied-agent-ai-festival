import sys

import numpy as np

from perception import viewer
from perception.detection import Detection
from perception.geometry import Intrinsics, point_cloud
from perception.pose_estimation import Pose
from perception.segmentation import Instance, Segmentation

WIDTH, HEIGHT = 640, 480
INTRINSICS = Intrinsics(fx=600.0, fy=600.0, cx=320.0, cy=240.0, width=WIDTH, height=HEIGHT)


def synthetic_rgb() -> np.ndarray:
    rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    rgb[100:380, 220:420] = (60, 120, 200)
    return rgb


def synthetic_pose() -> Pose:
    landmarks = [(0.5, 0.5)] * 33
    landmarks[12] = (0.6, 0.4)
    landmarks[16] = (0.62, 0.2)
    return Pose(landmarks=landmarks, visibilities=[1.0] * 33)


def main(path: str) -> None:
    viewer.init("smoke", spawn=False, save_path=path)

    rgb = synthetic_rgb()
    viewer.log_camera(INTRINSICS)
    viewer.log_image(rgb)
    viewer.log_detections(
        [Detection(x=220, y=100, width=200, height=280, label="person", score=0.94)]
    )
    viewer.log_segmentation(
        Segmentation(
            label_map=(rgb[:, :, 2] > 100).astype(np.uint16),
            instances=[Instance(id=1, label="person", score=0.9)],
        )
    )
    viewer.log_pose(synthetic_pose(), WIDTH, HEIGHT)

    depth = np.full((HEIGHT, WIDTH), 2.0, dtype=np.float32)
    points, colors = point_cloud(depth, rgb, INTRINSICS, max_depth=4.0)
    viewer.log_point_cloud(points, colors)

    viewer.log_status("wave detected", alert=True)
    print(f"logged {len(points)} points to {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "smoke.rrd")
