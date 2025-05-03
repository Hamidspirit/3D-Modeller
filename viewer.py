from OpenGL.GL import (
    glEnable, glCullFace,
    glDepthFunc, glLightfv,
    glColorMaterial, glClearColor,
    GL_LIGHT0, GL_BACK, GLfloat_4, GLfloat_3, GL_CULL_FACE, 
    GL_DEPTH_TEST, GL_LESS, GL_POSITION, GL_SPOT_DIRECTION,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_COLOR_MATERIAL
    )
from OpenGL.GLUT import (
    glutMainLoop, glutInit,
    glutInitWindowSize, glutCreateWindow,
    glutInitDisplayMode, GLUT_SINGLE, GLUT_RGB,
    glutDisplayFunc,
    )

import numpy

from scene import Scene
from cube import Cube
from sphere import Sphere
from snowfiqure import SnowFiqure
from interaction import Interaction

class Viewer(object):
    def __init__(self):
        """Initialize the viewer"""
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        init_primitives()

    def init_interface(self):
        """Initialize the window and register the render function"""
        glutInit()
        glutInitWindowSize(640, 480)
        glutCreateWindow("3D-Modeller")
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunc(self.render)

        print("interface")

    def init_opengl(self):
        """Initialize opengl settings to render scen"""
        self.inverseModelView = numpy.identity(4)
        self.modelView = numpy.identity(4)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.4, 0.4, 0.4, 0.0)

        print("Open GL")

    def init_scene(self):
        """Initialize the scene object and initialize scene"""
        self.scene = Scene()
        self.create_sample_scene()

        print("scene")

    def create_sample_scene(self):
        cube_node = Cube()
        cube_node.translate(2, 0, 2)
        cube_node.color_index = 2
        self.scene.add_node(cube_node)

        sphere_node = Sphere()
        sphere_node.translate(-2, 0, 2)
        sphere_node.color_index = 1
        self.scene.add_node(sphere_node)

        hierarchical_node = SnowFiqure()
        hierarchical_node.translate(-2, 0, -2)
        self.scene.add_node(hierarchical_node)


    def init_interaction(self):
        """init user interaction and callback"""
        self.interaction = Interaction()
        self.interaction = Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interaction.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)
        print("interaction")

    def render():
        print("Render")

    def main_loop(self):
        glutMainLoop()

def init_primitives():
    print("init primitive")