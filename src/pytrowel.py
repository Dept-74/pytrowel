#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##
#	PyTrowel (entry point)
#
#	@author: Romain DURAND
##

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4.QtGui import QApplication, QWidget
from PyQt4.QtOpenGL import QGLWidget


class GLViewWidget(QGLWidget):
	def __init__(self, parent):
		super(QGLWidget, self).__init__(parent)
		self.setMinimumSize(560, 480)

	def paintGL(self):
		pass

	def resizeGL(self, w, h):
		side = min(w, h)
		if side < 0:
			return
		glViewport((w - side) // 2, (h - side) // 2, side, side)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
		glMatrixMode(GL_MODELVIEW)

	def initializeGL(self):
		glShadeModel(GL_FLAT)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)


class MainWindow(QWidget):
	def __init__(self):
		super(QWidget, self).__init__(None)
		self.setWindowTitle("PyTrowel")
		self.glWidget = GLViewWidget(self)
		self.layout()

	def layout(self):
		pass


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
