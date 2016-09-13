class RendezvousHashing(Resizer):
    """Implement Highest Random Weight hashing method."""
    def __init__(self):
        pass

    def get_nodeid(self, key, nodes):
        """Find the node to use for the given key's storage."""
        hashes = []
        for node in nodes:
            hashes.append((hash(node.name+key), node))
        _, node = max(hashes)
        return node.id

    def add_node(self, node, nodes):
        """Nothing is done when a new node is added.

         If a new site Sn+1 is added, new object placements or requests will compute n+1 hash values, and pick the largest of these. If an object already in the system at Sk maps to this new site Sn+1, it will be fetched afresh and cached at Sn+1. All clients will henceforth obtain it from this site, and the old cached copy at Sk will ultimately be replaced by the local cache management algorithm."""
        return {}

    def get_storage(self, node):
        """Take all key-value pairs from this node.

        If Sk is taken offline, its objects will be remapped uniformly to the remaining n-1 sites."""
        return node.hashmap

