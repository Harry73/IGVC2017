from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
camera=PiCamera()
camera.resolution=(320,240)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(640,480))

time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_vbideo_port=True):
	image=frame.array

	cv2.imshow("Frame", image)
	key=cv2.waitkey(1) & 0xFF

	rawCapture.truncate(0)

	if key ==ord("q"):
		break
