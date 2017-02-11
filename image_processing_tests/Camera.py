# Odroid: 159.91.228.92

import cv2
import numpy as np

# Take picture from camera and apply Hough lines transform
def main():
	cap = cv2.VideoCapture(0)
	
	while True:
		ret, frame = cap.read()
	
		edges = cv2.Canny(frame, 50, 150)
		lines = cv2.HoughLines(edges, 1, np.pi/180, 400)
		
		for rho, theta in lines[0]:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			# Draw lines on the original image in red
			cv2.line(frame, (x1,y1), (x2,y2), (0, 0, 255), 2)
		
		# Display the resulting frame
		cv2.imshow('frame',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
	cap.release()
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	main()
