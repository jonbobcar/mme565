# E2-9.py

# MME565 LRPK E2.9

import MME565
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


polygon_vertices = [
    [8, 1],
    [15, 3.5],
    [10, 4],
    [11, 7],
    [7, 5],
    [3, 7],
    [5, 3],
    [1, 2],
    ]

polygon = MME565.Polygon(polygon_vertices)


fig, ax = plt.subplots()
patches = [mpatches.Polygon(polygon.vertex_array)]
colors = np.linspace(0, 1, 1)
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
collection.set_array(colors)
ax.add_collection(collection)
for vertex in polygon.vertices:
    if vertex.convex:
        ax.annotate("convex", (vertex.x, vertex.y))
    else:
        ax.annotate("non-convex", (vertex.x, vertex.y))
plt.axis('equal')
plt.tight_layout()
plt.show()
