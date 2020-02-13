
#Import required packages
import cv2
import numpy as np
import imutils

#Portions of this code borrowed from Dr. Mitchell's ENPM809T and ENME489Y

# Define the HSV bounds that make the AR tag really clear (determined experimentally)
colorLower = (0, 0, 0)
colorUpper = (255, 255, 180)

video = cv2.VideoCapture('data/data_1.mp4') 
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
while(video.isOpened()):
	ret, frame = video.read()
	frame=imutils.resize(frame, width=1000)

	# grab the current frame
	#image = frame.array

	# blur the frame and convert to the HSV
	# color space
	#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsvmask = cv2.inRange(hsv, colorLower, colorUpper)

	# Find the edges
	edges = cv2.Canny(hsvmask,20,200)

	cv2.imshow('mask',hsvmask)
	cv2.imshow('edges',edges)
	if cv2.waitKey(1) == ord('q'):
		break


