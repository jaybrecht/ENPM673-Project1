import cv2
# from PIL import Image 
def halfFrames(frame_array):
	# Take in frame_array (effectively a video)
	new_frame_array=[]
	print("Time to make some half frames. This will take a moment")
	for i in range(0,len(frame_array)-300):
		# add the frame to the new array
		new_frame_array.append(frame_array[i])

		# compute the half frame between that frame and it's next
		for q in range(1,10):
			a=.1*q
			b=1-a
			#print(b,a)
			half_frame = cv2.addWeighted(frame_array[i], b, frame_array[i+1], a, 0) 

			# add the half frame to the array
			new_frame_array.append(half_frame)

	print("Done")
	return new_frame_array
