import threading

class Node(object):
    """Implements a node. 

    Node will run in its own thread and emulate a separate machine.
    Eventually :)

    Part of 'Imperative Shell' (except the do_pop() method), does destructive 
    operations on node's storage and updates the information related to 
    eviction strategies, like frequencies counts, use order...
    """
    def __init__(self, name, nodeid, size=128):
        self.name = name
        self.id = nodeid
        # self.thread = threading.Thread(target=self.run)
        self.size = size
        self.hashmap = {}

    def read(self, accessor, key):
        return self.hashmap.get(key, None)

    def write(self, accessor, key, value):
        self.hashmap[key] = value

    def do_pop(self, start, end):
        if end < start:
            left_updates, left_storage = self.pop(-2**63, end)
            right_updates, right_storage = self.pop(start, 2**63)
            return left_updates + right_updates, left_storage + right_storage
        updates = []
        new_storage = {}
        for k, v in self.hashmap.items():
            if start < hash(k) < end:
                updates.append((k, v))
            else:
                new_storage[k] = v   
        return updates, new_storage     

    def pop(self, start, end):
        updates, self.hashmap = self.do_pop(start, end)
        return updates

    def push(self, entries):
        self.hashmap.update(entries)

    def run(self):
        pass

