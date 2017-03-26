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
import time
import math
import numpy as np
from Map import Map
from Vision_sim import Vision

file = "Field4.png"

def avoid():
	location = (600, 580)		# initial position (bottom center)
	goal = (600, 80)			# goal
	direction = 90				# initial direction (up)
	buffer_distance = 50		# space to keep between agent and obstacles
	width = 50					# width of agent
	buff_width = width + buffer_distance
	R = 200						# maximum distance to consider
	move_scale = 0.25			# Percentage of R to actually move

	vis = Vision(file)
	map = Map(vis.width, vis.height, width)

	while True:
		# Update location and run the sensor simulation
		vis.setLocation(location)
		vis.setDirection(direction)
		r = vis.run()

		# Record the resulting data
		map.record(r, location, direction)
	
		cv2.circle(vis.img, (int(location[0]), int(location[1])), int(width/2), (255, 255, 0), thickness=2)	# Draw agent
		cv2.circle(vis.img, (int(location[0]), int(location[1])), R, (255, 0, 0), thickness=1)	# Draw max range of consideration
		cv2.circle(vis.img, goal, 10, (0, 255, 0), thickness=2)	# Draw goal

		# Pick a direction to move
		viable_angles = []
		for i in range(25, 156):	# Angles beyond this range lack the vision needed to make safe decisions
			theta = (direction - 90 + i) % 360
			viable = True
			for rgn in range(math.ceil(buff_width/2), R+10, 10):
				theta_range_needed = 180/np.pi*2*math.asin(buff_width/(2*rgn))
				low_lim = math.floor(i-theta_range_needed/2)
				high_lim = math.ceil(i+theta_range_needed/2)

				if (np.any(r[low_lim:high_lim] < rgn)):
					viable = False

			if viable:
				viable_angles.append(theta)

		# If there are no viable angles, decrease R and try again, up until a point
		if len(viable_angles) == 0:
			if R < buff_width:
				print("Help, I'm stuck and too stupid to get out!")
				break
			else:
				print("No viable angles, decreasing R")
				R = int(R*0.9)
				continue
		
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
		location = min_location
		direction = viable_angles[min_index]

		# Show the image
		cv2.imshow("Field", vis.img)
		k = cv2.waitKey(0)
		if k == ord('q'):
			cv2.destroyAllWindows()
			break

	map.draw_map()
	cv2.imshow("Map", map.img)
	k = cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	avoid()