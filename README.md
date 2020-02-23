# ENPM673-Project1

This project tracks up to 3 AR tags in a video. Examples of the 3 tags (after processing) can be seen below. These tags are divided into an 8x8 grid for orientation analysis and identification. 


![tag1](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/tag1.png) ![tag2](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/tag2.png) ![tag3](https://github.com/jaybrecht/ENPM673-Project1/blob/master/images/tag3.png) 


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


## video_src
This allows you to change which of the three available videos are used in the program. 

`video_src = 1` is the first video (data_1.mp4), which has 1 AR tag. 

`video_src = 2` is the second video (data_2.mp4), which has 2 AR tags. 

`video_src = 3` is the third video (data_3.mp4), which has 3 AR tags.

You can use any of these three videos with any combination of other modes. 


# How It Works


