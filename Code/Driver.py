"""
File: Driver.py

Description: Starts threads to manage sensors and run vehicle
	Uses usb_identify.sh script to determine the hardware path 
	of each usb device. 
	
	Current only starts a GPS data collector thread
"""

import time
import logging
from subprocess import Popen, PIPE
from GPS import GPS
from threading import Thread, Semaphore

IGVC_HOME = "/home/odroid/IGVC2017"

# Set up IGVC logger
logger = logging.getLogger("IGVC")
logger.setLevel(logging.DEBUG)
ch = logging.FileHandler(os.path.join(os.getcwd(), "IGVC.log"), mode="w")
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def main():
	logger.debug("Getting USB device mapping")
	device_to_path = get_device_paths()
	stop = False
	
	# GPS setup
	gps_coords_stack = []
	gps_n = Semaphore(0)
	gps_s = Semaphore(1)
	gps_sensor = GPS(gps_coords_stack, gps_n, gps_s, device_to_path["GPS"], stop)
	
	# LMS setup
	lms_data_stack = []
	lms_n = Semaphore(0)
	lms_s = Semaphore(1)
	lms_sensor = LMS(lms_data_stack, lms_n, lms_s, device_to_path["LMS"], stop)
	
	# Start all the threads
	gps_sensor.start()
	lms_sensor.start()

	time.sleep(30)
	
	# Stop and clean up the threads
	stop = True
	gps_sensor.join()
	lms_sensor.join()
	
	print("Done")
	
def get_device_paths():
	# Get usb device paths
	usb_identify_path = IGVC_HOME + "/Code/usb_identify.sh"
	(stdout, stderr) = Popen([usb_identify_path], stdout=PIPE, stderr=PIPE).communicate()
	
	if stderr:
		raise Exception(stderr)

	# Create dictionary of device to path
	device_to_path = {}
		
	for line in stdout.splitlines():
		pieces = line.split(" ")
		if "Prolific" in pieces[1]:
			device_to_path["GPS"] = pieces[0]
		elif "LMS" in pieces[1]:
			device_to_path["LMS"] = pieces[0]

	return device_to_path
	
if __name__ == "__main__":
	main()
