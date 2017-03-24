import cv2
import math
import numpy as np

# Records a map of the environment the agent has seen so far
class Map():
	
	# Set up a blank image
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.img = np.zeros((height, width, 3), np.uint8)
		self.obstacle_locations = []
		
	# Save points the sensors have seen
	def record(self, r, current_location, current_direction):
		for i in range(181):
			angle = (current_direction - 90 + i) % 360
			
			# Draw obstacle points seen
			draw_radius = 5
			x = current_location[0] + (r[i]+draw_radius)*np.cos(angle*np.pi/180)
			y = current_location[1] - (r[i]+draw_radius)*np.sin(angle*np.pi/180)
			self.obstacle_locations.append((x, y))
			cv2.circle(self.img, (int(x), int(y)), draw_radius, (0, 0, 255), thickness=-1)
