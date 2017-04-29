# Example of how to use the Kalman filter
# Of course you will need all the libraries in EKF

import os
import numpy as np
from GPS import GPS
from math import sqrt
from numpy import eye, array, asarray
from multiprocessing import Semaphore, Manager
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter

def main():
	gps_n = Semaphore(0)
	gps_s = Semaphore(1)
	gps_coords_stack = Manager().list()

	gps = GPS(gps_coords_stack, gps_n, gps_s)

	gps.start()

	# Get the first position
	z = gps.getPosition()

	dt = 0.05
	range_std = 5. # Means meters

	# Instantiate the filter
	filterk = ExtendedKalmanFilter(2, 1, 0) # 1 type of value of position, but in 2 dimensions. sensor provides position in (x,y) so use 2

	# Insert first position
	filterk.x = array(z)
	# Pretty sure this sets up the taylor series
	filterk.F = eye(2) + array([[0,1], [0,0]])*dt
	# Sets the uncertainty
	filterk.R = np.diag([range_std**2])
	# Trains it using white noise?
	filterk.Q[0:2, 0:2] = Q_discrete_white_noise(2, dt=dt, var=0.1)
	filterk.Q[2, 2] = 0.1
	# Covariance matrix
	filterk.P *= 50

	for i in range(10):
		# Pull a value from the GPS stack
		gps_n.acquire()
		gps_s.acquire()
		result = gps_coords_stack.pop()
		gps_s.release()

		# Put new z value in
		filterk.predict_update(array(result), HJacobian_at, hx) #this maaaaay need to be formatted differently, otherwise just put the longitude and lattitude as an array [x,y]

		# Get the predicted value
		np.append(xs, filterk.x)
		print(filterk.x)

# Hjacobian function
def HJacobian_at(x):
	x_dist = x[0]
	y_dist = x[2]
	denom = sqrt(x_dist**2 + y_dist**2)
	return array([x_dist/denom, 0., y_dist/denom])

# Measurement update function
def hx(x):
	return (x[0]**2 + x[2]**2) ** 0.5

if __name__ == "__main__":
	main()
