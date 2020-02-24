import cv2
import math
from functions import*
from cube import*
import time

write_to_video = True
show_contours = False
Dog_mode = False
Cube_mode = True
video_src = 3 # 1 for data1, 2 for data2, 3 for data3
Smooth_mode = False
Fast_mode = False # Wont show the frame to screen. Best for write_to_video=True

# Cube settings
face_color = (100, 100, 100) 
edge_color = (0, 0, 0) 


fourcc = cv2.VideoWriter_fourcc(*'XVID')
today = time.strftime("%m-%d__%H.%M.%S")
videoname=str(today)+('_contours' if show_contours == True else '')+("_dog" if Dog_mode == True else '')+('_cube' if Cube_mode == True else '')+('_smooth' if Smooth_mode == True else '')+str(video_src)
fps_out = 29
out = cv2.VideoWriter(str(videoname)+".avi", fourcc, fps_out, (1920, 1080))

tag_ids = ['0101','0111','1111']
img_paths = ['data/Tucker.jpg','data/Hailey.jpg','data/Tessa.jpg']

video = cv2.VideoCapture('data/data_'+str(video_src)+'.mp4') 

#start_frame = 400

#ret=True

#count = start_frame
#video.set(1,start_frame)

print("Reading video into memory...")
count = 0
frame_array=[]
flag = False

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

total_frames=len(frame_array)

for count,frame in enumerate(frame_array):
    cur_bot = getCorners(frame)
    cur_top = getTopCorners(cur_bot)
    if count == 0:
        p1 = {}
        p1t = {}
        p2 = {}
        p2t = {}

    if count==total_frames-2:
        break
        # f1 = getCorners(frame_array[count+1])
        # f1t = getTopCorners(f1)
        # f2 = {}
        # f2t = {}
    # elif count==total_frames:
    #     f1 = {}
    #     f1t = {}
    #     f2 = {}
    #     f2t = {}
    else:
        f1 = getCorners(frame_array[count+1])
        f1t = getTopCorners(f1)
        f2 = getCorners(frame_array[count+2])
        f2t = getTopCorners(f2)

    bot_corners=avgCorners(p2, p1, cur_bot, f1, f2)
    top_corners=avgCorners(p2t, p1t, cur_top, f1t, f2t)

    for tag_id in bot_corners:
        set1 = bot_corners[tag_id]
        set2 = top_corners[tag_id]
        frame=drawCube(set1,set2,frame,face_color,edge_color,flag)

    p2=p1
    p2t = p1t
    p1=bot_corners
    p1t=top_corners

    if not Fast_mode:
        cv2.imshow("Frame",frame)

    if cv2.waitKey(1) == ord('q'):
            break

    out.write(frame)

out.release()





# print("Cur")
# for tag in current_corners:
#     print(tag)
#     print(current_corners[tag])

# print("F1")
# for tag in f1:
#     print(tag)
#     print(f1[tag])

# print("F2") 
# for tag in f2:
#     print(tag)
#     print(f2[tag])


# print("P1")
# for tag in p1:
#     print(tag)
#     print(p1[tag])

# print("P2") 
# for tag in p2:
#     print(tag)
#     print(p2[tag])

# average_corners=avgCorners(p2, p1, current_corners, f1, f2)
# print("Avg")
# for tag in average_corners:
#     print(tag)
#     print(average_corners[tag])



