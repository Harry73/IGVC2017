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
		self.normal_location = (1830, 6650)
		self.normal_direction = 180
		self.normal_goal = (1000, 6650)

		# Average three values for the initial real-world direction and location
		self.initial_direction = (
			sensors.compass_data() +
			sensors.compass_data() +
			sensors.compass_data()
		)/3

		loc1 = sensors.gps_data()
		loc2 = sensors.gps_data()
		loc3 = sensors.gps_data()
		self.initial_location = (
			(loc1[0] + loc2[0] + loc3[0])/3,
			(loc1[1] + loc2[1] + loc3[1])/3
		)

		# Start the vehicle motors
		self.motors = Motors()
		self.motors.start()
		self.motors.restart()

		self.queue = Queue()

	def run(self):
		repeat = False
		speed_signal = 1360
		turn_signal = 1200

		map_width = 120*12*2.54		# cm
		map_height = 220*12*2.54	# cm

		vehicle_width = 35*2.54		# Width of agent (cm)

		buffer_distance = 12*2.54	# Space to keep between agent and obstacles (cm)
		buff_width = vehicle_width + buffer_distance

		MAX_R = int(10*12*2.54)		# Maximum distance to ever consider (cm)
		R = MAX_R					# Maximum distance to consider for a iteration
		move_scale = 0.25			# Percentage of R to actually move

		# Create initial map of environment
		map = AStar(map_width, map_height, vehicle_width)

		# GPS calculations
		"""
		phi 	latitude	longitude
		0		110.574		111.32
		15		110.649		107.55
		30		110.852		96.486
		45		111.132		78.847
		60		111.412		55.8
		75		111.618		28.902
		90		111.694		0
		"""
		# Linear interpolation using known values
		deg_lat = (110.852 - 111.132)/(30 - 45)*(self.initial_position[0] - 45) + 111.132
		deg_long = (96.486 - 78.847)/(30 - 45)*(self.initial_position[0] - 45) + 78.847
		deg_lat *= 1000*100		# 1 degree latitude = deg_lat cm
		deg_long *= 1000*100	# 1 degree longitude = deg_long cm

		angle_to_00 = self.initial_direction - math.atan2(self.normal_location[1], self.normal_location[0])
		distance_to_00 = math.sqrt(self.normal_location[0]**2 + self.normal_location[1]**2)
		zero_zero = (
			initial_position[0] - distance_to_00*math.cos(angle_to_00)*deg_lat,
			initial_position[1] - distance_to_00*math.sin(angle_to_00)*deg_long
		)
		xscale = (zero_zero[0]-self.initial_position[0])/(0-self.normal_location[0])	# Slope
		yscale = (zero_zero[1]-self.initial_position[1])/(0-self.normal_location[1])	# Slope
		xshift = -xscale*self.normal_location[0] + self.initial_position[0]				# "y" intercept
		yshift = -yscale*self.normal_location[1] + self.initial_position[1]				# "y" intercept

		theta_shift = self.normal_direction - self.initial_direction

		while self.queue.empty():
			if not repeat:
				data = 500000*np.ones(360)

				# Get LiDAR data
				data[0:181] = self.sensors.lidar_data()

				# Get direction from compass and normalize to programmatic world
				self.direction = self.sensors.compass_data()
				self.direction = (self.direction - (self.initial_direction-self.normal_direction)) % 360

				# Rotate, scale, and translate GPS coordinates to programmatic world
				self.location = np.array(self.sensors.gps_data())
				transform = np.array([
					[np.cos(theta_shift), -np.sin(theta_shift)],
					[np.sin(theta_shift), np.cos(theta_shift)]
				])
				self.location = np.dot(transform, self.location)	# Unrotate GPS coordinates
				self.location = np.append(self.location, [1])		# Add bias term to allow translation
				transform = np.array([
					[xscale, 0, xshift],
					[0, yscale, yshift]
				])
				self.location = np.dot(transform, self.location)	# Scale and translate to correct range
				self.location = tuple(self.location[:2])			# Throw out bias term


			# Add in past data set from LiDAR
			for sample in map.last_data_set:
				r = math.sqrt((self.location[0]-sample[0])**2 + (self.location[1]-sample[1])**2)
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
					self.motors.drive(1360)
					repeat = True
					continue
				else:	# Stuck situation
					# TODO: Use A* and Map to find a path out
					motors.stop()
					print("Help, I'm stuck and too stupid to get out!")
					break
			else:
				R = MAX_R
				repeat = False

			# Determine which viable angle will move you towards goal the fastest
			min_index = 0
			min_distance = 10000000
			for i, angle in enumerate(viable_angles):
				# Simulate moving forward R movement at the current angle and calculate distance to goal
				x = self.location[0] + move_scale*R*np.cos(angle*np.pi/180)
				y = self.location[1] - move_scale*R*np.sin(angle*np.pi/180)
				sim_distance = math.sqrt((x-self.normal_goal[0])**2 + (y-self.normal_goal[1])**2)

				# Keep the minimum distance to find the most efficient angle
				if sim_distance < min_distance:
					min_distance = sim_distance
					min_index = i
					min_location = (int(x), int(y))

			# Record the resulting data
			map.record_data(data, self.location, self.direction)

			# Calculate speed and turning based on amount of turn desired
			angle_change = self.direction - viable_angles[min_index]
			speed_signal = int(20*math.fabs(angle_change)/3 + 1000)
			turn_signal = int(-80*angle_change/9 + 1200)
			print("Speed: {0}".format(speed_signal))
			print("Turn to: {0}".format(angle_change))
			print("Turn signal: {0}".format(turn_signal))
			self.motors.drive(speed_signal)
			self.motors.turn(turn_signal)

	def stop(self):
		self.motors.terminate()
		self.queue.put(True)
