import cv2
import numpy as np

video = cv2.VideoCapture('data/data_1.mp4') 

while(video.isOpened()):
    ret, frame = video.read()
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2]
    blank = np.zeros((height, width, channels), dtype = "uint8")

    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray= cv2.medianBlur(imgray,5)
    ret, thresh = cv2.threshold(imgray, 190, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Output of hierarchy: [Next, Previous, First_Child, Parent]
    parent = []
    child = []
    for ind in hierarchy[0]:
        parent.append(ind[3])
        child.append(ind[2])

    new_lst = []
    new_lst2 = []

    # Find list of points that have a parent
    for i in range(len(hierarchy[0])):
        if parent[i] != -1:
            new_lst.append(i)
            # cv2.drawContours(frame, contours, i,(0,255,0), 3)

    # Find all points that belong to the next level in the heirarchy
    for i in new_lst:
        if parent[i] not in new_lst:
            new_lst2.append(i)

    for i in new_lst2:
        cv2.drawContours(blank,contours,i,(255,255,255), 4)

    gray = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    num_corners = 4
    corners = cv2.goodFeaturesToTrack(gray, num_corners, .1, 100)
    corners = np.int0(corners)

    for corner in corners:
        x,y = corner.ravel()
        cv2.circle(frame,(x,y),5,255,-1)

    cv2.imshow("Corners",frame)
    cv2.imshow("Contours",blank)

    if cv2.waitKey(1) == ord('q'):
        break
