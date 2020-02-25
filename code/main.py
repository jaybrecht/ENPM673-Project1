import cv2
import math
from functions import*
from cube import*
import time

# Toggles for different modes
write_to_video = False
show_contours = False
Dog_mode = False
Cube_mode = True
Fast_mode = False # Wont show the frame to screen. Best for write_to_video=True
Fast_warp = False # if true the code uses cv2.remap(), if false it does not

# Video settings
video_src = 3 # 1 for data1, 2 for data2, 3 for data3
start_frame = 1 # change which frame the video starts on

# Cube settings
face_colors = [(0, 127, 255),(255, 127, 0),(0, 191, 0)] 
edge_color = (0, 0, 0) 

# Define the codec and initialize the output file
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

# define the tag id's and the assoicated images
tag_ids = ['0101','0111','1111']
img_paths = ['data/Tucker.jpg','data/Hailey.jpg','data/Tessa.jpg']

# read the images into memory
imgs = []
for path in img_paths:
    imgs.append(cv2.imread(path))

# open the video specified by video_src
video = cv2.VideoCapture('data/data_'+str(video_src)+'.mp4') 

# move the video to the start frame and adjust the counter
video.set(1,start_frame)
count = start_frame

while(video.isOpened()):
    if not Fast_mode:
        print("Current frame:" + str(count))
    count += 1
    ret, frame = video.read() # ret is false if the video cannot be read
    if ret:
        #find correct contours
        [all_cnts,cnts] = findcontours(frame,180)
        
        #approximate quadralateral to each contour and extract corners
        [tag_cnts,corners] = approx_quad(cnts)
        if show_contours == True:
            cv2.drawContours(frame,all_cnts,-1,(0,255,0), 4)
            cv2.drawContours(frame,tag_cnts,-1,(255,0,0), 4)

        for i,tag in enumerate(corners):
            # find number of points in the polygon
            num_points = num_points_in_poly(frame,tag_cnts[i])

            # set the dimension for homography
            dim = int(math.sqrt(num_points))
   
            #compute homography, for the forward warp we need the inverse
            H = homography(tag,dim)
            H_inv = np.linalg.inv(H)

            # get squared tag
            if Fast_warp:
                square_img = fastwarp(H_inv,frame,dim,dim)
            else:
                square_img = warp(H_inv,frame,dim,dim)

            # threshold the squared tag
            imgray = cv2.cvtColor(square_img, cv2.COLOR_BGR2GRAY)
            ret, square_img = cv2.threshold(imgray, 180, 255, cv2.THRESH_BINARY)

            #decode squared tile
            [tag_img,id_str,orientation] = encode_tag(square_img)
        
            if Dog_mode:
                 #pick image based on id
                if id_str in tag_ids:
                    index = tag_ids.index(id_str)
                    new_img = imgs[index]
                else:
                    continue

                #rotate image to reflect tag orientation
                rotated_img = rotate_img(new_img,orientation)

                #superimpose the image on the tag
                dim = rotated_img.shape[0]
                H = homography(tag,dim)
                h = frame.shape[0] 
                w = frame.shape[1]
                if Fast_warp:
                    frame1 = fastwarp(H,rotated_img,h,w)
                else:
                    frame1 = warp(H,rotated_img,h,w)

                frame2 = blank_region(frame,tag_cnts[i],0)
                frame = cv2.bitwise_or(frame1,frame2)

            if Cube_mode:
                # Pick the color based on the tag id
                if id_str in tag_ids:
                    index = tag_ids.index(id_str)
                    face_color = face_colors[index]
                else:
                    continue

                # Find top corners for the cube  
                H=homography(tag,200)
                H_inv = np.linalg.inv(H)
                P=projection_mat(K,H_inv)
                new_corners=cubePoints(tag, H, P, 200)

                # draw the cube onto the frame
                frame=drawCube(tag, new_corners,frame,face_color,edge_color,Dog_mode)

        if not Fast_mode:
            # Display the frame after superposition
            cv2.imshow("Superposition",frame)

        if write_to_video:
            out.write(frame)
    else:
        # if ret is False release the video which will exit the loop
        video.release()

    # if the user presses 'q' release the video which will exit the loop
    if cv2.waitKey(1) == ord('q'):
        video.release()

if write_to_video:
    out.release()