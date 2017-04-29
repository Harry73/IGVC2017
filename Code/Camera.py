"""
File: Camera.py

Description: Camera Manager Module
	Controls picture-taking with the two cameras and image processing.

	Takes a new set of pictures, processes the images to obtain
	the coordinates of the white lines of the course, and saves
	the lines to a thread-safe stack.
"""

import cv2
import time
import numpy as np
import logging
from multiprocessing import Process, Queue

class Camera(Process):

	def __init__(self, camera_stack, camera_n, camera_s, right_camera_index, left_camera_index):
		# Call Process initializer
		super(Camera, self).__init__()

		# Get IGVC logger
		self.logger = logging.getLogger("IGVC")

		# Save stack and semaphores
		self.camera_stack = camera_stack
		self.camera_n = camera_n
		self.camera_s = camera_s
		self.stopped = Queue()

		# Instantiates cameras
		self.right_camera = cv2.VideoCapture(right_camera_index)
		self.left_camera = cv2.VideoCapture(left_camera_index)

	def run(self):
		# Run until Driver calls for a stop
		while self.stopped.empty():
			# Take a picture with each of the cameras
			ret, right_frame = self.right_camera.read()
			ret, left_frame = self.left_camera.read()

			# Perform image processing on each frame
			right_lines = self.process(right_frame)
			left_lines = self.process(left_frame)

			# Further processing of the two frames combined would go here...
			

			# Push the data on the stack thread-safely
			self.camera_s.acquire()
			self.camera_stack.append(right_lines)
			self.camera_stack.append(left_lines)
			self.camera_s.release()
			self.camera_n.release()

		# Free the cameras when complete
		self.right_camera.release()
		self.left_camera.release()

	# Standard image processing sequence to be performed on each image taken
	def process(self, frame):
		# Convert to HSV color space
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Remove value component
		frame[:,:,2] = 0

		# Blur the image
		frame = cv2.GaussianBlur(frame, (31, 31), 0)

		# Canny edge detection
		frame = cv2.Canny(frame, 0, 45)

		# Dilation
		kernel = np.ones((3, 3), np.uint8)
		frame = cv2.dilate(frame, kernel, iterations=1)

		# Hough line transform
		lines = cv2.HoughLinesP(frame, 1, np.pi/180, 100, 100, 10)
		if lines is None:
			self.logger.warning("No lines detected!")

		return lines

	# Tell run() to end
	def stop(self):
		self.stopped.put(True)

# Test run
if __name__ == "__main__":
	import os
	from multiprocessing import Semaphore, Manager

	camera_data_stack = Manager().list()
	camera = Camera(
		camera_data_stack,
		Semaphore(0),
		Semaphore(1),
		int(os.readlink("/dev/IGVC_RIGHT_CAMERA")[-1]),
		int(os.readlink("/dev/IGVC_LEFT_CAMERA")[-1])
	)

	camera.start()

	time.sleep(10)

	camera.stop()
	camera.join()

	for set in camera_data_stack:
		print(set)
		print("---------------------------")
