import time
import subprocess
from gps3.agps3threaded import AGPS3mechanism
from threading import Thread

class GPS(Thread):

	def __init__(self, gps_stack, gps_n, gps_s):
		# Call Thread initializer
		super(GPS, self).__init__()

		# Set up GPS sensor for 10 reports per second
		subprocess.call(['gpsctl', '-c', '0.1'])

		# Save stack and semaphores
		self.gps_stack = gps_stack
		self.gps_n = gps_n
		self.gps_s = gps_s

		# Instantiates AGPS3 mechanisms and sets up the data stream
		self.agps_thread = AGPS3mechanism()
		self.agps_thread.stream_data()
		self.agps_thread.run_thread()

	# Thread operation
	def run(self):
		# Run for 60 seconds for this test
		for i in range(0, 240):
			time.sleep(0.25)	# New request every 0.25s

			# Get coordinates
			position = self.getPosition()

			# Obtain semaphores, push to gps stack, release semaphores
			self.gps_s.acquire()
			self.gps_stack.append(position)
			self.gps_s.release()
			self.gps_n.release()

	# Retrieve the latitude and longitude from the sensor
	def getPosition(self):
		latitude = self.agps_thread.data_stream.lat
		longitude = self.agps_thread.data_stream.lon
		position = (latitude, longitude)
		return position
