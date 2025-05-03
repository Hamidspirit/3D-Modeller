class Cube(object):
    def __init__(self):
        self.color_index = None
        print("Cube")

    def translate(self, x, y, z):
        print(f"translate: {x}, {y}, {z}")
