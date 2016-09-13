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
import pdb
from DHash import DHash
from MockNode import MockNode
from Resizer import Resizer
from ConsistentHashing import ConsistentHashing
from MockDB import MockDB
from Client import Client

if __name__ == '__main__':
    r = Resizer()
    client = Client()
    print(r.hash_functions)
    for _ in range(10):
        key = client.dummy_key()
        print(key, r.hashes(key))

    node1 = MockNode('Machine 0', 0)
    node2 = MockNode('Machine 1', 1)

    dhash = DHash([node1, node2])
    for _ in range(10):
        key, value = client.dummy_key_value_pair()
        dhash.write(key, value)
        if random.randint(0,5) == 0:
            print(dhash.read(client.dummy_key()))

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
