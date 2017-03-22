

import time
import math
import numpy as np
import cv2
from threading import Thread

res = 5

# A simulation of how LiDAR/cameras would hopefully see, using an image
class Vision():

	def __init__(self, img_path):
		# Open image
		self.img = cv2.imread(img_path)
		self.height = self.img.shape[0]
		self.width = self.img.shape[1]
		
	# Scans and returns values in an array
	def run(self):
		data = [0] * (181)

		for i in range(181):
			angle_deg = (self.direction - 90 + i) % 360
			print(angle_deg)
			if angle_deg == 90:
				self.y = np.arange(0, self.location[1])
				self.y = self.y[::-1]
				self.x = np.ones(self.y.shape[0])*self.location[0]

			elif angle_deg == 270:
				self.y = np.arange(self.location[1], self.height)
				self.x = np.ones(self.y.shape[0])*self.location[0]

			elif angle_deg < 90:
				self.x = np.arange(self.location[0]*res, self.width*res)/res
				m = np.sin(angle_deg*np.pi/180) / np.cos(angle_deg*np.pi/180)
				self.y = -1 * m * (self.x - self.location[0]) + self.location[1]

			elif angle_deg > 90 and angle_deg <= 180:
				self.x = np.arange(0, self.location[0]*res)/res
				self.x = self.x[::-1]
				m = np.sin((180-angle_deg)*np.pi/180) / np.cos((180-angle_deg)*np.pi/180)
				self.y = m * (self.x - self.location[0]) + self.location[1]

			elif angle_deg > 180 and angle_deg < 270:
				self.x = np.arange(0, self.location[0]*res)/res
				self.x = self.x[::-1]
				m = np.sin(angle_deg*np.pi/180) / np.cos(angle_deg*np.pi/180)
				self.y = -1 * m * (self.x - self.location[0]) + self.location[1]

			else:
				self.x = np.arange(self.location[0]*res, self.width*res)/res
				m = np.sin((180-angle_deg)*np.pi/180) / np.cos((180-angle_deg)*np.pi/180)
				self.y = m * (self.x - self.location[0]) + self.location[1]

			# Find first point where vision hits an object
			for j in range(self.x.shape[0]):
				if self.y.item(j) < 0 or self.y.item(j) >= self.height:
					break
				if np.all(self.img[int(self.y.item(j)), int(self.x.item(j)), :] > 200):
					break
				#self.img[int(self.y.item(j)), int(self.x.item(j)), :] = np.array([0,0,255])	# Draw vision lines in red

			# Record distance to nearest object
			data[i] = math.sqrt(math.pow(self.location[0]-self.x.item(j), 2) + math.pow(self.location[1]-self.y.item(j), 2))
			
			cv2.circle(self.img, (int(self.x.item(j)), int(self.y.item(j))), 5, (0, 0, 255), thickness=1)	# Draw vision results
			
		# Return the vision
		return np.array(data)

	def setLocation(self, new_location):
		self.location = new_location

	def setDirection(self, direction):
		self.direction = direction

# Test run
if __name__ == "__main__":
	vis = Vision("Field.png")
	data = vis.run()
	cv2.circle(vis.img, (int(vis.location[0]), int(vis.location[1])), 10, (255, 255, 0), thickness=2)	# Draw agent
	for set in data:
		cv2.circle(vis.img, (int(set[0]), int(set[1])), 5, (0, 0, 255), thickness=1)	# Draw vision results
	cv2.imshow("blah", vis.img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
