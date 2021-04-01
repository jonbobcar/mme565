import math
import inspect


def prepare_point(point: list):
    if len(point) != 2:
        raise Exception("One of the provided points was not a 2D Cartesian coordinate")
    for i, n in enumerate(point):
        point[i] = round(n, 8)
    return point


def check_if_segment(p1: list, p2: list):
    p1 = prepare_point(p1)
    p2 = prepare_point(p2)
    if p1[0] == p2[0] and p1[1] == p2[1]:
        raise Exception("Some points are the same, no segment exists between them")


def distance_between_points(p1: list, p2: list, debug=False):
    p1 = prepare_point(p1)
    p2 = prepare_point(p2)
    if debug:
        print("FUNCTION: ", inspect.currentframe().f_code.co_name)  # print function name to console
        print("p1:", p1, "p2:", p2)
        print("Distance between points:", math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def compute_line_through_two_points(p1: list, p2: list, debug=False):
    """Computes a line (Ax + By + C = 0) from two points. Normalizes result such that sqrt(A**2 + B**2) == 1."""

    if debug:
        print("FUNCTION: ", inspect.currentframe().f_code.co_name)  # print function name to console

    p1 = prepare_point(p1)
    p2 = prepare_point(p2)
    check_if_segment(p1, p2)

    if p1[0] == p2[0]:
        a = 1.0
        b = 0
        c = p1[0]
        if debug:
            print(f"A: {a}, B: {b}, C: {c}")
        return a, b, c
    if p1[1] == p2[1]:
        a = 0
        b = 1.0
        c = p1[1]
        if debug:
            print(f"A: {a}, B: {b}, C: {c}")
        return a, b, c

    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])  # line slope calculation (y2 - y1) / (x2 - x1)
    intercept = -slope * p1[0] + p1[1]  # line y-intercept calculation ( b = y - mx )

    # ax + by + c = 0
    a = slope
    b = -1
    c = intercept

    if debug:
        print(f"A: {a}, B: {b}, C: {c}")

    normalizer = math.sqrt(a**2 + b**2)
    a /= normalizer
    b /= normalizer
    c /= normalizer

    if debug:
        print(f"nA: {a}, nB: {b}, nC: {c}")

    return a, b, c


def compute_distance_point_to_line(q: list, p1: list, p2: list, debug=False):
    """Computes the distance from a point (q) to a line defined by two points (p1 & p2)"""

    if debug:
        print("FUNCTION: ", inspect.currentframe().f_code.co_name)  # print function name to console

    prepare_point(q)

    a, b, c = compute_line_through_two_points(p1, p2, debug=False)

    if debug:
        print(f"nA: {a}, nB: {b}, nC: {c}")

    # Check for horizontal and vertical lines. These are a special case and need to be handled differently.
    if p1[0] == p2[0]:
        if debug:
            print("Distance to vertical line:", max([abs(q[0] - p1[0]), abs(q[0] - p2[0])]))
        return max([abs(q[0] - p1[0]), abs(q[0] - p2[0])])
    elif p1[1] == p2[1]:
        if debug:
            print("Distance to horizontal line:", max([abs(q[1] - p1[1]), abs(q[1] - p2[1])]))
        return max([abs(q[1] - p1[1]), abs(q[1] - p2[1])])
    else:
        if debug:
            print("Distance point to line: ", abs(a*q[0] + b*q[1] + c) / math.sqrt(a**2 + b**2))
        return abs(a*q[0] + b*q[1] + c) / math.sqrt(a**2 + b**2)  # denominator is normalized, so always == 1


def compute_distance_point_to_segment(q: list, p1: list, p2: list, debug=False):
    """
    Computes the distance from a point (q) to a line segment defined by two points (p1 & p2) All three must be
    one one plane. Returns the distance from the point to the segment and a value (w) as follows:

    w = 0: orthogonal projection of point is on the segment

    w = 1: orthogonal projection of point is not on the segment and point is closest to p1

    w = 2: orthogonal projection of point is not on the segment and point is closest to p2
    """

    if debug:
        print("FUNCTION: ", inspect.currentframe().f_code.co_name)  # print function name to console

    p1 = prepare_point(p1)
    p2 = prepare_point(p2)
    q = prepare_point(q)
    check_if_segment(p1, p2)
    a, b, c = compute_line_through_two_points(p1, p2, debug=debug)

    if a == 0:
        # compute the intersection to a horizontal line
        intersection = [q[0], b]
        slope = "horizontal"
        ortho_slope = "vertical"
        intercept = b
        ortho_intercept = "none"
    elif b == 0:
        # compute the intersection to a vertical line
        intersection = [a, q[1]]
        slope = "vertical"
        ortho_slope = "horizontal"
        intercept = "none"
        ortho_intercept = a
    else:
        # compute the slope-intercept properties for the segment and orthogonal projection from q to the segment
        slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
        intercept = -slope * p1[0] + p1[1]
        ortho_slope = -1 / slope
        ortho_intercept = -ortho_slope * q[0] + q[1]

        # compute the intersection of the two lines (segment and orthogonal projection from q)
        intersection = [
            (ortho_intercept - intercept) / (slope - ortho_slope),
            (slope * (ortho_intercept - intercept) / (slope - ortho_slope) + intercept)
                    ]
    # compute distances from each important point to each other important point
    q_to_line = compute_distance_point_to_line(q, p1, p2, debug=debug)
    intersection_to_p1 = distance_between_points(intersection, p1, debug=debug)
    intersection_to_p2 = distance_between_points(intersection, p2, debug=debug)
    q_to_p1 = distance_between_points(q, p1, debug=debug)
    q_to_p2 = distance_between_points(q, p2, debug=debug)
    p1_to_p2 = distance_between_points(p1, p2, debug=debug)

    if debug:
        print("Distance q to line: ", q_to_line)
        print("q to p1: ", q_to_p1)
        print("q to p2: ", q_to_p2)
        print("Slope-Intercept: ", slope, "-", intercept)
        print("Ortho Slope-Intercept: ", ortho_slope, "-", ortho_intercept)
        print("Intersection: ", intersection)
        print("Intersection to p1: ", intersection_to_p1)
        print("Intersection to p2: ", intersection_to_p2)
        print("Sum of intersection distances: ", intersection_to_p1 + intersection_to_p2)
        print("p1 to p2: ", p1_to_p2)

    if round(intersection_to_p1 + intersection_to_p2, 8) == round(p1_to_p2, 8):
        if debug:
            print("q to segment, ortho", q_to_line, "0")
        return q_to_line, 0
    elif q_to_p1 < p1_to_p2:
        if debug:
            print("q to p1", q_to_p1, "1")
        return q_to_p1, 1
    else:
        if debug:
            print("q to p2", q_to_p2, "2")
        return q_to_p2, 2


if __name__ == "__main__":
    # point_p1 = [0, 0]
    # point_p2 = [5, 0]

    point_p1 = [9, 3]
    point_p2 = [5, 4]

    point_q = [6, 4]

    compute_line_through_two_points(point_p1, point_p2, debug=True)
    compute_distance_point_to_line(point_q, point_p1, point_p2, debug=True)
    compute_distance_point_to_segment(point_q, point_p1, point_p2, debug=True)
