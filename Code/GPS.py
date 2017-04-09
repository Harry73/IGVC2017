"""
File: GPS.py

Description: GPS Data Collector
	Sets up the Adafruit GPS device with system commands.

	Collects a new set of coordinates every 0.25 seconds
	and saves the coordinates to a thread-safe stack.
"""

import time
import logging
import subprocess
from gps3.agps3threaded import AGPS3mechanism
from multiprocessing import Process

class GPS(Process):

	def __init__(self, gps_stack, gps_n, gps_s, device_path):
		# Call Process initializer
		super(GPS, self).__init__()

		# Get IGVC logger
		self.logger = logging.getLogger("IGVC")

		# Set up GPS sensor for 10 reports per second
		subprocess.call(['sudo', 'systemctl', 'stop', 'gpsd.socket'])
		subprocess.call(['sudo', 'systemctl', 'disable', 'gpsd.socket'])
		subprocess.call(['sudo', 'gpsd', device_path, '-F', '/var/run/gpsd.sock'])
		subprocess.call(['gpsctl', '-c', '0.1'])
		self.logger.debug("GPS command line setup complete")

		# Save stack and semaphores
		self.gps_stack = gps_stack
		self.gps_n = gps_n
		self.gps_s = gps_s

		# Instantiates AGPS3 mechanisms and sets up the data stream
		self.agps_thread = AGPS3mechanism()
		self.agps_thread.stream_data()
		self.logger.debug("Starting GPS data collection")
		self.agps_thread.run_thread()

	# Process operation
	def run(self):
		time.sleep(1)	# Let GPS warm up a bit

		# Run until Driver calls for a stop
		while True:
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

	def stop(self):
		self.terminate()
		
# Test run
if __name__ == "__main__":
	import os
	from multiprocessing import Semaphore, Manager
	
	gps_coords_stack = Manager().list()
	gps = GPS(gps_coords_stack, Semaphore(0), Semaphore(1), "/dev/" + os.readlink("/dev/IGVC_GPS"))
	
	gps.start()
	
	time.sleep(10)
	
	gps.stop()
	gps.join()
	
	for set in gps_coords_stack:
		print(set)
		print("---------------------------")
