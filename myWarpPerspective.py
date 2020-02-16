
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
	#H=cv2.invert(H)[1]
	#print(H)

	# Create a new image, all black
	new_image=np.zeros((width,height,3),dtype="uint8")


	#https://stackoverflow.com/questions/44457064/displaying-stitched-images-together-without-cutoff-using-warpaffine/44459869#44459869
	y,x=np.indices((height,width))
	homogenous_points=np.stack((x.ravel(),y.ravel(),np.ones(y.size)))
	#print(homogenous_points)
	new_hom_points=H.dot(homogenous_points)
	new_hom_points/=new_hom_points[2]
	#print(new_hom_points)

	# Many of the pixels in the skewed image will be way outside the bounds of the new image
	# 		# They don't fit in the new image so they are discarded
	# 		# Populate the new image's pixels only with those that are in bounds
	skewx=np.empty(y.size,dtype="int")
	skewy=np.empty(y.size,dtype="int")
	for i in range (0,y.size):
		skewx[i]=int(new_hom_points[0,i:i+1])
		skewy[i]=int(new_hom_points[1,i:i+1])
		# print("x="+str(skewx))
		# print("y="+str(skewy))

	i=0
	
	for newx in range (0,width):
		for newy in range (0,height):
			if (skewx[i]>=0) and (skewx[i]<width) and (skewy[i]>=0) and (skewy[i]<height):
				new_image[skewx[i],skewy[i],0]=skewed_image[newx,newy,0]
				new_image[skewx[i],skewy[i],1]=skewed_image[newx,newy,1]
				new_image[skewx[i],skewy[i],2]=skewed_image[newx,newy,2]
			i+=1





	# Warp Transform Calculation
	# for x in range (0,width):
	# 	for y in range (0,height):
	# 		skewx=int((H[0,0]*x+H[0,1]*y+H[0,2])/(H[2,0]*x+H[2,1]*y+H[2,2]))
	# 		skewy=int((H[1,0]*x+H[1,1]*y+H[1,2])/(H[2,0]*x+H[2,1]*y+H[2,2]))

	# 		#print("("+str(skewx)+","+str(skewy)+")")

	# 		# Many of the pixels in the skewed image will be way outside the bounds of the new image
	# 		# They don't fit in the new image so they are discarded
	# 		# Populate the new image's pixels only with those that are in bounds
	# 		if (skewx>=0) and (skewx<width) and (skewy>=0) and (skewy<height):
	# 			new_image[x,y,0]=skewed_image[skewx,skewy,0]
	# 			new_image[x,y,1]=skewed_image[skewx,skewy,1]
	# 			new_image[x,y,2]=skewed_image[skewx,skewy,2]

	cv2.imshow("new image", new_image)
	cv2.waitKey(0)




