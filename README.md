# ENPM673-Project1

This project tracks up to 3 AR tags in a video. The program has several modes, all accessible via a series of Boolean toggles at the top of `main.py`.

## Write_to_video
This mode, when set `True`, saves the output of the video to an AVI file. The video will save in the same directory as `main.py`. If you only want to export a video (to watch later) we recommend toggling `Fast_mode` to `True`. This disables previewing the frames on screen, and offers some performance increases. `Fast_mode` is not recommended in conjunction with any other mode.

## show_contours
You have the option to enable the display of the contours found in the frame. Green contours denote the outer edge of the paper. The blue contours denote the edge of the AR tag. This mode can be enabled alongside any other mode. 

## Dog_mode
Dog_mode, when toggled `True`, takes our 3 dog images and superposes them on their respective tags. 

## Cube_mode
Cube_mode displays a cube on each tag. You can run `Dog_mode` and `Cube_mode` at the same time. If you do, the cubes will render transparent so that the dogs can be seen on the bottom face. If you run just `Cube_mode`, the cubes will render with grey faces. 

## video_src
This allows you to change which of the three available videos are used in the program. 

`video_src = 1` is the first video (data_1.mp4), which has 1 AR tag. 

`video_src = 2` is the second video (data_2.mp4), which has 2 AR tags. 

`video_src = 3` is the third video (data_3.mp4), which has 3 AR tags.

You can use any of these three videos with any combination of other modes. 