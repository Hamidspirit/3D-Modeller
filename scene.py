class Scene(object):

    # The default depth from the camera to place an object
    PLACE_DEPTH = 15.0

    def __init__(self):
        # the camera keeps list of nodes being displayed
        self.node_list = list()
        # Keep track of currently selected nodes 
        # action may depend on currently selected node
        self.selcted_node = None

        print("scene")

    def add_node(self, node):
        self.node_list.append(node)

        print(f"add node {node}")

    def render(self):
        """Render scene """
        for node in self.node_list:
            node.render()