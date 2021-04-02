# MME556 LRPK E1.3

import MME565
import numpy as np

# computeLineThroughTwoPoints

p1 = []
p2 = []

for x in np.linspace(0, 10, 10):
    for y in np.linspace(0, 10, 10):
        p1.append([x, y])
        p2.append([x, y])

lines = []

for point1 in p1:
    for point2 in p2:
        if point1 != point2:
            segment = MME565.LRPKSegment(point1, point2)
            a, b, c = segment.a, segment.b, segment.c
            lines.append([a, b, c])

for line in lines:
    if np.round(np.sqrt(line[0]**2 + line[1]**2)) != 1:
        raise Exception("A line is not normalized")

print(f"{len(lines)} lines were created and checked")
