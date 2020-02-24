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
    map_x, map_y = map_ind[:-1]/map_ind[-1]  # ensure homogeneity
    map_x = map_x.reshape(h, w).astype(np.float32)
    map_y = map_y.reshape(h, w).astype(np.float32)

    new_img = cv2.remap(src, map_x, map_y, cv2.INTER_LINEAR)
    
    return new_img

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
        orientation = 3
        id_str = a+b+c+d
        center = (5*k+(k//2),5*k+(k//2))
        cv2.circle(square_img,center,k//4,125)
    elif encoding[2,5] == 1:
        orientation = 2
        id_str = d+a+b+c
        center = (5*k+(k//2),2*k+(k//2))
        cv2.circle(square_img,center,k//4,125)
    elif encoding[2,2] == 1:
        orientation = 1
        id_str = c+d+a+b
        center = (2*k+(k//2),2*k+(k//2))
        cv2.circle(square_img,center,k//4,125)
    elif encoding[5,2] == 1:
        orientation = 0
        id_str = b+c+d+a
        center = (2*k+(k//2),5*k+(k//2))
        cv2.circle(square_img,center,k//4,125)
    else:
        orientation = 0
        id_str = '0000'

    return [square_img,id_str,orientation]

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



def getCorners(frame):
    [all_cnts,cnts] = findcontours(frame,180)
    #approximate quadralateral to each contour and extract corners
    [tag_cnts,corners] = approx_quad(cnts)

    tag_corners={}

    for i,tag in enumerate(corners):
        #compute homography
        dim = 200
        H = homography(tag,dim)
        H_inv = np.linalg.inv(H)
        
        #get squared tile
        square_img = warp(H_inv,frame,dim,dim)
        imgray = cv2.cvtColor(square_img, cv2.COLOR_BGR2GRAY)
        ret, square_img = cv2.threshold(imgray, 180, 255, cv2.THRESH_BINARY)
        
        #encode squared tile
        [tag_img,id_str,orientation] = encode_tag(square_img)

        ordered_corners=[]
        # print("tag:")
        # print(tag)
        # print("tag[1]:")
        # print(tag[1])

        if orientation==0:
            ordered_corners=tag

        elif orientation==1:
            ordered_corners.append(tag[1])
            ordered_corners.append(tag[2])
            ordered_corners.append(tag[3])
            ordered_corners.append(tag[0])

        elif orientation==2:
            ordered_corners.append(tag[2])
            ordered_corners.append(tag[3])
            ordered_corners.append(tag[0])
            ordered_corners.append(tag[1])

        elif orientation==3:
            ordered_corners.append(tag[3])
            ordered_corners.append(tag[0])
            ordered_corners.append(tag[1])
            ordered_corners.append(tag[2])
        
        tag_corners[id_str] = ordered_corners
        

    return tag_corners


def avgCorners(p2, p1, current, f1, f2):
    average_corners={}
    for tag in current:
        templist=[current[tag]]
        if tag in p1:
            templist.append(p1[tag])
        elif tag in p2:
            templist.append(p2[tag])
        if tag in f1:
            templist.append(f1[tag])
        elif tag in f2:
            templist.append(f2[tag])
        
        newcorners=[]
        c1x=0
        c1y=0
        c2x=0
        c2y=0
        c3x=0
        c3y=0
        c4x=0
        c4y=0
        for allcorners in templist:
            c1x+=allcorners[0][0]
            c1y+=allcorners[0][1]
            c2x+=allcorners[1][0]
            c2y+=allcorners[1][1]
            c3x+=allcorners[2][0]
            c3y+=allcorners[2][1]
            c4x+=allcorners[3][0]
            c4y+=allcorners[3][1]


        newcorners=np.array([[c1x,c1y],[c2x,c2y],[c3x,c3y],[c4x,c4y]])
        newcorners=np.divide(newcorners,len(templist))
        newcorners=newcorners.astype(int)
        newcorners=np.ndarray.tolist(newcorners)
        average_corners[tag] = newcorners
        
    return average_corners
        










