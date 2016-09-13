import threading

class MockNode(object):
    """Implement a node. 

    Node will run in its own thread and emulate a separate machine.
    Eventually :)
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

    def pop(self, start, end):
        if end < start:
            # edge case
            return self.pop(-2**63, end) + self.pop(start, 2**63)
        # pdb.set_trace()
        res = []
        temp = {}
        for k, v in self.hashmap.items():
            if start < hash(k) < end:
                res.append((k, v))
            else:
                temp[k] = v
        self.hashmap = temp
        return res

    def push(self, entries):
        self.hashmap.update(entries)

    def run(self):
        pass

