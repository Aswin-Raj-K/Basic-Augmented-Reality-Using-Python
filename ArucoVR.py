import numpy as np
import cv2 as cv
from cv2 import aruco
import CameraPoseEstimation as camera

# Function to get the camera matrix and distrotion Coeffiecients
ret, mtx, dist, rvecs, tvecs = camera.CalibrateCamera()


# Some basic functions to draw primitive 3D Objects onto real world
##########################################################################################################
# Name: drawAxis(img)
# Desc: Draws the coordinate axis at the origin
###############################################
def drawAxis(frame):
    # Directional vector of each axis
    pts = np.float32([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, -1]])
    # For getting the projection of each points into 2D frame plane
    imgpts, jac = cv.projectPoints(pts, rvecs, tvecs, mtx, dist)
    imgpts = np.int32(imgpts).reshape(-1, 2)
    # Drawing x-axis
    cv.line(frame, (imgpts[0][0], imgpts[0][1]), (imgpts[1][0], imgpts[1][1]), (0, 0, 255), 3, cv.LINE_AA)
    # Drawing y-axis
    cv.line(frame, (imgpts[0][0], imgpts[0][1]), (imgpts[2][0], imgpts[2][1]), (0, 255, 0), 3, cv.LINE_AA)
    # Drawing z-axis
    cv.line(frame, (imgpts[0][0], imgpts[0][1]), (imgpts[3][0], imgpts[3][1]), (255, 0, 0), 3, cv.LINE_AA)


################################################
# Name: drawRectangle(x,y,z,length,img)
# Desc: Draws a rectangle with one corner at (x,y,z) with side 'length' long in the real world,The rectangle is
#       parallel to the X-Y Plane
###############################################
def drawRectangle(x, y, z, length, frame):
    z = -z  # Flipping the z-axis
    # Intializing all the corners of the rectangle
    pts = np.array([[x, y, z], [x, y + length, z], [x + length, y + length, z], [x + length, y, z]],
                   dtype=np.float32).reshape(-1, 3)
    # For projecting the real world coordinates onto the frame coordinates
    imgpts, jac = cv.projectPoints(pts, rvecs, tvecs, mtx, dist)
    imgpts = np.int32(imgpts.reshape(1, -1, 2))
    # Drawing lines through the corner points
    cv.polylines(frame, imgpts, True, (0, 0, 255), 3, cv.LINE_AA)


################################################
# Name: drawCube(x,y,z,length,img)
# Desc: Draws a cube with one corner at (x,y,z) with side 'length' long in the real world.
###############################################
def drawCube(x, y, z, length, frame):
    z = -z  # Flipping the z-axis
    # Intializing all the corners of the cube
    pts = np.float32(
        [[x, y, z], [x, y, z - length], [x + length, y, z], [x + length, y, z - length], [x + length, y + length, z],
         [x + length, y + length, z - length], [x, y + length, z], [x, y + length, z - length]]).reshape(-1, 3)
    # For projecting the real world coordinates onto the frame coordinates
    imgpts, jac = cv.projectPoints(pts, rvecs, tvecs, mtx, dist)
    imgpts = np.int32(imgpts).reshape(-1, 2)
    # Drawing the vertical lines of the cube
    for i in range(0, 8, 2):
        cv.line(frame, (imgpts[i][0], imgpts[i][1]), (imgpts[i + 1][0], imgpts[i + 1][1]), (0, 0, 255), 3, cv.LINE_AA)

    # Creating rectangle on top and bottom of the cube so that the object finall appears like a cube
    drawRectangle(x, y, -z, length, frame)
    drawRectangle(x, y, -(z - length), length, frame)


########################################################################

cap = cv.VideoCapture(0)
# Points of the aruco marker in real world taking plane of the marker as X-Y plane
objp = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], dtype=np.float32).reshape(-1, 3)

while True:
    _, frame = cap.read()

    # Initializing the aruco marker library
    dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
    # For detecting the marker position on the frame
    corners, ids, _ = aruco.detectMarkers(frame, dict, parameters=parameters)

    # if corners are detected
    if (len(corners) > 0):
        corners = np.array(corners, dtype=np.float32)
        corners = corners.reshape((-1, 2))
        # For getting the rotational and translational vectors of the corners of
        # the aruco markers in the real world
        _, rvecs, tvecs, inliers = cv.solvePnPRansac(objp, corners, mtx, dist)

        # Write your functionns here to draw objects
        ######################################################################

        # For drawing the axis
        drawAxis(frame)

        # For drawing the inverted L-shape using 3 cubes.
        # drawCube(0,0,0,1,frame)
        # drawCube(0,0,1,1,frame)
        # drawCube(0,-1,1,1,frame)

        ######################################################################
    # For showing the frame
    cv.imshow("Frame", frame)
    k = cv.waitKey(1)

    if k == 27:
        cv.imwrite("Result4.jpg", frame)
        break

cap.release()
cv.destroyAllWindows()
