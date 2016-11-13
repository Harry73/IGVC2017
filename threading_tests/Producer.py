import time
from threading import Thread

class Producer(Thread):
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
			print "Producer #%d requesting s semaphore" % self.number
			self.s.acquire()
			
			print "Producer #%d pushing %.1f to stack" % (self.number, i + self.number/10.0, )
			self.stack.append(i + self.number/10.0)
			
			print "Producer #%d releasing s semaphore" % self.number
			self.s.release()
			
			print "Producer #%d releasing n semaphore" % self.number
			self.n.release()
			