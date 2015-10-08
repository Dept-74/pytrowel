# -*- coding: utf-8 -*-

##
# STL File parser
#
# @author: Romain DURAND
##

import struct


def openStl(file: str):
    if not isinstance(file, str):
        raise TypeError('Expected string, got ', type(file))
    # Detect binary vs ascii
    f = open(file, 'rb')
    s = str(f.read(80)[0:5])
    f.close()
    if s == "b'solid'":
        triangles = __loadSTL(file)
    else:
        triangles = __loadBSTL(file)
    return triangles


def __loadSTL(file):
    with open(file, 'r') as f:
        name = f.readline().split()
        if not name[0] == "solid":
            raise IOError("Expecting first input as \"solid\" [name]")

        triangles = []

        for line in f:
            params = line.split()
            cmd = params[0]
            if cmd == "endsolid":
                break
            elif cmd == "facet":
                continue
            elif cmd == "outer":
                triangle = []
            elif cmd == "vertex":
                vertex = map(float, params[1:4])
                triangle.append(tuple(vertex))
            elif cmd == "endloop":
                continue
            elif cmd == "endfacet":
                triangles.append(tuple(triangle))
                triangle = []
    return triangles


def __loadBSTL(file):
    if not isinstance(file, str):
        raise TypeError("Expected a string, got ", type(file))

    with open(file, 'rb') as f:
        f.read(80)  # Header ignored
        numTriangles = struct.unpack("@i", f.read(4))
        numTriangles = numTriangles[0]

        triangles = [(0, 0, 0)] * numTriangles

        for i in range(numTriangles):
            struct.unpack("<3f", f.read(12))  # Norms: unused
            vertex1 = struct.unpack("<3f", f.read(12))
            vertex2 = struct.unpack("<3f", f.read(12))
            vertex3 = struct.unpack("<3f", f.read(12))
            struct.unpack("H", f.read(2))  # Unused

            triangles[i] = (vertex1, vertex2, vertex3)

    return triangles


if __name__ == '__main__':
    tr = openStl("/home/romain/Bureau/3D PRINT/20mm-box.stl")
    print(tr)