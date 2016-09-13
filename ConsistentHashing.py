from Resizer import Resizer

class ConsistentHashing(Resizer):
    """Implement a consistent hashing ring."""
    def __init__(self, nodes):
        super(ConsistentHashing, self).__init__()
        self.hash_functions = [
            self._hash0, 
            self._hash1, 
            self._hash2
        ]
        self.positions = []
        for node in nodes:
            for somehash in self.hashes(node.name):
                self.positions.append((somehash, node.id))
        self.positions.sort()

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
        """Find the node to use for the given key's storage."""
        key_position = hash(key)
        for node_position in self.positions:
            if key_position < node_position[0]:
                return node_position[1]
        return self.positions[0][1]

    def do_add_node(self, node, nodes):
        pops = {}
        hashes = self.hashes(node.name)
        new_positions = []
        for somehash in hashes: 
            new_positions.append((somehash, node.id))
    
        # figure out which nodes would share some of their load
        for new_pos in new_positions:
            aux_node_pos = 0
            for i in range(len(self.positions)):
                if new_pos[0] < self.positions[i][0]:
                    aux_node_pos = i
                    break
            aux_node_id = self.positions[aux_node_pos][1]
            pops[aux_node_id] = (self.positions[aux_node_pos-1][0], new_pos[0])

        return new_positions, pops

    def add_node(self, node, nodes):
        new_positions, pops = self.do_add_node(node, nodes)
        for new_pos in new_positions:
            self.positions.append(new_pos)

        self.positions.sort()
        return pops        

    def get_storage(self, node):
        return node.hashmap