
#import required packages
import cv2
import numpy as np
from datetime import datetime

# import my packages
from homography import myHomography
from myWarpPerspective import myWarpPerspective

imgpath="skewed_colors.jpg"


# Define coordinates of corners (clockwise around from the top left)
point1=[240,11]
point2=[557,232]
point3=[800,800]
point4=[0,800]


original_coords = np.array([point1, point2, point3, point4])
desired_coords = np.array([[0, 0], [800, 0], [800, 800], [0, 800]])


# Homography processing to make flat image
# cvh, status = cv2.findHomography(original_coords, desired_coords)
# print(type(cvh))
# print(cvh) ###

# Compute Homography matrix to make flat image from warped
h = myHomography(original_coords, desired_coords)
# print(type(h))
# print(h)





# Read in the skewed image
skewed_image=cv2.imread(imgpath)

# Check that the image exists
if skewed_image is None:
	print("Error: Couldn't import '"+str(imgpath)+"'. Check that the file path and name are correct.")
	print("Exiting...")
	exit()
else:
	print("Image '"+str(imgpath)+"' imported properly.")


print("Started warp. Please be patient - this may take a few seconds.")

#Time the warp operation
start = datetime.now()

# Warp the image
#cv_Homography = cv2.warpPerspective(skewed_image, h, (800, 800))
cv_Homography = myWarpPerspective(skewed_image, h, (800, 800))

end = datetime.now()
runtime=end-start
#runtime=runtime.strftime("%H:%M:%S")
print("Finished warp in "+str(runtime)+" (hours:min:sec)")


# showing flat image
cv2.imshow("Unwarped image", cv_Homography)
cv2.waitKey(0)



