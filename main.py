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
from dhash import DHash
from MockNode import MockNode
from Resizer import Resizer
from ConsistentHashing import ConsistentHashing


class MockDB(object):
    """Emulate database via file read/write."""
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
