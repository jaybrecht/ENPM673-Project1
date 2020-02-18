import cv2
from functions import*

video = cv2.VideoCapture('data/data_3.mp4') 

imgpath="Tucker.JPG"
dim = 320
new_img=cv2.imread(imgpath)

while(video.isOpened()):
    ret, frame = video.read()
    #find correct contours
    cnts = findcontours(frame,190)
    #approximate quadralateral to each contour and extract corners
    [tag_cnts,corners] = approx_quad(cnts)
    # cv2.drawContours(frame,tag_cnts,-1,(255,0,0), 4)

    for i,tag in enumerate(corners):
        #compute homography 
        H = homography(tag,dim)
        #find list of points in each tag
        orig_points = points_in_poly(frame,tag_cnts[i])
        #get squared tile
        square_img = warp2square(orig_points,H,dim)
        #encode squared tile
        [square_img,orientation] = encode_tag(square_img)
        #rotate image to reflect tag orientation
        rotated_img = rotate_img(new_img,orientation)
        # cv2.imshow("Tag",square_img)
        # cv2.imshow("Rotate",rotated_img)
        # cv2.waitKey(0)
        H_inv = cv2.invert(H)[1]
        frame = square2warp(frame,rotated_img,H_inv)

    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) == ord('q'):
        break

