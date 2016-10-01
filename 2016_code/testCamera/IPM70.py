from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

img = cv2.imread('70degrees.jpg')
rows,cols,ch = img.shape

src = np.zeros((rows,cols,3),dtype=np.float32)

#5ft
cv2.circle(img,(440,1670), 10, (0,0,255), -1)
cv2.circle(img,(1285,1670), 10, (0,0,255), -1)
cv2.circle(img,(2105,1670), 10, (0,0,255), -1)

#7ft
cv2.circle(img,(630,1250), 10, (0,0,255), -1)
cv2.circle(img,(1275,1250), 10, (0,0,255), -1)
cv2.circle(img,(1905,1250), 10, (0,0,255), -1)

#9
cv2.circle(img,(745,985), 10, (0,0,255), -1)
cv2.circle(img,(1270,985), 10, (0,0,255), -1)
cv2.circle(img,(1780,985), 10, (0,0,255), -1)

#11
cv2.circle(img,(825,815), 10, (0,0,255), -1)
cv2.circle(img,(1265,815), 10, (0,0,255), -1)
cv2.circle(img,(1705,815), 10, (0,0,255), -1)

#13
cv2.circle(img,(890,690), 10, (0,0,255), -1)
cv2.circle(img,(1263,690), 10, (0,0,255), -1)
cv2.circle(img,(1635,690), 10, (0,0,255), -1)

#initialize arrays
objectsPoints = []
imagePoints = []


pts1 = np.array([[-24,60],[-24,84],[24,108],[24,156]], dtype=np.float32)
pts2 = np.array([[440,1670],[630,1250],[1780,925],[1635,690]], dtype=np.float32)
M = np.array((3,3),dtype=np.float32)
#new points
#realWorldPoints = np.array([[-24,60,0],[0,60,0],[24,60,0],[-24,84,0],[0,84,0],[24,84,0],[-24,108,0],[0,108,0],[24,108,0],[-24,132,0],[0,132,0],[24,132,0],[-24,156,0],[0,156,0],[24,156,0]], dtype=np.float32)
#pixPoints = np.array([[440,1670],[1285,1670],[2105,1670],[630,1250],[1275,1250],[1905,1250],[745,985],[1270,985],[1780,985],[825,815],[1265,815],[1705,815],[890,690],[1263,690],[1635,690]],dtype=np.float32)

#M = cv2.getPerspectiveTransform(pixPoints,realWorldPoints)

M = cv2.getPerspectiveTransform(pts2,pts1)
pixPoints = np.array([[440,1670,0],[1285,1670,0],[2105,1670,0],[630,1250],[1275,1250],[1905,1250],[745,985],[1270,985],[1780,985],[825,815],[1265,815],[1705,815],[890,690],[1263,690],[1635,690]],dtype=np.float32)

converted = cv2.perspectiveTransform(img,M,src)

#objectsPoints.append(realWorldPoints)
#imagePoints.append(pixPoints)


#cv2.perspectiveTransform(img,src,M)
#H,matches = cv2.findHomography(pts2,pts1,cv2.RANSAC)
small = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
print()
cv2.imshow('output', small)
cv2.imwrite('cameracalibration.png',small)

#print(src)

#ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectsPoints, imagePoints, (rows,cols), None, None)
#print("Camera Matrix\n")
#print(mtx)
#print("\nDistance Coefficients\n")
#print(dist)
#print("\nRotation Vectors\n")
#print(rvecs)
#print("\nTranslation Vectors\n")
#print(tvecs)






if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()
