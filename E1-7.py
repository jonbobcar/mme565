# MME565 LRPK E1.7

import MME565
import numpy as np

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

star_vertices = [
    [2, 2],
    [4, 7],
    [6, 2],
    [1, 5],
    [7, 5],
]

point_test = []

for point in star_vertices:
    point_test.append(MME565.Point(point))

polygon = MME565.Polygon(point_test)

points = []
for _ in range(1000):
    points.append(MME565.Point([np.random.random() * 10, np.random.random() * 10]))

distances = []

for point in points:
    if polygon.check_point_inside_polygon(point):
        distances.append([0, "point inside polygon"])
    else:
        distances.append([polygon.distance_point_to_polygon(point), None])

MME565.show_polygon(polygon, points)
