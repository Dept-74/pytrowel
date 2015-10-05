#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# Mesh class
#
# @author: Romain DURAND
##

from src.utils.math import Vec3d, Point


class Face:
    def __init__(self, v1: Vec3d, v2: Vec3d, v3: Vec3d):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.normal = (self.v2-self.v1).cross(self.v3-self.v1).normalize()

    def computeNormal(self):
        self.normal = (self.v2-self.v1).cross(self.v3-self.v1).normalize()

    def flipVertexOrder(self):
        self.v1, self.v3 = self.v3, self.v1

    def getCentroid(self):
        """
        Calculates the centroid of the face.
        :return: Point
        """
        return Point((self.v1.x+self.v2.x+self.v3.x)/3,
                     (self.v1.y+self.v2.y+self.v3.y)/3,
                     (self.v1.z+self.v2.z+self.v3.z)/3)


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
