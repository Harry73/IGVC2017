from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

'''
camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture, format = "bgr")
'''

file= 'output.jpg'
img = cv2.imread(file)

x,y, ch = img.shape

print(x)
print(y)
newx = x/4
newy = y/4

#newx,newy = img.shape[1]/4,img.shape[0]/4
small = cv2.resize(img, (0,0), fx=0.15, fy=0.15)

#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#dst = cv2.cornerHarris(gray,2,3,.04)

cv2.imshow('input',small)


if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()
	
