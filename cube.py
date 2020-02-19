import numpy as np
import cv2

def projection_mat(K,H):
	h1=H[:,0]
	h2=H[:,1]
	h3=H[:,2]

	K=np.transpose(K)

	K_inv=np.linalg.inv(K)
	a=np.dot(K_inv,h1)
	c=np.dot(K_inv,h2)
	# lamda=1/((np.linalg.norm(a)+np.linalg.norm(c))/2)
	lamda=400

	Bhat=lamda*np.dot(K_inv,H)

	if np.linalg.det(Bhat)>0:
		B=lamda*Bhat
	else:
		B=-lamda*Bhat

	b1=B[:,0]
	b2=B[:,1]
	b3=B[:,2]
	r1=lamda*b1
	r2=lamda*b2
	r3=np.cross(r1,r2)
	t=lamda*b3

	P=np.dot(K,(np.stack((r1,r2,r3,t), axis=1)))
	#print(P)

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
	# print("P_w")
	# print(P_w)
	# print("P")
	# print(P)

	sP_c=np.dot(P,P_w)
	P_c=sP_c/sP_c[2]
	print(P_c)
	
	for i in range(4):
		new_corners.append([int(P_c[0][i]),int(P_c[1][i])])

	return new_corners


def drawCube(tagcorners, new_corners,frame):
	color=(0, 0, 255) 
	thickness=2
	for i, point in enumerate(tagcorners):
		cv2.line(frame, tuple(point), tuple(new_corners[i]), color, thickness) 

	for i in range (4):
		if i==3:
			cv2.line(frame,tuple(tagcorners[i]),tuple(tagcorners[0]),color,thickness)
			cv2.line(frame,tuple(new_corners[i]),tuple(new_corners[0]),color,thickness)
		else:
			cv2.line(frame,tuple(tagcorners[i]),tuple(tagcorners[i+1]),color,thickness)
			cv2.line(frame,tuple(new_corners[i]),tuple(new_corners[i+1]),color,thickness)

	return frame

#H=np.array([[1,2,3],[4,5,6],[7,8,9]])


# P=projection_mat(K,H)


# print(P)