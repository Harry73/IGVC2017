"""
File: Driver.py

Description: Starts threads to manage sensors and run vehicle
	Uses links created by udev rules to determine the hardware path
	of each usb device.

	Currently starts GPS, LMS, Camera, and Compass threads
"""

import os
import time
import logging
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

	# Camera setup
	camera_lines_stack = []
	camera_n = Semaphore(0)
	camera_s = Semaphore(1)
	camera_controller = Camera(camera_lines_stack, camera_n, camera_s, device_to_path["RIGHT_CAM"], device_to_path["LEFT_CAM"])

	# Compass setup
	compass_stack = []
	compass_n = Semaphore(0)
	compass_s = Semaphore(1)
	compass = Compass(compass_stack, compass_n, compass_s)
	
	# Start the threads
	gps_sensor.start()
	lms_sensor.start()
	camera_controller.start();
	compass.start();

	time.sleep(30)

	# Stop the threads
	gps_sensor.stop()
	lms_sensor.stop()
	camera_controller.stop()
	compass.stop()

	# Clean up the threads
	gps_sensor.join()
	lms_sensor.join()
	camera_controller.join()
	compass.join()
	
	print("--------------- GPS STACK ---------------")
	print(gps_coords_stack)
	print("--------------- LMS STACK ---------------")
	print(lms_data_stack)
	print("--------------- CAMERA STACK ---------------")
	print(camera_lines_stack)
	print("--------------- COMPASS STACK ---------------")
	print(compass_stack)
	print("--------------- DONE ---------------")

def get_device_paths():
	# Get usb device paths from udev rules
	right_camera_index = int(os.readlink("/dev/IGVC_RIGHT_CAMERA")[-1])
	left_camera_index = int(os.readlink("/dev/IGVC_LEFT_CAMERA")[-1])
	gps_path = os.readlink("/dev/IGVC_GPS")
	lidar_path = os.readlink("dev/IGVC_LIDAR")

	# Create dictionary of device to path
	device_to_path = {}
	device_to_path["GPS"] = "/dev/" + gps_path
	device_to_path["LMS"] = "/dev/" + lidar_path
	device_to_path["RIGHT_CAM"] = right_camera_index
	device_to_path["LEFT_CAM"] = left_camera_index

	return device_to_path

if __name__ == "__main__":
	main()
