import numpy as np
import matplotlib.path as mpltpath
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


class LRPKPoint:
    """Creates a point from a pair of 2D Cartesian coordinates and rounds them to 8 decimal places."""
    def __init__(self, coordinates):
        if len(coordinates) != 2:
            raise Exception("Some point is not a 2D Cartesian coordinate")
        self.x = np.round(coordinates[0], 8)
        self.y = np.round(coordinates[1], 8)
        self.cartesian = [self.x, self.y]

    def __str__(self):
        return f"({self.x}, {self.y})"


class LRPKSegment:
    """Create segments from two provided points, p1 and p2. LRPKPoints must be 2D cartesian coordinates."""
    def __init__(self, p1: LRPKPoint, p2: LRPKPoint):
        if type(p1) != LRPKPoint:
            self.p1 = LRPKPoint(p1)
        else:
            self.p1 = p1
        if type(p2) != LRPKPoint:
            self.p2 = LRPKPoint(p2)
        else:
            self.p2 = p2

        if self.p1.x == self.p2.x and self.p1.y == self.p2.y:
            raise Exception("Some points are the same, no segment exists between them")

        self.length = np.sqrt((self.p1.x - self.p2.x)**2 + (self.p1.y - self.p2.y)**2)

        # x coordinates of p1 and p2 are equal (vertical segment): undefined slope
        if self.p1.x == self.p2.x:
            self.slope = np.nan
            self.intercept = np.nan
            self.a = 1.0
            self.b = 0
            self.c = self.p1.x
        else:
            # y = (slope * x) + intercept
            # equation of line collinear with the segment
            self.slope = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
            self.intercept = -self.slope * self.p1.x + self.p1.y

            # ax + by + c = 0
            # equation of line collinear with the segment
            self.a = -self.slope
            self.b = 1
            self.c = -self.intercept

            # scale the vector of the line such that sqrt(a**2 + b**2) == 1
            normalizer = np.sqrt(self.a**2 + self.b**2)
            self.a /= normalizer
            self.b /= normalizer
            self.c /= normalizer

    def distance_point_to_segment(self, q: LRPKPoint):
        """
        Computes the distance from a point (q) to a line segment defined by two points (p1 & p2) All three must be
        one one plane. Returns the distance from the point to the segment and a value (w) as follows:

        w = 0: orthogonal projection of point is on the segment

        w = 1: orthogonal projection of point is not on the segment and point is closest to p1

        w = 2: orthogonal projection of point is not on the segment and point is closest to p2
        """

        if type(q) != LRPKPoint:
            q = LRPKPoint(q)

        if self.a == 0:  # horizontal line
            intersection = LRPKPoint([q.x, self.c])
            ortho_slope = np.nan
            ortho_intercept = self.c
            q_to_line = max([abs(q.y - self.p1.y), abs(q.y - self.p2.y)])
        elif self.b == 0:  # vertical line
            intersection = LRPKPoint([self.c, q.y])
            ortho_slope = 0
            ortho_intercept = np.nan
            q_to_line = max([abs(q.x - self.p1.x), abs(q.x - self.p2.x)])
        else:
            ortho_slope = -1 / self.slope
            ortho_intercept = -ortho_slope * q.x + q.y
            intersection = LRPKPoint([
                (ortho_intercept - self.intercept) / (self.slope - ortho_slope),
                self.slope * (ortho_intercept - self.intercept) / (self.slope - ortho_slope) + self.intercept
            ])
            q_to_line = abs(self.a*q.x + self.b*q.y + self.c) / np.sqrt(self.a**2 + self.b**2)

        p1_to_p2 = np.round(distance_between_points(self.p1, self.p2), 8)
        intersection_to_p1 = np.round(distance_between_points(intersection, self.p1), 8)
        intersection_to_p2 = np.round(distance_between_points(intersection, self.p2), 8)
        q_to_p1 = np.round(distance_between_points(q, self.p1), 8)
        q_to_p2 = np.round(distance_between_points(q, self.p2), 8)

        if np.round((intersection_to_p1 + intersection_to_p2), 8) == np.round(p1_to_p2, 8):
            return q_to_line, 0 
        elif q_to_p1 < p1_to_p2:
            return q_to_p1, 1
        else:
            return q_to_p2, 2

    def __str__(self):
        return f"LRPKSegment with endpoints {self.p1} and {self.p2} and length {round(self.length,4)}"

    def __repr__(self):
        return f"MME565.LRPKSegment({self.p1}, {self.p2})"


class LRPKPolygon:
    """Creates a polygon from a list of 2D Cartesian coordinates."""
    def __init__(self, vertices):
        # check points for 2d cartesian-ness
        for vertex in vertices:
            if len(vertex) != 2:
                raise Exception("One of the provided polygon vertices was not a 2D Cartesian coordinate")

        # build a list of LRPKSegment objects from adjacent pairs of vertices
        for vertex in range(len(vertices)):
            if vertex == len(vertices) - 1:
                self.segments.append(LRPKSegment(self.vertices[-1], self.vertices[0]))
            else:
                self.segments.append(LRPKSegment(self.vertices[vertex], self.vertices[vertex + 1]))

        # if type(vertices[0]) == list:
        #     self.segments = []
        #     for vertex in range(len(vertices)):
        #         if vertex == len(vertices) - 1:
        #             self.segments.append(LRPKSegment(LRPKPoint(self.vertices[-1]), LRPKPoint(self.vertices[0])))
        #         else:
        #             self.segments.append(LRPKSegment(LRPKPoint(self.vertices[vertex]), LRPKPoint(self.vertices[vertex + 1])))
        # elif type(vertices[0]) == LRPKPoint:
        #     self.segments = []
        #     for vertex in range(len(vertices)):
        #         if vertex == len(vertices) - 1:
        #             self.segments.append(LRPKSegment(self.vertices[-1], self.vertices[0]))
        #         else:
        #             self.segments.append(LRPKSegment(self.vertices[vertex], self.vertices[vertex + 1]))
        # else:
        #     raise Exception("LRPKPolygon vertices not a list of lists or a list of LRPKPoints")

    def distance_point_to_polygon(self, q: LRPKPoint):
        distances = []
        for segment in self.segments:
            distances.append(segment.distance_point_to_segment(q))
        return min(distances)

    def check_point_inside_polygon(self, q: LRPKPoint):
        # uses matplotlib.path.Path method
        # if I have time I will build a custom method that isn't so opaque
        path = mpltpath.Path(self.vertices)
        inside = path.contains_point([q.x, q.y])
        return inside

    def __str__(self):
        return f"A polygon with {len(self.segments)} segments and centered at [maybe calculate COM of polygon?]"

    def __repr__(self):
        pass


def distance_between_points(p1: LRPKPoint, p2: LRPKPoint):
    """Computes the distance between two provided LRPKPoint objects"""
    if type(p1) != LRPKPoint:
        p1 = LRPKPoint(p1)
    if type(p2) != LRPKPoint:
        p2 = LRPKPoint(p2)
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def show_polygon(polygon: LRPKPolygon, q: LRPKPoint):
    fig, ax = plt.subplots()
    patches = [mpatches.Polygon(polygon.vertices)]
    colors = np.linspace(0, 1, 1)
    collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
    collection.set_array(colors)
    ax.add_collection(collection)
    for point in q:
        if polygon.check_point_inside_polygon(point):
            plt.plot(point.x, point.y, "bo")
        else:
            plt.plot(point.x, point.y, "rx")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def show_distance_to_segment(segment: LRPKSegment, q: LRPKPoint):
    fig, ax = plt.subplots()
    plt.plot(q.x, q.y, "rx")
    fig.add_artist(mlines.Line2D(segment.p1.cartesian, segment.p2.cartesian))
    plt.show()


if __name__ == "__main__":
    point1 = LRPKPoint([1, 1])
    point2 = LRPKPoint([2, 2])
    polygon1 = LRPKPolygon([
        [1, 1],
        [5, 0],
        [5, 2.5],
        [9, 3.6],
        [5, 4],
        [8, 8],
        [1, 5],
    ])

    point_q = LRPKPoint([5.2345, 4.5])



    # print(polygon1)

    print(polygon1.distance_point_to_polygon(point_q))


    seggy = LRPKSegment(point1, point2)
    # dist, w = seggy.distance_point_to_segment(point_q)
    # print(seggy.a, seggy.b, seggy.c)
    # print(dist, w)

    # print(seggy.p1.x)

    show_polygon(polygon1, points)
    # show_distance_to_segment(seggy, point_q)