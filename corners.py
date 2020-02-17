import cv2
import numpy as np


video = cv2.VideoCapture('data/data_1.mp4') 
imgpath="Tucker.JPG"

# Read in the square image
square_image=cv2.imread(imgpath)

# Check that the image exists
if square_image is None:
    print("Error: Couldn't import '"+str(imgpath)+"'. Check that the file path and name are correct.")
    print("Exiting...")
    exit()
else:
    print("Image '"+str(imgpath)+"' imported properly.")

while(video.isOpened()):
    ret, frame = video.read()

    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray= cv2.medianBlur(imgray,5)
    ret, thresh = cv2.threshold(imgray, 190, 255, cv2.THRESH_BINARY)

    cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # remove any contours that do not have a parent or child
    wrong_cnts = []
    for i,h in enumerate(hierarchy[0]):
        if h[2] == -1 or h[3] == -1:
            wrong_cnts.append(i)
    cnts = [c for i, c in enumerate(cnts) if i not in wrong_cnts]

    # sort the contours to include only the three largest
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]

    tag_cnt = []
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, peri*.015, True)
        # if the countour can be approximated by a polygon with four sides include it
        if len(approx) == 4:
            tag_cnt.append(approx)

    # draw the approximate polygons on a blank image
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2]
    blank = np.zeros((height, width, channels), dtype = "uint8")
    cv2.drawContours(blank,tag_cnt,-1,(255,0,0), 4)
    
    # draw the corners on the orignal image and store the values in the list corners
    corners = []
    for shape in tag_cnt:
        coords = []
        for p in shape:
            coords.append([p[0][0],p[0][1]])
            cv2.circle(frame,(p[0][0],p[0][1]),5,(0,0,255),-1)
        corners.append(coords)

    cv2.imshow("Corners",frame)
    cv2.imshow("Contours",blank)
    if cv2.waitKey(1) == ord('q'):
        break