# A tensor is a NumPy-like array that can also run on a GPU and track gradients.
# Each line has a short comment saying WHAT it is.

# numpy: array maths library.
import numpy as np
# torch (PyTorch): library for tensors and deep learning.
import torch

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Creating
# torch.tensor(data): makes a tensor from a list; floats give float32.
a = torch.tensor([1.0, 2.0, 3.0])
# A list of lists makes a 2D tensor (a table); whole numbers give int64.
b = torch.tensor([[1, 2], [3, 4]])
# dtype = kind of number stored; shape = size of each dimension.
print(a, a.dtype, a.shape)
print(b, b.dtype)
# zeros(r, c): all 0s; ones: all 1s; full(shape, value): filled with one value.
print(torch.zeros(2, 3), torch.ones(2, 2), torch.full((2, 2), 7.0))
# arange(n): 0..n-1; linspace(start, end, count): evenly spaced numbers.
print(torch.arange(6), torch.linspace(0, 1, 5))
# eye(n): identity matrix (1s on the diagonal).
print(torch.eye(3))
# manual_seed(0): fixes random numbers so results repeat.
torch.manual_seed(0)
# rand: random 0 to 1; randn: random bell-curve numbers; randint(low, high, shape): random whole numbers.
print(torch.rand(2, 2), torch.randn(2, 2), torch.randint(0, 10, (5,)))

# %% Attributes
# randn(3, 4): 3x4 tensor of random numbers.
x = torch.randn(3, 4)
# ndim = number of dimensions; numel() = total items; device = where it lives (CPU or GPU).
print(x.shape, x.ndim, x.numel(), x.dtype, x.device)

# %% Math works like NumPy
# Operators work item by item; sqrt = square root; exp = e to the power.
print(a + 10, a * a, a ** 2, torch.sqrt(a), torch.exp(a))
# sum/mean/max/std: total, average, biggest, spread; argmax = position of the biggest.
print(a.sum(), a.mean(), a.max(), a.argmax(), a.std())
# dim=0 sums down the rows, dim=1 across columns.
print(x.sum(dim=0).shape, x.mean(dim=1).shape)           # dim is the same as axis

# %% Indexing and reshaping
# x[0] = first row; x[:, 1] = second column; x[x > 0] = only items above 0.
print(x[0], x[:, 1], x[x > 0].shape)
# reshape = new shape; view(-1) = flatten (-1 = figure it out); .T = swap rows/columns; unsqueeze(0) = add a new dimension.
print(x.reshape(2, 6).shape, x.view(-1).shape, x.T.shape, x.unsqueeze(0).shape)
# cat: glue tensors along an existing dimension; stack: glue along a new one.
print(torch.cat([x, x]).shape, torch.stack([x, x]).shape)

# %% Matrix multiplication (the heart of neural networks)
# A weight matrix of random numbers.
w = torch.randn(4, 2)
# @ = matrix multiplication (rows times columns).
print((x @ w).shape)
# matmul: the same as @.
print(torch.matmul(x, w).shape)

# %% NumPy <-> torch (they can share memory)
# np.array: a NumPy array.
array = np.array([1.0, 2.0, 3.0])
# from_numpy: NumPy array -> tensor (shares memory); numpy(): tensor -> NumPy.
t = torch.from_numpy(array)
print(t, t.numpy())


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Types and devices
# to(dtype) / long(): convert the number type (16-bit float, 64-bit integer).
print(a.to(torch.float16).dtype, a.long().dtype)
# is_available(): True if an NVIDIA GPU (cuda) or Apple GPU (mps) can be used.
print("cuda available:", torch.cuda.is_available(), "| mps (Apple GPU):", torch.backends.mps.is_available())
# Picks the best available device, else 'cpu'.
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print("using", device)
# to(device): moves the tensor to that device.
on_device = x.to(device)
print(on_device.device)

# %% In-place operations end with an underscore
# ones(3): tensor [1, 1, 1].
c = torch.ones(3)
# A name ending with _ changes the tensor itself (adds 5).
c.add_(5)
print(c)

# %% Broadcasting works just like NumPy
# Broadcasting: shapes stretch to fit, giving a 3x4 result.
print(torch.ones(3, 1) + torch.arange(4))
