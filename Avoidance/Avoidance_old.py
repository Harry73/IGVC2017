"""
File: Avoidance.py

Description: Obstacle Avoidance Algorithm
	Uses LiDAR and camera data to navigate to a goal without colliding

	This algorithm is similar to the Vector Field Histogram algorithm,
	but simplified a bit. The agent considers each direction from 25 to 156
	degrees. For each angle, it checks if an obstacle was detected within
	the range R and the width equal to the robot's width plus a buffer distance
	to determine if the angle is viable. From all these viable angles, the
	angle that will move the agent towards the goal the fastest is selected.
"""

import cv2
import math
import numpy as np
from Map_old import Map
from Vision_sim import Vision

file = "Field1.png"

def avoid():
	location = (600, 580)		# Initial position (bottom center)
	goal = (600, 80)			# Goal
	direction = 90				# Initial direction (up)
	width = 50					# Width of agent

	MAX_BUFF = 50
	buffer_distance = MAX_BUFF	# Space to keep between agent and obstacles
	buff_width = width + buffer_distance

	MAX_R = 100					# Maximum distance to consider
	R = MAX_R					# Maximum distance to consider for a iteration
	move_scale = 0.25			# Percentage of R to actually move

	vis = Vision(file)
	map = Map(vis.width, vis.height, width)

	while True:
		data = 50000*np.ones(360)
		# Update location and run the sensor simulation
		vis.setLocation(location)
		vis.setDirection(direction)
		data[0:181] = vis.run()

		cv2.circle(vis.img, (int(location[0]), int(location[1])), int(buff_width/2), (255, 255, 0), thickness=2)	# Draw agent
		cv2.circle(vis.img, (int(location[0]), int(location[1])), R, (255, 0, 0), thickness=1)	# Draw max range of consideration
		cv2.circle(vis.img, goal, 10, (0, 255, 0), thickness=2)	# Draw goal

		# Add in past 2 data sets from sensors
		for sample in map.last_data_set:
			r = math.sqrt(math.pow(location[0]-sample[0], 2) + math.pow(location[1]-sample[1], 2))
			theta = math.atan2(location[1]-sample[1], location[0]-sample[0])
			theta = np.pi - theta	# Needed because y coordinates are upside down
			theta = (theta*180/np.pi - (direction-90))	# Find relative angle from absolute
			theta = theta % 360

			# Only modify unknown region around agent
			if theta > 180:
				angle = int(theta)
				if r < data[angle]:
					data[angle] = r

		# Draw the vision + recent memory
		for i, r in enumerate(data):
			theta = (direction - 90 + i) % 360
			x = location[0] + (r)*np.cos(theta*np.pi/180)
			y = location[1] - (r)*np.sin(theta*np.pi/180)
			if x >= 0 and x < vis.width and y >= 0 and y < vis.height:
				if i <= 180:
					cv2.circle(vis.img, (int(x), int(y)), 5, (0, 0, 255))
				else:
					cv2.circle(vis.img, (int(x), int(y)), 5, (0, 255, 255))

		# Pick a direction to move
		viable_angles = []
		for i in range(25, 156):
			theta = (direction - 90 + i) % 360
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

		# If there are no viable angles, try adjusting parameters
		if len(viable_angles) == 0:
			if R > buff_width/2:	# Try decreasing R first
				print("No viable angles, decreasing R")
				R = int(R*0.9)
				continue
			elif buff_width > 5:	# Try decreasing the distance buffer second
				print("No viable angles, decreasing distance buffer")
				buffer_distance = int(buffer_distance*0.9)
				buff_width = width + buffer_distance
				continue
			else:	# Stuck situation -> should turn around or back up
				print("Help, I'm stuck and too stupid to get out!")
				break
		else:
			R = MAX_R
			buffer_distance = MAX_BUFF
			buff_width = width + buffer_distance

		# Determine which viable angle will move you towards goal the fastest
		min_index = 0
		min_distance = 10000000
		for i, angle in enumerate(viable_angles):
			# Simulate moving forward R movement at the current angle and calculate distance to goal
			x = location[0] + move_scale*R*np.cos(angle*np.pi/180)
			y = location[1] - move_scale*R*np.sin(angle*np.pi/180)
			sim_distance = math.sqrt(math.pow(x-goal[0], 2) + math.pow(y-goal[1], 2))

			# Keep the minimum distance to find the most efficient angle
			if sim_distance < min_distance:
				min_distance = sim_distance
				min_index = i
				min_location = (int(x), int(y))

		cv2.arrowedLine(vis.img, location, min_location, (0,255,255), thickness=2)	# Draw direction of next movement
		print("Best angle: {0}".format(viable_angles[min_index]))

		# Record the resulting data
		map.record(data, location, direction)

		# Show the image
		cv2.imshow("Field", vis.img)
		k = cv2.waitKey(0)
		if k == ord('q'):
			cv2.destroyAllWindows()
			break

		# Update location and direction
		location = min_location
		direction = viable_angles[min_index]

	# When simulation is complete, show the recorded map
	map.draw_map()
	cv2.imshow("Map", map.img)
	k = cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	avoid()