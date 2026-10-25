# Every array carries facts about itself: shape, type, size in memory.

import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# %% Attributes
print("shape   :", arr.shape)      # (rows, columns)
print("ndim    :", arr.ndim)       # number of dimensions
print("size    :", arr.size)       # total elements
print("dtype   :", arr.dtype)      # element type
print("itemsize:", arr.itemsize)   # bytes per element
print("nbytes  :", arr.nbytes)     # total bytes
print("len     :", len(arr))       # length of first axis
print("T       :\n", arr.T)        # transpose

# %% Data types
print(np.array([1, 2, 3]).dtype)      # int64
print(np.array([1.0, 2, 3]).dtype)    # float64
print(np.array([True, False]).dtype)  # bool
print(np.array(["a", "bc"]).dtype)    # <U2  (unicode text)
print(np.array([1, "a"]).dtype)       # mixed becomes text

# %% Converting types with astype (returns a new array)
f = np.array([1.7, 2.2, -3.9])
print(f.astype(int))                  # cuts decimals toward zero
print(np.round(f).astype(int))        # round first, then convert
print(np.array([1, 0, 5]).astype(bool))
print(np.array(["1", "2"]).astype(int))

# %% Integer sizes and overflow
small = np.array([120], dtype=np.int8)   # int8 holds -128..127
print(small + np.int8(10))               # wraps around (overflow), watch out
print(np.iinfo(np.int8))
print(np.finfo(np.float32))

# %% Reshape: same data, new shape
flat = np.arange(12)
print(flat.reshape(3, 4))
print(flat.reshape(2, -1))            # -1 means "figure it out"
print(flat.reshape(2, 3, 2).shape)

# %% Flatten
two_d = np.array([[1, 2], [3, 4]])
print(two_d.flatten())   # always a copy
print(two_d.ravel())     # a view when possible (faster)

# %% Change shape in place
z = np.arange(6)
z.shape = (2, 3)
print(z)
z.resize(3, 2)
print(z)
print(np.resize(np.arange(3), (2, 4)))   # repeats values to fill

# %% Check types
print(np.issubdtype(arr.dtype, np.integer))
print(np.issubdtype(f.dtype, np.floating))
print(np.result_type(np.int32, np.float64))
print(arr.dtype.name, arr.dtype.kind)
