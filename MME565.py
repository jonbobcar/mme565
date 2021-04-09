# MME565.py

import numpy as np
import matplotlib.path as mpltpath
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from math import atan2


class Point:
    """Creates a point from a pair of 2D Cartesian coordinates and rounds them to 8 decimal places."""
    def __init__(self, x: float, y: float):
        self.x = np.round(x, 8)
        self.y = np.round(y, 8)
        self.cartesian = [x, y]

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"MME565.Point({self.x}, {self.y})"


class Vertex:
    """Vertex of a polygon"""
    def __init__(self, x: float, y: float):
        self.x = np.round(x, 8)
        self.y = np.round(y, 8)
        self.cartesian = [self.x, self.y]

        self.convex = None

    def convex_test(self, p_prev, p_next):
        """Checks for polygon vertex convexity. p_next and p_prev must be in the same order as the polygon
        vertex array."""
        leading_vector = Vector([self.x, self.y], p_next.cartesian)
        trailing_vector = Vector([self.x, self.y], p_prev.cartesian)
        lead_angle = atan2(leading_vector.y, leading_vector.x)
        trail_angle = atan2(trailing_vector.y, trailing_vector.x)
        angle_between = trail_angle - lead_angle
        if angle_between < 0:
            angle_between += 2 * np.pi
        if 0 < angle_between < np.pi:
            self.convex = True
        else:
            self.convex = False

        return self.convex

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"MME565.Vertex({self.x}, {self.y})"


class Vector:
    def __init__(self, p1: Point, p2: Point):
        if type(p1) not in [Point, Vertex]:
            p1 = Point(p1[0], p1[1])
        else:
            p1 = p1
        if type(p2) not in [Point, Vertex]:
            p2 = Point(p2[0], p2[1])
        else:
            p2 = p2

        self.x = p2.x - p1.x
        self.y = p2.y - p1.y

        self.vector = [self.x, self.y]

        # convert to unit vector
        normalizer = np.sqrt(self.x**2 + self.y**2)
        self.u_x = self.x / normalizer
        self.u_y = self.y / normalizer

        self.unit = [self.u_x, self.u_y]

    def __str__(self):
        return f"<{self.u_x}, {self.u_y}>"

    def __repr__(self):
        return f"MME565.Vector({self.u_x}, {self.u_y})"


class Line:
    """Creates a line from a two provided points, p1 and p2. Points must be 2D cartesian coordinates."""
    def __init__(self, p1, p2):
        if type(p1) not in [Point, Vertex]:
            self.p1 = Point(p1[0], p1[1])
        else:
            self.p1 = p1
        if type(p2) not in [Point, Vertex]:
            self.p2 = Point(p2[0], p2[1])
        else:
            self.p2 = p2

        # x coordinates of p1 and p2 are equal (vertical segment): undefined slope
        if self.p1.x == self.p2.x:
            self.slope = np.nan
            self.intercept = np.nan
            self.a = 1.0
            self.b = 0
            self.c = self.p1.x

            self.ortho_slope = 0
            self.ortho_intercept = self.p1.y
        else:
            # y = (slope * x) + intercept
            self.slope = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
            self.intercept = -self.slope * self.p1.x + self.p1.y

            # ax + by + c = 0
            self.a = -self.slope
            self.b = 1
            self.c = -self.intercept

            # scale the vector of the line such that sqrt(a**2 + b**2) == 1
            normalizer = np.sqrt(self.a ** 2 + self.b ** 2)
            self.a /= normalizer
            self.b /= normalizer
            self.c /= normalizer

    def distance_point_to_line(self, q: Point):
        """Computes the orthogonal distance from a point (q) to the MME565.Line object"""
        if type(q) != Point:
            q = Point(q[0], q[1])

        if self.a == 0:  # horizontal line
            return max([abs(q.y - self.p1.y), abs(q.y - self.p2.y)])
        elif self.b == 0:  # vertical line
            return max([abs(q.x - self.p1.x), abs(q.x - self.p2.x)])
        else:
            return abs(self.a*q.x + self.b*q.y + self.c) / np.sqrt(self.a**2 + self.b**2)

    def __str__(self):
        return f"Line through points {self.p1} and {self.p2}"

    def __repr__(self):
        return f"MME565.Line({self.p1}, {self.p2})"


class Segment(Line):
    """Creates a line segment from two provided points, p1 and p2. Points must be 2D cartesian coordinates."""
    def __init__(self, p1: Point, p2: Point):
        if type(p1) not in [Point, Vertex]:
            self.p1 = Point(p1[0], p1[1])
        else:
            self.p1 = p1
        if type(p2) not in [Point, Vertex]:
            self.p2 = Point(p2[0], p2[1])
        else:
            self.p2 = p2

        if self.p1.x == self.p2.x and self.p1.y == self.p2.y:
            raise Exception("Some points are the same, no segment exists between them")

        self.length = np.sqrt((self.p1.x - self.p2.x)**2 + (self.p1.y - self.p2.y)**2)

        Line.__init__(self, self.p1, self.p2)

        self.mid_point = Point(np.average([self.p1.x, self.p2.x]), np.average([self.p1.y, self.p2.y]))

    def distance_point_to_segment(self, q: Point):
        """
        Computes the distance from a point (q) to a line segment defined by two points (p1 & p2) All three must be
        one one plane. Returns the distance from the point to the segment, the intersection, and a value (w) as follows:

        w = 0: orthogonal projection of point is on the segment

        w = 1: orthogonal projection of point is not on the segment and point is closest to p1

        w = 2: orthogonal projection of point is not on the segment and point is closest to p2
        """

        if type(q) != Point:
            q = Point(q[0], q[1])

        if self.a == 0:  # horizontal line
            intersection = Point(q.x, self.intercept)
            ortho_slope = np.nan
            ortho_intercept = self.c
            q_to_line = abs(q.y - self.p1.y)
        elif self.b == 0:  # vertical line
            intersection = Point(self.c, q.y)
            ortho_slope = 0
            ortho_intercept = np.nan
            q_to_line = abs(q.x - self.p1.x)
        else:
            ortho_slope = -1 / self.slope
            ortho_intercept = -ortho_slope * q.x + q.y
            intersection = Point(
                (ortho_intercept - self.intercept) / (self.slope - ortho_slope),
                self.slope * (ortho_intercept - self.intercept) / (self.slope - ortho_slope) + self.intercept
            )
            q_to_line = abs(self.a*q.x + self.b*q.y + self.c) / np.sqrt(self.a**2 + self.b**2)

        p1_to_p2 = np.round(distance_between_points(self.p1, self.p2), 8)
        intersection_to_p1 = np.round(distance_between_points(intersection, self.p1), 8)
        intersection_to_p2 = np.round(distance_between_points(intersection, self.p2), 8)
        q_to_p1 = np.round(distance_between_points(q, self.p1), 8)
        q_to_p2 = np.round(distance_between_points(q, self.p2), 8)

        if np.round((intersection_to_p1 + intersection_to_p2), 7) == np.round(p1_to_p2, 7):
            return q_to_line, 0, intersection
        elif q_to_p1 < p1_to_p2:
            return q_to_p1, 1, self.p1
        else:
            return q_to_p2, 2, self.p2

    def vector_point_to_segment(self, q: Point):
        if type(q) != Point:
            q = Point(q[0], q[1])

        _, _, intersection = self.distance_point_to_segment(q)

        if type(intersection) not in [Point, Vertex]:
            intersection = Point(intersection[0], intersection[1])

        return Vector(q, intersection)

    def tangent_vector_point_to_segment(self, q: Point):
        if type(q) != Point:
            q = Point(q[0], q[1])

        _, _, intersection = self.distance_point_to_segment(q)

        vector = Vector(q, intersection)

        vector.x, vector.y = vector.y, -vector.x
        vector.u_x, vector.u_y = vector.u_y, -vector.u_x

        return vector

    def __str__(self):
        return f"Segment with endpoints {self.p1} and {self.p2} and length {round(self.length,4)}"

    def __repr__(self):
        return f"MME565.Segment({self.p1}, {self.p2})"


class Polygon:
    """Creates a polygon from a list of MME.565.Point objects."""
    def __init__(self, vertices):
        self.vertices = []
        for vertex in vertices:
            if type(vertex) != Vertex:
                self.vertices.append(Vertex(vertex[0], vertex[1]))
            elif type(vertex) == Vertex:
                self.vertices.append(vertex)
            else:
                raise Exception("Wrong input type to MME565.Polygon. Must be MME565.Vertex or List")
        self.vertex_array = np.array(vertices)

        # build a list of Segment objects from adjacent pairs of vertices
        self.segments = []
        for vertex in range(len(vertices)):
            if vertex == len(vertices) - 1:
                self.segments.append(Segment(self.vertices[-1], self.vertices[0]))
            else:
                self.segments.append(Segment(self.vertices[vertex], self.vertices[vertex + 1]))

        self.num_sides = len(self.segments)

        self.convex_list = []
        for i, vertex in enumerate(self.vertices):
            if i == 0:
                self.convex_list.append(vertex.convex_test(self.vertices[-1], self.vertices[i+1]))
            elif i == len(self.vertices) - 1:
                self.convex_list.append(vertex.convex_test(self.vertices[i-1], self.vertices[0]))
            else:
                self.convex_list.append(vertex.convex_test(self.vertices[i-1], self.vertices[i+1]))

    def distance_point_to_polygon(self, q: Point):
        distance = [[np.inf], None]
        for segment in self.segments:
            dist, _, _ = segment.distance_point_to_segment(q)
            if dist < distance[0][0]:
                distance = [segment.distance_point_to_segment(q), segment]
        return distance

    def check_point_inside_polygon(self, q: Point):
        # uses matplotlib.path.Path method
        # if I have time I will build a custom method that isn't so opaque.
        # this method has trouble if some polygon segments intersect (like a star with 5 vertices)
        if type(q) != Point:
            q = Point(q[0], q[1])
        path = mpltpath.Path(self.vertex_array)
        inside = path.contains_point([q.x, q.y])
        return inside

    def classify_vertex(self, vertex):
        pass

    def __str__(self):
        return f"A polygon with {len(self.segments)} segments and centered at [maybe calculate COM of polygon?]"

    def __repr__(self):
        return f"MME565.Polygon({self.vertices})"


class Trapezoid:
    def __init__(self, vertices):
        self.vertices = []
        for vertex in vertices:
            if type(vertex) != Point:
                self.vertices.append(Point(vertex[0], vertex[1]))
            elif type(vertex) == Point:
                self.vertices.append(vertex)
            else:
                raise Exception("Wrong input type to MME565.Trapezoid. Must be MME565.Point or List")
        self.vertex_array = np.array(vertices)

        # build a list of Segment objects from adjacent pairs of vertices
        self.segments = []
        for vertex in range(len(vertices)):
            if vertex == len(vertices) - 1:
                self.segments.append(Segment(self.vertices[-1], self.vertices[0]))
            else:
                self.segments.append(Segment(self.vertices[vertex], self.vertices[vertex + 1]))
    
        self.center = Point(np.average(self.vertex_array[...,0]), np.average(self.vertex_array[...,1]))

    def __str__(self):
        return f"A trapezoid with {len(self.segments)} segments and centered at {self.center}"

    def __repr__(self):
        return f"MME565.Trapezoid({self.vertices})"


def distance_between_points(p1: Point, p2: Point):
    """Computes the distance between two provided Point objects"""
    if type(p1) not in [Point, Vertex]:
        p1 = Point(p1[0], p1[1])
    if type(p2) not in [Point, Vertex]:
        p2 = Point(p2[0], p2[1])
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def distance_point_to_line(p1: Point, p2:  Point, q: Point):
    """Computes the distance from a point (q) to a line through two points (p1 and p2)"""
    line = Segment(p1, p2)
    q = Point(q[0], q[1])
    return line.distance_point_to_segment(q)


def show_polygon(polygon: Polygon, q: Point):
    fig, ax = plt.subplots()
    patches = [mpatches.Polygon(polygon.vertex_array)]
    colors = np.linspace(0, 1, 1)
    collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
    collection.set_array(colors)
    ax.add_collection(collection)
    if type(q[0]) != list:
        q = [q]
    for point in q:
        if type(point) != Point:
            point = Point(point[0], point[1])
        if polygon.check_point_inside_polygon(point):
            plt.plot(point.x, point.y, "bo")
        else:
            plt.plot(point.x, point.y, "rx")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    pass
