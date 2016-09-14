class Resizer(object):

    def get_nodeid(self, key):
        raise NotImplementedError()

    def add_node(self, node, nodes):
        raise NotImplementedError()

    def get_storage(self, node):
        raise NotImplementedError()
