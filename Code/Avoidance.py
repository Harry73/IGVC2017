"""
File: Avoidance.py

Description: Obstacle Avoidance Algorithm
	Uses LiDAR and camera data to navigate to a goal without colliding

	This algorithm is similar to the Vector Field Histogram algorithm,
	but simplified a bit. The agent considers each direction from 45 to 136
	degrees. For each angle, it checks if an obstacle was detected within
	the range R and the width equal to the robot's width plus a buffer distance
	to determine if the angle is viable. From all these viable angles, the
	angle that will move the agent towards the goal the fastest is selected.

	This file acts as the centerpiece that connects and uses the other classes
"""

import cv2
import time
import math
import numpy as np
from AStar import AStar
from Motors import Motors
from multiprocessing import Process, Queue

class Avoidance(Process):
	def __init__(self, sensors):
		super(Avoidance, self).__init__()

		self.sensors = sensors

		# Initial conditions in the programmatic world
		self.normal_location = (600, 580)
		self.normal_direction = 180
		self.normal_goal = (600, 80)

		self.initial_direction = (
			(sensors.compass_data())[0] +
			(sensors.compass_data())[0] +
			(sensors.compass_data())[0])/3

		self.motors = Motors()
		self.motors.start()
		self.motors.restart()
		
		self.queue = Queue()
		self.queue.put(self.motors)

	def run(self):
		map_width = 100*12*2.54				# cm
		map_height = 200*12*2.54			# cm

		vehicle_width = 35*2.54		# Width of agent (cm)

		buffer_distance = 12*2.54	# Space to keep between agent and obstacles (cm)
		buff_width = vehicle_width + buffer_distance

		MAX_R = int(10*12*2.54)		# Maximum distance to consider (cm)
		R = MAX_R					# Maximum distance to consider for a iteration
		move_scale = 0.25			# Percentage of R to actually move

		# Create initial map of environment
		map = AStar(map_width, map_height, vehicle_width)
		
		self.motors = self.queue.get()

		while self.queue.empty():
			data = 500000*np.ones(360)

			# TODO: Update location based on GPS
			data[0:182] = self.sensors.lidar_data()				# Get LiDAR data
			self.direction = (self.sensors.compass_data())[0]	# Get compass degrees
			self.direction = (self.direction - (self.initial_direction-self.normal_direction)) % 360 # Normalize direction to programatic world
			self.location = (0, 0)

			# Add in past 2 data sets from sensors
			for sample in map.last_data_set:
				r = math.sqrt(math.pow(self.location[0]-sample[0], 2) + math.pow(self.location[1]-sample[1], 2))
				theta = math.atan2(self.location[1]-sample[1], self.location[0]-sample[0])
				theta = np.pi - theta	# Needed because y coordinates are upside down
				theta = (theta*180/np.pi - (self.direction-90))	# Find relative angle from absolute
				theta = theta % 360

				# Only modify unknown region around agent
				if theta > 180:
					angle = int(theta) % 360
					if r < data[angle]:
						data[angle] = r

			# Pick a direction to move
			viable_angles = []
			for i in range(45, 136):
				theta = (self.direction - 90 + i) % 360
				viable = True
				for rgn in range(math.ceil(buff_width/2), R+10, 5):
					# Calculate theta range and limits to search for obstacles in range rgn
					theta_range_needed = 180/np.pi*2*math.asin(buff_width/(2*rgn))
					low_lim = math.floor(i-theta_range_needed/2) % 360
					high_lim = math.ceil(i+theta_range_needed/2) % 360

					# Check if the path around theta is clear
					if low_lim > high_lim:	# Handle the roll over case made possible by "% 360"
						if np.any(np.concatenate((data[low_lim:], data[0:high_lim])) < rgn):
							viable = False
							break
					else:
						if (np.any(data[low_lim:high_lim] < rgn)):
							viable = False
							break

				# Save viable angles for further inspection later
				if viable:
					viable_angles.append(theta)

			# If there are no viable angles, try decreasing R
			if len(viable_angles) == 0:
				if R > buff_width/2:
					print("No viable angles, decreasing R")
					R = int(R*0.9)
					continue
				else:	# Stuck situation
					# TODO: Use A* and Map to find a path out
#					motors.stop()
					print("Help, I'm stuck and too stupid to get out!")
					break
			else:
				R = MAX_R

			# Determine which viable angle will move you towards goal the fastest
			min_index = 0
			min_distance = 10000000
			for i, angle in enumerate(viable_angles):
				# Simulate moving forward R movement at the current angle and calculate distance to goal
				x = self.location[0] + move_scale*R*np.cos(angle*np.pi/180)
				y = self.location[1] - move_scale*R*np.sin(angle*np.pi/180)
				sim_distance = math.sqrt(math.pow(x-self.normal_goal[0], 2) + math.pow(y-self.normal_goal[1], 2))

				# Keep the minimum distance to find the most efficient angle
				if sim_distance < min_distance:
					min_distance = sim_distance
					min_index = i
					min_location = (int(x), int(y))

			# Record the resulting data
			map.record_data(data, self.location, self.direction)

			# TODO: send instructions to motor control
			# Calculate speed and turning based on amount of turn desired
			angle_change = viable_angles[min_index] - self.direction
			speed_signal = 3*math.fabs(angle_change)/20 - 150
			turn_signal = -100*angle_change/9 + 1000
			print("Turn to: {0}".format(angle_change))
			print("Turn signal: {0}".format(turn_signal))
#			self.motors.drive(speed_signal)
			self.motors.turn(int(turn_signal))
			#location = min_location
			#direction = viable_angles[min_index]

	def stop(self):
		self.motors.terminate()
		self.queue.put(True)