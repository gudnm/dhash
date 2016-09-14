import unittest
from DHash import DHash
from Node import Node
from Resizer import Resizer
from Client import Client
from ConsistentHashing import ConsistentHashing
from RendezvousHashing import RendezvousHashing

class NodeTest(unittest.TestCase):
	def setUp(self):
		self.node = Node('Node #0', 0)
		self.node.hashmap = {
			'myself4': 'alreadynoonethough',  #-3199944916903827169 (10)
			'yours2': 'thinbeyondwere', # 3759286853173002204 (22)
			'ourselves0': 'towardshundredhad', # 3434016154199216262 (21)
			'do5': 'fillbutthat' #-1925086808205474881 (12)
		}

	def test_do_pop_over_the_edge(self):
		updates, new_storage = self.node.do_pop(3434016154199216269, 
												-3199944916903827109)
		self.assertEqual(len(updates), 2)
		self.assertEqual(len(new_storage), 2)

	def test_do_pop(self):
		updates, new_storage = self.node.do_pop(-3199944916903827199, 
												3434016154199216269)
		self.assertEqual(len(updates), 3)
		self.assertEqual(len(new_storage), 1)


class ClientTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()

	def test_key_value(self):
		self.assertEqual(len(self.client.dummy_key_value_pair()), 2)

	def test_key_value(self):
		self.assertTrue(len(self.client.dummy_key()))

class ConsistentHashingTest(unittest.TestCase):
	"""docstring for ConsistentHashingTest"""

	def setUp(self):
		self.node = Node('Node #0', 0)
		self.dhash = DHash([self.node], resizing_method=ConsistentHashing)
		self.resizer = self.dhash.resizer
		self.client = Client()
		self.dhash.write(*self.client.dummy_key_value_pair())

	def test_hashes(self):
		hashes = self.resizer.hashes(self.node.name)
		self.assertEqual(len(hashes), 3)

	def test_nodeid(self):
		node_id = self.resizer.get_nodeid(self.node.name)
		self.assertEqual(node_id, 0)

	def test_do_add_node(self):
		new_node = Node('Node #1', 1)
		positions, updates = self.resizer.do_add_node(new_node)
		self.assertEqual(len(positions), 3)
		print(positions) 
		print(updates)
		self.assertEqual(len(updates), 3)

	def test_get_storage(self):
		storage = self.resizer.get_storage(self.node)
		self.assertEqual(len(storage), 1)

class RendezvousHashingTest(unittest.TestCase):
	"""docstring for RendezvousHashingTest"""

	def setUp(self):
		self.node = Node('Node #0', 0)
		self.dhash = DHash([self.node], resizing_method=RendezvousHashing)
		self.resizer = self.dhash.resizer

	def test_nodeid(self):
		node_id = self.resizer.get_nodeid(self.node.name, self.dhash.nodes)
		self.assertEqual(node_id, 0)

	def test_add_node(self):
		self.another_node = Node('Node #1', 1)
		updates = self.resizer.add_node(self.another_node, self.dhash.nodes)
		self.assertEqual(updates, {})

	def test_get_storage(self):
		storage = self.resizer.get_storage(self.node)
		self.assertEqual(storage, {})

if __name__ == '__main__':
	unittest.main()