def bound_to_180(angle):
    """Bounds the provided angle to [-180, 180) degrees.

    e.g.)
        bound_to_180(135) = 135.0
        bound_to_180(200) = -160.0

    Args:
        angle (float): The input angle in degrees.

    Returns:
        float: The bounded angle in degrees. Note that both 180 and -180
            map to -180, since the interval is open on the right.
    """
    return float((angle + 180.0) % 360.0 - 180.0)


def is_angle_between(bound_a, middle_angle, bound_b):
    """Determines whether an angle lies on the minor arc between two others.

    The two bounding angles are unordered: swapping them does not change
    the result. When the bounds are exactly 180 degrees apart, neither arc
    is shorter and the result depends on argument order.

    e.g.)
        is_angle_between(0, 45, 90) = True
        is_angle_between(45, 90, 270) = False

    Args:
        bound_a (float): One bounding angle in degrees.
        middle_angle (float): The angle in question in degrees.
        bound_b (float): The other bounding angle in degrees.

    Returns:
        bool: True when `middle_angle` is not in the reflex angle of
            `bound_a` and `bound_b`, False otherwise.
    """
    sweep = bound_to_180(bound_b - bound_a)
    offset = bound_to_180(middle_angle - bound_a)

    if sweep >= 0:
        return 0 <= offset <= sweep
    else:
        return sweep <= offset <= 0
    
