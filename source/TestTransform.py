import cv2
import numpy as np
import pickle 


X,Y,Theta = pickle.load( open( "Translation.p", "rb" ))
xB,xE,yB,yE = pickle.load( open( "Crop.p", "rb" ))
h = pickle.load( open( "homographyMatrix.p", "rb" ))

width = 320
height = 240
dim = (width, height)
sliderMax = 1000

camera = input("input camera: ")
cam = cv2.VideoCapture(int(camera))
while True:
    ret_val, image = cam.read()
    rows =  image.shape[0]
    cols = image.shape[1]
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    image = cv2.warpPerspective(image, h, (4*image.shape[1],4*image.shape[0]))
    M = np.float32([[1,0,X-int(sliderMax/2)],[0,1,Y-int(sliderMax/2)]])
    image = cv2.warpAffine(image,M,(cols,rows))
    M = cv2.getRotationMatrix2D((cols/2,rows/2),Theta-90,1)
    image = cv2.warpAffine(image,M,(cols,rows))
    print(image.shape[0],image.shape[1])
    image = image[yB:yE, xB:xE]
    cv2.imshow('image', image)
    if cv2.waitKey(1) == 27: 
        break  # esc to quit