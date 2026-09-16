import pytest

from standard_calc import bound_to_180, is_angle_between


""" Tests for bound_to_180() """


# --- Angles already inside [-180, 180) pass through unchanged ---

def test_bound_basic1():
    assert bound_to_180(0) == 0


def test_bound_positive_inside():
    assert bound_to_180(135) == 135


def test_bound_negative_inside():
    assert bound_to_180(-135) == -135


# --- Angles outside one revolution get wrapped ---

def test_bound_just_over_180():
    assert bound_to_180(200) == -160


def test_bound_just_under_negative_180():
    assert bound_to_180(-200) == 160


def test_bound_multiple_revolutions_positive():
    assert bound_to_180(540) == -180


def test_bound_multiple_revolutions_negative():
    assert bound_to_180(-540) == -180


def test_bound_full_revolution():
    assert bound_to_180(360) == 0


def test_bound_large_input():
    assert bound_to_180(3600) == 0


# --- Interval boundaries: [-180, 180) is closed left, open right ---

def test_bound_left_endpoint_is_kept():
    assert bound_to_180(-180) == -180


def test_bound_right_endpoint_wraps_to_left():
    assert bound_to_180(180) == -180


# --- Return type and float inputs ---

def test_bound_returns_float():
    assert isinstance(bound_to_180(135), float)


def test_bound_float_input():
    assert bound_to_180(200.5) == pytest.approx(-159.5)


# --- Property: the output is always inside the stated interval ---

@pytest.mark.parametrize(
    "angle",
    [0, 1, -1, 179, 180, -180, 181, 359, 360, 361, 540, -540, 1000, -1000, 45.5],
)
def test_bound_output_always_in_range(angle):
    result = bound_to_180(angle)
    assert -180 <= result < 180


# --- Property: bounding an already-bounded angle changes nothing ---

@pytest.mark.parametrize("angle", [0, 90, -90, 200, -200, 540, 1000])
def test_bound_is_idempotent(angle):
    once = bound_to_180(angle)
    assert bound_to_180(once) == once


# --- Property: adding a full revolution does not change the result ---

@pytest.mark.parametrize("angle", [0, 45, -45, 179, 200, -200])
def test_bound_revolution_invariance(angle):
    assert bound_to_180(angle) == bound_to_180(angle + 360)
    assert bound_to_180(angle) == bound_to_180(angle - 360)


""" Tests for is_angle_between() """


# --- Basic cases from the docstring ---

def test_between_basic1():
    assert is_angle_between(0, 1, 2)


def test_between_docstring_true():
    assert is_angle_between(0, 45, 90)


def test_between_docstring_false():
    assert not is_angle_between(45, 90, 270)


# --- Angles outside the arc ---

def test_between_outside_low_side():
    assert not is_angle_between(0, -45, 90)


def test_between_outside_high_side():
    assert not is_angle_between(0, 135, 90)


def test_between_directly_opposite_the_arc():
    assert not is_angle_between(0, 225, 90)


# --- Wrapping across 0 / 360, the case naive comparison gets wrong ---

def test_between_wraps_across_zero():
    assert is_angle_between(350, 0, 10)


def test_between_wraps_across_zero_outside():
    assert not is_angle_between(350, 180, 10)


def test_between_wraps_with_negative_input():
    assert is_angle_between(-10, 0, 10)


def test_between_equivalent_representations():
    # 350 and -10 are the same direction, so the result must match.
    assert is_angle_between(350, 0, 10) == is_angle_between(-10, 0, 10)


# --- Endpoints (inclusive behaviour) ---

def test_between_middle_equals_first_bound():
    assert is_angle_between(0, 0, 90)


def test_between_middle_equals_second_bound():
    assert is_angle_between(0, 90, 90)


# --- Degenerate case: both bounds are the same angle ---

def test_between_identical_bounds_matching_middle():
    assert is_angle_between(45, 45, 45)


def test_between_identical_bounds_other_middle():
    assert not is_angle_between(45, 90, 45)


# --- Property: the bounds are unordered, so swapping them changes nothing ---

@pytest.mark.parametrize(
    "a, m, b",
    [
        (0, 45, 90),
        (45, 90, 270),
        (350, 0, 10),
        (0, 135, 90),
        (-90, -45, 0),
    ],
)
def test_between_is_symmetric_in_its_bounds(a, m, b):
    assert is_angle_between(a, m, b) == is_angle_between(b, m, a)


# --- Property: rotating all three angles together changes nothing ---

@pytest.mark.parametrize("offset", [0, 30, 90, 180, -90, 360, -360, 1000])
def test_between_is_rotation_invariant(offset):
    assert is_angle_between(0 + offset, 45 + offset, 90 + offset)
    assert not is_angle_between(45 + offset, 90 + offset, 270 + offset)


# --- Property: adding a full revolution to any one argument changes nothing ---

@pytest.mark.parametrize(
    "a, m, b",
    [
        (0, 45, 90),
        (45, 90, 270),
        (350, 0, 10),
    ],
)
def test_between_argument_revolution_invariance(a, m, b):
    expected = is_angle_between(a, m, b)
    assert is_angle_between(a + 360, m, b) == expected
    assert is_angle_between(a, m + 360, b) == expected
    assert is_angle_between(a, m, b - 360) == expected
    
