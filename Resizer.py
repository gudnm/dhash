class Resizer(object):
    def __init__(self):
        self.hash_functions = [
            self._hash0, 
            self._hash1, 
            self._hash2
        ]

    # I need to generate a bunch of new positions, for now I have 3 hash functions, including the built-in, and all nodes get 3 'locations' in the ring, eventually this needs to be variable where some nodes will get more or less depending on their capacity
    def _custom_hash(self, node_name, prime):
        res = 0
        for char in node_name:
            res += prime**ord(char)
        res %= 2**63
        return res if res % 10 < 5 else -res        

    def _hash0(self, node_name):
        return hash(node_name)

    def _hash1(self, node_name):
        return self._custom_hash(node_name, 1723)

    def _hash2(self, node_name):
        return self._custom_hash(node_name, 1327)

    def hashes(self, node_name, num=3):
        res = []
        for i in range(min(len(self.hash_functions), num)):
            res.append(self.hash_functions[i](node_name))
        return res

    def get_nodeid(self, key):
        raise NotImplementedError()

    def add_node(self, node, nodes):
        raise NotImplementedError()

    def remove_node(self, node):
        raise NotImplementedError()
