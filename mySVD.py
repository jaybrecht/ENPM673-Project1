import numpy as np

def mySVD(A):
    # Get eigenvalues and eigenvectors of A*A^t
    m = A.shape[0];
    n = A.shape[1];

    At = np.transpose(A)
    eigenvalues, eigenvectors = np.linalg.eig(np.dot(At,A))

    # Find the order of the indicies of the eigenvalues from largest to smallest
    val_order = np.flip(np.argsort(eigenvalues))

    # Sort the eigenvector columns to reflect the order of the eigenvalues
    V = np.empty([n, n])
    for i in range(0,n):
        V[:,i] = eigenvectors[:,val_order[i]]

    # Sort the eigenvalues
    eigenvalues = np.flip(np.sort(eigenvalues))
    if n>m:
        eigenvalues = np.delete(eigenvalues,m)

    # Find the singular values and compute the Sigma matrix
    sing_vals = np.sqrt(eigenvalues)
    S = np.zeros([m, n])
    for i in range(0,m):
        S[i,i] = sing_vals[i]

    # Use the property that A*v_i = sigma_i*u_i to compute U 
    U = np.empty([m, m])
    for i in range(0,m):
        U[:,i] = np.dot(A,V[:,i])/S[i,i]

    return U,S,V
