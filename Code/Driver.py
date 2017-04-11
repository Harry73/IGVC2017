"""
File: Driver.py

Description: Starts threads to manage sensors and run vehicle
	Uses links created by udev rules to determine the hardware path
	of each usb device.

	Behavior:
	1) Starts GPS, LIDAR, Camera, and Compass threads.
	2) Waits for motor controller to be turned on.
	3) Begins autonomous navigation using Avoidance.py.
	4) Eventually stops all the threads and prints information.
"""

import os
import time
import logging
import wiringpi2 as wpi
from GPS import GPS
from LIDAR import LIDAR
from Camera import Camera
from Compass import Compass
from Sensors import Sensors
from Avoidance import Avoidance
from multiprocessing import Semaphore, Manager

IGVC_HOME = "/home/odroid/IGVC2017"

# Set up IGVC logger
logger = logging.getLogger("IGVC")
logger.setLevel(logging.DEBUG)
ch = logging.FileHandler(os.path.join(os.getcwd(), "IGVC.log"), mode="w")
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def main():
	logger.debug("Starting TCNJ IGVC 2017")
	logger.debug("Getting USB device mappings")
	device_to_path = get_device_paths()

	# GPS setup
	logger.debug("Beginning GPS setup")
	gps_coords_stack = Manager().list()
	gps_n = Semaphore(0)
	gps_s = Semaphore(1)
	gps_sensor = GPS(gps_coords_stack, gps_n, gps_s, device_to_path["GPS"])
	logger.debug("GPS setup complete")

	# LiDAR setup
	logger.debug("Beginning LiDAR setup")
	lidar_data_stack = Manager().list()
	lidar_n = Semaphore(0)
	lidar_s = Semaphore(1)
	lidar_sensor = LIDAR(lidar_data_stack, lidar_n, lidar_s, device_to_path["LIDAR"])
	logger.debug("LiDAR setup complete")

	# Camera setup
	logger.debug("Beginning camera setup")
	camera_lines_stack = Manager().list()
	camera_n = Semaphore(0)
	camera_s = Semaphore(1)
	camera_controller = Camera(camera_lines_stack, camera_n, camera_s, device_to_path["RIGHT_CAM"], device_to_path["LEFT_CAM"])
	logger.debug("Camera setup complete")

	# Compass setup
	logger.debug("Beginning compass setup")
	compass_stack = Manager().list()
	compass_n = Semaphore(0)
	compass_s = Semaphore(1)
	compass = Compass(compass_stack, compass_n, compass_s)
	logger.debug("Compass setup complete")

	# Wrap all the sensors' stacks and semaphores into 1 object
	sensors = Sensors(
		gps_coords_stack, gps_n, gps_s,
		lidar_data_stack, lidar_n, lidar_s,
		camera_lines_stack, camera_n, camera_s,
		compass_stack, compass_n, compass_s
	)

	# Start the sensor threads
	logger.debug("Setup complete")
	logger.debug("Starting GPS thread")
	gps_sensor.start()
	logger.debug("Startting LiDAR thread")
	lidar_sensor.start()
	logger.debug("Starting camera thread")
	camera_controller.start();
	logger.debug("Starting compass thread")
	compass.start();


	# Set up wiringpi2 and GPIO pin 6 as input
	logger.debug("Sensor threads started, waiting for motors to turn on")
	motors_on_pin = 6
	wpi.wiringPiSetup()
	wpi.pinMode(motors_on_pin, 0)

	# Wait for motor controller to be turned on
	motors_on = False
	while not motors_on:
		value = wpi.digitalRead(motors_on_pin)
		if value == 1:
			motors_on = True
		else:
			time.sleep(1)

	logger.debug("Motors are on, begin autonomous navigation")
	path_find = Avoidance(sensors)
	path_find.start()

	time.sleep(10)

	# Stop the threads
	logger.debug("Calling for threads to stop")
	path_find.stop()
	time.sleep(1)
	gps_sensor.stop()
	lidar_sensor.stop()
	camera_controller.stop()
	compass.stop()

	# Clean up the threads
	logger.debug("Waiting for threads to end")
	path_find.join()
	gps_sensor.join()
	lidar_sensor.join()
	camera_controller.join()
	compass.join()

	print("--------------- CAMERA STACK ---------------")
	print(camera_lines_stack)
	print("--------------- GPS STACK ---------------")
	print(gps_coords_stack)
	print("--------------- LIDAR STACK ---------------")
	print(lidar_data_stack)
	print("--------------- COMPASS STACK ---------------")
	print(compass_stack)
	print("--------------- DONE ---------------")

def get_device_paths():
	# Get usb device paths from udev rules
	right_camera_index = int(os.readlink("/dev/IGVC_RIGHT_CAMERA")[-1])
	left_camera_index = int(os.readlink("/dev/IGVC_LEFT_CAMERA")[-1])
	gps_path = os.readlink("/dev/IGVC_GPS")
	lidar_path = os.readlink("/dev/IGVC_LIDAR")

	# Create dictionary of device to path
	device_to_path = {}
	device_to_path["GPS"] = "/dev/" + gps_path
	device_to_path["LIDAR"] = "/dev/" + lidar_path
	device_to_path["RIGHT_CAM"] = right_camera_index
	device_to_path["LEFT_CAM"] = left_camera_index

	return device_to_path

if __name__ == "__main__":
	main()
