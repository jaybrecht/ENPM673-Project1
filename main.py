import cv2
import math
from functions import*
from cube import*

video = cv2.VideoCapture('data/data_3.mp4') 

fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps_out = 29
out = cv2.VideoWriter('output.avi', fourcc, fps_out, (1920, 1080))

K=np.array([[1406.08415449821,0,0],
           [2.20679787308599, 1417.99930662800,0],
           [1014.13643417416, 566.347754321696,1]])

tag_ids = ['0101','0111','1111']
img_paths = ['data/Tucker.jpg','data/Hailey.jpg','data/Tessa.jpg']

print("Writing to Video, Please Wait")
count = 1
while(video.isOpened()):
    print("Current frame:" + str(count))
    count += 1
    ret, frame = video.read()
    #find correct contours
    cnts = findcontours(frame,190)
    #approximate quadralateral to each contour and extract corners
    [tag_cnts,corners] = approx_quad(cnts)
    # cv2.drawContours(frame,tag_cnts,-1,(255,0,0), 4)
    for i,tag in enumerate(corners):        
        #find list of points in each tag
        orig_points = points_in_poly(frame,tag_cnts[i])

        #find applicable size for squared image based on total number of points
        tag_dim = int(math.sqrt(len(orig_points)))
        #compute homography
        H = homography(tag,tag_dim)
        
        #get squared tile
        square_img = warp2square(orig_points,H,tag_dim)
        
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

        #blank tag area in image
        frame = blank_region(frame,orig_points)

        #superimpose the image on the tag
        H = homography(tag,rotated_img.shape[0])
        H_inv = cv2.invert(H)[1]
        frame = square2warp(frame,rotated_img,H_inv)

        # Find new cube points and draw on image
        # H=homography(tag,5)
        # P=projection_mat(K,H)
        # new_corners=cubePoints(tag, H, P, 5)
        # frame=drawCube(tag, new_corners,frame)

    # cv2.imshow("Frame",frame)
    # cv2.waitKey(0)
    out.write(frame)
    if cv2.waitKey(1) == ord('q'):
        break

out.release()