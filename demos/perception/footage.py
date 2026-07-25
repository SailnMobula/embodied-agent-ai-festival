import argparse

import numpy as np
from PIL import Image

from perception import viewer
from perception.sources import estimated_intrinsics
from perception.zeroshot import GroundedSam


def main() -> None:
    parser = argparse.ArgumentParser(description="Zero-shot footage: prompt -> GroundingDINO boxes -> SAM masks")
    parser.add_argument("images", nargs="+", help="Image files to annotate")
    parser.add_argument("--prompt", default="person.", help="Lowercase phrases, each ending in a period")
    args = parser.parse_args()

    model = GroundedSam()
    viewer.init("footage")

    for path in args.images:
        rgb = np.array(Image.open(path).convert("RGB"))
        height, width = rgb.shape[:2]

        detections, segmentation = model.detect_and_segment(rgb, args.prompt)
        print(f"{path}: {[f'{d.label} {d.score:.2f}' for d in detections]}")

        viewer.log_camera(estimated_intrinsics(width, height))
        viewer.log_image(rgb)
        viewer.log_detections(detections)
        viewer.log_segmentation(segmentation)


if __name__ == "__main__":
    main()
