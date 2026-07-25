import argparse

from perception import viewer
from perception.cli import add_source_arguments, build_source
from perception.detection import Detector
from perception.geometry import locate_in_3d, point_cloud


def main() -> None:
    parser = argparse.ArgumentParser(description="Fuse colour detections into the 3D point cloud")
    add_source_arguments(parser)
    parser.add_argument("--max-depth", type=float, default=4.0)
    args = parser.parse_args()

    detector = Detector(only_classes=[0])
    viewer.init("fusion")

    with build_source(args) as source:
        for frame in source.frames():
            viewer.log_camera(frame.intrinsics)
            viewer.log_image(frame.color_rgb)

            detections = detector.detect(frame.color_rgb)
            viewer.log_detections(detections)

            if not frame.has_depth:
                viewer.log_status("No depth on this source — the RealSense shows the fusion", alert=True)
                continue

            points, colors = point_cloud(frame.depth_m, frame.color_rgb, frame.intrinsics, args.max_depth)
            viewer.log_point_cloud(points, colors)

            located = [
                (locate_in_3d(d.x, d.y, d.width, d.height, frame.depth_m, frame.intrinsics), d)
                for d in detections
            ]
            viewer.log_located_detections(
                [point for point, _ in located if point is not None],
                [f"{d.label} {d.score:.2f}" for point, d in located if point is not None],
            )


if __name__ == "__main__":
    main()
