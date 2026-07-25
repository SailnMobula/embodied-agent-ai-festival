from perception.wave import WaveDetector, count_direction_changes, wrist_is_raised

SHOULDER_LOW = [(0.0, 0.5)] * 33


def landmarks_with_right_wrist(x: float, y: float) -> list[tuple[float, float]]:
    points = [(0.0, 0.5)] * 33
    points[12] = (0.6, 0.4)
    points[16] = (x, y)
    return points


def test_wrist_raised_when_above_shoulder():
    points = landmarks_with_right_wrist(x=0.6, y=0.2)
    assert wrist_is_raised(points, 16, 12)


def test_wrist_not_raised_when_below_shoulder():
    points = landmarks_with_right_wrist(x=0.6, y=0.7)
    assert not wrist_is_raised(points, 16, 12)


def test_count_direction_changes_ignores_jitter():
    values = [0.5, 0.505, 0.498, 0.5]
    assert count_direction_changes(values, min_travel=0.03) == 0


def test_count_direction_changes_counts_swings():
    values = [0.4, 0.6, 0.4, 0.6]
    assert count_direction_changes(values, min_travel=0.03) == 3


def test_raised_but_still_is_not_waving():
    detector = WaveDetector()
    state = detector.update(0.0, landmarks_with_right_wrist(x=0.6, y=0.2))
    assert state.wrist_raised
    assert not state.is_waving


def test_oscillating_raised_wrist_is_waving():
    detector = WaveDetector(min_oscillations=3)
    xs = [0.45, 0.6, 0.45, 0.6, 0.45]
    state = None
    for index, x in enumerate(xs):
        state = detector.update(index * 0.1, landmarks_with_right_wrist(x=x, y=0.2))
    assert state.is_waving


def test_dropping_the_arm_clears_history():
    detector = WaveDetector(min_oscillations=3)
    for index, x in enumerate([0.45, 0.6, 0.45, 0.6]):
        detector.update(index * 0.1, landmarks_with_right_wrist(x=x, y=0.2))
    state = detector.update(0.5, landmarks_with_right_wrist(x=0.6, y=0.8))
    assert not state.is_waving
    assert not state.wrist_raised
