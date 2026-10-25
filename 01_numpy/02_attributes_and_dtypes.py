# Every array carries facts about itself: shape, type, size in memory.
# Each line has a short comment saying WHAT it is.

import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Attributes (facts stored on the array, no brackets needed)
print("shape   :", arr.shape)      # size of each dimension: (rows, columns)
print("ndim    :", arr.ndim)       # how many dimensions (1D, 2D, 3D ...)
print("size    :", arr.size)       # total number of elements
print("dtype   :", arr.dtype)      # data type of the elements
print("itemsize:", arr.itemsize)   # memory used by ONE element, in bytes
print("nbytes  :", arr.nbytes)     # memory used by the WHOLE array, in bytes
print("len     :", len(arr))       # number of rows (length of the first axis)
print("T       :\n", arr.T)        # transpose: rows become columns

# %% Data types
# int64 = whole numbers, float64 = decimals, bool = True/False, <U2 = text.
print(np.array([1, 2, 3]).dtype)      # int64
print(np.array([1.0, 2, 3]).dtype)    # float64 (one decimal makes all decimals)
print(np.array([True, False]).dtype)  # bool
print(np.array(["a", "bc"]).dtype)    # <U2: text up to 2 characters
print(np.array([1, "a"]).dtype)       # mixing numbers and text turns all into text

# %% Converting types with astype (returns a new array)
f = np.array([1.7, 2.2, -3.9])
# .astype(type): makes a copy converted to another type.
print(f.astype(int))                  # drops decimals (1.7 -> 1, -3.9 -> -3)
# np.round(x): rounds to the nearest whole number.
print(np.round(f).astype(int))        # round first, then convert
print(np.array([1, 0, 5]).astype(bool))   # 0 -> False, others -> True
print(np.array(["1", "2"]).astype(int))   # text "1" -> number 1

# %% Reshape: same data, new shape
flat = np.arange(12)                  # arange: numbers 0..11
# .reshape(rows, cols): rearranges the same numbers into a new shape.
print(flat.reshape(3, 4))
print(flat.reshape(2, -1))            # -1 = "work this size out for me"
print(flat.reshape(2, 3, 2))

# %% Flatten
two_d = np.array([[1, 2], [3, 4]])
# .flatten(): squashes any array into 1D, always a separate copy.
print(two_d.flatten())
# .ravel(): also makes it 1D, but reuses the same data when it can (faster).
print(two_d.ravel())

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Integer sizes and overflow
small = np.array([120], dtype=np.int8)   # int8 can only hold -128..127
print(small + np.int8(10))               # 130 doesn't fit, wraps to -126 (overflow)
# np.iinfo(type): shows min/max of an integer type.
print(np.iinfo(np.int8))
# np.finfo(type): shows precision and limits of a float type.
print(np.finfo(np.float32))

# %% Change shape in place
z = np.arange(6)
z.shape = (2, 3)                      # setting .shape reshapes the array itself
print(z)
# .resize(r, c): changes the array itself to a new size.
z.resize(3, 2)
print(z)
# np.resize(arr, shape): returns a new array, repeating values to fill the space.
print(np.resize(np.arange(3), (2, 4)))

# %% Check types
# np.issubdtype(a, b): True if type a belongs to family b (integer, floating...).
print(np.issubdtype(arr.dtype, np.integer))
print(np.issubdtype(f.dtype, np.floating))
# np.result_type(a, b): the type you get when mixing a and b.
print(np.result_type(np.int32, np.float64))
# dtype.name / dtype.kind: type's readable name / one-letter code (i=int, f=float).
print(arr.dtype.name, arr.dtype.kind)
