import argparse

from perception import viewer
from perception.cli import add_source_arguments, build_source
from perception.geometry import point_cloud


def main() -> None:
    parser = argparse.ArgumentParser(description="Live 3D point cloud — how the robot sees — in Rerun")
    add_source_arguments(parser)
    parser.add_argument("--max-depth", type=float, default=4.0, help="Drop points beyond this many metres")
    args = parser.parse_args()

    viewer.init("depth")

    with build_source(args) as source:
        for frame in source.frames():
            viewer.log_camera(frame.intrinsics)
            viewer.log_image(frame.color_rgb)
            if not frame.has_depth:
                viewer.log_status("This source has no depth — use the RealSense for the 3D view", alert=True)
                continue
            points, colors = point_cloud(frame.depth_m, frame.color_rgb, frame.intrinsics, args.max_depth)
            viewer.log_point_cloud(points, colors)


if __name__ == "__main__":
    main()
