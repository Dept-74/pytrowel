#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# PyTrowel (entry point)
#
# @author: Romain DURAND
##

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4.QtGui import QApplication, QWidget
from PyQt4.QtOpenGL import QGLWidget
from Mesh import Mesh


class GLViewWidget(QGLWidget):
    def __init__(self, parent):
        super(QGLWidget, self).__init__(parent)
        self.setMinimumSize(560, 480)
        self.mesh = Mesh('Test', "/home/romain/Bureau/3D PRINT/S-Plugs.stl")

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -8.0)
        glRotatef(20, 0, 1, 0)
        glRotatef(10, 1, 0, 0)

        glBegin(GL_QUADS)

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)

        glColor3f(1.0, 0.5, 0.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)

        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, -1.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, 1.0)

        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glEnd()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 560 / 480, 0.1, 100.0)

    def initializeGL(self):
        glClearColor(0.05, 0.2, 1, 1.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glShadeModel(GL_SMOOTH)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


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
