from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

img = cv2.imread('calibration.jpg')
rows,cols,ch = img.shape

#2ft
cv2.circle(img,(100,1820), 10, (0,0,255), -1)
cv2.circle(img,(705,1815), 10, (0,0,255), -1)
cv2.circle(img,(1315,1810), 10, (0,0,255), -1)
cv2.circle(img,(1935,1805), 10, (0,0,255), -1)
cv2.circle(img,(2550,1790), 10, (0,0,255), -1)

#3ft
cv2.circle(img,(270,1325), 10, (0,0,255), -1)
cv2.circle(img,(785,1320), 10, (0,0,255), -1)
cv2.circle(img,(1315,1310), 10, (0,0,255), -1)
cv2.circle(img,(1845,1305), 10, (0,0,255), -1)
cv2.circle(img,(2365,1305), 10, (0,0,255), -1)

#4ft
cv2.circle(img,(400,958), 10, (0,0,255), -1)
cv2.circle(img,(855,950), 10, (0,0,255), -1)
cv2.circle(img,(1310,945), 10, (0,0,255), -1)
cv2.circle(img,(1770,940), 10, (0,0,255), -1)
cv2.circle(img,(2230,935), 10, (0,0,255), -1)
#cv2.circle(img,(2565,940), 10, (0,0,255), -1)

#5
cv2.circle(img,(100,670), 10, (0,0,255), -1)
cv2.circle(img,(500,665), 10, (0,0,255), -1)
cv2.circle(img,(900,665), 10, (0,0,255), -1)
cv2.circle(img,(1310,655), 10, (0,0,255), -1)
cv2.circle(img,(1720,650), 10, (0,0,255), -1)
cv2.circle(img,(2130,645), 10, (0,0,255), -1)
cv2.circle(img,(2540,640), 10, (0,0,255), -1)

#6
cv2.circle(img,(225,440), 10, (0,0,255), -1)
cv2.circle(img,(580,435), 10, (0,0,255), -1)
cv2.circle(img,(945,435), 10, (0,0,255), -1)
cv2.circle(img,(1310,430), 10, (0,0,255), -1)
cv2.circle(img,(1670,420), 10, (0,0,255), -1)
cv2.circle(img,(2040,410), 10, (0,0,255), -1)
cv2.circle(img,(2425,410), 10, (0,0,255), -1)

#7
cv2.circle(img,(300,255), 10, (0,0,255), -1)
cv2.circle(img,(635,250), 10, (0,0,255), -1)
cv2.circle(img,(975,245), 10, (0,0,255), -1)
cv2.circle(img,(1305,240), 10, (0,0,255), -1)
cv2.circle(img,(1645,235), 10, (0,0,255), -1)
cv2.circle(img,(1970,225), 10, (0,0,255), -1)
#cv2.circle(img,(2425,420), 10, (0,0,255), -1)

#8
cv2.circle(img,(385,98), 10, (0,0,255), -1)
cv2.circle(img,(690,88), 10, (0,0,255), -1)
cv2.circle(img,(993,83), 10, (0,0,255), -1)
cv2.circle(img,(1305,75), 10, (0,0,255), -1)
cv2.circle(img,(1613,74), 10, (0,0,255), -1)
cv2.circle(img,(1924,65), 10, (0,0,255), -1)
cv2.circle(img,(2230,61), 10, (0,0,255), -1)

objectsPoints = []
imagePoints = []

#old points
realWorldPoints = np.array([[36,-24,0],[36,-12,0],[36,0,0],[36,12,0],[36,24,0],[48,-24,0],[48,-12,0],[48,0,0],[48,12,0],[48,24,0],[60,-24,0],[60,-12,0],[60,0,0],[60,12,0],[60,24,0],[60,36,0],[72,-24,0],[72,-12,0],[72,0,0],[72,12,0],[72,24,0],[72,36,0],[84,-24,0],[84,-12,0],[84,0,0],[84,12,0],[84,24,0],[84,36,0],[96,-24,0],[96,-12,0],[96,0,0],[96,12,0],[96,24,0],[96,36,0],[96,48,0]], dtype=np.float32)
pixPoints = np.array([[225,1905],[775,1905],[1335,1905],[1900,1905],[2460,1905],[380,1475],[855,1475],[1335,1475],[1805,1475],[2280,1475],[500,1175],[910,1175],[1335,1175],[1740,1175],[2155,1175],[2565,1175],[600,940],[955,940],[1335,940],[1685,940],[2060,940],[2430,940],[670,750],[955,750],[1335,750],[1650,750],[1990,750],[2305,750],[715,600],[1020,600],[1335,600],[1620,600],[1915,600],[2215,600],[2515,600]],dtype=np.float32)
objectsPoints.append(realWorldPoints)
imagePoints.append(pixPoints)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectsPoints, imagePoints, (rows,cols), None, None)
print("Camera Matrix\n")
print(mtx)
print("\nDistance Coefficients\n")
print(dist)
print("\nRotation Vectors\n")
print(rvecs)
print("\nTranslation Vectors\n")
print(tvecs)

'''
small = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
cv2.imshow('output', small)



if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()
'''
