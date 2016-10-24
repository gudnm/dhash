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
from Node import Node
from Resizer import Resizer
from ConsistentHashing import ConsistentHashing
from MockDB import MockDB
from Client import Client

if __name__ == '__main__':
    r = ConsistentHashing([])
    client = Client()
    # print(r.hash_functions)
    for _ in range(10):
        key = client.dummy_key()
        print(key, r.hashes(key))

    node0 = Node('Machine 0', 0)
    node1 = Node('Machine 1', 1)

    dhash = DHash([node0, node1])
    for _ in range(10):
        key, value = client.dummy_key_value_pair()
        dhash.write(key, value)
        print(dhash.read(client.dummy_key()))

    node2 = Node('Machine 2', 2)
    print('Hashmaps before adding #2')
    print(dhash)
    print()
    for node in dhash.nodes:
        print(node.hashmap)
        print()
    dhash.add_node(node2)
    print('Hashmaps after adding #2')
    print(dhash)
    print()
    for node in dhash.nodes:
        print(node.name, node.hashmap)
        print()
    dhash.remove_node(node0)
    print('Hashmaps after removing #1')
    print(dhash)
    print()
    for node in dhash.nodes:
        print(node.name, node.hashmap)
        print()
