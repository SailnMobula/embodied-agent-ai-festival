import argparse

import cv2
import numpy as np

from perception import viewer
from perception.geometry import point_cloud
from perception.sources import estimated_intrinsics

DEPTH_SCALE = 0.001
D455_DEPTH_HFOV = 87.0


def load_depth_metres(path: str, width: int, height: int) -> np.ndarray:
    raw = np.fromfile(path, dtype=np.uint16).reshape(height, width)
    return raw.astype(np.float32) * DEPTH_SCALE


def colour_by_distance(depth_metres: np.ndarray, max_depth: float) -> np.ndarray:
    normalized = np.clip(depth_metres / max_depth, 0.0, 1.0)
    coloured = cv2.applyColorMap((normalized * 255).astype(np.uint8), cv2.COLORMAP_TURBO)
    return cv2.cvtColor(coloured, cv2.COLOR_BGR2RGB)


def main() -> None:
    parser = argparse.ArgumentParser(description="Show raw depth frames (rs-convert -r) as a 3D cloud in Rerun")
    parser.add_argument("raw", nargs="+", help="Raw z16 depth files")
    parser.add_argument("--width", type=int, default=848)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--max-depth", type=float, default=4.0)
    args = parser.parse_args()

    intrinsics = estimated_intrinsics(args.width, args.height, D455_DEPTH_HFOV)
    viewer.init("depth")

    for index, path in enumerate(sorted(args.raw)):
        depth = load_depth_metres(path, args.width, args.height)
        depth[depth > args.max_depth] = 0.0
        points, colours = point_cloud(depth, colour_by_distance(depth, args.max_depth), intrinsics, args.max_depth)

        viewer.set_frame(index)
        viewer.log_camera(intrinsics)
        viewer.log_point_cloud(points, colours)


if __name__ == "__main__":
    main()
