import time
import cv2
import numpy as np

img = cv2.imread('whitelines2.jpg')
rows,cols,ch = img.shape

pts2 = np.float32([[0,0],[2592,0],[0,1944],[2592,1944]])
pts1 = np.float32([[150,600],[2400,600],[0,1600],[2592,1600]])
 
M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(img,M,(2592,1944))

print(dst)

smallimg = cv2.resize(img, (0,0),fx=0.25,fy=0.25)
small = cv2.resize(dst, (0,0), fx=0.25, fy=0.25)

cv2.imshow("original",smallimg)
cv2.imshow("perspective", small)

if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()

