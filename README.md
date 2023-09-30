# BASIC AUGMENTED REALITY USING PYTHON

## AIM
To create a simple augmented reality using OpenCV and Aruco.

## INTRODUCTION
Augmented reality (AR) is an interactive experience of a real-world environment where the objects that reside in the real world are enhanced by computer-generated perceptual information, sometimes across multiple sensory modalities, including visual, auditory, haptic, somatosensory, and olfactory. AR can be defined as a system that fulfills three basic features: a combination of real and virtual worlds, real-time interaction, and accurate 3D registration of virtual and real objects.

Aruco markers have been used for a while in augmented reality, camera pose estimation, and camera calibration. ArUco markers were originally developed in 2014 by S. Garrido-Jurado et al., in their work "Automatic generation and detection of highly reliable fiducial markers under occlusion." ArUco stands for Augmented Reality University of Cordoba. An ArUco marker is a fiducial marker that is placed on the object or scene being imaged. It is a binary square with a black background and boundaries and a white generated pattern within it that uniquely identifies it. The black boundary helps make their detection easier. They can be generated in a variety of sizes, chosen based on the object size and the scene, for successful detection. If very small markers are not being detected, increasing their size can make their detection easier.

The project aims to use Aruco markers to create a simple augmented reality. Libraries used for this project are OpenCV and Numpy.

## EXPLANATION
### Removing Camera Distortion
To project points in the real world to 2D on the screen, camera calibration is required. Camera lenses introduce distortion effects that can be noticeable when high precision and accuracy are needed. These distortion effects need to be removed to obtain accurate results.

The calibration process involves taking images of a known pattern, such as a checkerboard, from different angles and positions. OpenCV provides functions to find the corners of the checkerboard pattern. 2D points can be obtained directly from the images. Corresponding 3D points in the real world are assigned to the checkerboard corners, considering the plane of the board as the X-Y plane and Z as perpendicular to the board. The intrinsic camera matrix and distortion coefficients can be obtained by calibrating the camera using the obtained 2D and 3D points.

### Projecting the Points
After calibrating the camera, the camera matrix and distortion coefficients can be used to project points in the real world to 2D points on the frame. Aruco markers are used as reference points. The corner points of the Aruco marker can be detected using OpenCV. The detected 2D points and corresponding 3D points (where the 3D points are calculated assuming the Aruco plane as the X-Y plane) can be used to estimate rotational and translational vectors. These vectors can be used to project real-world points onto the frame.

### Sample Outputs
The project includes functions to draw 3D objects and coordinate axes that appear to rotate and translate when the Aruco marker changes its position or orientation. The outputs show 3D objects and axes projected onto the frame.

![Sample Outputs](Results/Sample_Outputs.png)

## CONCLUSION
The program works well regardless of the orientation of the Aruco marker. Improved camera calibration with more sample images can increase accuracy. This project provides a basic implementation of AR using OpenCV in Python, with potential applications in online teaching and other real-world scenarios.

