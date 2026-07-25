import numpy as np

from perception.geometry import Intrinsics, locate_in_3d, median_depth_in_box, pixel_to_point, point_cloud

INTR = Intrinsics(fx=600.0, fy=600.0, cx=320.0, cy=240.0, width=640, height=480)


def test_principal_point_maps_straight_ahead():
    point = pixel_to_point(INTR.cx, INTR.cy, depth_meters=2.0, intr=INTR)
    assert np.allclose(point, [0.0, 0.0, 2.0])


def test_pixel_right_of_centre_has_positive_x():
    point = pixel_to_point(INTR.cx + 60, INTR.cy, depth_meters=1.0, intr=INTR)
    assert point[0] > 0
    assert point[2] == 1.0


def test_point_cloud_drops_zero_and_far_depth():
    depth = np.full((INTR.height, INTR.width), 2.0, dtype=np.float32)
    depth[0, 0] = 0.0
    depth[0, 1] = 99.0
    colors = np.zeros((INTR.height, INTR.width, 3), dtype=np.uint8)

    points, kept_colors = point_cloud(depth, colors, INTR, max_depth=4.0)

    assert len(points) == INTR.width * INTR.height - 2
    assert len(kept_colors) == len(points)


def test_median_depth_ignores_holes():
    depth = np.full((INTR.height, INTR.width), 2.5, dtype=np.float32)
    depth[250:260, 330:340] = 0.0
    assert median_depth_in_box(depth, 320, 240, 40, 40) == 2.5


def test_locate_in_3d_returns_none_without_depth():
    depth = np.zeros((INTR.height, INTR.width), dtype=np.float32)
    assert locate_in_3d(320, 240, 40, 40, depth, INTR) is None


def test_locate_in_3d_places_centred_box_straight_ahead():
    depth = np.full((INTR.height, INTR.width), 3.0, dtype=np.float32)
    point = locate_in_3d(INTR.cx - 20, INTR.cy - 20, 40, 40, depth, INTR)
    assert np.allclose(point, [0.0, 0.0, 3.0])
