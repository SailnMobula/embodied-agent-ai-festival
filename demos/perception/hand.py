import argparse

import numpy as np
from PIL import Image

from perception import annotate, viewer
from perception.cli import add_source_arguments, build_source
from perception.hands import HandEstimator


def render_image(path: str, out: str) -> None:
    rgb = np.array(Image.open(path).convert("RGB"))
    hands = HandEstimator().estimate(rgb, timestamp_seconds=0.0)
    if not hands:
        raise SystemExit(f"No hand found in {path}")
    annotate.save(annotate.draw_hands(rgb, hands), out)
    print(f"saved {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Live hand and finger tracking in Rerun")
    add_source_arguments(parser)
    parser.add_argument("--image", help="Run on one image instead of a live source")
    parser.add_argument("--out", help="With --image, save an annotated PNG instead of opening Rerun")
    args = parser.parse_args()

    if args.image and args.out:
        render_image(args.image, args.out)
        return

    estimator = HandEstimator()
    viewer.init("hands")

    with build_source(args) as source:
        for frame in source.frames():
            hands = estimator.estimate(frame.color_rgb, frame.timestamp)
            viewer.log_image(annotate.draw_hands(frame.color_rgb, hands))


if __name__ == "__main__":
    main()
