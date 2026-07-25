from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class Instance:
    id: int
    label: str
    score: float


@dataclass(frozen=True)
class Segmentation:
    label_map: np.ndarray
    instances: list[Instance]


class Segmenter:
    def __init__(self, model_name: str = "yolo11n-seg.pt", min_confidence: float = 0.4, only_classes: list[int] | None = None):
        from ultralytics import YOLO

        self._model = YOLO(model_name)
        self._min_confidence = min_confidence
        self._only_classes = only_classes

    def segment(self, rgb: np.ndarray) -> Segmentation:
        height, width = rgb.shape[:2]
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        result = self._model.predict(
            bgr, conf=self._min_confidence, classes=self._only_classes, verbose=False
        )[0]

        label_map = np.zeros((height, width), dtype=np.uint16)
        instances: list[Instance] = []
        if result.masks is None:
            return Segmentation(label_map, instances)

        names = result.names
        for index, (mask, box) in enumerate(zip(result.masks.data, result.boxes), start=1):
            resized = cv2.resize(mask.cpu().numpy(), (width, height)) > 0.5
            label_map[resized] = index
            instances.append(Instance(id=index, label=names[int(box.cls)], score=float(box.conf)))

        return Segmentation(label_map, instances)
