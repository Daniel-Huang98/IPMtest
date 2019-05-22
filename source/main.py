import cv2
import numpy as np
image = cv2.imread("./../sampleImages/tape1.jpg")
cv2.imshow("image",image)
pts_src = np.array([[174, 377],[301, 44],[545, 51],[659,379]])
pts_dst = np.array([[174, 377],[174, 0],[659, 0],[659,379]])
h, status = cv2.findHomography(pts_src, pts_dst)
im_out = cv2.warpPerspective(image, h, (image.shape[1],image.shape[0]))
cv2.imshow("image1",im_out)
cv2.resizeWindow('image', 600,600)
cv2.waitKey(0)
