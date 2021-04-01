import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpltpath


class Point:
    """Creates a point from a pair of 2D Cartesian coordinates and rounds them to 8 decimal places."""
    def __init__(self, coordinates):
        if len(coordinates) != 2:
            raise Exception("Some point is not a 2D Cartesian coordinate")
        self.x = np.round(coordinates[0], 8)
        self.y = np.round(coordinates[1], 8)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Segment:
    """Create segments from two provided points, p1 and p2. Points must be 2D cartesian coordinates."""
    def __init__(self, p1: Point, p2: Point):
        # ingest given points as Numpy arrays and round to 8 decimal places
        self.p1 = p1
        self.p2 = p2

        if p1.x == p2.x and p1.y == p2.y:
            raise Exception("Some points are the same, no segment exists between them")

        self.length = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

        if p1.x == p2.x:  # x coordinates of p1 and p2 are equal (vertical segment): undefined slope
            self.slope = np.nan
            self.intercept = np.nan
            self.a = 1.0
            self.b = 0
            self.c = self.p1.x
        else:
            # y = (slope * x) + intercept
            # equation of line collinear with the segment
            self.slope = (p2.y - p1.y) / (p2.x - p1.x)
            self.intercept = -self.slope * p1.x + p1.y

            # ax + by + c = 0
            # equation of line collinear with the segment
            self.a = -self.slope
            self.b = 1
            self.c = -self.intercept

            # normalize the vector equation of the line such that sqrt(a**2 + b**2) == 1
            normalizer = np.sqrt(self.a**2 + self.b**2)
            self.a /= normalizer
            self.b /= normalizer
            self.c /= normalizer

    def distance_point_to_segment(self, q: Point):
        """
        Computes the distance from a point (q) to a line segment defined by two points (p1 & p2) All three must be
        one one plane. Returns the distance from the point to the segment and a value (w) as follows:

        w = 0: orthogonal projection of point is on the segment

        w = 1: orthogonal projection of point is not on the segment and point is closest to p1

        w = 2: orthogonal projection of point is not on the segment and point is closest to p2
        """

        if self.a == 0:  # horizontal line
            intersection = Point([q.x, self.c])
            ortho_slope = np.nan
            ortho_intercept = self.c
            q_to_line = max([abs(q.y - self.p1.y), abs(q.y - self.p2.y)])
        elif self.b == 0:  # vertical line
            intersection = Point([self.c, q.y])
            ortho_slope = 0
            ortho_intercept = np.nan
            q_to_line = max([abs(q.x - self.p1.x), abs(q.x - self.p2.x)])
        else:
            ortho_slope = -1 / self.slope
            ortho_intercept = -ortho_slope * q.x + q.y
            intersection = Point([
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
        return f"Segment with endpoints {self.p1} and {self.p2} and length {round(self.length,4)}"

    def __repr__(self):
        return f"MME565.Segment({self.p1}, {self.p2})"


class Polygon:
    """Creates a polygon from a list of 2D Cartesian coordinates."""
    def __init__(self, vertices):
        # check points for 2d cartesian-ness
        for vertex in vertices:
            if len(vertex) != 2:
                raise Exception("One of the provided polygon vertices was not a 2D Cartesian coordinate")

        # pack vertices into a Numpy array and round to 8 decimal
        self.vertices = np.round(vertices, 8)

        # build a list of Segment objects from adjacent pairs of vertices
        if type(vertices[0]) == list:
            self.segments = []
            for vertex in range(len(vertices)):
                if vertex == len(vertices) - 1:
                    self.segments.append(Segment(Point(self.vertices[-1]), Point(self.vertices[0])))
                else:
                    self.segments.append(Segment(Point(self.vertices[vertex]), Point(self.vertices[vertex + 1])))
        elif type(vertices[0]) == Point:
            self.segments = []
            for vertex in range(len(vertices)):
                if vertex == len(vertices) - 1:
                    self.segments.append(Segment(self.vertices[-1], self.vertices[0]))
                else:
                    self.segments.append(Segment(self.vertices[vertex], self.vertices[vertex + 1]))
        else:
            raise Exception("Polygon vertices not a list of lists or a list of Points")

    def distance_point_to_polygon(self, q: Point):
        distances = []
        for segment in self.segments:
            distances.append(segment.distance_point_to_segment(q))
        return min(distances)

    def check_point_inside_polygon(self, q: Point):
        # uses matplotlib.path.Path method
        path = mpltpath.Path(self.vertices)
        inside = path.contains_point([q.x, q.y])
        return inside

    def __str__(self):
        return f"A polygon with {len(self.segments)} segments and centered at [maybe calculate COM of polygon?]"

    def __repr__(self):
        pass


def distance_between_points(p1: Point, p2: Point):
    """Computes the distance between two provided Point objects"""
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def show_polygon(polygon, q: Point):
    my_poly = polygon.vertices
    poly = plt.Polygon(my_poly, fc="r")
    plt.plot(q.x, q.y, "bo")
    plt.gca().add_patch(poly)
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    point1 = Point([1, 1])
    point2 = Point([2, 2])
    polygon1 = Polygon([
        [0, 0],
        [5, 0],
        [5, 2],
        [9, 3],
        [5, 4],
        [5, 5],
        [1, 5],
    ])
    point_q = Point([5.2345, 4.5])

    # print(polygon1)

    print(polygon1.distance_point_to_polygon(point_q))


    # seggy = Segment(point1, point2)
    # dist, w = seggy.distance_point_to_segment(point_q)
    # print(seggy.a, seggy.b, seggy.c)
    # print(dist, w)

    # print(seggy.p1.x)

    print(polygon1.check_point_inside_polygon(point_q))
    show_polygon(polygon1, point_q)
