from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

img = cv2.imread('70degrees.jpg')
rows,cols,ch = img.shape

src = np.zeros((rows,cols,3),dtype=np.float32)

#initialize arrays
objectsPoints = []
imagePoints = []

# perspective points
pts1 = np.array([[-24,60],[-24,84],[24,108],[24,156]], dtype=np.float32)
pts2 = np.array([[440,1670],[630,1250],[1780,925],[1635,690]], dtype=np.float32)

# get perspective Matrix
M = cv2.getPerspectiveTransform(pts2,pts1)

# map points
realWorldPoints = np.array([[-24,60,0],[0,60,0],[24,60,0],[-24,84,0],[0,84,0],[24,84,0],[-24,108,0],[0,108,0],[24,108,0],[-24,132,0],[0,132,0],[24,132,0],[-24,156,0],[0,156,0],[24,156,0]], dtype=np.float32)
imgpts = np.array([((440,1670),(1285,1670),(2105,1670),(630,1250),(1275,1250),(1905,1250),(745,985),(1270,985),(1780,985),(825,815),(1265,815),(1705,815),(890,690),(1263,690),(1635,690))],dtype = np.float32)

# use perspective Matrix to remap img points
converted = cv2.perspectiveTransform(imgpts, M)

# insert all points into proper array for formatting
objectsPoints.append(realWorldPoints)
#imagePoints.append(converted)
imagePoints.append(imgpts)

# get all Camera Properties
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectsPoints, imagePoints, (rows,cols), None, None)

rmatrix = cv2.Rodrigues(rvecs[0])[0]
r1 = [rmatrix[0][0],rmatrix[1][0],rmatrix[2][0]]
r2 = [rmatrix[0][1],rmatrix[1][1],rmatrix[2][1]]
tmatrix = tvecs[0]
t = [tmatrix[0][0],tmatrix[1][0],tmatrix[2][0]]
h = [r1,r2,t]
H = mtx*h

'''
print("Camera Matrix\n")
#mtx = np.append(mtx,[[0],[0],[0]],1)
print(mtx)
print("\nDistance Coefficients\n")
print(dist)
print("\nRotation Matrix\n")
#rmatrix = np.append(rmatrix,[(0,0,0)],0)
print(rmatrix)
print("\nTranslation Matrix\n")
#tmatrix = np.append(tmatrix,[(1)])
#tmatrix = np.reshape(tmatrix, (4,1))
print(tmatrix)
'''

# load image with white lines and prepare it for processing
img = cv2.imread("whitelines2.jpg")
small = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
blur1 = cv2.GaussianBlur(hsv, (3,3),0)

# identify green in image
lower = np.array([20, 90, 50])
upper = np.array([60, 255, 180])
mask = cv2.inRange(blur1, lower, upper)

# make a grayscale copy of the image for white pixel detection
gray = cv2.cvtColor(small,cv2.COLOR_RGB2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)

# detect white lines in grayscale image
(T,thresh1) = cv2.threshold(blur,140,255,cv2.THRESH_TOZERO)
(T,thresh2) = cv2.threshold(thresh1,255,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# subtract non grass white pixels from grayscale image
colors = thresh2 - mask

# initialize array for storing white pixels
whitepts = np.array([((0,0))],dtype=np.float32)

# obtain all remaining white points in image
for x in range(647,0,-1):
	for y in range(150,480,1):
		if colors[y,x] == 255:
			whitepts = np.append(whitepts,[(y,x)],0)

# store white pixels in properly formatted array			
whiteness = np.array([(whitepts)],dtype = np.float32)

# perspective transform all white pixels
#converted = cv2.perspectiveTransform(whiteness,M)

# initialize array for storing line pixels
linepts = np.array([((0,0,0))],dtype=np.float32)

# insert 1 and the end of every 2d coordinate per white pixel for 3D world mapping
for x in range(0,len(whiteness[0])):
#for x in range(0,1):
	# create film 2d points
	# lineworld  = np.insert(converted[0][x],2, 1)
	lineworld  = np.insert(whiteness[0][x],2, 1)
	lineworld = np.reshape(lineworld, (3,1))
	T = np.dot(np.linalg.inv(rmatrix), tmatrix)
	D = np.dot(np.linalg.inv(rmatrix) , lineworld)
	#print(T)
	#print(D)
	X = (-T[2] / D[2] ) * D[0] + T[0]
	Y = (-T[2] / D[2] ) * D[1] + T[1]
	'''
	lineworld[0] = (lineworld[0] - mtx[0][2]) / mtx[0][0]
	lineworld[1] = (lineworld[1] - mtx[1][2]) / mtx[1][1]
	projection = H * lineworld
	lineworld = 
	'''
	
	linepts = np.append(linepts,[(X[0], Y[0], 0)],0)
	
print(linepts)
