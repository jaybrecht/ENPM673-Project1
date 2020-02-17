
#import required packages
import cv2
import numpy as np
from datetime import datetime

# import my packages
from homography import myHomography
from myWarpPerspective import square2Warp


# imgpath="tucker.JPG"

# # Read in the skewed image
# square_image=cv2.imread(imgpath)
# warped_image=cv2.imread("frame.png")


def squareWarper(corners,frame,square_image):

	width,height,depth=square_image.shape
	warped_image=frame#.copy()


	original_coords = np.array(corners)
	desired_coords = np.array([[0, 0], [width, 0], [width, height], [0, height]])


	# Homography processing to make flat image
	# cvh, status = cv2.findHomography(original_coords, desired_coords)
	# print(type(cvh))
	# print(cvh) ###

	# Compute Homography matrix to make warped image from square
	h = myHomography(original_coords, desired_coords)
	# print(type(h))
	# print(h)



	print("Starting warp. Please be patient - this may take a few seconds.")

	#Time the warp operation
	#start = datetime.now()

	# Warp the image
	#cv_Homography = cv2.warpPerspective(square_image, h, (800, 800))
	cv_Homography = square2Warp(warped_image, square_image, h, (width, height))

	#end = datetime.now()
	#warptime=end-start
	#print("Finished warp in "+str(warptime)+" (hours:min:sec)")


	# showing flat image
	#cv2.imshow("Unwarped image", cv_Homography)
	#cv2.waitKey(0)

	return cv_Homography


