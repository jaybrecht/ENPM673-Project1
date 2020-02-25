import cv2
import numpy as np

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


def num_points_in_poly(frame,contour):
    H = frame.shape[0]
    L = frame.shape[1]
    matrix =np.zeros((H,L),dtype=np.int32)
    cv2.drawContours(matrix,[contour],-1,(1),thickness=-1)
    inds=np.nonzero(matrix)
    num_points = len(inds[0])
    return num_points


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
        x.append(point[0])
        y.append(point[1])
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


def warp(H,src,h,w):
    # create indices of the destination image and linearize them
    indy, indx = np.indices((h, w), dtype=np.float32)
    lin_homg_ind = np.array([indx.ravel(), indy.ravel(), np.ones_like(indx).ravel()])

    # warp the coordinates of src to those of true_dst
    map_ind = H.dot(lin_homg_ind)
    map_x, map_y = map_ind[:-1]/map_ind[-1] 
    map_x = map_x.reshape(h,w).astype(np.float32)
    map_y = map_y.reshape(h,w).astype(np.float32)

    # generate new image
    new_img = np.zeros((h,w,3),dtype="uint8")

    map_x[map_x>=src.shape[1]] = -1
    map_x[map_x<0] = -1
    map_y[map_y>=src.shape[0]] = -1
    map_x[map_y<0] = -1

    for new_x in range(w):
        for new_y in range(h):
            x = int(map_x[new_y,new_x])
            y = int(map_y[new_y,new_x])

            if x == -1 or y == -1:
                pass
            else:
                new_img[new_y,new_x] = src[y,x]

    return new_img


def fastwarp(H,src,h,w):
    # create indices of the destination image and linearize them
    indy, indx = np.indices((h, w), dtype=np.float32)
    lin_homg_ind = np.array([indx.ravel(), indy.ravel(), np.ones_like(indx).ravel()])

    # warp the coordinates of src to those of true_dst
    map_ind = H.dot(lin_homg_ind)
    map_x, map_y = map_ind[:-1]/map_ind[-1] 
    map_x = map_x.reshape(h,w).astype(np.float32)
    map_y = map_y.reshape(h,w).astype(np.float32)

    new_img = cv2.remap(src, map_x, map_y, cv2.INTER_LINEAR)
    
    return new_img


def encode_tag(square_img):
    report_img = np.zeros((square_img.shape[0],square_img.shape[0],3), np.uint8)
    dim = square_img.shape[0]
    grid_size = 8
    k = dim//grid_size
    sx = 0
    sy = 0
    font = cv2.FONT_HERSHEY_SIMPLEX 
    encoding = np.zeros((grid_size,grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            roi = square_img[sy:sy+k, sx:sx+k]
            if roi.mean() > 255//2:
                encoding[i][j] = 1
                cv2.rectangle(report_img,(sx,sy),(sx+k,sy+k),(255,255,255),-1)
                # cv2.putText(report_img,'1',(sx+int(k*.3),sy+int(k*.7)),font,.6,(255,0,0),2)
            # else:
                # cv2.putText(report_img,'0',(sx+int(k*.3),sy+int(k*.7)),font,.6,(255,0,0),2)
            cv2.rectangle(report_img,(sx,sy),(sx+k,sy+k),(127,127,127),1)
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

    cv2.putText(report_img,a,(3*k+int(k*.3),3*k+int(k*.7)),font,.6,(227,144,27),2)
    cv2.putText(report_img,b,(4*k+int(k*.3),3*k+int(k*.7)),font,.6,(227,144,27),2)
    cv2.putText(report_img,d,(3*k+int(k*.3),4*k+int(k*.7)),font,.6,(227,144,27),2)
    cv2.putText(report_img,c,(4*k+int(k*.3),4*k+int(k*.7)),font,.6,(227,144,27),2)

    if encoding[5,5] == 1:
        orientation = 3
        id_str = a+b+c+d
        center = (5*k+(k//2),5*k+(k//2))
        cv2.circle(report_img,center,k//4,(0,0,255),-1)
    elif encoding[2,5] == 1:
        orientation = 2
        id_str = d+a+b+c
        center = (5*k+(k//2),2*k+(k//2))
        cv2.circle(report_img,center,k//4,(0,0,255),-1)
    elif encoding[2,2] == 1:
        orientation = 1
        id_str = c+d+a+b
        center = (2*k+(k//2),2*k+(k//2))
        cv2.circle(report_img,center,k//4,(0,0,255),-1)
    elif encoding[5,2] == 1:
        orientation = 0
        id_str = b+c+d+a
        center = (2*k+(k//2),5*k+(k//2))
        cv2.circle(report_img,center,k//4,(0,0,255),-1)
    else:
        orientation = 0
        id_str = '0000'

    return [report_img,id_str,orientation]


def rotate_img(img,orientation):
    if orientation == 1:
        rotated_img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    elif orientation == 2:
        rotated_img = cv2.rotate(img,cv2.ROTATE_180)
    elif orientation == 3:
        rotated_img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        rotated_img = img

    return rotated_img


def blank_region(frame,contour,color):
    cv2.drawContours(frame,[contour],-1,(color),thickness=-1)
    return frame


        










