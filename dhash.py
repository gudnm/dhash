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
class DHash(object):
	def __init__(self, config={}):
		if not config:
			config = {
				'size': 1024,
				'resizing_method': 'consistent-hashing',
				'access_pattern': 'write-around',
				'evection_strategy': 'LRU'
			}
		self.size = config['size']
		self.resizing_method = config['resizing_method']
		self.access_pattern = config['access_pattern']

	def read(self, key):
		pass

	def write(self, key, value):
		pass

class MockNode(object):
	"""Implement a node. 

	Node will run in a separate thread and emulate a separate machine.
	"""
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

class ConsistentHashRing(object):
    """Implement a consistent hashing ring."""
    pass

class RendezvousHashing(object):
	"""Implement Highest Random Weight hashing method."""
	pass

if __name__ == '__main__':
	dhash = DHash()
