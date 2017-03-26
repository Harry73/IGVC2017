"""
File: Map.py

Description: Mapping utility
	Records a map of the environment based on data array

	Represents the environment as a grid, where each tile has the
	height and width of the robot's width. When a vision point falls
	in a tile, the value of the tile is incremented by 1 to indicate
	that an obstacle is "probably" in this tile. Over time, higher 
	values then represent higher confidence of the obstacle's location. 
"""

import cv2
import math
import numpy as np

# Records a map of the environment the agent has seen so far
class Map():

	# Set up a blank image
	def __init__(self, width, height, size):
		self.width = width
		self.height = height
		self.img = np.zeros((height, width, 3), np.uint8)
		self.xscale = size
		self.yscale = size
		self.grid_dim = (int(self.width/self.xscale), int(self.height/self.yscale))
		self.map = np.zeros(self.grid_dim, np.uint8)

	# Save points the sensors have seen
	def record(self, r, current_location, current_direction):
		for i in range(181):
			angle = (current_direction - 90 + i) % 360

			# Draw obstacle points seen
			x = current_location[0] + (r[i])*np.cos(angle*np.pi/180)
			y = current_location[1] - (r[i])*np.sin(angle*np.pi/180)
			cv2.circle(self.img, (int(x), int(y)), 5, (0, 0, 255), thickness=1)

			if x < 0:	# Fix when cos and sin run past image limits
				x = 0
			if y < 0:
				y = 0
			if x > self.width:
				x = self.width-1
			if y > self.height:
				y = self.height-1

			# Increase likelihood that grid tile has an obstacle
			self.map[math.floor(x/self.xscale), math.floor(y/self.yscale)] += 1

	def draw_map(self):
		# Vertical lines
		for i in range(self.grid_dim[0]):
			cv2.line(self.img, (int(self.xscale*i), 0), (int(self.xscale*i), self.height), (255, 255, 255))

		# Horizontal lines
		for i in range(self.grid_dim[1]):
			cv2.line(self.img, (0, int(self.yscale*i)), (self.width, int(self.yscale*i)), (255, 255, 255))

		# Map text
		for x in range(self.grid_dim[0]):
			for y in range(self.grid_dim[1]):
				if self.map[x, y] != 0:
					cv2.putText(
						self.img,
						str(self.map[x, y]), 	# text
						(int(self.xscale*x+self.xscale/2), int(self.yscale*y+self.yscale/2)),	# location
						cv2.FONT_HERSHEY_PLAIN ,
						0.8,
						(255, 255, 255)	# color
					)
