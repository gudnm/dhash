import unittest
from DHash import DHash
from MockNode import MockNode
from Resizer import Resizer
from Client import Client
from ConsistentHashing import ConsistentHashing
from RendezvousHashing import RendezvousHashing

class ConsistentHashingTest(unittest.TestCase):
	"""docstring for ConsistentHashingTest"""

	def setUp(self):
		self.node = MockNode('Node #0', 0)
		self.dhash = DHash([self.node], resizing_method=ConsistentHashing)
		self.resizer = self.dhash.resizer
		self.client = Client()
		self.dhash.write(*self.client.dummy_key_value_pair())

	def test_hashes(self):
		hashes = self.resizer.hashes(self.node.name)
		self.assertEqual(len(hashes), 3)

	def test_nodeid(self):
		node_id = self.resizer.get_nodeid(self.node.name, self.dhash.nodes)
		self.assertEqual(node_id, 0)

	def test_add_node(self):
		self.another_node = MockNode('Node #1', 1)
		pops = self.resizer.add_node(self.another_node, self.dhash.nodes)
		self.assertEqual(len(pops), 1)

	def test_get_storage(self):
		storage = self.resizer.get_storage(self.node)
		self.assertEqual(storage, {})

class RendezvousHashingTest(unittest.TestCase):
	"""docstring for RendezvousHashingTest"""

	def setUp(self):
		self.node = MockNode('Node #0', 0)
		self.dhash = DHash([self.node], resizing_method=RendezvousHashing)
		self.resizer = self.dhash.resizer

	def test_nodeid(self):
		node_id = self.resizer.get_nodeid(self.node.name, self.dhash.nodes)
		self.assertEqual(node_id, 0)

	def test_add_node(self):
		self.another_node = MockNode('Node #1', 1)
		pops = self.resizer.add_node(self.another_node, self.dhash.nodes)
		self.assertEqual(pops, {})

	def test_get_storage(self):
		storage = self.resizer.get_storage(self.node)
		self.assertEqual(storage, {})

if __name__ == '__main__':
	unittest.main()