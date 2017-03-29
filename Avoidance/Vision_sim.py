"""
File: Vision_sim.py

Description: Sensor Simulation
	Simulates the data LiDAR and cameras would ideally produce

	White lines are represented as physical obstacles. The Bresenham March 
	algorithm is used to generate a list of data points for lines in every 
	direction from 0 to 180 degrees. This simulates the LiDAR's vision. 
	Each line is searched through until an obstacle is hit or the line ends. 
	The (x, y) coordinates are converted to (r, theta) and returned to mimic 
	the LiDAR's actual output. 
"""

import cv2
import time
import math
import numpy as np

# A simulation of how LiDAR/cameras would hopefully see, using an image
class Vision():

	def __init__(self, img_path):
		# Open image
		self.original = cv2.imread(img_path)
		self.height = self.original.shape[0]
		self.width = self.original.shape[1]
		
		self.sensor_range = 800	# The maximum range the 'sensors' can see
		self.data = [0] * (181)	# The sensor data

	# Generates a list of pixel locations and values between the two points provided
	def bresenham_march(self, p1, p2):
		x1 = p1[0]
		y1 = p1[1]
		x2 = p2[0]
		y2 = p2[1]
		steep = math.fabs(y2 - y1) > math.fabs(x2 - x1)
		if steep:
			t = x1
			x1 = y1
			y1 = t

			t = x2
			x2 = y2
			y2 = t
		also_steep = x1 > x2
		if also_steep:

			t = x1
			x1 = x2
			x2 = t

			t = y1
			y1 = y2
			y2 = t

		dx = x2 - x1
		dy = math.fabs(y2 - y1)
		error = 0.0
		delta_error = 0.0; # Default if dx is zero
		if dx != 0:
			delta_error = math.fabs(dy/dx)

		if y1 < y2:
			y_step = 1
		else:
			y_step = -1

		y = y1
		ret = list([])
		for x in range(x1, x2):
			if steep:
				p = (y, x)
			else:
				p = (x, y)

			(b,r,g) = (-1,)*3
			if p[0] < self.width and p[1] < self.height and p[0] >= 0 and p[1] >= 0:
				(b,r,g) = self.img[p[1],p[0]]

				ret.append((p,(b,r,g)))

			error += delta_error
			if error >= 0.5:
				y += y_step
				error -= 1

		if also_steep:
			ret.reverse()

		return ret

	# Scans and returns values in an array
	def run(self):
		self.img = self.original.copy()

		for i in range(181):
			angle = (self.direction - 90 + i) % 360

			# Get a line iterator for the vision line at 'angle'
			line = self.bresenham_march(
				self.location,
				(int(self.location[0] + self.sensor_range*np.cos(angle*np.pi/180)),
				int(self.location[1] - self.sensor_range*np.sin(angle*np.pi/180)))
			)

			# Find first point where vision hits an object
			for point, value in line:
				if np.all(np.array(value) > 100):
					break

				# Draw vision lines in red
				#self.img[point[1], point[0]] = np.array([0,0,255])

			# Record distance to nearest object
			self.data[i] = math.sqrt(math.pow(self.location[0]-point[0], 2) + math.pow(self.location[1]-point[1], 2))

			# Draw vision endpoints
			#cv2.circle(self.img, (point[0], point[1]), 5, (0, 0, 255), thickness=1)

		# Return the vision
		return np.array(self.data)

	def setLocation(self, new_location):
		self.location = new_location

	def setDirection(self, direction):
		self.direction = direction

# Test run
if __name__ == "__main__":
	vis = Vision("Field1.png")
	vis.setLocation((600, 580))
	vis.setDirection(90)
	data = vis.run()
	cv2.circle(vis.img, (int(vis.location[0]), int(vis.location[1])), 10, (255, 255, 0), thickness=2)	# Draw agent
	cv2.imshow("blah", vis.img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
