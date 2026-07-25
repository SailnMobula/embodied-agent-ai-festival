import argparse

import cv2
import numpy as np

from perception import viewer
from perception.geometry import point_cloud
from perception.monodepth import MonoDepth, to_metres
from perception.sources import WebcamSource, estimated_intrinsics


def snapshot(index: int, warmup: int = 10) -> np.ndarray:
    with WebcamSource(index) as source:
        for _ in range(warmup):
            source.read()
        frame = source.read()
        if frame is None:
            raise RuntimeError("Webcam gave no frame")
        return frame.color_rgb


def colour_map(depth_metres: np.ndarray, near: float, far: float) -> np.ndarray:
    normalized = np.clip((depth_metres - near) / (far - near), 0.0, 1.0)
    coloured = cv2.applyColorMap((normalized * 255).astype(np.uint8), cv2.COLORMAP_TURBO)
    return cv2.cvtColor(coloured, cv2.COLOR_BGR2RGB)


def main() -> None:
    parser = argparse.ArgumentParser(description="Depth from a single webcam photo, shown as a 3D cloud")
    parser.add_argument("--webcam", type=int, default=0)
    parser.add_argument("--near", type=float, default=0.4)
    parser.add_argument("--far", type=float, default=3.0)
    parser.add_argument("--image", help="Use an image file instead of the webcam")
    args = parser.parse_args()

    rgb = load_image(args.image) if args.image else snapshot(args.webcam)
    height, width = rgb.shape[:2]

    depth = to_metres(MonoDepth().relative_depth(rgb), args.near, args.far)
    intrinsics = estimated_intrinsics(width, height)
    points, colours = point_cloud(depth, rgb, intrinsics, max_depth=args.far + 0.5)

    viewer.init("depth-anything")
    viewer.log_image(rgb)
    viewer.log_depth_map(colour_map(depth, args.near, args.far))
    viewer.log_camera(intrinsics)
    viewer.log_point_cloud(points, colours)
    print(f"cloud points: {len(points)}")


def load_image(path: str) -> np.ndarray:
    from PIL import Image

    return np.array(Image.open(path).convert("RGB"))


if __name__ == "__main__":
    main()
