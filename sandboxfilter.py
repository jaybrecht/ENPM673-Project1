import cv2

def moveMean(framecornersarray,stepsize):
		# [all_cnts,cnts] = findcontours(frame,180)
	 #        #approximate quadralateral to each contour and extract corners
	 #    [tag_cnts,corners] = approx_quad(cnts)


	print(framecornersarray)
	 # for tag_set in range(0,len(framecornersarray)):
	 # 	framecornersarray[tag_set] #3 lists, each containing x,y
	 # 	framecornersarray[tag_set][0] #tag 1, containing x,y
	 # 	framecornersarray[tag_set][0][0] #tag 1 x
	 # 	framecornersarray[tag_set][0][1] #tag 1 y

 	for i,tag_set in enumerate(framecornersarray-stepsize):
	 	# tag_set #3 lists, each containing x,y = framecornersarray[i]
	 	# tag_set[0] #tag 1, containing x,y
	 	# tag_set[0][0] #tag 1 x
	 	# tag_set[0][1] #tag 1 y


		#framecornersarray is a list of list of lists?
		# each top level element is corners from original main
		# each "corners" contains 3 lists, one for each tag
		# each of those 3 lists contains an x,y for that corner
	 	# Want:
# (framecornersarray[i][tag][x]+framecornersarray[i+1][tag][x]+...+framecornersarray[i+stepsize][tag][x])/stepsize
# (framecornersarray[i][tag][y]+framecornersarray[i+1][tag][y]+...+framecornersarray[i+stepsize][tag][y])/stepsize



	x=0
	y=1
	for tag in range(0,len(framecornersarray[i])): #should be 1,2, or 3
		new_tag_set=[]
		for i in range(0,stepsize):
			new_x_set.append(framecornersarray[i][tag][x])

		new_x=sum(new_x_set)/stepsize







	 	# tag_sets_to_avg=[]
	 	# for j in range (0,stepsize):
	 	# 	tag_sets_to_avg.append(framecornersarray[j])



	 	new_tag_set=mean(tag_sets_to_avg[0][1])



	 cv2.waitKey(0)



# for i in range (0,len(video)-stepsize):
# 	for j in range (0,stepsize)
# 		all_corners.append(corners[j])
	
# 	avg_corners[i]=mean(all_corners)


