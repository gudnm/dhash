import asyncio
import time
import random
import string

class ASyncDHash(object):
	def __init__(self):
		self.nodes = [ASyncNodes('#1'), ASyncNodes('#2')]	

	async def read(self, key):
		if key % 2 == 0:
			await self.nodes[0].read(key)
		else:
			await self.nodes[1].read(key)

	async def write(self, key, value):
		if key % 2 == 0:
			await self.nodes[0].write(key, value)
		else:
			await self.nodes[1].write(key, value)

class ASyncNodes(object):
	def __init__(self, name):
		self.name = name
		self.storage = {}

	async def read(self, key):
		await asyncio.sleep(1)
		if key in self.storage:
			print('Read ', self.storage[key], 'with key of ', key)
			return self.storage[key]
		else:
			print('Nothing read for key of ', key)

	async def write(self, key, value):
		await asyncio.sleep(2)
		print('Wrote ', value, 'with key of ', key)
		self.storage[key] = value

async def random_gen(dhash):

	while True:
		key = random.randint(0,10)
		value = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
		if random.choice([0,1]):
			await dhash.read(key)
		else:
			await dhash.write(key, value)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	dhash = ASyncDHash()
	tasks = [
		loop.create_task(random_gen(dhash)),
		loop.create_task(random_gen(dhash)),
		loop.create_task(random_gen(dhash)),
		loop.create_task(random_gen(dhash)),
		loop.create_task(random_gen(dhash))
	]
	loop.run_until_complete(asyncio.gather(*tasks))

	