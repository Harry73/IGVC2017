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

	# Set up an empty map
	def __init__(self, map_width, map_height, vehicle_size):
		self.map_width = map_width
		self.map_height = map_height
		self.xscale = vehicle_size
		self.yscale = vehicle_size
		self.grid_dim = (int(self.map_width/self.xscale), int(self.map_height/self.yscale))
		self.map = np.zeros(self.grid_dim, np.uint8)
		self.last_data_set = []

	# Save points the sensors have seen
	def record(self, r, current_location, current_direction):
		positions = []
		for i in range(181):
			angle = (current_direction - 90 + i) % 360

			# Draw obstacle points seen
			x = current_location[0] + (r[i])*np.cos(angle*np.pi/180)
			y = current_location[1] - (r[i])*np.sin(angle*np.pi/180)
			positions.append((x, y))

			# Fix when cos and sin run past image limits
			if x < 0:
				x = 0
			if y < 0:
				y = 0
			if x > self.map_width:
				x = self.map_width-1
			if y > self.map_height:
				y = self.map_height-1

			# Increase likelihood that grid tile has an obstacle
			self.map[math.floor(x/self.xscale), math.floor(y/self.yscale)] += 1
			
		self.last_data_set = positions
