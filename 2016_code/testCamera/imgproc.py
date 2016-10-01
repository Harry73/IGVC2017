from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(640,480))

time.sleep(0.5)

def get_canny(frame, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(frame, lower, upper)
 
	# return the edged image
	return edged	

#Capture frames from camera 
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#get numpy array representing image 
	image = frame.array
	
	#do image processing
	
	#convert to grayscale	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	#convert to HSV
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	#Apply Gaussian Blur
	blur = cv2.GaussianBlur(hsv, (3,3),0)
	gray_blur = cv2.GaussianBlur(gray, (3,3),0)
	
	
	#Blue
	lower_blue = np.array([70,50,50])
	upper_blue = np.array([130,255,255])
	blue_mask = cv2.inRange(blur, lower_blue, upper_blue)
	
	#Red
	lower_red = np.array([0, 50, 50])
	upper_red = np.array([10, 255, 255])
	red_mask = cv2.inRange(blur, lower_red, upper_red)
	
	#White
	white_mask = cv2.inRange(gray_blur, 200, 255)
	
	#Output Image
	mask = blue_mask + red_mask
	colors = cv2.bitwise_and(image, image, mask = mask)
	edges = get_canny(colors, 0.33);
	output = white_mask + edges
	
	#cv2.imshow("White Lines", white_mask)
	#cv2.imshow("Objects", edges)
	cv2.imshow("Image", output);
	key = cv2.waitKey(1) & 0xFF
	
	# clear stream for next frame 
	rawCapture.truncate(0)
	
	
	if key == ord("q"):
		break
