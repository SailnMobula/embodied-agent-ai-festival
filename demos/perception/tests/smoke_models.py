import sys

import numpy as np
import rerun as rr
from PIL import Image

from perception import viewer
from perception.detection import Detector
from perception.segmentation import Segmenter
from perception.sources import estimated_intrinsics


def load_sample() -> np.ndarray:
    from ultralytics.utils import ASSETS

    return np.array(Image.open(ASSETS / "bus.jpg").convert("RGB"))


def main(path: str) -> None:
    rgb = load_sample()
    height, width = rgb.shape[:2]

    detections = Detector(only_classes=[0]).detect(rgb)
    print(f"detections: {[f'{d.label} {d.score:.2f}' for d in detections]}")

    segmentation = Segmenter().segment(rgb)
    print(f"instances: {[(i.label, round(i.score, 2)) for i in segmentation.instances]}")

    rr.init("perception/smoke-models")
    rr.save(path)
    viewer.log_camera(estimated_intrinsics(width, height))
    viewer.log_image(rgb)
    viewer.log_detections(detections)
    viewer.log_segmentation(segmentation)
    print(f"saved {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "smoke_models.rrd")
