import numpy as np
import cv2

cont = 0
while (cont < 1):
	try:
		blue = int(input("Input a blue value\n"))
	except ValueError:
		print("Not a number")
	try:
		green = int(input("Input a green value\n"))
	except ValueError:
		print("Not a number")
	try:
		red = int(input("Input a red value\n"))
	except ValueError:
		print("Not a number")
	color = np.uint8([[[blue, green, red]]])
	hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
	print(hsv)
	cont = int(input("Continue Input Values?\n"))
