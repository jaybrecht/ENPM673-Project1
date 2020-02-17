
#import required packages
import cv2
import numpy as np
from datetime import datetime

# import my packages
from homography import myHomography
from myWarpPerspective import square2Warp


def squareWarper(corners,frame,square_image):

	width,height,depth=square_image.shape
	warped_image=frame#.copy()


	original_coords = np.array(corners)
	desired_coords = np.array([[0, 0], [width, 0], [width, height], [0, height]])

	# Compute Homography matrix to make warped image from square
	h = myHomography(original_coords, desired_coords)

	print("Starting warp. Please be patient - this may take a few seconds.")


	# Warp the image
	#cv_Homography = cv2.warpPerspective(square_image, h, (800, 800))
	cv_Homography = square2Warp(warped_image, square_image, h, (width, height))

	# showing flat image
	#cv2.imshow("Unwarped image", cv_Homography)
	#cv2.waitKey(0)

	return cv_Homography


