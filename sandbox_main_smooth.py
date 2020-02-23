import cv2
import math
from functions import*
from cube import*
import time
import statistics
#from sandboxfilter import moveMean

write_to_video = False
show_contours = True
Dog_mode = True
Cube_mode = True
video_src = 3 # 1 for data1, 2 for data2, 3 for data3
Smooth_mode = False
Fast_mode = False # Wont show the frame to screen if true. Best for write_to_video=True

stepsize=5

if write_to_video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    today = time.strftime("%m-%d__%H.%M.%S")
    videoname=str(today)+('_contours' if show_contours == True else '')+("_dog" if Dog_mode == True else '')+('_cube' if Cube_mode == True else '')+('_smooth' if Smooth_mode == True else '')+str(video_src)
    fps_out = 29
    out = cv2.VideoWriter(str(videoname)+".avi", fourcc, fps_out, (1920, 1080))
    print("Writing to Video, Please Wait")

K=np.array([[1406.08415449821,0,0],
           [2.20679787308599, 1417.99930662800,0],
           [1014.13643417416, 566.347754321696,1]])

tag_ids = ['0101','0111','1111']
img_paths = ['data/Tucker.jpg','data/Hailey.jpg','data/Tessa.jpg']

video = cv2.VideoCapture('data/data_'+str(video_src)+'.mp4') 

start_frame = 0
count = start_frame
video.set(1,start_frame)

while(video.isOpened()):
    if Fast_mode == False:
        print("Current frame:" + str(count))
    count += 1
    ret, frame = video.read()
    if ret:
        
        next_frame=video.read(video.set(1,count+1))[1]

        numtag=0
        numcorn=0
        x=0
        y=1
        cnts=[]
        all_cnts=[]
        tag_cnts=[]
        corners=[]
        for q in range(0,stepsize):

            
            my_frame=video.read(video.set(1,count+q))[1]
            # cv2.imshow("myframe",my_frame)
            # cv2.waitKey(0)
            #find correct contours
            [temp_all_cnts,temp_cnts] = findcontours(my_frame,180)
            all_cnts.append(temp_all_cnts)
            cnts.append(temp_cnts)
          #approximate quadralateral to each contour and extract corners
            [temp_tag_cnts,temp_corners] = approx_quad(temp_cnts)
            tag_cnts.append(temp_tag_cnts)
            corners.append(temp_corners)

        #print(corners[0][numtag][numcorn][x])

        mytag=[]
        for numtag in range(0,3): #change this 3 to something more dynamic
            corn=[]
            for numcorn in range (0,4):
                x_array=[]
                y_array=[]
                for j in range (0,stepsize):
                    #print(corners[j])[numtag][numcorn][x]) #x coordinate of the numcorn corner of the numtag tag of the j'th element in corners
                    corners_x_array.append(corners[j][numtag][numcorn][x])
                    corners_y_array.append(corners[j][numtag][numcorn][y])

                    tag_cnts_x_array.append(tag_cnts[j][numtag][numcorn][x])
                    tag_cnts_y_array.append(tag_cnts[j][numtag][numcorn][y])

                corners_new_x=statistics.mean(corners_x_array)
                corners_new_y=statistics.mean(corners_y_array)
                
                #print(new_x)  
                corn.append([new_x,new_y]) 
            #print(corn)
            mytag.append(corn)
            print(mytag)


        #avg_corners[j][numtag][numcorn][0][x]=

        #moveMean(corners,3)








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

        if Fast_mode == False:
            cv2.imshow("Frame",frame)

        if write_to_video:
            out.write(frame)
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break

if write_to_video:
    out.release()