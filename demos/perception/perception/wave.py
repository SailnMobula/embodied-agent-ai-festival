from __future__ import annotations

from collections import deque
from dataclasses import dataclass

RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
RIGHT_WRIST = 16
LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15

Landmark = tuple[float, float]


@dataclass(frozen=True)
class WaveState:
    is_waving: bool
    wrist_raised: bool
    oscillations: int
    x_norm: float | None = None


def wrist_is_raised(landmarks: list[Landmark], wrist: int, shoulder: int) -> bool:
    return landmarks[wrist][1] < landmarks[shoulder][1]


def count_direction_changes(values: list[float], min_travel: float) -> int:
    changes = 0
    direction = 0
    last_extreme = values[0] if values else 0.0

    for value in values:
        if value - last_extreme > min_travel:
            if direction <= 0:
                changes += 1
            direction = 1
            last_extreme = value
        elif last_extreme - value > min_travel:
            if direction >= 0:
                changes += 1
            direction = -1
            last_extreme = value

    return changes


class WaveDetector:
    def __init__(self, window_seconds: float = 1.2, min_oscillations: int = 3, min_travel: float = 0.03):
        self._window_seconds = window_seconds
        self._min_oscillations = min_oscillations
        self._min_travel = min_travel
        self._history: deque[tuple[float, float]] = deque()

    def update(self, timestamp: float, landmarks: list[Landmark]) -> WaveState:
        raised = self._raised_side(landmarks)
        if raised is None:
            self._history.clear()
            return WaveState(is_waving=False, wrist_raised=False, oscillations=0)

        wrist_x = landmarks[raised][0]
        self._history.append((timestamp, wrist_x))
        self._forget_older_than(timestamp)

        oscillations = count_direction_changes(
            [x for _, x in self._history], self._min_travel
        )
        return WaveState(
            is_waving=oscillations >= self._min_oscillations,
            wrist_raised=True,
            oscillations=oscillations,
            x_norm=wrist_x,
        )

    def _raised_side(self, landmarks: list[Landmark]) -> int | None:
        if wrist_is_raised(landmarks, RIGHT_WRIST, RIGHT_SHOULDER):
            return RIGHT_WRIST
        if wrist_is_raised(landmarks, LEFT_WRIST, LEFT_SHOULDER):
            return LEFT_WRIST
        return None

    def _forget_older_than(self, now: float) -> None:
        while self._history and now - self._history[0][0] > self._window_seconds:
            self._history.popleft()
