#!/usr/bin/env python3
#-*- coding: utf-8 -*-

## @author: Romain DURAND
#
#	Set of usefull mathematical objects
#
##

import math
from warnings import warn

class Vec3d(object):
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def magnitude(self):
		return math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)

	def normalize(self):
		self = 1/self.magnitude() * self
		return self

	def __rmul__(self, other):
		return Vec3d(other*self.x, other*self.y, other*self.z)

	def __mul__(self, other):
		warn("Scalars should be placed before vectors", DeprecationWarning)
		self.__rmul__(other)

	def __add__(self, other):
		assert isinstance(other, Vec3d)
		return Vec3d(self.x+other.x, self.y+other.y, self.z+other.z)

	def __eq__(self, other):
		assert isinstance(other, Vec3d)
		if self.x == other.x and self.y == other.y and self.z == other.z:
			return True
		return False


class Plane(object):
	pass


if __name__ == '__main__':
	assert Vec3d(1, 1, 1).normalize() == Vec3d(1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3))
	Vec3d(1, 0, 2)*4 #Deprecation warning