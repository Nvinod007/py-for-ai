# Random numbers: simulations, shuffling, sampling, fake data.
# Use a Generator (default_rng). Same seed -> same numbers every time.
# Each line has a short comment saying WHAT it is.

import numpy as np

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# np.random.default_rng(seed): creates a random number generator.
# seed = a starting number; the same seed always gives the same "random" numbers.
rng = np.random.default_rng(seed=42)

# %% Basics
print(rng.random())                    # random decimal from 0 up to (not incl.) 1
print(rng.random(3))                   # 3 of them
print(rng.random((2, 2)))              # a 2x2 grid of them
print(rng.integers(0, 10, size=5))     # random whole numbers 0..9
# endpoint=True: include the top number, so this acts like a die (1..6).
print(rng.integers(1, 7, size=(2, 3), endpoint=True))
print(rng.uniform(5, 10, size=3))      # random decimals between 5 and 10

# %% Bell curve and choice
# normal(loc, scale): bell curve around the mean (loc) with spread (scale).
print(rng.normal(loc=50, scale=10, size=5))
# standard_normal: bell curve with mean 0 and spread 1.
print(rng.standard_normal(3))
# choice(options, p=...): pick with chosen odds (80% zeros, 20% ones).
print(rng.choice([0, 1], size=5, p=[0.8, 0.2]))

# %% Picking from data
items = np.array(["red", "green", "blue", "pink"])
print(rng.choice(items))                          # pick one at random
print(rng.choice(items, size=2, replace=False))   # replace=False: no repeats
print(rng.choice(items, size=6, replace=True))    # repeats allowed

# %% Shuffling
nums = np.arange(10)
# rng.shuffle(arr): mixes the array itself (no return value).
rng.shuffle(nums)
print(nums)
# rng.permutation(x): returns a new shuffled copy.
print(rng.permutation(10))                        # shuffled 0..9
print(rng.permutation(np.array([[1, 2], [3, 4], [5, 6]])))   # rows shuffled

# %% Reproducibility check
print(np.random.default_rng(1).random(3))
print(np.random.default_rng(1).random(3))   # exactly the same as above

# %% Fake dataset for practice
heights = rng.normal(170, 8, size=1000)     # 1000 fake heights around 170 cm
print(heights.mean(), heights.std())
print(np.percentile(heights, [5, 50, 95]))  # percentile: value below which p% fall

# %% Simulations: roll two dice 10000 times
rolls = rng.integers(1, 7, size=(10000, 2)).sum(axis=1)   # sum of the two dice
values, counts = np.unique(rolls, return_counts=True)     # how often each total
for value, count in zip(values, counts):                  # zip: pair them up
    print(value, count)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Other distributions
# binomial(n, p): number of successes in n tries (heads in 10 coin flips).
print(rng.binomial(n=10, p=0.5, size=5))
# poisson(lam): counts of events in a time period (average = lam).
print(rng.poisson(lam=3, size=5))
# exponential(scale): waiting time between events.
print(rng.exponential(scale=2, size=3))

# %% Old style (you will see it in tutorials)
np.random.seed(0)                     # old way to fix the seed globally
print(np.random.rand(2))              # old: random decimals 0..1
print(np.random.randn(2))             # old: bell curve numbers
print(np.random.randint(0, 5, 3))     # old: random whole numbers
