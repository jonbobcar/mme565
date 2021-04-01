import E1_6
import matplotlib.pyplot as plt


def compute_distance_point_to_polygon(q, P, debug=False):
    """Computes the minimum distance from point q to polygon P"""

    # Add checks for two polygon points that are the same

    distances = []
    for i in range(len(P)):
        if i == len(P) - 1:
            if debug:
                print("Computing edge: ", i + 1, ": ", P[-1], P[0])
            distances.append(E1_6.compute_distance_point_to_segment(q, P[-1], P[0], debug=debug))
            print(distances)
        else:
            if debug:
                print("Computing edge: ", i + 1, ": ", P[i], P[i+1])
            distances.append(E1_6.compute_distance_point_to_segment(q, P[i], P[i+1], debug=debug))
            print(distances)
    distance = min(distances)

    if debug:
        print("Minimum distance to polygon: ", distance[0])

    return distance


if __name__ == "__main__":
    q = [6, 4]

    # Polygon should be a Numpy Array, not a list of lists.
    P = [
        [1, 1],
        [5, 1],
        [5, 2],
        [9, 3],
        [5, 4],
        [5, 5],
        [1, 5],
    ]
    compute_distance_point_to_polygon(q, P, debug=True)
    # print(E1_6.compute_distance_point_to_segment(q, P[1], P[0]))

    mypoly = P
    poly = plt.Polygon(mypoly, fc="r")
    plt.plot(q[0], q[1], "bo")
    plt.gca().add_patch(poly)
    plt.axis("equal")
    plt.show()
