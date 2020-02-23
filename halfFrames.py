import cv2
# from PIL import Image 
def halfFrames(frame_array):
	# Take in frame_array (effectively a video)
	new_frame_array=[]
	print("Time to make some half frames. This will take a moment")
	for i in range(0,len(frame_array)-1):
		# add the frame to the new array
		new_frame_array.append(frame_array[i])

		# compute the half frame between that frame and it's next
		#half_frame=(frame_array[i]+frame_array[i+1])*.5
		#half_frame=Image.blend(frame_array[i], frame_array[i+1], .5)
		half_frame = cv2.addWeighted(frame_array[i], 0.5, frame_array[i+1], 0.5, 0) 
		#cv2.imshow("half",half_frame)
		#cv2.waitKey(0)
		#print("made a half frame for frame #"+str(i))

		# add the half frame to the array
		new_frame_array.append(half_frame)

	print("Done")
	return new_frame_array
