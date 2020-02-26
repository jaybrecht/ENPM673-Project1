# ENPM673-Project1

This project tracks up to 3 AR tags in a video. Examples of the 3 tags (after processing) can be seen below. These tags are divided into an 8x8 grid for orientation analysis and identification. 


![tag1](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/tag1.jpg) ![tag2](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/tag2.jpg) ![tag3](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/tag3.jpg) 


# Program Modes
The program has several modes, all accessible via a series of Boolean toggles at the top of `main.py`.

## Write_to_video
This mode, when set `True`, saves the output of the video to an AVI file. The video will save in the same directory as `main.py`. The name of the video is determined by the modes you have enabled, so that the output video filename is a clear log of the configuration it recorded. If you only want to export a video (to watch later) we recommend toggling `Fast_mode` to `True`. This disables previewing the frames on screen, and offers some performance increases. `Fast_mode` is not recommended in conjunction with any other mode. 

## show_contours
You have the option to enable the display of the contours found in the frame. Green contours denote the outer edge of the paper. The blue contours denote the edge of the AR tag. This mode can be enabled alongside any other mode. 
![contours](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/contours.png)

## Dog_mode
Dog_mode, when toggled `True`, takes our 3 dog images and superposes them on their respective tags. 
![dog_mode](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/dog_mode.jpeg)

## Cube_mode
Cube_mode displays a cube on each tag. You can run `Dog_mode` and `Cube_mode` at the same time. If you do, the cubes will render transparent so that the dogs can be seen on the bottom face. If you run just `Cube_mode`, the cubes will render with grey faces. 

![cube_mode](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/cube_mode.png)

You can change the color of the cube faces by editing `face_color` near the top of `main.py`. The colors are in (B,G,R) from 0-255. Similarly, you can edit the color of the cube edges by changing `edge_color` near the top of `main.py`.
The cube faces can also be colored to correspond to their unique tag IDs. 
![colored_cubes](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/colored_cubes.png)


## video_src
This allows you to change which of the three available videos are used in the program. 

`video_src = 1` is the first video (data_1.mp4), which has 1 AR tag. 

`video_src = 2` is the second video (data_2.mp4), which has 2 AR tags. 

`video_src = 3` is the third video (data_3.mp4), which has 3 AR tags.

You can use any of these three videos with any combination of other modes. 


# Smooth Cubes
There is another executable program in this set: `smooth_cubes.py`. This program renders cubes with less jittery motion. It uses a forward and backward looking approach, averaging the cube corner positions over several preceeding and post frames. Similarly to `main.py`, there are several customizable program parameters that can be adjusted at the top of `smooth_cubes.py`: 

Once again, `write_to_video` toggles saving the output video file and `video_src` changes the input source video.
`num_future_frames` is the number of frames (in both directions) to average the points over. This smoothing function works for an arbitrary number of preceding and post frames, allowing for varying amounts of smoothing. The more frames that are averaged results in a smoother, less jittery cube, but may cause cube drift, where the cube position slides slightly from the tag due to camera movement in neighboring frames. Cube drift becomes more noticeable as the frame count increases.



# Notes on Usage
Everything is designed to run in Python 3.7. Download the entire directory before beginning (all files are required). Open `main.py` and adjust the toggle parameters to the configuration you want to run. Save the file and run `python3 main.py` in Terminal. The run may take several minutes, depending on the configuration selected.

You can also run `smooth_cubes.py` in the same fashion. We do not recommend running `main.py` and `smooth_cubes.py` simultaneously. 



## Required Packages
The following packages are required for this project:
* numpy
* cv2
* math
* time


# How it Works
For a more detailed overview of program functionality and processes, please read `Report.pdf`.


# Videos
## 1 Tag

Dog: https://youtu.be/eMDw7v8iKVM

Dog and Contours: https://youtu.be/u8Eu2P4GyU8

Cube: https://youtu.be/832ytyWuLog

Cube and Contours: https://youtu.be/AOtB_EfQM8M

Cube and Dog: https://youtu.be/XJA6ZihT7dM

Cube, Dog, and Contours: https://youtu.be/5Ye-M5kQ49s


## 1 Tag - Smoothed

Cube (4 frames, with color): https://youtu.be/e78oBha6Y-k

Cube (5 frames): https://youtu.be/ptrkv0mcJ-o

Cube (15 frames): https://youtu.be/4-SMcVtxhTY


## 2 Tags

Dogs: https://youtu.be/W07xNjdikj4

Dogs and Contours: https://youtu.be/MZroDtzSx2U

Cubes: https://youtu.be/qDmahYQLtnI

Cubes and Contours: https://youtu.be/Y0AVKwwF5Rs

Cubes and Dogs: https://youtu.be/G0JwnAY8btk

Cubes, Dogs, and Contours: https://youtu.be/SjvsdsYbnNc


## 2 Tags - Smoothed

Cubes (4 frames, with color): https://youtu.be/LD1vFiq3ZNg

Cubes: (5 frames) https://youtu.be/WOoJEzgwbFA


## 3 Tags

Dogs: https://youtu.be/6kUJMu_lp6s

Dog and Contours: https://youtu.be/hTnjIdVy1As

Cubes: https://youtu.be/S5xvTcTTBsw

Cubes and Contours: https://youtu.be/pob9dMti9o0

Cubes and Dogs: https://youtu.be/ERwL77zEsw8

Cubes, Dogs, and Contours: https://youtu.be/j1lANCtlTnI




## 3 Tags - Smoothed
Cubes (4 Frames, with color): https://youtu.be/bwa-wyenpoI

Cubes (5 Frames): https://youtu.be/UzQukBC6EkI

Cubes (15 Frames): https://youtu.be/ZHo5AcK5vZE
