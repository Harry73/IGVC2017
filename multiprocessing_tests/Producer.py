import time
import psutil
import numpy as np
from multiprocessing import Process

class Producer(Process):
	def __init__(self, stack, n, s, number):
		super(Producer, self).__init__()
		self.stack = stack
		self.n = n
		self.s = s
		self.number = number
		
	def run(self):
		# Produce 11 numbers
		for i in range(1, 11):
			# Obtain semaphores, push to stack, release semaphores
			print("Producer #{0} requesting s semaphore".format(self.number))
			self.s.acquire()
			
			print("Producer #{0} pushing {1} to stack".format(self.number, i + self.number/10.0))
			self.stack.append((i+self.number/10.0) * np.ones(5))
			
			print("Producer #{0} releasing s semaphore".format(self.number))
			self.s.release()
			
			print("Producer #{0} releasing n semaphore".format(self.number))
			self.n.release()
			time.sleep(0.1)
			
		print("Producer #{0} pid: {1}".format(self.number, psutil.Process().pid))
			