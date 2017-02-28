# Odroid: 159.91.228.92

import os
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
	right_cam_index = int(os.readlink("/dev/right_cam")[-1])
	left_cam_index = int(os.readlink("/dev/left_cam")[-1])
	right_cam = cv2.VideoCapture(right_cam_index)
	left_cam = cv2.VideoCapture(left_cam_index)

	while True:
		ret, right_frame = right_cam.read()
		ret, left_frame = left_cam.read()

		right_frame = process(right_frame)
		left_frame = process(left_frame)


		# Display the resulting frame
		cv2.imshow('right frame', right_frame)
		cv2.imshow('left frame', left_frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	right_cam.release()
	left_cam.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
