# -*- coding: utf-8 -*-

##
# Set of useful mathematical objects
#
# @author: Romain DURAND
##

import math
from warnings import warn


class Point(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def fromVec3d(self, v):
        """
        Set coordinates from a Vec3d.
        Return self.
        """
        if not isinstance(v, Vec3d):
            raise TypeError("Expected Vec3d, got ", type(v))
        self.x, self.y, self.z = v.x, v.y, v.z
        return self

    def __eq__(self, other):
        assert isinstance(other, (Point, Vec3d))
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

    def __str__(self):
        return '('+str(self.x)+', '+str(self.y)+', '+str(self.z)+')'


class Vec3d(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        """
        Modify the vector to get a normalized vector.
        """
        self *= 1 / self.magnitude

    def getNormalized(self):
        """
        Return the normalized vector without modifying the current vector.
        """
        return 1 / self.magnitude * Vec3d(self.x, self.y, self.z)

    def dot(self, v2):
        if not isinstance(v2, Vec3d):
            raise TypeError("Expected Vec3d, got ", type(v2))
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def cross(self, v2):
        if not isinstance(v2, Vec3d):
            raise TypeError("Expected Vec3d, got ", type(v2))
        return Vec3d(self.y*v2.z-v2.y*self.z,
                     self.z*v2.x-v2.z*self.x,
                     self.x*v2.y-v2.x*self.y)

    def fromPoint(self, p):
        """
        Set the coordinates from those of a point.
        """
        if not isinstance(p, Point):
            raise TypeError("Expected a Point, got ", type(p))
        self.x = p.x
        self.y = p.y
        self.z = p.z
        return self

    def fromPoints(self, p1, p2):
        """
        Set the coordinates as self is the vector p1->p2
        """
        if not (isinstance(p1, (Point, Vec3d)) and isinstance(p2, (Point, Vec3d))):
            raise TypeError("Expected two Points, got ", type(p1), " and ", type(p2))
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y
        self.z = p2.z - p1.z
        return self

    def __rmul__(self, other):
        return Vec3d(other * self.x, other * self.y, other * self.z)

    def __mul__(self, other):
        warn("Scalars should be placed before vectors", DeprecationWarning)
        self.__rmul__(other)

    def __add__(self, other):
        assert isinstance(other, Vec3d)
        return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        assert isinstance(other, Vec3d)
        return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        assert isinstance(other, (Point, Vec3d))
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False


class Plane(object):
    def __init__(self, normal, point=None):
        """
        Initialize a plane defined by a normal Vec3d and a Point.
        If point is None, self.normal will be used.
        """
        if not isinstance(normal, Vec3d):
            raise TypeError("Expected Vec3d, got ", type(normal))
        if point is None:
            point = Point().fromVec3d(normal)
            normal.normalize()
        elif isinstance(point, Vec3d):
            point = Point().fromVec3d(point)

        self.normal = normal
        self.point = point

    def lineIntersection(self, point, direction=None):
        """
        Calculate intersection point with the line resulting
        from a point and a direction with the plane.

        :param: point 	Point / Vec3d  	A point of the line.
        :param: direction 	Vec3d 	    Direction of the line.
                                        If None, the normal of the plane will be used instead.
        """
        if not isinstance(point, Point):
            if isinstance(point, Vec3d):
                point = Point().fromVec3d(point)
            else:
                raise TypeError("Expected Point or Vec3d for point, got ", type(point))
        if not isinstance(direction, (type(None), Vec3d)):
            raise TypeError("Expected Vec3d or None for direction, got ", type(point))
        if direction is None:
            direction = self.normal
        else:
            direction.normalize()

        ddn = direction.dot(self.normal)
        if abs(ddn) < 0.000001:
            # Means either there is an infinite number of points or None.
            return None
        mu = Vec3d().fromPoints(point, self.point).dot(self.normal) / ddn
        p = Point().fromVec3d(Vec3d().fromPoint(point) + mu * direction)
        return p

    def distanceToPoint(self, p, signed=True):
        """
        Calculate the euclidian distance from a point to the plane.
        """
        if not isinstance(p, (Point, Vec3d)):
            raise TypeError("Expected Point or Vec3d for p, got ", type(p))
        proj = self.lineIntersection(p)
        if proj is None:
            raise SystemError("Something strange happened")
        d = Vec3d().fromPoints(proj, p).magnitude
        if not signed or Vec3d().fromPoints(proj, p).dot(self.normal) >= 0:
            return d
        # else
        return -1 * d


if __name__ == '__main__':
    assert Vec3d(1, 1, 1).getNormalized() == Vec3d(1 / math.sqrt(3), 1 / math.sqrt(3), 1 / math.sqrt(3))
    Vec3d(1, 0, 2) * 4  # Deprecation warning
    Point().fromVec3d(Vec3d(1, 0, 2))
    assert Plane(Vec3d(0, 0, 1), Point(0, 0, 0)).lineIntersection(Point(1, 1, 5)) == Point(1, 1, 0)
    assert Plane(Vec3d(0, 0, -1), Point(0, 0, 0)).distanceToPoint(Point(10, 20, 12)) == -12
