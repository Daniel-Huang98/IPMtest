import cv2
import numpy as np
import pickle 

pts_src = np.array([[174, 377],[301, 44],[545, 51],[659,379]])
pts_dst = np.array([[174, 377],[174, 0],[659, 0],[659,379]])

counter = 0



def nothing(x):
    pass

def readmouse(event,x,y,flags,param):
	global counter
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print (x,y)
		print(pts_src[counter][0])
		print(pts_src[counter][1])
		pts_src[counter][0] = x;
		pts_src[counter][1] = y;
		counter+=1


cv2.namedWindow('image')
sliderMax = 1000

cv2.createTrackbar('X','image',int(sliderMax/2),sliderMax,nothing)
cv2.createTrackbar('Y','image',int(sliderMax/2),sliderMax,nothing)
cv2.createTrackbar('Theta','image',90,180,nothing)

cv2.createTrackbar('Xwidth','image',100,500,nothing)
#cv2.createTrackbar('XEnd','image',400,500,nothing)
cv2.createTrackbar('YBegin','image',100,500,nothing)
cv2.createTrackbar('YEnd','image',400,500,nothing)





camera = input("input camera: ")
cam = cv2.VideoCapture(int(camera))
print("[0] re-tune matrix \n[1] reload old matrix")

val = input()
if(int(val) == 0):
	cv2.namedWindow('image')
	cv2.setMouseCallback('image',readmouse)
	while(counter < 4):
		ret_val, image = cam.read()
		cv2.line(image,(int(image.shape[1]/2),0),(int(image.shape[1]/2),image.shape[0]),(0,0,0),5)
		cv2.imshow("image",image)
		k = cv2.waitKey(1) & 0xFF
		if k == ord('b'):
			break
	print(pts_src);
	
	pts_dst = np.array([[690, 620],[690, 720],[790, 720],[790,620]])
	#cv2.destroyAllWindows()
	h, status = cv2.findHomography(pts_src, pts_dst)
	pickle.dump( h, open( "homographyMatrix.p", "wb" ))
	print(image.shape[0],image.shape[1])

h = pickle.load( open( "homographyMatrix.p", "rb" ))
ret_val, image = cam.read()
rows =  image.shape[0]
cols = image.shape[1]

X = 0
Y = 0
Theta = 0

XCrop = 50
YCrop = 50
XMiddle = 0
YMiddle = 0

print(h)
while True:
	ret_val, image = cam.read()
	img = cv2.warpPerspective(image, h, (4*image.shape[1],4*image.shape[0]))

	X = cv2.getTrackbarPos('X','image')
	Y = cv2.getTrackbarPos('Y','image')
	Theta = cv2.getTrackbarPos('Theta','image')

	M = np.float32([[1,0,X-int(sliderMax/2)],[0,1,Y-int(sliderMax/2)]])
	image = cv2.warpAffine(img,M,(cols,rows))
	M = cv2.getRotationMatrix2D((cols/2,rows/2),Theta-90,1)
	image = cv2.warpAffine(image,M,(cols,rows))
	#image = cv2.resize(image,(4*image.shape[1],4*image.shape[0]))
	cv2.line(image,(int(image.shape[1]/2),0),(int(image.shape[1]/2),image.shape[0]),(0,0,0),5)
	#crop shit here
	xB = int(image.shape[1]/2)-cv2.getTrackbarPos('Xwidth','image')
	yB = cv2.getTrackbarPos('YBegin','image')
	xE = int(image.shape[1]/2)+cv2.getTrackbarPos('Xwidth','image')
	yE = cv2.getTrackbarPos('YEnd','image')
	cv2.line(image,(xB,0),(xB,image.shape[0]),(255,0,0),5)
	cv2.line(image,(xE,0),(xE,image.shape[0]),(0,0,255),5)
	cv2.line(image,(0,yB),(image.shape[1],yB),(255,0,0),5)
	cv2.line(image,(0,yE),(image.shape[1],yE),(0,0,255),5)
	#crop shit here
	cv2.imshow('image', image)
	if cv2.waitKey(1) == 27: 
		break  # esc to quit

pickle.dump( [X,Y,Theta], open("Translation.p", "wb" ))
pickle.dump( [xB,xE,yB,yE], open("Crop.p", "wb" ))
print(image.shape[0],image.shape[1])



cv2.destroyAllWindows()
