import cv2
import math
from functions import*
from cube import*
import time
from halfFrames import halfFrames

write_to_video = True
show_contours = True
Dog_mode = False
Cube_mode = True
video_src = 3 # 1 for data1, 2 for data2, 3 for data3
Smooth_mode = False
Fast_mode = True # Wont show the frame to screen. Best for write_to_video=True

# Cube settings
face_color = (100, 100, 100) 
edge_color = (0, 0, 0)

stepsize=3 


video = cv2.VideoCapture('data/data_'+str(video_src)+'.mp4') 

start_frame = 0
count = start_frame
video.set(1,start_frame)
frame_array=[]

kernel_sharpening = np.array([[-1,-1,-1], 
                              [-1, 9,-1],
                              [-1,-1,-1]])

print("Reading video into memory...")
while(video.isOpened()):
    #if Fast_mode == False:
        #print("Current frame:" + str(count))
    count += 1
    ret, frame = video.read()
    if ret:
        #next_frame=video.read(video.set(1,count+1))[1]
        #frame_array.append(cv2.filter2D(frame, -1, kernel_sharpening))
        frame_array.append(frame)

    else:
        print("Finished reading in video")
        break


if write_to_video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    today = time.strftime("%m-%d__%H.%M.%S")
    videoname=str(today)+('_contours' if show_contours == True else '')+("_dog" if Dog_mode == True else '')+('_cube' if Cube_mode == True else '')+('_smooth' if Smooth_mode == True else '')+str(video_src)
    fps_out = 29
    out = cv2.VideoWriter(str(videoname)+".avi", fourcc, fps_out, (1920, 1080))
    print("Writing to output video, Please Wait")

K=np.array([[1406.08415449821,0,0],
           [2.20679787308599, 1417.99930662800,0],
           [1014.13643417416, 566.347754321696,1]])

tag_ids = ['0101','0111','1111']
img_paths = ['data/Tucker.jpg','data/Hailey.jpg','data/Tessa.jpg']



if Smooth_mode==True:
    frame_array=halfFrames(frame_array)
#new_frame_array=halfFrames(new_frame_array)

avgcorners=[]
for g,frame in enumerate(frame_array):  
        #find correct contours
        [all_cnts,cnts] = findcontours(frame,180)
        [all_cnts2,cnts2] = findcontours(frame_array[g+1],180)

        #approximate quadralateral to each contour and extract corners
        [tag_cnts,corners] = approx_quad(cnts)
        [tag_cnts2,corners2] = approx_quad(cnts2)
        
        if len(corners)==3 and len(corners2)==3:
            print("averaging")
            sumcorners=np.add(corners,corners2)
            avgcorners=np.divide(sumcorners,2)
            corners=avgcorners.astype(int)
        else:
            print("insufficient tags")
        # #print(len(corners))
        # if len(corners)==3:
        #     avgcorners.append(corners)

        # if len(avgcorners)==2:
        #     sumavgcnts=np.add(avgcorners[0],avgcorners[1])
        #     newavgcnts=np.divide(sumavgcnts,2)
        #     corners=newavgcnts.astype(int)
        #     avgcorners=[]





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
                frame=drawCube(tag, new_corners,frame,face_color,edge_color,flag)

        if Fast_mode == False:
            cv2.imshow("Frame",frame)

        if write_to_video:
            out.write(frame)
        if cv2.waitKey(1) == ord('q'):
            break
# else:
#     break

if write_to_video:
    out.release()