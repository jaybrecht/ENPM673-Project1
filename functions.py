import cv2
import numpy as np
# from mySVD import mySVD

def findcontours(frame,threshold):
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray= cv2.medianBlur(imgray,5)
    ret, thresh = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)

    all_cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # remove any contours that do not have a parent or child
    wrong_cnts = []
    for i,h in enumerate(hierarchy[0]):
        if h[2] == -1 or h[3] == -1:
            wrong_cnts.append(i)
    cnts = [c for i, c in enumerate(all_cnts) if i not in wrong_cnts]

    # sort the contours to include only the three largest
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]

    return [all_cnts,cnts]

def approx_quad(cnts):
    tag_cnts = []
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, peri*.015, True)
        # if the countour can be approximated by a polygon with four sides include it
        if len(approx) == 4:
            tag_cnts.append(approx)

    corners = []
    for shape in tag_cnts:
        coords = []
        for p in shape:
            coords.append([p[0][0],p[0][1]])
        corners.append(coords)

    return tag_cnts,corners

def homography(corners,dim):
    #Define the eight points to compute the homography matrix
    x = []
    y = []
    for point in corners:
        x.append(point[1])
        y.append(point[0])
    #ccw corners
    xp=[0,dim,dim,0]
    yp=[0,0,dim,dim]

    n = 9
    m = 8
    A = np.empty([m, n])

    val = 0
    for row in range(0,m):
        if (row%2) == 0:
            A[row,0] = -x[val]
            A[row,1] = -y[val]
            A[row,2] = -1
            A[row,3] = 0
            A[row,4] = 0
            A[row,5] = 0
            A[row,6] = x[val]*xp[val]
            A[row,7] = y[val]*xp[val]
            A[row,8] = xp[val]

        else:
            A[row,0] = 0
            A[row,1] = 0
            A[row,2] = 0
            A[row,3] = -x[val]
            A[row,4] = -y[val]
            A[row,5] = -1
            A[row,6] = x[val]*yp[val]
            A[row,7] = y[val]*yp[val]
            A[row,8] = yp[val]
            val += 1

    U,S,V = np.linalg.svd(A)
    # x is equivalent to the eigenvector column of V that corresponds to the 
    # smallest singular value. A*x ~ 0
    x = V[-1]

    # reshape x into H
    H = np.reshape(x,[3,3])
    return H

def points_in_poly(frame,contour):
    H = frame.shape[0]
    L = frame.shape[1]
    matrix =np.zeros((H,L),dtype=np.int32)
    cv2.drawContours(matrix,[contour],-1,(1),thickness=-1)
    inds=np.nonzero(matrix)
    points = []
    for i in range(len(inds[0])):
        x = inds[0][i]
        y = inds[1][i]
        points.append([x,y,frame[x][y]])
    return points

def warp2square(orig_points,H,dim):
    new_points = []
    x = []
    y = []
    for point in orig_points:
        x.append(point[0])
        y.append(point[1])
    old_points = np.stack((np.array(x),np.array(y),np.ones(len(x))))
    new_points=H.dot(old_points)
    new_points/=new_points[2]
    square_img =np.full((dim,dim,3),255//2,dtype="uint8")
    for i in range(len(new_points[0])-1):
        new_x = int(new_points[0][i])
        new_y = int(new_points[1][i])
        if new_x<0 or new_y<0 or new_x>=dim or new_y>=dim:
            pass
        else:
            square_img[new_y][new_x] = orig_points[i][2]
    imgray = cv2.cvtColor(square_img, cv2.COLOR_BGR2GRAY)
    ret, square_img = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY)
    return square_img

def encode_tag(square_img):
    dim = square_img.shape[0]
    grid_size = 8
    k = dim//grid_size
    sx = 0
    sy = 0
    encoding = np.zeros((grid_size,grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            roi = square_img[sy:sy+k, sx:sx+k]
            cv2.rectangle(square_img,(sx,sy),(sx+k,sy+k),(150),2)
            if roi.mean() > 255//2:
                encoding[i][j] = 1
            sx += k
        sx = 0
        sy += k
    # Id is contained in the inner four elements of the tag
    # a  b
    # d  c

    a = str(int(encoding[3][3]))
    b = str(int(encoding[3][4]))
    c = str(int(encoding[4][4]))
    d = str(int(encoding[4][3]))
    if encoding[5,5] == 1:
        orientation = 1
        id_str = a+b+c+d
        # center = (5*k+(k//2),5*k+(k//2))
        # cv2.circle(square_img,center,k//4,125)
    elif encoding[5,2] == 1:
        orientation = 2
        id_str = b+c+d+a
        # center = (2*k+(k//2),5*k+(k//2))
        # cv2.circle(square_img,center,k//4,125)
    elif encoding[2,2] == 1:
        orientation = 3
        id_str = c+d+a+b
        # center = (2*k+(k//2),2*k+(k//2))
        # cv2.circle(square_img,center,k//4,125)
    elif encoding[2,5] == 1:
        orientation = 0
        id_str = d+a+b+c
        center = (5*k+(k//2),2*k+(k//2))
        cv2.circle(square_img,center,k//4,125)

    return [square_img,id_str,orientation]

def rotate_img(new_img,orientation):
    (h, w) = new_img.shape[:2]
    center = (w/2, h/2)
    angle = orientation*90
    M = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_img = cv2.warpAffine(new_img, M, (h, w))
    return rotated_img

def blank_region(frame,region):
    for point in region:
        frame[point[0],point[1]] = 255
    return frame

def square2warp(frame,new_img,H_inv):
    (h, w) = new_img.shape[:2]
    y,x=np.indices((h,w))
    old=np.stack((x.ravel(),y.ravel(),np.ones(y.size)))
    new=H_inv.dot(old)
    new/=new[2]
    for i in range(len(new[0])-1):
        x = int(new[0][i])
        y = int(new[1][i])
        x_ = int(old[0][i])
        y_ = int(old[1][i])
        frame[x,y] = new_img[x_,y_]
    return frame
