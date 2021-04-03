# MME565 LRPK E1.7

import MME565
import numpy as np

random_samples = 5

# computeDistanceToPolygon

polygon_vertices = [
        [1, 1],
        [5, 0],
        [5, 2.5],
        [9, 3.6],
        [5, 4],
        [8, 8],
        [1, 5],
    ]

polygon = MME565.Polygon(polygon_vertices)

p_q = []

for x in np.linspace(0, 9, 25):
    for y in np.linspace(0, 9, 25):
        p_q.append([x, y])

# computeDistancePointToPolygon

distances = []

for point in p_q:
    distances.append([polygon.distance_point_to_polygon(point), point])

print(distances[-1])

print(f"{len(p_q)} points checked against {polygon.num_sides} polygon segments.")

for _ in range(random_samples):
    rand_dist = distances[np.random.randint(0, len(distances))]
    rand_dist_dist = f"Distance: {rand_dist[0][0][0]} \n"
    rand_dist_q = f"q: {rand_dist[1]}. \n"
    rand_dist_seg = f"{rand_dist[0][1]}"
    rand_dist_str = rand_dist_dist + rand_dist_q + rand_dist_seg
    print(f"Random sample point to polygon: \n{rand_dist_str} \n")


MME565.show_polygon(polygon, p_q)
