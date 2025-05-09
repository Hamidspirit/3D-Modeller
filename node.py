from OpenGL import GL
import numpy

import random

import color
from aabb import AABB
from primitive import G_OBJ_SPHERE, G_OBJ_CUBE
from transformation import scaling, translation

class Node(object):
    """Base class for nodes in scene"""
    def __init__(self):
        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.translation_matrix = numpy.identity(4)
        self.scaling_matrix = numpy.identity(4)
        self.selected = False

    def render(self):
        """renders the item to the screen"""
        GL.glPushMatrix()
        GL.glMultMatrixf(numpy.transpose(self.translation_matrix))
        GL.glMultMatrixf(self.scaling_matrix)

        cur_color = color.COLORS[self.color_index]
        GL.glColor3f(cur_color[0], cur_color[1], cur_color[2])
        if self.selected: # emit light if the node is selected
            GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, [0.3, 0.3, 0.3])

        self.render_self()

        if self.selected:
            GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, [0.0, 0.0, 0.0])
        GL.glPopMatrix()

    def render_self(self):
        raise NotImplementedError(
            "The abstract Node Class doesn't define 'render_self'"
        )

    def pick(self, start, direction, mat):
        """ 
        Return whether or not the ray hits the object

        Consume:  
        start, direction form the ray to check
        mat is the modelview matrix to transform the ray by 
        """

        # transform the modelview matrix by the current translation
        newmat = numpy.dot(
            numpy.dot(mat, self.translation_matrix),
            numpy.linalg.inv(self.scaling_matrix)
        )
        result = self.aabb.ray_hit(start, direction, newmat)
        return result
    
    def select(self, select=None):
        """ Toggles or sets selected state """
        if select is None:
            self.selected = select
        else:
            self.selected = not self.selected
        
    def rotate_color(self, forwards):
        self.color_index += 1 if forwards else -1
        if self.color_index > color.MAX_COLOR:
            self.color_index = color.MIN_COLOR
        if self.color_index < color.MIN_COLOR:
            self.color_index = color.MAX_COLOR

    def scale(self, up):
        s =  1.1 if up else 0.9
        self.scaling_matrix = numpy.dot(self.scaling_matrix, scaling([s, s, s]))
        self.aabb.scale(s)

    def translate(self, x, y, z):
        self.translation_matrix = numpy.dot(
            self.translation_matrix, 
            translation([x, y, z]))


class Primitive(Node):
    def __init__(self):
        super(Primitive, self).__init__()
        self.call_list = None

    def render_self(self):
        GL.glCallList(self.call_list)


class Sphere(Primitive):
    """Sphere primitive"""
    def __init__(self):
        super(Sphere, self).__init__()
        self.call_list = G_OBJ_SPHERE

class Cube(Primitive):
    """Cube primitive"""
    def __init__(self):
        super(Cube, self).__init__()
        self.call_list = G_OBJ_CUBE

class HierarchicalNode(Node):
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()

class SnowFigure(HierarchicalNode):
    def __init__(self):
        super(SnowFigure, self).__init__()
        self.child_nodes = [Sphere(), Sphere(), Sphere()]
        self.child_nodes[0].translate(0, -0.6, 0) # scale 1.0
        self.child_nodes[1].translate(0, 0.1, 0)
        self.child_nodes[1].scaling_matrix = numpy.dot(
            self.scaling_matrix, scaling([0.8, 0.8, 0.8]))
        self.child_nodes[2].translate(0, 0.75, 0)
        self.child_nodes[2].scaling_matrix = numpy.dot(
            self.scaling_matrix, scaling([0.7, 0.7, 0.7]))
        for child_node in self.child_nodes:
            child_node.color_index = color.MIN_COLOR
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 1.1, 0.5])
        print("Snow figure")