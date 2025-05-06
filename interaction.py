from collections import defaultdict
from OpenGL import GLUT
from trackball import Trackball


class Interaction(object):

    """Handles user interaction"""
    def __init__(self):
        # currently pressed mouse button
        self.pressed = None
        # the current location of camera
        self.translation = [0, 0, 0, 0]
        # the trackball to calculate ritation
        self.trackball = Trackball(theta = -25, distance=15)
        # current mouse location
        self.mouse_loc = None
        # Unsophisticated callback mechanism
        self.callback = defaultdict(list)

        self.register()
        print("interaction")

    def register(self):
        """register calbacks with GLUT"""
        GLUT.glutMouseFunc(self.handle_mouse_button)
        GLUT.glutMotionFunc(self.handle_mouse_move)
        GLUT.glutKeyboardFunc(self.handle_keystroke)
        GLUT.glutSpecialFunc(self.handle_keystroke)

    def register_callback(self, name,function):
        self.callback[name].append(function)
        print("register callback")

    def trigger(self, name, *args, **kwargs):
        for func in self.callback[name]:
            func(*args, **kwargs)
        print("trigger")

    def translate(self, x, y, z):
        """Translate the camera"""
        self.translation[0] += x
        self.translation[1] += y
        self.translation[2] += z

    def handle_mouse_button(self,button, mode, x, y):
        """Called when mouse button is pressed or released"""
        xSize, ySize = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH), GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)
        y = ySize - y # invert the y cordinate because opengl is inverted
        self.mouse_loc = (x, y)

        if mode == GLUT.GLUT_DOWN:
            self.pressed = button
            if button == GLUT.GLUT_RIGHT_BUTTON:
                pass
            elif button == GLUT.GLUT_LEFT_BUTTON: # pick
                self.trigger('pick', x, y)
            elif button == 3: # scroll up
                self.translate(0, 0, 0.1)
            elif button == 4: # scroll down
                self.translate(0, 0, -0.1)
        else : # mouse button released
            self.pressed = None
            GLUT.glutPostRedisplay()

        print("Handle mouse func")

    def handle_mouse_move(self, x, screen_y):
        """Called when mouse is moved"""
        xSize, ySize = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH), GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)
        y = ySize - screen_y
        if self.pressed is not None:
            dx = x - self.mouse_loc[0]
            dy = y - self.mouse_loc[1]
            if self.pressed == GLUT.GLUT_RIGHT_BUTTON and self.trackball is not None:
                # ignore th updated camera loc because we 
                # want to always rotate around origin
                self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy) 
            elif self.pressed == GLUT.GLUT_LEFT_BUTTON:
                self.trigger('move', x, y)
            elif self.pressed == GLUT.GLUT_MIDDLE_BUTTON:
                self.translate(dx/60.0, dy/60.0, 0)
            else:
                pass
            GLUT.glutPostRedisplay()
        self.mouse_loc = (x, y)

        print("hansle mouse move")

    def handle_keystroke(self,key, x, screen_y):
        """Called on keyboard input from user"""
        xSize, ySize = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH), GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)
        y = ySize - screen_y
        match key:
            case 's': self.trigger('place', 'sphere', x, y)
            case 'c': self.trigger('place', 'cube', x, y)
            case GLUT.GLUT_KEY_UP: self.trigger('scale', up=True)
            case GLUT.GLUT_KEY_DOWN: self.trigger('scale', up=False)
            case GLUT.GLUT_KEY_LEFT: self.trigger('rotate_color', forward=True)
            case GLUT.GLUT_KEY_RIGHT: self.trigger('rotate_color', forward=False)
            case _: print("had an stroke")
        GLUT.glutPostRedisplay()

        print("Handle key stroke")
