# RasPi: 159.91.228.47

import time
import cv2
import numpy as np
	
def grayscale(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return image

def blur(image, xblur, yblur):
	blur = cv2.GaussianBlur(image, (xblur, yblur), 0)
	return blur

def colorDetect(image, lower, upper, hsv):
	if hsv:
		img = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
		lower = np.array(lower)
		upper = np.array(upper)
	else:
		img = image			
		
	mask = cv2.inRange(img, lower, upper)	
	result = cv2.bitwise_and(image, image, mask=mask)
		
	return result

def black_white(image, thresh):
	bw = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
	return bw

def canny(image, lower, upper):
	edges = cv2.Canny(image, lower, upper)
	return edges
		
def main1():
	file = "wallpaper.jpg"
	img = cv2.imread(file, 1)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

	img[:,:,0] = img[:,:,0]
	#img[:,:,1] = img[:,:,1]+60
	#img[:,:,2] = img[:,:,2]-210
	
	show(img, "image")
	
#	img = colorDetect(img, [0,0,0], [255,255,255], True)

	img = blur(img, 25, 25)
	
#	img = grayscale(img)
	
	img = canny(img, 0, 50)
	
def main():
	file = "wallpaper.jpg"
	start = time.time()

	img = cv2.imread(file, 1)
#	img = grayscale(img)
	img = blur(img, 9,9)
	img = colorDetect(img, 190, 255, False)
	img = canny(img, 50, 350)
	
	end = time.time()
	
	print(end-start)
	
if __name__ == "__main__":
	main()
	
	
	
