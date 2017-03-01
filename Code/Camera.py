"""
File: Camera.py

Description: Camera Manager Module
	Controls picture-taking with the two cameras and image processing.
	
	Takes a new set of pictures, processes the images to obtain
	the coordinates of the white lines of the course, and saves
	the lines to a thread-safe stack. 
"""

import cv2
import logging
import numpy as np
from threading import Thread

class Camera(Thread):
	def __init__(self, camera_stack, camera_n, camera_s):
		# Call Thread initializer
		super(Camera, self).__init__()
		
		# Get IGVC logger
		self.logger = logging.getLogger("IGVC")
		
		# Save stack and semaphores
		self.camera_stack = camera_stack
		self.camera_n = camera_n
		self.camera_s = camera_s
		self.stopped = False

		# Instantiates cameras
		right_camera_index = int(os.readlink("/dev/right_cam")[-1])
		left_camera_index = int(os.readlink("/dev/left_cam")[-1])
		self.right_camera = cv2.VideoCapture(right_camera_index)
		self.left_camera = cv2.VideoCapture(left_camera_index)
	
	def run(self):
		# Run until Driver calls for a stop
		while not self.stopped:
			time.sleep(0.5)		# New image set every 0.5 seconds
			
			# Take a picture with each of the cameras
			ret, right_frame = self.right_camera.read()
			ret, left_frame = self.left_camera.read()

			# Perform image processing on each frame
			right_lines = process(right_frame)
			left_lines = process(left_frame)
			
			# Further processing of the two frames combined would go here...
			"""
			if lines != None:
				for line in lines:
					for rho, theta in line:
						a = np.cos(theta)
						b = np.sin(theta)
						x0 = a*rho
						y0 = b*rho
						x1 = int(x0 + 1000*(-b))
						y1 = int(y0 + 1000*(a))
						x2 = int(x0 - 1000*(-b))
						y2 = int(y0 - 1000*(a))

						cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
			"""

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
		# Canny edge detection and Hough Line Transform
		edges = cv2.Canny(frame, 50, 150, apertureSize=3)
		lines = cv2.HoughLines(edges, 1, np.pi/180, 150)

		return lines

	# Tell run() to end
	def stop(self):
		self.stopped = True