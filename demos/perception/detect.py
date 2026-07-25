import argparse

from perception import viewer
from perception.cli import add_source_arguments, build_source
from perception.detection import Detector


def main() -> None:
    parser = argparse.ArgumentParser(description="Live object detection (YOLO) in Rerun")
    add_source_arguments(parser)
    parser.add_argument("--all-classes", action="store_true", help="Detect every class, not just people")
    args = parser.parse_args()

    detector = Detector(only_classes=None if args.all_classes else [0])
    viewer.init("detection")

    with build_source(args) as source:
        for frame in source.frames():
            viewer.log_image(frame.color_rgb)
            viewer.log_detections(detector.detect(frame.color_rgb))


if __name__ == "__main__":
    main()
