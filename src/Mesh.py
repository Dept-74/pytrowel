# -*- coding: utf-8 -*-

##
# Mesh class
#
# @author: Romain DURAND
##

from utils.math import Vec3d, Point, Plane


class Face:
    def __init__(self, v1: Vec3d, v2: Vec3d, v3: Vec3d):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.normal = (self.v2-self.v1).cross(self.v3-self.v1).getNormalized()

    def computeNormal(self):
        self.normal = (self.v2-self.v1).cross(self.v3-self.v1).normalize()
        return self

    def flipVertexOrder(self):
        self.v1, self.v3 = self.v3, self.v1
        return self

    def getCentroid(self):
        """
        Calculates the centroid of the face.
        :return: Point
        """
        return Point((self.v1.x+self.v2.x+self.v3.x)/3,
                     (self.v1.y+self.v2.y+self.v3.y)/3,
                     (self.v1.z+self.v2.z+self.v3.z)/3)

    def planeIntersection(self, plane, checkInclusion=True):
        if checkInclusion:
            d1 = plane.distanceToPoint(Point().fromVec3d(self.v1))
            d2 = plane.distanceToPoint(Point().fromVec3d(self.v2))
            d3 = plane.distanceToPoint(Point().fromVec3d(self.v3))
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
            p1 = plane.lineIntersection(Point().fromVec3d(self.v1), Vec3d().fromPoints(self.v1, self.v2))
            p2 = plane.lineIntersection(Point().fromVec3d(self.v1), Vec3d().fromPoints(self.v1, self.v3))
            return [(p1, p2)]
        if ((d2 > 0) and (d1 < 0 and d3 < 0)) or ((d2 < 0) and (d1 > 0 and d3 > 0)):
            p1 = plane.lineIntersection(Point().fromVec3d(self.v2), Vec3d().fromPoints(self.v2, self.v1))
            p2 = plane.lineIntersection(Point().fromVec3d(self.v2), Vec3d().fromPoints(self.v2, self.v3))
            return [(p1, p2)]
        if ((d3 > 0) and (d2 < 0 and d1 < 0)) or ((d3 < 0) and (d2 > 0 and d1 > 0)):
            p1 = plane.lineIntersection(Point().fromVec3d(self.v3), Vec3d().fromPoints(self.v3, self.v2))
            p2 = plane.lineIntersection(Point().fromVec3d(self.v3), Vec3d().fromPoints(self.v3, self.v1))
            return [(p1, p2)]
        return []


class Mesh:
    def __init__(self, name: str):
        assert isinstance(name, str)
        self.name = name
        self.faces = []

    def addFace(self, face):
        if not isinstance(face, Face):
            raise TypeError("Expected Face, got ", type(face))
        self.faces.append(face)

    def computeCentroid(self):
        """
        Computes the average position of all vertices.
        :return: Point
        """
        x, y, z = 0
        for face in self.faces:
            center = face.getCentroid()
            x += center.x
            y += center.y
            z += center.z
        l = len(self.faces)
        return Point(x/l, y/l, z/l)

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
        return xmax-xmin, ymax-ymin, zmax-zmin


if __name__ == '__main__':
    f = Face(Vec3d(0, 0, 0), Vec3d(1, 0, 0), Vec3d(1, 1, 0))
    print(f.planeIntersection(Plane(Vec3d(0, 0, 1), Point(0, 0, 0)))[0][0],
          f.planeIntersection(Plane(Vec3d(0, 0, 1), Point(0, 0, 0)))[0][1])
