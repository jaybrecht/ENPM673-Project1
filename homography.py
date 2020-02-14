import numpy as np


x = [5, 150, 150, 5]
y = [5, 5, 150, 150]
xp = [100, 200, 220, 100]
yp = [100, 80, 80, 200]

n = 9
m = 8
A = np.empty([m, n])

val = 0
for row in range(0,m):
    if (row%2) == 0:
        A[row,0] = -x[val]
        A[row,1] = -y[val]
        A[row,2] = -1
        A[row,3] = 0
        A[row,4] = 0
        A[row,5] = 0
        A[row,6] = x[val]*xp[val]
        A[row,7] = y[val]*xp[val]
        A[row,8] = xp[val]
    else:
        A[row,0] = 0
        A[row,1] = 0
        A[row,2] = 0
        A[row,3] = -x[val]
        A[row,4] = -y[val]
        A[row,5] = -1
        A[row,6] = x[val]*yp[val]
        A[row,7] = y[val]*yp[val]
        A[row,8] = yp[val]
        val += 1

U,S,V = np.linalg.svd(A)

# Check to see if A = USV' 
# A_ = np.round(np.linalg.multi_dot([U,S,np.transpose(V)]))
# print(A_)

# x is equivalent to the eigenvector column of V that corresponds to the 
# smallest singular value. A*x ~ 0
x = V[:,-1]

# reshape x into H
H = np.reshape(x,[3,3])

print("Homography Matrix for A")
print(H)




