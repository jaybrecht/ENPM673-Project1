
# import required packages
import cv2
import numpy as np

def myWarpPerspective(skewed_image, Homography, dimensions):
	# This function takes in a skewed image (cv mat), a homography 3x3 matrix (numpy array), 
	# and dimensions for a new image (width, height)
	# It warps the skewed image according to the homography


	# Establish key variables
	width=dimensions[0]
	height=dimensions[1]
	H=Homography
	#print(H)

	# Create a new image, all black
	new_image=np.zeros((width,height,3),dtype="uint8")

	# Warp Transform Calculation
	for y in range (0,height):
		for x in range (0,width):
			skewx=int((H[0,0]*x+H[0,1]*y+H[0,2])/(H[2,0]*x+H[2,1]*y+H[2,2]))
			skewy=int((H[1,0]*x+H[1,1]*y+H[1,2])/(H[2,0]*x+H[2,1]*y+H[2,2]))

			#print("("+str(skewx)+","+str(skewy)+")")

			# Many of the pixels in the skewed image will be way outside the bounds of the new image
			# They don't fit in the new image so they are discarded
			# Populate the new image's pixels only with those that are in bounds
			if (skewx>=0) and (skewx<width) and (skewy>=0) and (skewy<height):
				new_image[x,y,0]=skewed_image[skewx,skewy,0]
				new_image[x,y,1]=skewed_image[skewx,skewy,1]
				new_image[x,y,2]=skewed_image[skewx,skewy,2]

	cv2.imshow("new image", new_image)
	cv2.waitKey(0)




