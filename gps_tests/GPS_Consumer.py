import time
from threading import Thread

class GPS_Consumer(Thread):
	def __init__(self, stack, n, s):
		super(GPS_Consumer, self).__init__()
		self.stack = stack
		self.n = n
		self.s = s
		
	def run(self):
		# Print out the most recent GPS coordinates every second for 60 seconds
		for count in range(0, 60):
			time.sleep(1)
			
			self.n.acquire()
			self.s.acquire()
			coords = self.stack.pop()
			self.s.release()
			
			print("Coords: (%s, %s)" % (coords[0], coords[1]))

