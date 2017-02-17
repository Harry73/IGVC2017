# Odroid: 159.91.228.92

import cv2
import numpy as np

def process(frame):
	edges = cv2.Canny(frame, 50, 150, apertureSize=3)
	lines = cv2.HoughLines(edges, 1, np.pi/180, 150)

	if lines != None:
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

				cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

	return frame

# Take picture from camera and apply Hough lines transform
def main():
	cam1 = cv2.VideoCapture(0)
	cam2 = cv2.VideoCapture(1)

	while True:
		ret, frame1 = cam1.read()
		ret, frame2 = cam2.read()

		frame1 = process(frame1)
		frame2 = process(frame2)


		# Display the resulting frame
		cv2.imshow('frame1', frame1)
		cv2.imshow('frame2', frame2)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cam1.release()
	cam2.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
