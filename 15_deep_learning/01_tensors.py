# A tensor is a NumPy-like array that can also run on a GPU and track gradients.

import numpy as np
import torch

# %% Creating
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([[1, 2], [3, 4]])
print(a, a.dtype, a.shape)
print(b, b.dtype)
print(torch.zeros(2, 3), torch.ones(2, 2), torch.full((2, 2), 7.0))
print(torch.arange(6), torch.linspace(0, 1, 5))
print(torch.eye(3))
torch.manual_seed(0)
print(torch.rand(2, 2), torch.randn(2, 2), torch.randint(0, 10, (5,)))

# %% Attributes
x = torch.randn(3, 4)
print(x.shape, x.ndim, x.numel(), x.dtype, x.device)

# %% Math works like NumPy
print(a + 10, a * a, a ** 2, torch.sqrt(a), torch.exp(a))
print(a.sum(), a.mean(), a.max(), a.argmax(), a.std())
print(x.sum(dim=0).shape, x.mean(dim=1).shape)           # dim is the same as axis

# %% Indexing and reshaping
print(x[0], x[:, 1], x[x > 0].shape)
print(x.reshape(2, 6).shape, x.view(-1).shape, x.T.shape, x.unsqueeze(0).shape)
print(torch.cat([x, x]).shape, torch.stack([x, x]).shape)

# %% Matrix multiplication (the heart of neural networks)
w = torch.randn(4, 2)
print((x @ w).shape)
print(torch.matmul(x, w).shape)

# %% NumPy <-> torch (they can share memory)
array = np.array([1.0, 2.0, 3.0])
t = torch.from_numpy(array)
print(t, t.numpy())

# %% Types and devices
print(a.to(torch.float16).dtype, a.long().dtype)
print("cuda available:", torch.cuda.is_available(), "| mps (Apple GPU):", torch.backends.mps.is_available())
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print("using", device)
on_device = x.to(device)
print(on_device.device)

# %% In-place operations end with an underscore
c = torch.ones(3)
c.add_(5)
print(c)

# %% Broadcasting works just like NumPy
print(torch.ones(3, 1) + torch.arange(4))
