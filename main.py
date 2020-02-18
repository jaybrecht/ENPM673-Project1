import cv2
from functions import*

video = cv2.VideoCapture('data/data_3.mp4') 
ret, frame = video.read()
#find correct contours
cnts = findcontours(frame,190)
#approximate quadralateral to each contour and extract corners
[tag_cnts,corners] = approx_quad(cnts)
# cv2.drawContours(frame,tag_cnts,-1,(255,0,0), 4)
# for tag in corners:
#     for corner in tag:
#         cv2.circle(frame,(corner[0],corner[1]),5,(0,0,255),-1)
#         cv2.imshow("Contours",frame)
#         cv2.waitKey(0)

dim = 100
for i,tag in enumerate(corners):
    #compute homography 
    H = homography(tag,dim)
    #find list of points in each tag
    orig_points = points_in_poly(frame,tag_cnts[i])
    #get squared tile
    
    square_img = warp2square(orig_points,H,dim)
    cv2.imshow("Square",square_img)
    cv2.waitKey(0)
    # old_points = warp2square(orig_points,H,dim)
    # print(old_points[0][100])
#encode squared tile

