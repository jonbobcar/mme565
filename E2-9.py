# E2-9.py

# MME565 LRPK E2.9

import MME565
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


polygon_vertices = [
    [18, 11],
    [25, 13.5],
    [20, 14],
    [21, 17],
    [17, 15],
    [13, 17],
    [15, 13],
    [11, 12],
    ]

free_workspace_vertices = [
    [7, 8],
    [30, 8],
    [30, 20],
    [7, 20]
]

polygon = MME565.Polygon(polygon_vertices)
free_workspace = MME565.Polygon(free_workspace_vertices)

trapezoids = MME565.trapezoidation(free_workspace, [polygon])
print(trapezoids[0].vertex_array)

# plot convex / non-convex vertices
fig, ax = plt.subplots()
patches = [mpatches.Polygon(polygon.vertex_array), mpatches.Polygon(free_workspace.vertex_array)]
colors = np.linspace(0, 1, 9)
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

# plot vertex coordinates
fig, ax = plt.subplots()
patches = [mpatches.Polygon(polygon.vertex_array), mpatches.Polygon(free_workspace.vertex_array)]
colors = np.linspace(0, 1, 9)
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
collection.set_array(colors)
ax.add_collection(collection)
for vertex in polygon.vertices:
    ax.annotate(vertex.cartesian, (vertex.x, vertex.y))
for vertex in free_workspace.vertices:
    ax.annotate(vertex.cartesian, (vertex.x, vertex.y))
plt.axis('equal')
plt.tight_layout()

# plot vertex type
fig, ax = plt.subplots()
patches = [mpatches.Polygon(polygon.vertex_array), mpatches.Polygon(free_workspace.vertex_array)]
colors = np.linspace(0, 1, 9)
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
collection.set_array(colors)
ax.add_collection(collection)
for vertex in polygon.vertices:
    ax.annotate(vertex.type, (vertex.x, vertex.y))
plt.axis('equal')
plt.tight_layout()

# plot trapezoidation
fig, ax = plt.subplots()
patches = [
    mpatches.Polygon(polygon.vertex_array),
    mpatches.Polygon(free_workspace.vertex_array),
    ]
for trapezoid in trapezoids:
    patches.append(mpatches.Polygon(trapezoid.vertex_array))
colors = np.linspace(0, 1, 9)
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
collection.set_array(colors)
ax.add_collection(collection)
for trapezoid in trapezoids:
    ax.annotate(trapezoid.center_cartesian, (trapezoid.center.x, trapezoid.center.y))
plt.axis('equal')
plt.tight_layout()
plt.show()
