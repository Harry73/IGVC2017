from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
'''
camera=PiCamera()
camera.resolution=(320,240)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(640,480))
'''


img = cv2.imread("grasstest2.jpg")
small = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
print (small.shape) 
#blur = cv2.GaussianBlur(small,(5,5),0)
blur = cv2.GaussianBlur(small,(5,5),0)


#cv2.imshow('3,3',blur2)

gray = cv2.cvtColor(blur,cv2.COLOR_RGB2GRAY)
#hsv = cv2.cvtColor(blur,cv2.COLOR_RGB2HSV)
	
(T,thresh) = cv2.threshold(gray,190,255,cv2.THRESH_TOZERO)

cv2.imshow("threshName",thresh)
cv2.imshow("gray",gray)

#Make mask for white 
'''
sensitivity = 90
lower = np.array([0,0,255-sensitivity], dtype=np.uint8)
upper = np.array([255,sensitivity,255], dtype = np.uint8)
'''

#mask = cv2.inRange(hsv, lower, upper)
#result = cv2.bitwise_and(blur, blur, mask= mask)


if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()



