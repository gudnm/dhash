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
import pdb

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

    def read(self, key):
        nodeid = self.resizer.get_nodeid(key)
        return self.nodes[nodeid].read(self.accessor, key)

    def write(self, key, value):
        nodeid = self.resizer.get_nodeid(key)
        self.nodes[nodeid].write(self.accessor, key, value)

    def add_node(self, node):
        self.resizer.add_node(node, self.nodes)

    def remove_node(self, node):
        self.resizer.remove_node(node, self.nodes)

class MockNode(object):
    """Implement a node. 

    Node will run in its own thread and emulate a separate machine.
    """
    def __init__(self, name, nodeid, size=128):
        self.name = name
        self.id = nodeid
        self.thread = threading.Thread(target=self.run)
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
        for k, v in entries:
            self.hashmap[k] = v

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
    def __init__(self):
        self.hash_functions = [
            self._hash0, 
            self._hash1, 
            self._hash2
        ]

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

    def get_hashes(self, node_name, num=3):
        res = []
        for i in range(min(len(self.hash_functions), num)):
            res.append(self.hash_functions[i](node_name))
        return res

    def get_nodeid(self, key):
        raise NotImplementedError()

    def add_node(self, node):
        raise NotImplementedError()

    def remove_node(self, node):
        raise NotImplementedError()

class ConsistentHashing(Resizer):
    """Implement a consistent hashing ring."""
    def __init__(self, nodes):
        super(ConsistentHashing, self).__init__()
        self.positions = []
        for node in nodes:
            hashes = self.get_hashes(node.name)
            for somehash in hashes:
                self.positions.append((somehash, node.id))
        self.positions.sort()

    def get_nodeid(self, key):
        key_position = hash(key)
        for node_position in self.positions:
            if key_position < node_position[0]:
                return node_position[1]
        return self.positions[0][1]

    def add_node(self, node, nodes):
        nodes.append(node) # modifying list of node objects passed from DHash instance... this doesn't seem like a good idea though

        # I need to generate a bunch of new positions, for now I have 3 hash functions, including the built-in, and all nodes get 3 'locations' in the ring, eventually this needs to be variable where some nodes will get more or less depending on their capacity
        hashes = self.get_hashes(node.name)
        new_positions = []
        for somehash in hashes: 
            new_positions.append((somehash, node.id))
    
        # figure out which nodes would share some of their load
        for new_pos in new_positions:
            for i in range(len(self.positions)):
                if new_pos[0] < self.positions[i][0]:
                    aux_node = nodes[self.positions[i][1]]
                    res = aux_node.pop(self.positions[i-1][0], new_pos[0])
                    node.push(res)
                    break
            # when new_pos is bigger than biggest of old positions, nothing happens, however, it should take some of the entries from biggest of old positions... e.g. 
            # . 0 althoughwethickv(0)
            # .
            # ...
            # . 0 latterneverthence(0)
            # .
            # . cannotformerbecame(0)
            # .
            # . 2
            # .

        for new_pos in new_positions:
            self.positions.append(new_pos)

        self.positions.sort()

    def remove_node(self, node, nodes):
        del nodes[node.id]
        for pos in self.positions:
            if pos[1] == node.id:
                # should I pop parts of entries stored at the node being removed and push them into appropriate nodes, or should I traverse all the entries of node being removed and try and figure out where they go?
                pass

class RendezvousHashing(Resizer):
    """Implement Highest Random Weight hashing method."""
    def __init__(self):
        pass

    def get_nodeid(self, key):
        """For now, return 0."""
        return 0

    def add_node(self, node):
        pass

    def remove_node(self, node):
        pass

def stop_words():
    """"""
    return ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

def dummy_key_value_pair():
    names = ['dan', 'ben', 'jim', 'joe']
    words = stop_words()
    return (random.choice(names)+str(random.randint(1,9)), 
            ''.join([random.choice(words) for _ in range(3)]))

def dummy_key():
    names = ['dan', 'ben', 'jim', 'joe']
    return random.choice(names)+str(random.randint(1,9))

if __name__ == '__main__':
    r = Resizer()
    print(r.hash_functions)
    for _ in range(10):
        key = dummy_key()
        print(key, r.get_hashes(key))

    node1 = MockNode('Machine 0', 0)
    node2 = MockNode('Machine 1', 1)

    dhash = DHash([node1, node2])
    for _ in range(10):
        key, value = dummy_key_value_pair()
        dhash.write(key, value)
        if random.randint(0,5) == 0:
            print(dhash.read(dummy_key()))

    node3 = MockNode('Machine 2', 2)
    print('Hashmaps before adding #2')
    print(dhash)
    print()
    for node in dhash.nodes:
        print(node.hashmap)
        print()
    dhash.add_node(node3)
    print('Hashmaps after adding #2')
    print(dhash)
    print()
    for node in dhash.nodes:
        print(node.name, node.hashmap)
        print()
    dhash.remove_node(node1)
    print('Hashmaps after removing #1')
    print(dhash)
    print()
    for node in dhash.nodes:
        print(node.name, node.hashmap)
        print()
