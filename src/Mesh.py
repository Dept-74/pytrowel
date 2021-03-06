# -*- coding: utf-8 -*-

##
# Mesh class
#
# @author: Romain DURAND
##

from OpenGL.GL import *
from utils.math import Vec3d, Point, Plane
from utils.stl_file import openStl
from collections import namedtuple
from utils.lists import insort, bisect_left, bisect_right

ZBounds = namedtuple("ZBounds", ["lower", "upper"])


class Face:
    def __init__(self, v1: Vec3d, v2: Vec3d, v3: Vec3d):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    @property
    def normal(self):
        return (self.v2 - self.v1).cross(self.v3 - self.v1).getNormalized()

    @property
    def zBounds(self):
        return ZBounds(lower=min(self.v1.z, self.v2.z, self.v3.z),
                       upper=max(self.v1.z, self.v2.z, self.v3.z))

    def flipVertexOrder(self):
        self.v1, self.v3 = self.v3, self.v1
        return self

    def getCentroid(self):
        """
        Calculate the centroid of the face.
        :return: Point
        """
        return Point((self.v1.x + self.v2.x + self.v3.x) / 3,
                     (self.v1.y + self.v2.y + self.v3.y) / 3,
                     (self.v1.z + self.v2.z + self.v3.z) / 3)

    def planeIntersection(self, plane):
        d1 = plane.distanceToPoint(self.v1)
        d2 = plane.distanceToPoint(self.v2)
        d3 = plane.distanceToPoint(self.v3)
        if (d1 > 0 and d2 > 0 and d3 > 0) or (d1 < 0 and d2 < 0 and d3 < 0):
            return []
        if d1 == 0 and d2 == 0 and d3 == 0:
            return [(Point().fromVec3d(self.v1), Point().fromVec3d(self.v2)),
                    (Point().fromVec3d(self.v2), Point().fromVec3d(self.v3)),
                    (Point().fromVec3d(self.v1), Point().fromVec3d(self.v3))]
        if d1 == 0 and d2 == 0 and d3 != 0:
            return [(Point().fromVec3d(self.v1), Point().fromVec3d(self.v2))]
        if d1 == 0 and d3 == 0 and d2 != 0:
            return [(Point().fromVec3d(self.v1), Point().fromVec3d(self.v3))]
        if d3 == 0 and d2 == 0 and d1 != 0:
            return [(Point().fromVec3d(self.v2), Point().fromVec3d(self.v3))]
        if ((d1 >= 0) and (d2 < 0 and d3 < 0)) or ((d1 < 0) and (d2 >= 0 and d3 >= 0)):
            p1 = plane.lineIntersection(self.v1, Vec3d().fromPoints(self.v1, self.v2))
            p2 = plane.lineIntersection(self.v1, Vec3d().fromPoints(self.v1, self.v3))
            return [(p1, p2)]
        if ((d2 > 0) and (d1 < 0 and d3 < 0)) or ((d2 < 0) and (d1 > 0 and d3 > 0)):
            p1 = plane.lineIntersection(self.v2, Vec3d().fromPoints(self.v2, self.v1))
            p2 = plane.lineIntersection(self.v2, Vec3d().fromPoints(self.v2, self.v3))
            return [(p1, p2)]
        if ((d3 > 0) and (d2 < 0 and d1 < 0)) or ((d3 < 0) and (d2 > 0 and d1 > 0)):
            p1 = plane.lineIntersection(self.v3, Vec3d().fromPoints(self.v3, self.v2))
            p2 = plane.lineIntersection(self.v3, Vec3d().fromPoints(self.v3, self.v1))
            return [(p1, p2)]
        return []


class Mesh:
    def __init__(self, name: str, file: str=None):
        assert isinstance(name, str)
        self.name = name
        self.faces = list()
        if file is not None:
            self.faces = Mesh.readStlTriangles(openStl(file))
        self.__byLowerBound = []
        self.__byUpperBound = []
        self.computeSorting()

    def computeSorting(self):
        self.__byLowerBound = list(self.faces)
        self.__byUpperBound = list(self.faces)
        self.__byLowerBound.sort(key=lambda x: x.zBounds.lower)
        self.__byUpperBound.sort(key=lambda x: x.zBounds.upper)

    def addFaces(self, faces):
        if not isinstance(faces, list):
            raise TypeError("Expected list, got ", type(faces))
        self.faces.extend(faces)
        self.computeSorting()
        return self

    def addFace(self, face):
        """
        :param face: Face
        :return: self
        """
        if not isinstance(face, Face):
            raise TypeError("Expected Face, got ", type(face))
        self.faces.append(face)
        insort(self.__byLowerBound, face, key=lambda x: x.zBounds.lower)
        insort(self.__byUpperBound, face, key=lambda x: x.zBounds.upper)
        return self

    @staticmethod
    def readStlTriangles(triangles):
        """
        Convert a list of tuples to list of Faces
        :param triangles: Return list from openStl
        :return: list<Face>
        """
        fa = list()
        for tr in triangles:
            fa.append(Face(Vec3d(tr[0][0], tr[0][1], tr[0][2]),
                           Vec3d(tr[1][0], tr[1][1], tr[1][2]),
                           Vec3d(tr[2][0], tr[2][1], tr[2][2])))
        return fa

    def displayGL(self):
        sun = Vec3d(-1, -1, 1)
        glBegin(GL_TRIANGLES)
        x, y, z = self.getBoundingBoxDimensions()
        zh = self.computeCentroid().z
        for face in self.faces:
            c = 0.9-abs(face.normal.angleWith(sun))*(0.7/3.14)-0.2*(face.zBounds.upper/z)
            glColor3f(c, c, c)
            glVertex3f(face.v1.x, face.v1.y, face.v1.z)
            glVertex3f(face.v2.x, face.v2.y, face.v2.z)
            glVertex3f(face.v3.x, face.v3.y, face.v3.z)
        glEnd()

    def computeCentroid(self):
        """
        Compute the average position of all vertices.
        :return: Point
        """
        x = 0
        y = 0
        z = 0
        for face in self.faces:
            center = face.getCentroid()
            x += center.x
            y += center.y
            z += center.z
        l = len(self.faces)
        return Point(x / l, y / l, z / l)

    def scale(self, ratio):
        """
        Scale the mesh without changing its original centroid.
        :param ratio: float
        :return: None
        """
        c = Vec3d().fromPoint(self.computeCentroid())
        for f in self.faces:
            f.v1 = ratio*(f.v1 - c) + c
            f.v2 = ratio*(f.v2 - c) + c
            f.v3 = ratio*(f.v3 - c) + c

    def move(self, v):
        """
        Move the mesh to the location pointed by v.
        :param v: Vec3d  Translation vector
        :return: None
        """
        for f in self.faces:
            f.v1 += v
            f.v2 += v
            f.v3 += v

    def rotate(self, angle, v):
        """
        Rotate the mesh of angle (degrees) around v
        :param v: Vec3d  Rotation vector.
        :param angle: float
        :return: None
        """
        pos = self.computeCentroid()
        self.move(-1*Vec3d().fromPoint(pos))
        for f in self.faces:
            f.v1.rotate(angle, v)
            f.v2.rotate(angle, v)
            f.v3.rotate(angle, v)
        self.move(Vec3d().fromPoint(pos))

    def getBoundingBoxDimensions(self):
        """
        The resulting box is centered on the centroid of the mesh.
        :return: x, y, z (integers)
        """
        center = self.computeCentroid()
        xmin = xmax = center.x
        ymin = ymax = center.y
        zmin = zmax = center.z
        for f in self.faces:
            xmin = min(xmin, min(f.v1.x, f.v2.x, f.v3.x))
            xmax = max(xmax, max(f.v1.x, f.v2.x, f.v3.x))
            ymin = min(ymin, min(f.v1.y, f.v2.y, f.v3.y))
            ymax = max(ymax, max(f.v1.y, f.v2.y, f.v3.y))
            zmin = min(zmin, min(f.v1.z, f.v2.z, f.v3.z))
            zmax = max(zmax, max(f.v1.z, f.v2.z, f.v3.z))
        return xmax - xmin, ymax - ymin, zmax - zmin

    def selectIntersectingFaces(self, zValue: float):
        """
        Find every face that has at least one point at z = zValue.
        :param zValue: float  Height of the intersecting plane.
        :return: list<Face>
        """
        i = bisect_right(list(map(lambda x: x.zBounds.lower, self.__byLowerBound)), zValue)
        facesUnderPlane = self.__byLowerBound[:i]

        i = bisect_left(list(map(lambda x: x.zBounds.upper, self.__byUpperBound)), zValue)
        facesOverPlane = self.__byUpperBound[i-1:]

        return list(set(facesUnderPlane).intersection(set(facesOverPlane)))


if __name__ == '__main__':
    f = Face(Vec3d(0, 0, 0), Vec3d(1, 0, 0), Vec3d(1, 1, 0))
    f2 = Face(Vec3d(0, 0, 1), Vec3d(1, 0, 2), Vec3d(1, 1, 1))
    f3 = Face(Vec3d(1, 0, 0), Vec3d(1, 0, -1), Vec3d(3, 1, 2))
    f4 = Face(Vec3d(0, 2, 0), Vec3d(-1, 0, 0), Vec3d(1, 1, 1))
    print(f.planeIntersection(Plane(Vec3d(0, 0, 1), Point(0, 0, 0)))[0][0],
          f.planeIntersection(Plane(Vec3d(0, 0, 1), Point(0, 0, 0)))[0][1])
    print(f.zBounds)

    m = Mesh('Test', "/home/romain/Bureau/3D PRINT/SanguinololuEnclosureBot_Doom.stl")
    p = Plane(Vec3d(0, 0, 1))
    segs = list()
    for f in m.selectIntersectingFaces(1):
        segs.extend(f.planeIntersection(p))

    import pylab as pl
    from matplotlib import collections as mc

    for i in range(len(segs)):
        segs[i] = [(segs[i][0].x, segs[i][0].y), (segs[i][1].x, segs[i][1].y)]

    lc = mc.LineCollection(segs, linewidths=2)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    pl.axis('equal')
    ax.margins(0.1)
    pl.show()