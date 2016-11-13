# RasPi: 159.91.228.47

import time
import cv2
import numpy as np

def show(image, title):
	cv2.imshow(title, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
def grayscale(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	show(image, "Gray scale")
	return image

def blur(image, xblur, yblur):
	blur = cv2.GaussianBlur(image, (xblur, yblur), 0)
	show(blur, "Gaussian Blur")
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
	
	show(result, "color detection")
	
	return result

def black_white(image, thresh):
	bw = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
	show(bw, "Black and White")
	return bw

def canny(image, lower, upper):
	edges = cv2.Canny(image, lower, upper)
	show(edges, "Edge Detection")
	return edges
	
def main2():
	file = "whitelines5.jpg"
	img = cv2.imread(file, 1)

	# RED
	lower = np.array([0, 50, 50])
	upper = np.array([10, 255, 255])

	# GREEN
	# lower = np.array([50, 0, 0])
	# upper = np.array([70, 255, 255])

	# BLUE
	# lower = np.array([110, 0, 0])
	# upper = np.array([130, 255, 255])

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	result = cv2.bitwise_and(img, img, mask=mask)
	show(result, "final")
	
def main1():
	file = "whitelines1.jpg"
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
	file = "whitelines5.jpg"
	img = cv2.imread(file, 1)
	
	img = grayscale(img)
	
	img = blur(img, 9,9)
	
	img = colorDetect(img, 190, 255, False)
	
	img = canny(img, 50, 350)
	
if __name__ == "__main__":
	main1()
	
	
	
"""	lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
	if not lines:
		print "No lines"
		return
		
	for line in lines:
		for rho, theta in line:#
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			cv2.line(img,(x1,y1),(x2,y2), (255, 0, 0), 2)
			
	cv2.imshow("lines", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()"""
	