# RasPi: 159.91.228.47
# Odroid: 159.91.228.92

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

def colorDetect(image, lower, upper):
	hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
	lower = np.array(lower)
	upper = np.array(upper)	
	
	mask = cv2.inRange(hsv, lower, upper)
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
		
# For playing
def main1():
	file = "whitelines5.jpg"
	original = cv2.imread(file)
	img = original	# img to play with
	show(img, "original")
	
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	show(img, "hsv")
	
	# Prepare for color shifting
	img = img.astype(np.int32)
	
	# Remove color. 012 = BGR = HSV
	#img[:,:,0] = img[:,:,0]-100
	#img[:,:,1] = img[:,:,1]-100
	img[:,:,2] = 0
	
	# Get back in the right range and convert back to a normal picture
	img = np.clip(img, 0, 255)
	img = img.astype(np.uint8)
	
	show(img, "colored image")
	
	img = colorDetect(img, [0, 0, 0], [20, 255, 255])
	
	img = blur(img, 31, 31)
	#img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
	#show(img, "less noise")
	
	#img = canny(img, 0, 50)
	
	img = grayscale(img)
	img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)[1]
	show(img, "threshold")
	
	lines = cv2.HoughLines(img, 1, np.pi/180, 400)
		
	for line in lines:
		for rho, theta in line:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			# Draw lines on the original image in red
			cv2.line(original,(x1,y1),(x2,y2), (0, 0, 255), 2)
	
	show(original, "hough")
	

# "Normal" processing sequence
def main():
	file = "whitelines5.jpg"
	original = cv2.imread(file)
	show(original, "original")
	
	# Prepare for color shifting
	img = original.astype(np.int32)
	
	# Remove color? 0=B, 1=G, 2=R
	#img[:,:,0] = img[:,:,0]-100
	#img[:,:,1] = img[:,:,1]-100
	img[:,:,2] = 0
	
	# Get back in the right range and convert back to a normal picture
	img = np.clip(img, 0, 255)
	img = img.astype(np.uint8)
	
	show(img, "colored image")
	
	img = colorDetect(img, [0, 0, 0], [30, 255, 255])
	
	img = blur(img, 11, 11)
	#img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
	#show(img, "less noise")
	
	#img = canny(img, 0, 50)
	
	img = grayscale(img)
	img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)[1]
	show(img, "thresher")
	
	lines = cv2.HoughLines(img, 1, np.pi/180, 400)
		
	for line in lines:
		for rho, theta in line:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			# Draw lines on the original image in red
			cv2.line(original,(x1,y1),(x2,y2), (0, 0, 255), 2)
	
	show(original, "hough")
	
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
	