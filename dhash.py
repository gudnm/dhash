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
    def __init__(self, nodes, config={}):
        if not config:
            config = {
                'resizing_method': 'ConsistentHashing',
                'access_pattern': 'WriteAround',
                'evection_strategy': 'LFU'
            }
        self.resizing_method = config['resizing_method']
        self.access_pattern = config['access_pattern']
        self.nodes = nodes

    def read(self, key):
        resizer = self.resizing_method()
        nodeid = resizer.get_nodeid()
        pass

    def write(self, key, value):
        pass

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        del self.nodes[node]

class MockNode(object):
    """Implement a node. 

    Node will run in its own thread and emulate a separate machine.
    """
    def __init__(self, size=1024):
        self.thread = threading.Thread(target=self.run)
        self.size = size
        self.hashmap = {}

    def read(self, key):
        self.hashmap

    def write(self, key, value):
        pass

class MockDB(object):
    """Emulate database via file read/write."""
    pass

class WriteThru(object):
    """Implement write-thru access pattern."""
    pass

class WriteAround(object):
    """Implement write-around access pattern."""
    pass

class WriteBack(object):
    """Implement write-back access pattern."""
    pass

class LRU(object):
    """Implement Least-Recently-Used eviction strategy."""
    pass

class LFU(object):
    """Implement Least-Frequently-Used eviction strategy."""
    pass

class ConsistentHashing(object):
    """Implement a consistent hashing ring."""
    def __init__(self):
        pass

    def get_nodeid(self):
        """For now, return 0."""
        return 0

class RendezvousHashing(object):
    """Implement Highest Random Weight hashing method."""
    pass

def dummy_key_value_pair():
    names = ['dan', 'ben', 'jim', 'joe']
    return random.choice(names)+str(random.randint(100,999)), ''.join([random.choice(string.printable) for _ in range(20)])

def dummy_key():
    names = ['dan', 'ben', 'jim', 'joe']
    return random.choice(names)+str(random.randint(100,999))

if __name__ == '__main__':
    node1 = MockNode()
    node2 = MockNode()
    dhash = DHash([node1, node2])
    for _ in range(1000):
        key, value = dummy_key_value_pair()
        dhash.write(key, value)
        if random.randint(0,5) == 0:
            dhash.read(dummy_key())

