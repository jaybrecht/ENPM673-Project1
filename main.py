import cv2
import math
from functions import*
from cube import*
import time

video = cv2.VideoCapture('data/data_2.mp4') 

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# today = time.strftime("%Y%m%d-%H%M%S")
# fps_out = 29
# out = cv2.VideoWriter(str(today)+".avi", fourcc, fps_out, (1920, 1080))

K=np.array([[1406.08415449821,0,0],
           [2.20679787308599, 1417.99930662800,0],
           [1014.13643417416, 566.347754321696,1]])

tag_ids = ['0101','0111','1111']
img_paths = ['data/Tucker.jpg','data/Hailey.jpg','data/Tessa.jpg']

# print("Writing to Video, Please Wait")

show_contours = False
Dog_mode = True
Cube_mode = True

start_frame = 1
count = start_frame
video.set(1,start_frame)
while(video.isOpened()):
    print("Current frame:" + str(count))
    count += 1
    ret, frame = video.read()
    #find correct contours
    [all_cnts,cnts] = findcontours(frame,180)
    #approximate quadralateral to each contour and extract corners
    [tag_cnts,corners] = approx_quad(cnts)
    if show_contours == True:
        cv2.drawContours(frame,all_cnts,-1,(0,255,0), 4)
        cv2.drawContours(frame,tag_cnts,-1,(255,0,0), 4)

    flag = False

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
        
        #pick image based on id
        if id_str in tag_ids:
            index = tag_ids.index(id_str)
            new_img = cv2.imread(img_paths[index])
        else:
            continue

        #rotate image to reflect tag orientation
        rotated_img = rotate_img(new_img,orientation)

        if Dog_mode:
            #superimpose the image on the tag
            dim = rotated_img.shape[0]
            H = homography(tag,dim)
            h = frame.shape[0] 
            w = frame.shape[1]
            frame1 = warp(H,rotated_img,h,w)
            frame2 = blank_region(frame,tag_cnts[i],0)
            frame = cv2.bitwise_or(frame1,frame2)
            flag = True

        if Cube_mode:
        # Find new cube points and draw on image
            H=homography(tag,200)
            H_inv = np.linalg.inv(H)
            P=projection_mat(K,H_inv)
            new_corners=cubePoints(tag, H, P, 200)
            face_color = (100, 100, 100) 
            edge_color = (0, 0, 0) 
            frame=drawCube(tag, new_corners,frame,face_color,edge_color,flag)

    cv2.imshow("Frame",frame)

    # out.write(frame)
    if cv2.waitKey(1) == ord('q'):
        break

# out.release()