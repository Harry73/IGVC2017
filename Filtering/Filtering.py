#example of how to use the Kalman filter
#of course you will need all the libraries in EKF

import ExtendedKalmanFilter

#instantiate the filter
filterk = ExtendedKalmanFilter(2,2,0)#1 type of value of position, but in 2 dimensions. sensor provides position in (x,y) so use 2

#instantiate the gps
gps = GPS()

#get the first position
z = gps.getPosition()

#put new z value in
filterk.predict_update(z) #this maaaaay need to be formatted differently, otherwise just put the longitude and lattitude as an array [x,y]

#get the predicted value
x = filkerk.x



