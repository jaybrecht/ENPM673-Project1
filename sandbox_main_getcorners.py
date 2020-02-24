import cv2
import math
from functions import*
from cube import*
import time

video_src = 3 # 1 for data1, 2 for data2, 3 for data3

# Cube settings
face_color = (100, 100, 100) 
edge_color = (0, 0, 0) 


K=np.array([[1406.08415449821,0,0],
           [2.20679787308599, 1417.99930662800,0],
           [1014.13643417416, 566.347754321696,1]])

tag_ids = ['0101','0111','1111']
img_paths = ['data/Tucker.jpg','data/Hailey.jpg','data/Tessa.jpg']

video = cv2.VideoCapture('data/data_'+str(video_src)+'.mp4') 

#start_frame = 400

#ret=True

#count = start_frame
#video.set(1,start_frame)

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

total_frames=len(frame_array)

for count,frame in enumerate(frame_array):
    current_corners=getCorners(frame)
    if count == 0:
        p1={}
        p2={}


    if count==total_frames-1:
        f1=getCorners(frame_array[count+1])
        f2={}
    elif count==total_frames:
        f1={}
        f2={}
    else:
        f1=getCorners(frame_array[count+1])
        f2=getCorners(frame_array[count+2])

    average_corners=avgCorners(p2, p1, current_corners, f1, f2)
    p2=p1
    p1=current_corners



#     count += 1
#     #video.read()
#     ret, frame = video.read()




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



