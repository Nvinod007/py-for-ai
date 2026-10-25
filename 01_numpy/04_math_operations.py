# Math works on the whole array at once (no for loops). These are "ufuncs".
# Each line has a short comment saying WHAT it is.

import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Operators (applied item by item)
print(a + b, a - b, a * b, b / a)   # add, subtract, multiply, divide
print(b // 3, b % 3, a ** 2)        # // whole-number divide, % remainder, ** power
print(a + 100, a * 2)               # a single number is applied to every item
print(-a, np.negative(a))           # np.negative: flips the sign

# %% Powers, roots, logs
x = np.array([1, 4, 9, 16])
# np.sqrt: square root. np.cbrt: cube root. np.square: x * x.
print(np.sqrt(x), np.cbrt(x), np.square(x))
# np.exp(x): e to the power x. np.expm1(x): exp(x) - 1, accurate for tiny x.
print(np.exp(np.array([0, 1, 2])), np.expm1(np.array([0.0, 1e-5])))
# np.log: natural log (base e). log2: base 2. log10: base 10. log1p: log(1 + x).
print(np.log(x), np.log2(x), np.log10(x), np.log1p(x))

# %% Rounding
f = np.array([-2.7, -1.5, -0.2, 0.5, 1.5, 2.7])
# np.round / np.around: round to given decimals (halves go to the even number).
print(np.round(f), np.around(f, 1))
# np.floor: round down. np.ceil: round up. np.trunc: cut decimals off.
# np.rint: round to nearest whole number.
print(np.floor(f), np.ceil(f), np.trunc(f), np.rint(f))

# %% Sign, absolute, clip
# np.abs: remove the minus sign. np.sign: -1, 0 or 1 depending on the sign.
print(np.abs(f), np.sign(f))
# np.clip(x, lo, hi): force values to stay between lo and hi.
print(np.clip(f, -1, 1))
# np.maximum(x, y): bigger of each pair.
print(np.maximum(f, 0))
# np.minimum(x, y): smaller of each pair.
print(np.minimum(f, 0))

# %% Running totals and differences
# np.cumsum: running total. np.cumprod: running product.
print(np.cumsum(a), np.cumprod(a))
# np.diff: difference between neighbours. n=2 does it twice.
print(np.diff(b), np.diff(b, n=2))

# %% Comparisons (give True/False arrays)
print(a > 2, a == 3, a != 3)
# np.logical_and / or / not / xor: combine True/False arrays.
print(np.logical_and(a > 1, a < 4))      # both true
print(np.logical_or(a < 2, a > 3))       # at least one true
print(np.logical_not(a > 2))             # flip
print(np.logical_xor(a > 1, a > 3))      # exactly one true

# %% Comparing whole arrays
# np.array_equal(x, y): True if same shape and every item is equal.
print(np.array_equal(a, np.array([1, 2, 3, 4])))
# np.isclose(x, y): True if nearly equal (safe for decimals).
print(np.isclose(0.1 + 0.2, 0.3))
# np.allclose(x, y): True if ALL items are nearly equal.
print(np.allclose([1.0, 2.0], [1.0000001, 2.0]))
print(0.1 + 0.2 == 0.3)               # False: decimals are stored slightly off

# %% Products
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
# np.dot(x, y): multiply matching items and add them up (1*4 + 2*5 + 3*6).
print(np.dot(v1, v2))
print(v1 @ v2)                        # @ is the shortcut for dot / matrix multiply
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])
print(m1 * m2)                        # * multiplies matching cells only
print(m1 @ m2)                        # real matrix multiplication

# %% In-place operators
c = np.array([1.0, 2.0, 3.0])
c += 1                                # += changes c itself instead of making a new one
c *= 2
print(c)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% The same as functions
# Every operator has a function version with the same result.
print(np.add(a, b), np.subtract(b, a), np.multiply(a, b), np.divide(b, a))
print(np.floor_divide(b, 3), np.mod(b, 3), np.power(a, 3))
# np.reciprocal(x): 1 / x.
print(np.reciprocal(np.array([1.0, 2.0, 4.0])))

# %% Rounding extras
# np.fix: round toward zero (same as trunc).
print(np.fix(f))

# %% Trigonometry (angles are in radians)
angles = np.array([0, np.pi / 6, np.pi / 4, np.pi / 2])   # np.pi = 3.14159...
# np.sin / cos / tan: the usual trig functions.
print(np.sin(angles), np.cos(angles), np.tan(angles))
# np.degrees: radians to degrees. np.radians: degrees to radians.
print(np.degrees(angles), np.radians(np.array([0, 90, 180])))
# np.arcsin / arccos / arctan: reverse trig (value back to angle).
# np.hypot(x, y): length of the diagonal of a right triangle, sqrt(x² + y²).
print(np.arcsin(0.5), np.arccos(0.5), np.arctan(1.0), np.hypot(3, 4))

# %% Slope
# np.gradient: slope (rate of change) at each point.
print(np.gradient(np.array([1.0, 4.0, 9.0, 16.0])))

# %% Function-form comparisons
# Function forms: equal, greater, less_equal ...
print(np.equal(a, b), np.greater(b, a), np.less_equal(a, 2))

# %% More vector products
# np.outer(x, y): table of every x item times every y item.
print(np.outer(v1, v2))
# np.cross(x, y): 3D vector that is perpendicular to both.
print(np.cross(v1, v2))
# np.inner(x, y): same as dot for 1D arrays.
print(np.inner(v1, v2))

# %% matmul function
# np.matmul: function form of @.
print(np.matmul(m1, m2))

# %% gcd, lcm, modf, divmod
# np.gcd: biggest number dividing both. np.lcm: smallest number both divide into.
print(np.gcd(12, 18), np.lcm(4, 6))
# np.modf(x): splits into (decimal part, whole part).
print(np.modf(np.array([1.5, -2.25])))
# np.divmod(x, y): (whole-number quotient, remainder) in one go.
print(np.divmod(np.array([7, 9]), 4))

# %% Custom function over arrays
def square_plus_one(n):
    return n * n + 1


# np.vectorize(f): wraps a normal function so it works on whole arrays.
vectorized = np.vectorize(square_plus_one)
print(vectorized(a))
