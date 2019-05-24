import cv2
import numpy as np

title_window = 'img'

alpha_slider_max = 100
cv2.namedWindow('image')

def nothing(x):
    pass
cv2.createTrackbar('X','image',50,100,nothing)
cv2.createTrackbar('Y','image',50,100,nothing)
cv2.createTrackbar('Theta','image',90,180,nothing)


img = cv2.imread('./../sampleImages/messi.jpeg',1)
rows =  img.shape[0]
cols = img.shape[1]

X = 0
Y = 0
Theta = 0

while(1):
    X = cv2.getTrackbarPos('X','image')
    Y = cv2.getTrackbarPos('Y','image')
    Theta = cv2.getTrackbarPos('Theta','image')

    M = np.float32([[1,0,X-50],[0,1,Y-50]])
    image = cv2.warpAffine(img,M,(cols,rows))
    M = cv2.getRotationMatrix2D((cols/2,rows/2),Theta-90,1)
    image = cv2.warpAffine(image,M,(cols,rows))

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    cv2.imshow('image',image)


cv2.waitKey(0)
cv2.destroyAllWindows()