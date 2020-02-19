import numpy as np

def projection_mat(K,H):
	h1=H[:,0]
	h2=H[:,1]
	h3=H[:,2]

	# K=np.linalg.transpose(K)

	K_inv=np.linalg.inv(K)
	a=np.dot(K_inv,h1)
	c=np.dot(K_inv,h2)
	lamda=1/((np.linalg.norm(a)+np.linalg.norm(c))/2)

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

	return P



def cubePoints(corners, H, P, dim):
	# corners =[p1,p2,p3,p4]
	# pi=[xi,yi]
	new_corners=[]
	for point in corners:
		H_c=np.array([point[0],point[1],1])
		sH_w=np.dot(H,H_c)
		H_w/=sH_w[2]


		P_w=np.stack((H_w[0],H_w[1],-dim,1),axis=0)
		sP_c=np.dot(P_w)
		P_c/=sP_c[3]

		new_corners.append([int(P_c[0]),int(P_c[1])])

	return new_corners


def drawCube(tagcorners, new_corners,frame):
	color=(0, 0, 255) 
	thickness=2
	for i, point in enumerate(tagcorners):
		cv2.line(frame, point, new_corners[i], color, thickness) 

	for i in range (4)
		if i==3:
			cv2.line(frame,tagcorners[i],tagcorners[0],color,thickness)
			cv2.line(frame,new_corners[i],new_corners[0],color,thickness)
		else:
			cv2.line(frame,tagcorners[i],tagcorners[i+1],color,thickness)
			cv2.line(frame,new_corners[i],new_corners[i+1],color,thickness)



H=np.array([[1,2,3],[4,5,6],[7,8,9]])

K=np.array([[1406.08415449821,0,0],
		   [2.20679787308599, 1417.99930662800,0],
		   [1014.13643417416, 566.347754321696,1]])

P=projection_mat(K,H)


print(P)