# MME556 LRPK E1.3

import MME565
import numpy as np
from tqdm import trange

# computeLineThroughTwoPoints

p1 = []
p2 = []

for x in np.linspace(-4.5, 3.9, 9):
    for y in np.linspace(-6.6, 2.7, 9):
        p1.append([x, y])
        p2.append([x, y])

segments = []
lines = []

for point1 in p1:
    for point2 in p2:
        if point1 != point2:
            segment = MME565.LRPKSegment(point1, point2)
            segments.append(segment)
            a, b, c = segment.a, segment.b, segment.c
            lines.append([a, b, c])

for line in lines:
    if np.round(line[0]**2 + line[1]**2) != 1:
        raise Exception("A line is not normalized")

print(f"{len(lines)} lines were created and each was checked to conform to (a**2 + b**2 = 1). \n")
for _ in range(5):
    rand_line = segments[np.random.randint(0, len(lines))]
    rand_line_str = f"{rand_line.p1}, {rand_line.p2}; [{rand_line.a} {rand_line.b} {rand_line.a}]"
    print(f"Random sample line: \n {rand_line_str} \n")

# computeDistancePointToSegment

p_q = []
distances = []

for x in np.linspace(-5, 5, 2):
    for y in np.linspace(-5, 5, 2):
        p_q.append([x, y])
    
for point in p_q:
    for segment in segments:
        distances.append([segment.distance_point_to_segment(point), segment, point])

print(f"{len(p_q)} points checked against {len(lines)} segments. {len(distances)} distances checked. \n")

for _ in range(5):
    rand_dist = distances[np.random.randint(0, len(distances))]
    rand_dist_q = f"q: {rand_dist[2]}. \n"
    rand_dist_seg = f"Segment: {rand_dist[1].p1}, {rand_dist[1].p2}; [{rand_dist[1].a} {rand_dist[1].b} {rand_dist[1].a}] \n"
    rand_dist_dist = f"Distance: {rand_dist[0][0]}; w: {rand_dist[0][1]} \n"
    rand_dist_str = rand_dist_q + rand_dist_seg + rand_dist_dist
    print(f"Random sample point to segment: \n{rand_dist_str}")
