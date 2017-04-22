#example of how to use the Kalman filter
#of course you will need all the libraries in EKF

import math import sqrt
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import ExtendedKalmanFilter
from numpy import eye, array, asarray
import numpy as np

#instantiate the gps
gps = GPS()

#get the first position
z = gps.getPosition()


dt = 0.05
range_std = 5. #means meters

#instantiate the filter
filterk = ExtendedKalmanFilter(2,1,0)#1 type of value of position, but in 2 dimensions. sensor provides position in (x,y) so use 2

#insert first position
filterk.x = array(z)
#pretty sure this sets up the taylor series
filterk.F = eye(2) + array([[0,1],[0,0]])*dt
#sets the uncertainty
filterk.R = np.diag([range_std**2])
#trains it using white noise?
filterk.Q{0:2,0:2] = Q_discrete_white_noise(2, dt=dt, var=0.1)
filterk.Q[2,2] = 0.1
#covariance matrix
filterk.P *= 50

#Hjacobian function
def HJacobian_at(x):
	x_dist = x[0]
	y_dist = x[2]
	denom = sqrt(x_dist**2 + y_dist**2)
	return array([x_dist/denom, 0., y_dist/denom]])

#measurement update function
def hx(x):
	return (x[0]**2 + x[2]**2) ** 0.5

#put new z value in
filterk.predict_update(array([z]), HJacobian_at, hx) #this maaaaay need to be formatted differently, otherwise just put the longitude and lattitude as an array [x,y]

#get the predicted value
xs.append(filterk.x)
xs = asarray(xs)



