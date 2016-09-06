'''
- a way to separate entries by key to know which machine to store it at
- eviction strategy:
* FIFO
* LRU
* LFU
- access pattern:
* write-thru
* write-around
* write-back
- latency vs consistency vs availability
- how would multithreading work? locks?
- collision resolution method
- resizing
* consistent hashing
* HRW (Rendezvous) hashing
'''

import random
import string
import threading

class DHash(object):
    def __init__(self, nodes, config=None):
        self.nodes = nodes
        if not config:
            config = {
                'resizing_method': ConsistentHashing,
                'access_pattern': WriteAround,
                'evection_strategy': LFU
            }
        if not hasattr(config['resizing_method'], 'get_nodeid'):
            raise SystemError("Oh no!")
        else:
            self.resizer = config['resizing_method'](self.nodes)
        self.accessor = config['access_pattern']()

    def read(self, key):
        nodeid = self.resizer.get_nodeid(key)
        return self.nodes[nodeid].read(self.accessor, key)

    def write(self, key, value):
        nodeid = self.resizer.get_nodeid(key)
        self.nodes[nodeid].write(self.accessor, key, value)

    def add_node(self, node):
        self.nodes.append(node)
        self.resizer.resize()

    def remove_node(self, node):
        del self.nodes[node]
        self.resizer.resize()

class MockNode(object):
    """Implement a node. 

    Node will run in its own thread and emulate a separate machine.
    """
    def __init__(self, name, size=128):
        self.name = name
        self.thread = threading.Thread(target=self.run)
        self.size = size
        self.hashmap = {}

    def read(self, accessor, key):
        return self.hashmap.get(key, None)

    def write(self, accessor, key, value):
        self.hashmap[key] = value

    def run(self):
        pass

class MockDB(object):
    """Emulate database via file read/write."""
    pass

class Accessor(object):
    """"""
    pass

class WriteThru(Accessor):
    """Implement write-thru access pattern."""
    pass

class WriteAround(Accessor):
    """Implement write-around access pattern."""
    pass

class WriteBack(Accessor):
    """Implement write-back access pattern."""
    pass

class Evictor(object):
    def __init__(self):
        pass

    def update_on_read(self):
        pass

    def remove_for_write(self):
        pass

class LRU(Evictor):
    """Implement Least-Recently-Used eviction strategy."""
    pass

class LFU(Evictor):
    """Implement Least-Frequently-Used eviction strategy."""
    pass

class FIFO(Evictor):
    """Implement First-In-First-Out eviction strategy."""
    pass

class Resizer(object):

    def get_nodeid(self, key):
        raise NotImplementedError()

    def resize(self):
        raise NotImplementedError()

    def hash0(self, node_name):
        return hash(node_name)

    def hash1(self, node_name):
        res = 0
        for char in node_name:
            res += 1723**ord(char)
        res %= 2**64
        return res if res % 10 < 5 else -res

    def hash2(self, node_name):
        res = 0
        for char in node_name:
            res += 1327**ord(char)
        res %= 2**64
        return res if res % 10 < 5 else -res

class ConsistentHashing(Resizer):
    """Implement a consistent hashing ring."""
    def __init__(self, nodes):
        self.positions = []
        for node in nodes:
            self.positions.append((self.hash0(node.name), node.name))
            self.positions.append((self.hash1(node.name), node.name))
            self.positions.append((self.hash2(node.name), node.name))
        self.positions.sort()
        print(self.positions)

    def get_nodeid(self, key):
        hash(key)
        return 0

    def resize(self):
        pass

class RendezvousHashing(Resizer):
    """Implement Highest Random Weight hashing method."""
    def __init__(self):
        pass

    def get_nodeid(self, key):
        """For now, return 0."""
        return 0

    def resize(self):
        pass

def dummy_key_value_pair():
    names = ['dan', 'ben', 'jim', 'joe']
    return (random.choice(names)+str(random.randint(10,99)), 
        ''.join([random.choice(string.ascii_letters+string.digits) 
        for _ in range(20)]))

def dummy_key():
    names = ['dan', 'ben', 'jim', 'joe']
    return random.choice(names)+str(random.randint(10,99))

if __name__ == '__main__':
    r = Resizer()
    for _ in range(10):
        key = dummy_key()
        print(key, r.hash0(key), r.hash1(key), r.hash2(key))

    node1 = MockNode('Machine 1')
    # print(node1.name)
    print(r.hash0(node1.name))# == -4468146149083681170
    print(r.hash1(node1.name))# == 14738669757681942741
    print(r.hash2(node1.name))# == -5343253232099587805

    node2 = MockNode('Machine 2')

    dhash = DHash([node1, node2])
    for _ in range(100):
        key, value = dummy_key_value_pair()
        dhash.write(key, value)
        if random.randint(0,5) == 0:
            print(dhash.read(dummy_key()))
