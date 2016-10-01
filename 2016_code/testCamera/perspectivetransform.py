from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

src = np.array(((25,25),(200,20),(35,210),(215,200)),dtype = np.float32)
dest = np.array(((-50,-50),(50,-50),(-50,50),(50,50)),dtype=np.float32)
img = cv2.imread('70degrees.jpg')
pts1 = np.array(((-24,60),(-24,84),(24,108),(24,156)), dtype=np.float32)
pts2 = np.array(((440,1670),(630,1250),(1780,925),(1635,690)), dtype=np.float32)
m2 = cv2.getPerspectiveTransform(pts2,pts1)

m = cv2.getPerspectiveTransform(src,dest)

original = np.array([((42,42),(30,100),(150,75))],dtype=np.float32)
imgpts = np.array([((440,1670),(1285,1670),(2105,1670),(630,1250),(1275,1250),(1905,1250),(745,985),(1270,985),(1780,985),(825,815),(1265,815),(1705,815),(890,690),(1263,690),(1635,690))],dtype = np.float32)
converted = cv2.perspectiveTransform(original,m)
print(converted)
converted2 =cv2.perspectiveTransform(imgpts,m2)
print(converted2)
#print(converted2)
