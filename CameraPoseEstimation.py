import cv2 as cv
import numpy as np
import glob

# Function to be called in the  main program
#CalibrateCamera and return Camera Matrix and Distrotion Coefficients
def CalibrateCamera():
    # Getting all the paths to the sample images stored in /images/..
    images = glob.glob('images/*.jpg')
    CHECKERBOARD = (7,7)#Since i am using 8*8 checker board (only count the inside corners)
    criteria = (cv.TermCriteria_EPS + cv.TERM_CRITERIA_MAX_ITER,30,0.001)
    # For storing object points and it's corresponding image points
    objPoints=[]
    imgPoints=[]
    #Storing object points in the objPoints[]
    # np.mgrid() returns multidimensional mesh grid
    # eg: np.mgrid[0:2,0:2] returns
    #   [[[0,1],[0,1]],
    #    [[0,0],[1,1]]]
    #the obtained matrix is arranged such that is correspeonds to the obj coordinates
    objp = np.zeros((1,CHECKERBOARD[0]*CHECKERBOARD[1],3),np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0],0:CHECKERBOARD[1]].T.reshape(-1,2)

    for image in images:
        img = cv.imread(image)
        # Converting the image to grayscale
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        ret,corners = cv.findChessboardCorners(gray,CHECKERBOARD,cv.CALIB_CB_ADAPTIVE_THRESH+cv.CALIB_CB_FAST_CHECK+cv.CALIB_CB_NORMALIZE_IMAGE)
        # if all the 7*7 corners is succefully detected then ret = True
        if ret==True:
            objPoints.append(objp)
            # For again dividing each pixel to get more accurate results
            corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgPoints.append(corners2)
            # For drawing chessboard corners
            img = cv.drawChessboardCorners(img,CHECKERBOARD,corners2,ret)
        # if you wanna see each sample image after processing uncomment the following two lines
        # cv.imshow('img',img)
        # cv.waitKey(0)
    # Finally after getting imgpoints and corresponding img points
    # Calibrate the camera to get teh intrinsic camera matrix and distortion coefficient
    ret,mtx,dist,rvecs,tvecs = cv.calibrateCamera(objPoints,imgPoints,gray.shape[::-1],None,None)
    # Finally return the results
    return ret,mtx,dist,rvecs,tvecs
