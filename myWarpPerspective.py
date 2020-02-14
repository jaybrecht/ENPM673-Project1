
# import required packages
import cv2
import numpy as np

def myWarpPerspective(skewed_image, Homography, dimensions):
	width=dimensions[0]
	height=dimensions[1]
	H=Homography
	print(H)
	# (H[0,0]*x+H[0,1*y+M[0,2]])/(H[2,0]*x+M[2,1]*y+H[2,2])
	# (H[1,0]*x+H[1,1*y+M[1,2]])/(H[2,0]*x+M[2,1]*y+H[2,2])

	new_image=np.zeros((width,height,3),dtype="uint8")
	for y in range (0,height):
		for x in range (0,width):
			skewx=int((H[0,0]*x+H[0,1]*y+H[0,2])/(H[2,0]*x+H[2,1]*y+H[2,2]))
			skewy=int((H[1,0]*x+H[1,1]*y+H[1,2])/(H[2,0]*x+H[2,1]*y+H[2,2]))

			#print("("+str(skewx)+","+str(skewy)+")")
			if (skewx>=0) and (skewx<width) and (skewy>=0) and (skewy<height):
				new_image[x,y,0]=skewed_image[skewx,skewy,0]
				new_image[x,y,1]=skewed_image[skewx,skewy,1]
				new_image[x,y,2]=skewed_image[skewx,skewy,2]

	cv2.imshow("new image", new_image)
	cv2.waitKey(0)