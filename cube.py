import numpy as np
import cv2
from functions import*

def projection_mat(K,H):
	h1=H[:,0]
	h2=H[:,1]

	K=np.transpose(K)

	K_inv=np.linalg.inv(K)
	a=np.dot(K_inv,h1)
	c=np.dot(K_inv,h2)
	lamda=1/((np.linalg.norm(a)+np.linalg.norm(c))/2)

	Bhat=np.dot(K_inv,H)

	if np.linalg.det(Bhat)>0:
		B=1*Bhat
	else:
		B=-1*Bhat

	b1=B[:,0]
	b2=B[:,1]
	b3=B[:,2]
	r1=lamda*b1
	r2=lamda*b2
	r3=np.cross(r1,r2)
	t=lamda*b3

	P=np.dot(K,(np.stack((r1,r2,r3,t), axis=1)))

	return P



def cubePoints(corners, H, P, dim):
	# corners =[p1,p2,p3,p4]
	# pi=[xi,yi]
	new_points = []
	new_corners=[]
	x = []
	y = []
	for point in corners:
		x.append(point[0])
		y.append(point[1])
	H_c = np.stack((np.array(x),np.array(y),np.ones(len(x))))

	sH_w=np.dot(H,H_c)

	H_w=sH_w/sH_w[2]
	
	P_w=np.stack((H_w[0],H_w[1],np.full(4,-dim),np.ones(4)),axis=0)

	sP_c=np.dot(P,P_w)
	P_c=sP_c/(sP_c[2])

	for i in range(4):
		new_corners.append([int(P_c[0][i]),int(P_c[1][i])])

	return new_corners


def drawCube(tagcorners, new_corners,frame,face_color,edge_color,flag):
	thickness=5
	if not flag:
		contours = makeContours(tagcorners,new_corners)
		for contour in contours:
			cv2.drawContours(frame,[contour],-1,face_color,thickness=-1)

	for i, point in enumerate(tagcorners):
		cv2.line(frame, tuple(point), tuple(new_corners[i]), edge_color, thickness) 

	for i in range (4):
		if i==3:
			cv2.line(frame,tuple(tagcorners[i]),tuple(tagcorners[0]),edge_color,thickness)
			cv2.line(frame,tuple(new_corners[i]),tuple(new_corners[0]),edge_color,thickness)
		else:
			cv2.line(frame,tuple(tagcorners[i]),tuple(tagcorners[i+1]),edge_color,thickness)
			cv2.line(frame,tuple(new_corners[i]),tuple(new_corners[i+1]),edge_color,thickness)

	return frame


def makeContours(corners1,corners2):
	contours = []
	for i in range(len(corners1)):
		if i==3:
			p1 = corners1[i]
			p2 = corners1[0]
			p3 = corners2[0]
			p4 = corners2[i]
		else:
			p1 = corners1[i]
			p2 = corners1[i+1]
			p3 = corners2[i+1]
			p4 = corners2[i]
		contours.append(np.array([p1,p2,p3,p4], dtype=np.int32))
	contours.append(np.array([corners1[0],corners1[1],corners1[2],corners1[3]], dtype=np.int32))
	contours.append(np.array([corners2[0],corners2[1],corners2[2],corners2[3]], dtype=np.int32))

	return contours


def getTopCorners(bot_corners):
	K = np.array([[1406.08415449821,0,0],
			[2.20679787308599, 1417.99930662800,0],
 			[1014.13643417416, 566.347754321696,1]])

	top_corners = {}

	for tag_id, corners in bot_corners.items():
		H = homography(corners,200)
		H_inv = np.linalg.inv(H)
		P = projection_mat(K,H_inv)
		top_corners[tag_id] = cubePoints(corners, H, P, 200)

	return top_corners