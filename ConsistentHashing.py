from Resizer import Resizer

class ConsistentHashing(Resizer):
    """Implement a consistent hashing ring."""
    def __init__(self, nodes):
        super(ConsistentHashing, self).__init__()
        self.positions = []
        for node in nodes:
            for somehash in self.hashes(node.name):
                self.positions.append((somehash, node.id))
        self.positions.sort()

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