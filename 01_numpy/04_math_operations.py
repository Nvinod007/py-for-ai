# Math works on the whole array at once (no for loops). These are "ufuncs".

import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# %% Operators
print(a + b, a - b, a * b, b / a)
print(b // 3, b % 3, a ** 2)        # floor divide, remainder, power
print(a + 100, a * 2)               # a single number is applied to every item
print(-a, np.negative(a))

# %% The same as functions
print(np.add(a, b), np.subtract(b, a), np.multiply(a, b), np.divide(b, a))
print(np.floor_divide(b, 3), np.mod(b, 3), np.power(a, 3))
print(np.reciprocal(np.array([1.0, 2.0, 4.0])))

# %% Powers, roots, logs
x = np.array([1, 4, 9, 16])
print(np.sqrt(x), np.cbrt(x), np.square(x))
print(np.exp(np.array([0, 1, 2])), np.expm1(np.array([0.0, 1e-5])))
print(np.log(x), np.log2(x), np.log10(x), np.log1p(x))

# %% Rounding
f = np.array([-2.7, -1.5, -0.2, 0.5, 1.5, 2.7])
print(np.round(f), np.around(f, 1))   # note: 0.5 -> 0, 1.5 -> 2 (to even)
print(np.floor(f), np.ceil(f), np.trunc(f), np.rint(f))
print(np.fix(f))

# %% Sign, absolute, clip
print(np.abs(f), np.sign(f))
print(np.clip(f, -1, 1))              # keep inside [-1, 1]
print(np.maximum(f, 0))               # element-wise max with 0
print(np.minimum(f, 0))

# %% Trigonometry
angles = np.array([0, np.pi / 6, np.pi / 4, np.pi / 2])
print(np.sin(angles), np.cos(angles), np.tan(angles))
print(np.degrees(angles), np.radians(np.array([0, 90, 180])))
print(np.arcsin(0.5), np.arccos(0.5), np.arctan(1.0), np.hypot(3, 4))

# %% Running totals and differences
print(np.cumsum(a), np.cumprod(a))
print(np.diff(b), np.diff(b, n=2))
print(np.gradient(np.array([1.0, 4.0, 9.0, 16.0])))

# %% Comparisons (give True/False arrays)
print(a > 2, a == 3, a != 3)
print(np.equal(a, b), np.greater(b, a), np.less_equal(a, 2))
print(np.logical_and(a > 1, a < 4))
print(np.logical_or(a < 2, a > 3))
print(np.logical_not(a > 2))
print(np.logical_xor(a > 1, a > 3))

# %% Comparing whole arrays
print(np.array_equal(a, np.array([1, 2, 3, 4])))
print(np.isclose(0.1 + 0.2, 0.3))     # floats are never exact, use isclose
print(np.allclose([1.0, 2.0], [1.0000001, 2.0]))
print(0.1 + 0.2 == 0.3)               # False, famous float issue

# %% Products
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
print(np.dot(v1, v2))                 # 1*4 + 2*5 + 3*6
print(v1 @ v2)                        # same, operator form
print(np.outer(v1, v2))
print(np.cross(v1, v2))
print(np.inner(v1, v2))
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])
print(m1 * m2)                        # element-wise
print(m1 @ m2)                        # matrix product
print(np.matmul(m1, m2))

# %% gcd, lcm, modf, divmod
print(np.gcd(12, 18), np.lcm(4, 6))
print(np.modf(np.array([1.5, -2.25])))
print(np.divmod(np.array([7, 9]), 4))

# %% In-place operators
c = np.array([1.0, 2.0, 3.0])
c += 1
c *= 2
print(c)

# %% Custom function over arrays
def square_plus_one(n):
    return n * n + 1


vectorized = np.vectorize(square_plus_one)
print(vectorized(a))
