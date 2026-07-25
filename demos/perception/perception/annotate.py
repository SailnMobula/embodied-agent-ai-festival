from __future__ import annotations

import colorsys

import cv2
import numpy as np

from .detection import Detection
from .hands import Hand, hand_connections
from .pose_estimation import Pose, skeleton_connections
from .segmentation import Segmentation

ACCENT = (70, 220, 255)
INK = (20, 20, 20)


def draw_detections(rgb: np.ndarray, detections: list[Detection]) -> np.ndarray:
    out = rgb.copy()
    line = max(2, round(rgb.shape[1] / 400))
    for detection in detections:
        top_left = (int(detection.x), int(detection.y))
        bottom_right = (int(detection.x + detection.width), int(detection.y + detection.height))
        cv2.rectangle(out, top_left, bottom_right, ACCENT, line)
        _label(out, f"{detection.label} {detection.score:.2f}", top_left)
    return out


def draw_masks(rgb: np.ndarray, segmentation: Segmentation, alpha: float = 0.5) -> np.ndarray:
    out = rgb.copy()
    line = max(2, round(rgb.shape[1] / 400))
    for instance, colour in zip(segmentation.instances, _palette(len(segmentation.instances))):
        mask = segmentation.label_map == instance.id
        tinted = out.copy()
        tinted[mask] = colour
        out = cv2.addWeighted(tinted, alpha, out, 1 - alpha, 0)
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(out, contours, -1, colour, line)
    return out


def draw_pose(rgb: np.ndarray, pose: Pose, keep: tuple[int, ...] | None = None) -> np.ndarray:
    out = rgb.copy()
    height, width = rgb.shape[:2]
    points = [(int(x * width), int(y * height)) for x, y in pose.landmarks]
    kept = set(range(len(points))) if keep is None else set(keep)

    line = max(2, round(width / 300))
    for a, b in skeleton_connections(None if keep is None else tuple(keep)):
        cv2.line(out, points[a], points[b], ACCENT, line)
    for index in kept:
        cv2.circle(out, points[index], max(3, round(width / 200)), ACCENT, -1)
    return out


def draw_hands(rgb: np.ndarray, hands: list[Hand]) -> np.ndarray:
    out = rgb.copy()
    height, width = rgb.shape[:2]
    connections = hand_connections()
    line = max(2, round(width / 300))
    joint = max(3, round(width / 220))

    for hand in hands:
        points = [(int(x * width), int(y * height)) for x, y in hand.landmarks]
        for a, b in connections:
            cv2.line(out, points[a], points[b], ACCENT, line)
        for point in points:
            cv2.circle(out, point, joint, ACCENT, -1)
    return out


def save(rgb: np.ndarray, path: str, max_width: int = 1600) -> None:
    height, width = rgb.shape[:2]
    if width > max_width:
        scale = max_width / width
        rgb = cv2.resize(rgb, (max_width, round(height * scale)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))


def _label(out: np.ndarray, text: str, origin: tuple[int, int]) -> None:
    scale = max(0.5, out.shape[1] / 1600)
    thickness = max(1, round(scale * 2))
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)
    x, y = origin
    cv2.rectangle(out, (x, y - text_height - 10), (x + text_width + 10, y), ACCENT, -1)
    cv2.putText(out, text, (x + 5, y - 7), cv2.FONT_HERSHEY_SIMPLEX, scale, INK, thickness, cv2.LINE_AA)


def _palette(count: int) -> list[tuple[int, int, int]]:
    return [
        tuple(round(channel * 255) for channel in colorsys.hsv_to_rgb(index / max(count, 1), 0.7, 1.0))
        for index in range(count)
    ]
