import cv2
import numpy as np
import pickle 


class Camera():
    def __init__(self):
        pass

    def setCamera(self):
        self.camera = input("input camera: ")
        self.cam = cv2.VideoCapture(int(self.camera))
        ret_val, image = self.cam.read()
        self.rows =  image.shape[0]
        self.cols = image.shape[1]


class IPM(Camera):
    def __init__(self):
        self.counter = 0
        self.sliderMax = 1000
        self.windowName = 'image'
        self.pts_src = np.array([[174, 377],[301, 44],[545, 51],[659,379]])
        self.X = 0
        self.Y = 0
        self.Theta = 0
        self.XCrop = 50
        self.YCrop = 50
        self.XMiddle = 0
        self.YMiddle = 0
        self.initialise()

    def initialise(self):
        self.setCamera()
        self.setDimensions()
        self.setWindow()
        self.SetMouseCallBack()
        self.setSliders()   

    def TrainAll(self):
        self.TrainHomography()
        self.TrainTransform()
        self.TrainCrop()

    def setDimensions(self):
        width = 320
        height = 240
        self.dim = (width, height)
    
    def TrainHomography(self):
        while(self.counter < 4):
            ret_val, image = self.cam.read()
            image = cv2.resize(image, self.dim, interpolation = cv2.INTER_AREA)
            cv2.line(image,(int(image.shape[1]/2),0),(int(image.shape[1]/2),image.shape[0]),(0,0,0),5)
            cv2.imshow(self.windowName,image)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('b'):
                break
        print(self.pts_src)
        pts_dst = np.array([[690, 620],[690, 720],[790, 720],[790,620]])
        h, status = cv2.findHomography(self.pts_src, pts_dst)
        self.h = h
        pickle.dump( h, open( "homographyMatrix.p", "wb" ))


    def TrainTransform(self):
        while True:
            ret_val, image = self.cam.read()
            self.X = cv2.getTrackbarPos('X',self.windowName)
            self.Y = cv2.getTrackbarPos('Y',self.windowName)
            self.Theta = cv2.getTrackbarPos('Theta',self.windowName)
            #tranform the shit here
            image = self.TransformEverything(image)
            cv2.imshow(self.windowName, image)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        pickle.dump([self.X,self.Y,self.Theta], open("Translation.p", "wb" ))
            
	

    def TrainCrop(self):
        while True:
            ret_val, image = self.cam.read()
            image = self.TransformEverything(image)
            xB = int(image.shape[1]/2)-cv2.getTrackbarPos('Xwidth',self.windowName)
            yB = cv2.getTrackbarPos('YBegin',self.windowName)
            xE = int(image.shape[1]/2)+cv2.getTrackbarPos('Xwidth',self.windowName)
            yE = cv2.getTrackbarPos('YEnd',self.windowName)
            cv2.line(image,(xB,0),(xB,image.shape[0]),(255,0,0),5)
            cv2.line(image,(xE,0),(xE,image.shape[0]),(0,0,255),5)
            cv2.line(image,(0,yB),(image.shape[1],yB),(255,0,0),5)
            cv2.line(image,(0,yE),(image.shape[1],yE),(0,0,255),5)
            cv2.imshow(self.windowName, image)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit

    def TransformEverything(self,image):
        image = cv2.resize(image, self.dim, interpolation = cv2.INTER_AREA)
        image = cv2.warpPerspective(image, self.h, (4*image.shape[1],4*image.shape[0]))
        M = np.float32([[1,0,self.X-int(self.sliderMax/2)],[0,1,self.Y-int(self.sliderMax/2)]])
        image = cv2.warpAffine(image,M,(self.cols,self.rows))
        M = cv2.getRotationMatrix2D((self.cols/2,self.rows/2),self.Theta-90,1)
        image = cv2.warpAffine(image,M,(self.cols,self.rows))
        cv2.line(image,(int(image.shape[1]/2),0),(int(image.shape[1]/2),image.shape[0]),(0,0,0),5)
        return image


    def SetMouseCallBack(self):
        cv2.setMouseCallback(self.windowName,self.MouseCallBack)

    def MouseCallBack(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print (x,y)
            print(self.pts_src[self.counter][0])
            print(self.pts_src[self.counter][1])
            self.pts_src[self.counter][0] = x
            self.pts_src[self.counter][1] = y
            self.counter+=1
    
    def setWindow(self):
        cv2.namedWindow(self.windowName)

    def setSliders(self):
        cv2.createTrackbar('X','image',int(self.sliderMax/2),self.sliderMax,self.nothing)
        cv2.createTrackbar('Y','image',int(self.sliderMax/2),self.sliderMax,self.nothing)
        cv2.createTrackbar('Theta','image',90,180,self.nothing)
        cv2.createTrackbar('Xwidth','image',100,500,self.nothing)
        cv2.createTrackbar('YBegin','image',100,500,self.nothing)
        cv2.createTrackbar('YEnd','image',400,500,self.nothing)

    def nothing(self,x):
        pass