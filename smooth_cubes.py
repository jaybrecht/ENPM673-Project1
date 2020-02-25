import cv2
import math
from functions import*
from cube import*
import time

# Cube settings
face_colors = [(0, 127, 255),(255, 127, 0),(0, 191, 0)] 
tag_ids = ['0101','0111','1111']
edge_color = (0, 0, 0)

write_to_video = True
video_src = 3 # 1 for data1, 2 for data2, 3 for data3 
num_future_frames = 4 
start_frame = 0

video = cv2.VideoCapture('data/data_'+str(video_src)+'.mp4') 

if write_to_video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    today = time.strftime("%m-%d__%H.%M.%S")
    videoname=str(today)+"smooth_cube"+str(video_src)
    fps_out = 29
    out = cv2.VideoWriter(str(videoname)+".avi", fourcc, fps_out, (1920, 1080))
    print("Writing to Video, Please Wait")

frame_num = start_frame
video.set(1,start_frame)

fut_frames = []
flag = False

p_bot,p_top = [],[]

while(video.isOpened()):
    print("Frame: " + str(frame_num))
    
    if frame_num == start_frame:
        ret,cur_frame = video.read()
        for num in range(num_future_frames):
            ret,frontier = video.read()
            fut_frames.append(frontier)
    else:
        cur_frame = fut_frames.pop(0)
        ret,frontier = video.read()
        fut_frames.append(frontier)
    
    if ret:
        cur_bot = getCorners(cur_frame)
        cur_top = getTopCorners(cur_bot)

        f_bot,f_top = [],[]

        for fframe in fut_frames:
            d = getCorners(fframe)
            f_bot.append(d)
            f_top.append(getTopCorners(d))

        bot_corners=avgCorners(p_bot, cur_bot, f_bot)
        top_corners=avgCorners(p_top, cur_top, f_top)

        frame = cur_frame.copy()
        for tag_id in bot_corners:
            id_str = str(tag_id)
            if id_str in tag_ids:
                index = tag_ids.index(id_str)
                face_color = face_colors[index]
            else:
                continue
            set1 = bot_corners[tag_id]
            set2 = top_corners[tag_id]
            frame=drawCube(set1,set2,frame,face_color,edge_color,flag)

        p_bot.append(bot_corners)
        p_top.append(top_corners)
        if(len(p_bot) > num_future_frames):
            p_bot.pop(0)
            p_top.pop(0)

        cv2.imshow("Smooth Cubes",frame)

        if cv2.waitKey(1) == ord('q'):
                break

        frame_num += 1

        if write_to_video:
            out.write(frame)
    else:
        video.release()

if write_to_video:
    out.release()