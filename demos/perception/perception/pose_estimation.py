from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

os.environ.setdefault("GLOG_minloglevel", "2")

DEFAULT_MODEL = Path(__file__).resolve().parent.parent / "models" / "pose_landmarker_lite.task"

UPPER_BODY_LANDMARKS = (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24)
ARM_LANDMARKS = (11, 12, 13, 14, 15, 16)


@dataclass(frozen=True)
class Pose:
    landmarks: list[tuple[float, float]]
    visibilities: list[float]


def skeleton_connections(keep: tuple[int, ...] | None = None) -> list[tuple[int, int]]:
    from mediapipe.tasks.python import vision

    connections = [(c.start, c.end) for c in vision.PoseLandmarksConnections.POSE_LANDMARKS]
    if keep is None:
        return connections
    kept = set(keep)
    return [(a, b) for a, b in connections if a in kept and b in kept]


class PoseEstimator:
    def __init__(self, model_path: Path = DEFAULT_MODEL, min_confidence: float = 0.5):
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision

        options = vision.PoseLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(model_path)),
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=min_confidence,
            min_tracking_confidence=min_confidence,
        )
        self._mp = mp
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        self._last_timestamp_ms = -1

    def estimate(self, rgb: np.ndarray, timestamp_seconds: float) -> Pose | None:
        timestamp_ms = max(self._last_timestamp_ms + 1, int(timestamp_seconds * 1000))
        self._last_timestamp_ms = timestamp_ms

        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
        result = self._landmarker.detect_for_video(image, timestamp_ms)
        if not result.pose_landmarks:
            return None

        landmarks = result.pose_landmarks[0]
        return Pose(
            landmarks=[(point.x, point.y) for point in landmarks],
            visibilities=[point.visibility for point in landmarks],
        )
