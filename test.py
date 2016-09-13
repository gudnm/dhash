import unittest
from DHash import DHash
from MockNode import MockNode
from Resizer import Resizer
from ConsistentHashing import ConsistentHashing

class DHashTest(unittest.TestCase):

	def setUp(self):
		self.node = MockNode('Node #0', 0)
		self.dhash = DHash([self.node])
		self.resizer = self.dhash.resizer

	def testSomething(self):
		pass

class ResizerTest(unittest.TestCase):
	"""docstring for ResizerTest"""

	def setUp(self):
		self.node = MockNode('Node #0', 0)
		self.dhash = DHash([self.node])
		self.resizer = self.dhash.resizer

	def testHashes(self):
		hashes = self.resizer.hashes(self.node.name)
		self.assertEqual(len(hashes), 3)

if __name__ == '__main__':
	unittest.main()