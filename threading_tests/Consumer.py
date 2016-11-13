import time
from threading import Thread

class Consumer(Thread):
	def __init__(self, stack, n, s):
		super(Consumer, self).__init__()
		self.stack = stack
		self.n = n
		self.s = s
		
	def run(self):
		count = 0
	
		# Consume until 20 numbers
		while count < 50:
			# Obtain semaphores, pop from stack, release semaphores
			print "Consumer requesting n semaphore"
			self.n.acquire()
			
			print "Consumer requesting s sempahore"
			self.s.acquire()
			
			print "Consumer obtained semaphores"
			result = self.stack.pop()
			print "Consumer got %.1f from stack" % result
			
			print "Consumer releasing s semaphore"
			self.s.release()
			
			count += 1
			