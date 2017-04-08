"""
File: Sensors.py

Description: Sensor aggregation class
	Collects all the thread-safe measures of the
	sensors and provides methods to access the
	data stacks	safely.
"""

import logging

class Sensors():

	def __init__(self,
					gps_coords_stack, gps_n, gps_s,
					lms_data_stack, lms_n, lms_s,
					camera_lines_stack, camera_n, camera_s,
					compass_stack, compass_n, compass_s):

		# Get IGVC logger
		self.logger = logging.getLogger("IGVC")

		# Save stacks and semaphores
		self.gps_coords_stack = gps_coords_stack
		self.gps_n = gps_n
		self.gps_s = gps_s

		self.lms_data_stack = lms_data_stack
		self.lms_n = lms_n
		self.lms_s = lms_s

		self.camera_lines_stack = camera_lines_stack
		self.camera_n = camera_n
		self.camera_s = camera_s

		self.compass_stack = compass_stack
		self.compass_n = compass_n
		self.compass_s = compass_s

	def gps_data(self):
		self.gps_n.acquire()
		self.gps_s.acquire()
		result = self.gps_coords_stack.pop()
		self.gps_s.release()

		return result

	def lidar_data(self):
		self.lms_n.acquire()
		self.lms_s.acquire()
		result = self.lms_data_stack.pop()
		self.lms_s.release()

		return result

	def camera_data(self):
		self.camera_n.acquire()
		self.camera_s.acquire()
		result = self.camera_lines_stack.pop()
		self.camera_s.release()

		return result

	def compass_data(self):
		self.compass_n.acquire()
		self.compass_s.acquire()
		result = self.compass_stack.pop()
		self.compass_s.release()

		return result
