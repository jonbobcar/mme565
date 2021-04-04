# E1-6.py

# MME556 LRPK E1.6

import MME565
import numpy as np

# computeLineThroughTwoPoints

p1 = []
p2 = []
random_samples = 3

# construct a list of points to construct lines from
for x in np.linspace(-4.5, 3.9, 5):
    for y in np.linspace(-6.6, 2.7, 5):
        p1.append([x, y])
        p2.append([x, y])

lines = []
lines_abc = []
coincident_points = 0

# construct a list of lines from each of the points to each other point
for point1 in p1:
    for point2 in p2:
        if point1 != point2:
            line = MME565.Line(point1, point2)
            lines.append(line)
            a, b, c = line.a, line.b, line.c
            lines_abc.append([a, b, c])
        else:
            coincident_points += 1

# check each line to see that they are all scaled to
for line in lines_abc:
    if np.round(line[0]**2 + line[1]**2) != 1:
        raise Exception("A line is not normalized")

print(f"{len(lines)} lines were created and each was checked to conform to (a**2 + b**2 = 1).")
print(f"{coincident_points} sets of coincident points ignored. \n")

# generate print statements for (random_samples) sample of computeLineThroughTwoPoints
for _ in range(random_samples):
    rand_line = lines[np.random.randint(0, len(lines))]
    rand_line_str = f"{rand_line.p1}, {rand_line.p2}; [{rand_line.a} {rand_line.b} {rand_line.a}]"
    print(f"Random sample line: \n {rand_line_str} \n")

# computeDistancePointToLine

p_q = []

for x in np.linspace(-4, 4, 10):
    for y in np.linspace(-4, 4, 10):
        p_q.append([x, y])

line_distances = []

for point in p_q:
    for line in lines:
        line_distances.append([line.distance_point_to_line(point), line, point])

print(f"{len(p_q)} points checked against the {len(lines)} lines. {len(line_distances)} distances checked. \n")

# generate print statements for (random_samples) sample of computeDistancePointToLine
for _ in range(random_samples):
    rand_dist = line_distances[np.random.randint(0, len(line_distances))]
    rand_dist_q = f"q: {rand_dist[2]}. \n"
    rand_dist_line = f"Line: {rand_dist[1].p1}, {rand_dist[1].p2}; \n"
    rand_dist_dist = f"Distance: {rand_dist[0]} \n"
    rand_dist_str = rand_dist_q + rand_dist_line + rand_dist_dist
    print(f"Random sample point to line: \n{rand_dist_str}")

# computeDistancePointToSegment

segment_distances = []
segments = []

for line in lines:
    segments.append(MME565.Segment(line.p1, line.p2))
    
for point in p_q:
    for segment in segments:
        segment_distances.append([segment.distance_point_to_segment(point), segment, point])

print(f"{len(p_q)} points checked against the {len(segments)} segments. {len(segment_distances)} distances checked. \n")

# generate print statements for (random_samples) sample of computeDistancePointToSegment
for _ in range(random_samples):
    rand_dist = segment_distances[np.random.randint(0, len(segment_distances))]
    rand_dist_q = f"q: {rand_dist[2]}. \n"
    rand_dist_seg = f"Segment: {rand_dist[1].p1}, {rand_dist[1].p2} \n"
    rand_dist_dist = f"Distance: {rand_dist[0][0]}; w: {rand_dist[0][1]} \n"
    rand_dist_str = rand_dist_q + rand_dist_seg + rand_dist_dist
    print(f"Random sample point to segment: \n{rand_dist_str}")
