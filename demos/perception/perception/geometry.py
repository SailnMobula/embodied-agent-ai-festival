from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Intrinsics:
    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int

    def matrix(self) -> np.ndarray:
        return np.array(
            [[self.fx, 0.0, self.cx], [0.0, self.fy, self.cy], [0.0, 0.0, 1.0]],
            dtype=np.float32,
        )


def pixel_to_point(u: float, v: float, depth_meters: float, intr: Intrinsics) -> np.ndarray:
    x = (u - intr.cx) / intr.fx * depth_meters
    y = (v - intr.cy) / intr.fy * depth_meters
    return np.array([x, y, depth_meters], dtype=np.float32)


def median_depth_in_box(depth_meters: np.ndarray, x: float, y: float, width: float, height: float) -> float:
    region = depth_meters[int(y) : int(y + height), int(x) : int(x + width)]
    valid = region[region > 0]
    return float(np.median(valid)) if valid.size else 0.0


def locate_in_3d(
    x: float, y: float, width: float, height: float, depth_meters: np.ndarray, intr: Intrinsics
) -> np.ndarray | None:
    z = median_depth_in_box(depth_meters, x, y, width, height)
    if z <= 0:
        return None
    return pixel_to_point(x + width / 2.0, y + height / 2.0, z, intr)


def point_cloud(
    depth_meters: np.ndarray,
    colors_rgb: np.ndarray,
    intr: Intrinsics,
    max_depth: float = 4.0,
) -> tuple[np.ndarray, np.ndarray]:
    us, vs = np.meshgrid(np.arange(intr.width), np.arange(intr.height))
    z = depth_meters
    x = (us - intr.cx) / intr.fx * z
    y = (vs - intr.cy) / intr.fy * z

    points = np.stack([x, y, z], axis=-1).reshape(-1, 3).astype(np.float32)
    colors = colors_rgb.reshape(-1, 3)

    keep = (z.reshape(-1) > 0) & (z.reshape(-1) < max_depth)
    return points[keep], colors[keep]
