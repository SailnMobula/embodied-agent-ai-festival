from __future__ import annotations

import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

import cv2
import numpy as np

from .geometry import Intrinsics


@dataclass(frozen=True)
class Frame:
    color_rgb: np.ndarray
    depth_m: np.ndarray | None
    intrinsics: Intrinsics
    timestamp: float

    @property
    def has_depth(self) -> bool:
        return self.depth_m is not None


class FrameSource(ABC):
    def __enter__(self) -> "FrameSource":
        self.start()
        return self

    def __exit__(self, *_exc) -> None:
        self.stop()

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def read(self) -> Frame | None: ...

    def frames(self):
        while True:
            frame = self.read()
            if frame is None:
                return
            yield frame


class RealSenseSource(FrameSource):
    def __init__(
        self,
        width: int = 640,
        height: int = 480,
        fps: int = 30,
        bag_path: str | None = None,
        warmup_frames: int = 30,
        max_depth_m: float = 4.0,
    ):
        self._width = width
        self._height = height
        self._fps = fps
        self._bag_path = bag_path
        self._warmup_frames = warmup_frames
        self._max_depth_m = max_depth_m
        self._pipeline = None
        self._align = None
        self._depth_scale = 1.0
        self._intrinsics: Intrinsics | None = None

    def start(self) -> None:
        import pyrealsense2 as rs

        if self._bag_path is None and sys.platform == "darwin":
            print(
                "Live RealSense on macOS is unreliable and can crash the process. "
                "If this hangs or segfaults, rehearse with --webcam 0, or record a .bag and pass --bag <file>.",
                file=sys.stderr,
            )

        pipeline, config = rs.pipeline(), rs.config()
        if self._bag_path:
            config.enable_device_from_file(self._bag_path, repeat_playback=True)
        else:
            config.enable_stream(rs.stream.depth, self._width, self._height, rs.format.z16, self._fps)
            config.enable_stream(rs.stream.color, self._width, self._height, rs.format.bgr8, self._fps)

        profile = pipeline.start(config)
        if self._bag_path:
            profile.get_device().as_playback().set_real_time(True)

        self._depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
        self._align = rs.align(rs.stream.color)
        self._pipeline = pipeline

        for _ in range(self._warmup_frames):
            self._pipeline.wait_for_frames()

    def stop(self) -> None:
        if self._pipeline is not None:
            self._pipeline.stop()
            self._pipeline = None

    def read(self) -> Frame | None:
        frames = self._align.process(self._pipeline.wait_for_frames())
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            return None

        color_bgr = np.asanyarray(color_frame.get_data())
        depth_raw = np.asanyarray(depth_frame.get_data()).astype(np.float32)
        depth_m = depth_raw * self._depth_scale
        depth_m[depth_m > self._max_depth_m] = 0.0

        return Frame(
            color_rgb=cv2.cvtColor(color_bgr, cv2.COLOR_BGR2RGB),
            depth_m=depth_m,
            intrinsics=self._read_intrinsics(color_frame),
            timestamp=time.monotonic(),
        )

    def _read_intrinsics(self, color_frame) -> Intrinsics:
        if self._intrinsics is None:
            intr = color_frame.profile.as_video_stream_profile().intrinsics
            self._intrinsics = Intrinsics(
                fx=intr.fx, fy=intr.fy, cx=intr.ppx, cy=intr.ppy, width=intr.width, height=intr.height
            )
        return self._intrinsics


class WebcamSource(FrameSource):
    def __init__(self, index: int = 0, width: int = 640, height: int = 480):
        self._index = index
        self._width = width
        self._height = height
        self._capture = None
        self._intrinsics = estimated_intrinsics(width, height)

    def start(self) -> None:
        self._capture = cv2.VideoCapture(self._index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
        if not self._capture.isOpened():
            raise RuntimeError(f"Could not open webcam {self._index}")

    def stop(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def read(self) -> Frame | None:
        ok, color_bgr = self._capture.read()
        if not ok:
            return None
        return Frame(
            color_rgb=cv2.cvtColor(color_bgr, cv2.COLOR_BGR2RGB),
            depth_m=None,
            intrinsics=self._intrinsics,
            timestamp=time.monotonic(),
        )


def estimated_intrinsics(width: int, height: int, horizontal_fov_degrees: float = 60.0) -> Intrinsics:
    focal = width / (2.0 * np.tan(np.radians(horizontal_fov_degrees) / 2.0))
    return Intrinsics(fx=focal, fy=focal, cx=width / 2.0, cy=height / 2.0, width=width, height=height)
