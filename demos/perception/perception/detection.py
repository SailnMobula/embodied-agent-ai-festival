from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class Detection:
    x: float
    y: float
    width: float
    height: float
    label: str
    score: float


class Detector:
    def __init__(self, model_name: str = "yolo11n.pt", min_confidence: float = 0.4, only_classes: list[int] | None = None):
        from ultralytics import YOLO

        self._model = YOLO(model_name)
        self._min_confidence = min_confidence
        self._only_classes = only_classes

    def detect(self, rgb: np.ndarray) -> list[Detection]:
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        result = self._model.predict(
            bgr, conf=self._min_confidence, classes=self._only_classes, verbose=False
        )[0]

        names = result.names
        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(
                Detection(
                    x=x1,
                    y=y1,
                    width=x2 - x1,
                    height=y2 - y1,
                    label=names[int(box.cls)],
                    score=float(box.conf),
                )
            )
        return detections
