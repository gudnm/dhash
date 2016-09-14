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
        """Part of 'Functional Core', does not update state, just returns."""
        if end < start:
            left_updates, left_storage = self.do_pop(-2**63, end)
            right_updates, right_storage = self.do_pop(start, 2**63)
            new_storage = {x: left_storage[x] for x in left_storage 
                                                  if x in right_storage}
            return left_updates + right_updates, new_storage
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

