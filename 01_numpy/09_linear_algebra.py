# Linear algebra: the math behind machine learning.

import numpy as np

A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([1.0, 2.0])

# %% Basics
print(A.T)
print(np.trace(A))
print(np.linalg.det(A))
print(np.linalg.matrix_rank(A))
print(np.diag(A))

# %% Inverse and identity
inverse = np.linalg.inv(A)
print(inverse)
print(np.round(A @ inverse, 10))        # identity matrix

# %% Solve  A x = b  (better than inv(A) @ b)
x = np.linalg.solve(A, b)
print(x)
print(A @ x)

# %% Norms (length of vectors / size of matrices)
v = np.array([3.0, 4.0])
print(np.linalg.norm(v))                # 5.0
print(np.linalg.norm(v, ord=1))         # sum of absolute values
print(np.linalg.norm(A))                # Frobenius norm for matrices

# %% Eigenvalues and eigenvectors
values, vectors = np.linalg.eig(A)
print(values)
print(vectors)
print(A @ vectors[:, 0], values[0] * vectors[:, 0])   # A v = lambda v
print(np.linalg.eigvals(A))

# %% SVD (used in PCA and recommendation systems)
U, S, Vt = np.linalg.svd(A)
print(U, S, Vt)
print(np.allclose(U @ np.diag(S) @ Vt, A))

# %% Matrix power and products
print(np.linalg.matrix_power(A, 3))
print(np.dot(A, A))
print(np.kron(np.eye(2), A))

# %% Least squares (line fitting)
xs = np.array([0, 1, 2, 3])
ys = np.array([1, 3, 5, 7])
design = np.column_stack([xs, np.ones_like(xs)])
solution, residuals, rank, singular = np.linalg.lstsq(design, ys, rcond=None)
print(solution)                         # slope 2, intercept 1

# %% Cosine similarity (core idea behind AI embeddings)
u = np.array([1.0, 2.0, 3.0])
w = np.array([2.0, 4.0, 6.0])
cosine = u @ w / (np.linalg.norm(u) * np.linalg.norm(w))
print(cosine)                           # 1.0 means same direction

# %% Einstein summation (a compact way to write products)
print(np.einsum("i,i->", u, w))         # dot product
print(np.einsum("ij,jk->ik", A, A))     # matrix product
print(np.einsum("ii->", A))             # trace
