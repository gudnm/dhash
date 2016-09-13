from Resizer import Resizer
from ConsistentHashing import ConsistentHashing 
from Accessor import Accessor, WriteAround
from Evictor import LFU

DEFAULT_CONFIG = {
    'resizing_method': ConsistentHashing,
    'access_pattern': WriteAround,
    'evection_strategy': LFU
}

class DHash(object):
    def __init__(self, nodes, config=None):
        self.nodes = nodes
        if not config:
            config = DEFAULT_CONFIG
        assert issubclass(config['resizing_method'], Resizer)
        self.resizer = config['resizing_method'](self.nodes)
        assert issubclass(config['access_pattern'], Accessor)
        self.accessor = config['access_pattern']()

    def read(self, key):
        nodeid = self.resizer.get_nodeid(key)
        return self.nodes[nodeid].read(self.accessor, key)

    def write(self, key, value):
        nodeid = self.resizer.get_nodeid(key)
        self.nodes[nodeid].write(self.accessor, key, value)

    def add_node(self, node):
        """Add a node to dhash using current resizer."""
        self.nodes.append(node)

        # key-value pairs where key is node_id and value is a tuple with range of hashes
        pops = self.resizer.add_node(node, self.nodes)

        for node_id, (start, end) in pops.items():
            node.push(self.nodes[node_id].pop(start, end))

    def remove_node(self, node):
        """Remove a node from dhash using current resizer."""
        
        # just take entire node's storage
        pushes = self.resizer.remove_node(node)

        for key, value in pushes.items():
            self.write(key, value)

        for i in range(len(self.nodes)):
            if self.nodes[i] == node:
                del self.nodes[i]
                break

    def __str__(self):
        s = [['.'] for _ in range(32)]
        def maptothirtytwo(num):
            # num takes range from -2**63 to 2**63-1
            # we should get down to 0 to 31 via
            # dividing by 2**59 and adding 16
            num //= 2**59
            return num+16
        for pos, nodeid in self.resizer.positions:
            s[maptothirtytwo(pos)].append(str(nodeid))
        for node in self.nodes:
            for k, v in node.hashmap.items():
                s[maptothirtytwo(hash(k))].append(v + '(' + str(node.id) + ')')
        return '\n'.join(map(' '.join, s))
