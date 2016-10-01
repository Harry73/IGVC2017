from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

camera = PiCamera()
camera.framerate = 10
rawCapture = PiRGBArray(camera)

cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)

time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# RED
	lower = np.array([0, 50, 50])
	upper = np.array([10, 255, 255])

	# GREEN
	# lower = np.array([50, 0, 0])
	# upper = np.array([70, 255, 255])

	# BLUE
	# lower = np.array([110, 0, 0])
	# upper = np.array([130, 255, 255])

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	result = cv2.bitwise_and(image, image, mask= mask)
	cv2.imshow("image", result)

	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

