"""
File: Driver.py

Description: Starts threads to manage sensors and run vehicle
	Uses usb_identify.sh script to determine the hardware path 
	of each usb device. 
	
	Currently starts GPS, LMS, and Camera threads
"""

import time
import logging
from subprocess import Popen, PIPE
from GPS import GPS
from LMS import LMS
from Camera import Camera
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
	
	# GPS setup
	gps_coords_stack = []
	gps_n = Semaphore(0)
	gps_s = Semaphore(1)
	gps_sensor = GPS(gps_coords_stack, gps_n, gps_s, device_to_path["GPS"])
	
	# LMS setup
	lms_data_stack = []
	lms_n = Semaphore(0)
	lms_s = Semaphore(1)
	lms_sensor = LMS(lms_data_stack, lms_n, lms_s, device_to_path["LMS"])
	
	# LMS setup
	camera_lines_stack = []
	camera_n = Semaphore(0)
	camera_s = Semaphore(1)
	camera_controller = Camera(camera_lines_stack, camera_n, camera_s)
	
	# Start all the threads
	gps_sensor.start()
	lms_sensor.start()
	camera_controller.start();

	time.sleep(30)
	
	# Stop and clean up the threads
	gps_sensor.stop()
	lms_sensor.stop()
	camera_controller.stop()
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
		elif "LMS" in pieces[1]:	##### NEED TO BE CHECKED
			device_to_path["LMS"] = pieces[0]

	return device_to_path
	
if __name__ == "__main__":
	main()
