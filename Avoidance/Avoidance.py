import time
import math
import numpy as np
import cv2
from threading import Thread
from Vision_sim import Vision

file = "Field3.png"

def main():
	location = (600, 580)		# initial position (bottom center)
	goal = (600, 80)			# goal
	direction = 90				# initial direction (up)
	buffer_distance = 50		# space to keep between agent and obstacles
	width = 50					# width of agent
	width += buffer_distance	
	R = 100						# maximum distance to consider
	scale = 0.5					# Percentage of R to actually move
		
	while True:
		vis = Vision(file)
		vis.setLocation(location)
		vis.setDirection(direction)
		r = vis.run()
		
		cv2.circle(vis.img, (int(location[0]), int(location[1])), int((width-buffer_distance)/2), (255, 255, 0), thickness=2)	# Draw agent
		cv2.circle(vis.img, (int(location[0]), int(location[1])), R, (255, 0, 0), thickness=1)	# Draw max range of consideration
		cv2.circle(vis.img, goal, 10, (0, 255, 0), thickness=2)	# Draw goal

		viable_angles = []
		# Pick a direction to move
		for i in range(25,156):
			theta = (direction - 90 + i) % 360
			viable = True
			for rgn in range(math.ceil(width/2), R+10, 10):
				theta_range_needed = 180/np.pi*2*math.asin(width/(2*rgn))
				if (np.any(r[math.floor(i-theta_range_needed/2):math.ceil(i+theta_range_needed/2)] < rgn)):
					viable = False
					
			if viable:
				viable_angles.append(theta)

		# Determine which viable angle will move you towards goal the fastest
		min_index = 0
		min_distance = 10000000
		for i, angle in enumerate(viable_angles):
			print("Viable angle: {0}".format(angle))
			x = location[0] + scale*R*np.cos(angle*np.pi/180)
			y = location[1] - scale*R*np.sin(angle*np.pi/180)

			# Simulate moving forward R movement at the current angle and calculate distance to goal
			sim_distance = math.sqrt(math.pow(x-goal[0], 2) + math.pow(y-goal[1], 2))
			if sim_distance < min_distance:		# Keep the minimum distance to find the most efficient angle
				min_distance = sim_distance
				min_index = i
				min_location = (int(x), int(y))

		cv2.arrowedLine(vis.img, location, min_location, (0,255,255), thickness=2)
		print("Best angle: {0}".format(viable_angles[min_index]))
		location = min_location
		direction = viable_angles[min_index]
				
		cv2.destroyAllWindows()
		cv2.imshow("blah", vis.img)
		k = cv2.waitKey(0)
		if k == ord('q'):
			break

if __name__ == "__main__":
	main()