"""
GPS

Webpage:
https://www.adafruit.com/products/746#learn-anchor

Notes:
-run the following code in command window to install driver
for GPS and run systemd service fix:
sudo apt-get install gpsd gpsd-clients python-gps
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket

-the usb adapter should show up as:
/dev/ttyUSB0
-otherwise need to look at other usb devices:
sudo lsusb

MANUAL STARTUP:
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

MANUAL TEST OUTPUT:
cgps -s

MANUAL RESTART:
sudo killall gpsd
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

-need to install the library for gps:
sudo pip2 install gps3

"""

import time
import subprocess
from gps3.agps3threaded import AGPS3mechanism
from threading import Thread

class GPS(Thread):

	def __init__(self, gps_stack, gps_n, gps_s):
		# Call Thread initializer
		super(GPS, self).__init__()

		# Set up GPS device for 10 Hz report rate
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
		time.sleep(1)	# Small delay to allow sensor to warm up

		while True:
			time.sleep(0.25)	# Get new report every 0.25s

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
