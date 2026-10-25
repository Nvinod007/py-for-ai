# Linear algebra: the math behind machine learning.
# Each line has a short comment saying WHAT it is.

import numpy as np

A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([1.0, 2.0])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Basics
print(A.T)                              # transpose: swap rows and columns
print(np.trace(A))                      # trace: sum of the diagonal
print(np.linalg.det(A))                 # determinant: one number describing the matrix
print(np.linalg.matrix_rank(A))         # rank: how many independent rows/columns
print(np.diag(A))                       # the diagonal values

# %% Inverse and identity
# np.linalg.inv(A): the matrix that "undoes" A.
inverse = np.linalg.inv(A)
print(inverse)
print(np.round(A @ inverse, 10))        # A times its inverse = identity matrix

# %% Solve  A x = b  (better than inv(A) @ b)
# np.linalg.solve(A, b): finds x so that A @ x equals b.
x = np.linalg.solve(A, b)
print(x)
print(A @ x)                            # check: gives b back

# %% Norms (length of vectors / size of matrices)
v = np.array([3.0, 4.0])
# np.linalg.norm(v): the length of a vector (straight-line distance from 0).
print(np.linalg.norm(v))                # 5.0
print(np.linalg.norm(v, ord=1))         # ord=1: sum of absolute values
print(np.linalg.norm(A))                # for a matrix: sqrt of sum of all squares

# %% Cosine similarity (core idea behind AI embeddings)
u = np.array([1.0, 2.0, 3.0])
w = np.array([2.0, 4.0, 6.0])
# cosine similarity: how much two vectors point the same way (1 = identical direction).
cosine = u @ w / (np.linalg.norm(u) * np.linalg.norm(w))
print(cosine)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Eigenvalues and eigenvectors
# np.linalg.eig(A): special directions (vectors) a matrix only stretches,
# and by how much (values).
values, vectors = np.linalg.eig(A)
print(values)
print(vectors)
print(A @ vectors[:, 0], values[0] * vectors[:, 0])   # both sides are equal
print(np.linalg.eigvals(A))             # just the values

# %% SVD (used in PCA and recommendation systems)
# np.linalg.svd(A): splits a matrix into three simpler matrices U, S, Vt.
U, S, Vt = np.linalg.svd(A)
print(U, S, Vt)
print(np.allclose(U @ np.diag(S) @ Vt, A))   # multiplying them back gives A

# %% Matrix power and products
# np.linalg.matrix_power(A, n): A multiplied by itself n times.
print(np.linalg.matrix_power(A, 3))
print(np.dot(A, A))                     # same as A @ A
# np.kron(x, y): Kronecker product: copies of y scaled by each cell of x.
print(np.kron(np.eye(2), A))            # eye(2): 2x2 identity matrix

# %% Least squares (line fitting)
xs = np.array([0, 1, 2, 3])
ys = np.array([1, 3, 5, 7])
# np.column_stack: put arrays side by side as columns.
design = np.column_stack([xs, np.ones_like(xs)])   # ones_like: array of 1s, same shape
# np.linalg.lstsq: finds the best-fit solution when no exact one exists.
solution, residuals, rank, singular = np.linalg.lstsq(design, ys, rcond=None)
print(solution)                         # slope 2, intercept 1

# %% Einstein summation (a compact way to write products)
# np.einsum("pattern", ...): describe a multiply-and-sum with letters.
print(np.einsum("i,i->", u, w))         # dot product
print(np.einsum("ij,jk->ik", A, A))     # matrix product
print(np.einsum("ii->", A))             # trace
