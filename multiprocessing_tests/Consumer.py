import time
import psutil
from multiprocessing import Process, Queue

class Consumer(Process):
	def __init__(self, stack, n, s):
		super(Consumer, self).__init__()
		self.stack = stack
		self.n = n
		self.s = s
		self.queue = Queue()
		
	def run(self):
		# Consume
		while True:
			# Obtain semaphores, pop from stack, release semaphores
			print("Consumer requesting n semaphore")
			self.n.acquire()
			
			print("Consumer requesting s sempahore")
			self.s.acquire()
			
			print("Consumer obtained semaphores")
			result = self.stack.pop()
			print("Consumer got {0} from stack".format(result))
			
			print("Consumer releasing s semaphore")
			self.s.release()
			
			if not self.queue.empty():
				break
			
		print("Consumer pid: {0}".format(psutil.Process().pid))
		
	def stop(self):
		self.queue.put(True)