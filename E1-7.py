# E1-7.py

# MME565 LRPK E1.7

import MME565
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

random_samples = 5

# computeDistanceToPolygon

polygon_vertices = [
        [1, 1],
        [5, 0],
        [5, 2.5],
        [9, 3.6],
        [5, 4],
        [8, 7],
        [9, 7],
        [9, 8.5],
        [6, 8.5],
        [7, 8],
        [1, 7],
        [3, 4],
    ]

polygon = MME565.Polygon(polygon_vertices)

p_q = []
p_q_rand = []

num_rand_points = 250

for point in range(num_rand_points):
    p_q_rand.append([np.random.random() * 10, np.random.random() * 10])

for x in np.linspace(0, 10, 16):
    for y in np.linspace(0, 10, 16):
        p_q.append([x, y])

# computeDistancePointToPolygon

distances = []
rand_distances = []

for point in p_q:
    distances.append([polygon.distance_point_to_polygon(point), point])

for point in p_q_rand:
    rand_distances.append([polygon.distance_point_to_polygon(point), point])

print(f"{len(p_q)} points checked against {polygon.num_sides} polygon segments. \n")

for _ in range(random_samples):
    rand_dist = distances[np.random.randint(0, len(distances))]
    rand_dist_dist = f"Distance: {rand_dist[0][0][0]} \n"
    rand_dist_q = f"q: {rand_dist[1]}. \n"
    rand_dist_seg = f"{rand_dist[0][1]}"
    rand_dist_str = rand_dist_dist + rand_dist_q + rand_dist_seg
    print(f"Random sample point to polygon: \n{rand_dist_str} \n")

vectors = []
tangent_vectors = []

rand_vectors = []
rand_tangent_vectors = []

for point in range(len(distances)):
    vectors.append([distances[point][0][1].vector_point_to_segment(distances[point][1]), distances[point][1]])
    tangent_vectors.append([distances[point][0][1].tangent_vector_point_to_segment(distances[point][1]), distances[point][1]])

for i, point in enumerate(rand_distances):
    rand_vectors.append([rand_distances[i][0][1].vector_point_to_segment(rand_distances[i][1]), rand_distances[i][1]])
    rand_tangent_vectors.append([rand_distances[i][0][1].tangent_vector_point_to_segment(rand_distances[i][1]), rand_distances[i][1]])


# MME565.show_polygon(polygon, p_q)

# fig, ax = plt.subplots()
# patches = [mpatches.Polygon(polygon.vertex_array)]
# colors = np.linspace(0, 1, 1)
# collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
# collection.set_array(colors)
# ax.add_collection(collection)
# i = 0
# if type(p_q[0]) != list:
#     q = [p_q]
# for point in p_q:
#     if type(point) != MME565.Point:
#         point = MME565.Point(point)
#     if polygon.check_point_inside_polygon(point):
#         plt.plot(point.x, point.y, "bo")
#     else:
#         plt.plot(point.x, point.y, "rx")
#         q = ax.quiver(vectors[i][1][0], vectors[i][1][1], vectors[i][0].x, vectors[i][0].y)
#     i += 1
# plt.axis('equal')
# plt.tight_layout()
# plt.show()



fig, ax = plt.subplots()
patches = [mpatches.Polygon(polygon.vertex_array)]
colors = np.linspace(0, 1, 1)
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
collection.set_array(colors)
ax.add_collection(collection)
i = 0
if type(p_q[0]) != list:
    q = [p_q]
for point in p_q:
    if type(point) != MME565.Point:
        point = MME565.Point(point)
    if polygon.check_point_inside_polygon(point):
        plt.plot(point.x, point.y, "bo")
    else:
        plt.plot(point.x, point.y, "rx")
        q = ax.quiver(tangent_vectors[i][1][0],tangent_vectors[i][1][1], tangent_vectors[i][0].x, tangent_vectors[i][0].y)
    i += 1
plt.axis('equal')
plt.tight_layout()
plt.show()
