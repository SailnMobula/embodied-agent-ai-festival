import argparse

from perception import viewer
from perception.cli import add_source_arguments, build_source
from perception.segmentation import Segmenter


def main() -> None:
    parser = argparse.ArgumentParser(description="Live instance segmentation (YOLO-seg) in Rerun")
    add_source_arguments(parser)
    parser.add_argument("--all-classes", action="store_true", help="Segment every class, not just people")
    args = parser.parse_args()

    segmenter = Segmenter(only_classes=None if args.all_classes else [0])
    viewer.init("segmentation")

    with build_source(args) as source:
        for frame in source.frames():
            viewer.log_camera(frame.intrinsics)
            viewer.log_image(frame.color_rgb)
            viewer.log_segmentation(segmenter.segment(frame.color_rgb))


if __name__ == "__main__":
    main()
