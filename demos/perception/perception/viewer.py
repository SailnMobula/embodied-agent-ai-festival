from __future__ import annotations

import os

os.environ.setdefault("DO_NOT_TRACK", "1")

import numpy as np
import rerun as rr

from .detection import Detection
from .geometry import Intrinsics
from .pose_estimation import Pose, skeleton_connections
from .segmentation import Segmentation

CAMERA = "world/camera"
IMAGE = "world/camera/image"
BOXES = "world/camera/image/detections"
MASKS = "world/camera/image/masks"
SKELETON = "world/camera/image/pose"
POINTS = "world/points"

_POSE_CLASS = 1
_ACCENT = (70, 220, 255)


def init(title: str, spawn: bool = True, save_path: str | None = None) -> None:
    rr.init(f"perception/{title}")
    if save_path:
        rr.save(save_path)
    elif spawn:
        rr.spawn()


def enable_pose_skeleton(keep: tuple[int, ...] | None = None) -> None:
    rr.log(
        "world",
        rr.AnnotationContext(
            [
                rr.ClassDescription(
                    info=rr.AnnotationInfo(id=_POSE_CLASS, label="pose"),
                    keypoint_connections=skeleton_connections(keep),
                )
            ]
        ),
        static=True,
    )


def set_frame(index: int) -> None:
    rr.set_time("frame", sequence=index)


def log_camera(intrinsics: Intrinsics) -> None:
    rr.log(
        CAMERA,
        rr.Pinhole(
            image_from_camera=intrinsics.matrix(),
            resolution=[intrinsics.width, intrinsics.height],
        ),
    )


def log_image(rgb: np.ndarray) -> None:
    rr.log(IMAGE, rr.Image(rgb))


def log_detections(detections: list[Detection]) -> None:
    rr.log(
        BOXES,
        rr.Boxes2D(
            mins=[[d.x, d.y] for d in detections],
            sizes=[[d.width, d.height] for d in detections],
            labels=[f"{d.label} {d.score:.2f}" for d in detections],
            colors=_ACCENT,
        ),
    )


def log_segmentation(segmentation: Segmentation) -> None:
    rr.log(MASKS, rr.SegmentationImage(segmentation.label_map))


def log_pose(pose: Pose, width: int, height: int, keep: tuple[int, ...] | None = None) -> None:
    indices = range(len(pose.landmarks)) if keep is None else keep
    positions = [[pose.landmarks[i][0] * width, pose.landmarks[i][1] * height] for i in indices]
    rr.log(
        SKELETON,
        rr.Points2D(
            positions,
            class_ids=_POSE_CLASS,
            keypoint_ids=list(indices),
            radii=4.0,
        ),
    )


def clear_pose() -> None:
    rr.log(SKELETON, rr.Clear(recursive=True))


def log_point_cloud(points: np.ndarray, colors: np.ndarray) -> None:
    rr.log(POINTS, rr.Points3D(points, colors=colors, radii=0.004))


def log_located_detections(positions: list[np.ndarray], labels: list[str]) -> None:
    rr.log(
        "world/located",
        rr.Points3D(positions, labels=labels, colors=_ACCENT, radii=0.06, show_labels=True),
    )


def log_status(text: str, alert: bool = False) -> None:
    rr.log("status", rr.TextLog(text, level="WARN" if alert else "INFO"))
