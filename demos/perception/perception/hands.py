from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

os.environ.setdefault("GLOG_minloglevel", "2")

DEFAULT_MODEL = Path(__file__).resolve().parent.parent / "models" / "hand_landmarker.task"


@dataclass(frozen=True)
class Hand:
    landmarks: list[tuple[float, float]]


def hand_connections() -> list[tuple[int, int]]:
    from mediapipe.tasks.python import vision

    return [(c.start, c.end) for c in vision.HandLandmarksConnections.HAND_CONNECTIONS]


class HandEstimator:
    def __init__(self, model_path: Path = DEFAULT_MODEL, max_hands: int = 2, min_confidence: float = 0.5):
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision

        options = vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(model_path)),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=min_confidence,
            min_tracking_confidence=min_confidence,
        )
        self._mp = mp
        self._landmarker = vision.HandLandmarker.create_from_options(options)
        self._last_timestamp_ms = -1

    def estimate(self, rgb: np.ndarray, timestamp_seconds: float) -> list[Hand]:
        timestamp_ms = max(self._last_timestamp_ms + 1, int(timestamp_seconds * 1000))
        self._last_timestamp_ms = timestamp_ms

        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
        result = self._landmarker.detect_for_video(image, timestamp_ms)
        return [Hand([(point.x, point.y) for point in hand]) for hand in result.hand_landmarks]
