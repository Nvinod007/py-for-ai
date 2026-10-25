# Random numbers: simulations, shuffling, sampling, fake data.
# Use a Generator (default_rng). Same seed -> same numbers every time.

import numpy as np

rng = np.random.default_rng(seed=42)

# %% Basics
print(rng.random())                    # float in [0, 1)
print(rng.random(3))
print(rng.random((2, 2)))
print(rng.integers(0, 10, size=5))     # 0..9
print(rng.integers(1, 7, size=(2, 3), endpoint=True))  # 1..6 like a die
print(rng.uniform(5, 10, size=3))      # float between 5 and 10

# %% Bell curve and other distributions
print(rng.normal(loc=50, scale=10, size=5))     # mean 50, std 10
print(rng.standard_normal(3))
print(rng.binomial(n=10, p=0.5, size=5))        # heads in 10 coin flips
print(rng.poisson(lam=3, size=5))               # events per interval
print(rng.exponential(scale=2, size=3))
print(rng.choice([0, 1], size=5, p=[0.8, 0.2])) # weighted

# %% Picking from data
items = np.array(["red", "green", "blue", "pink"])
print(rng.choice(items))
print(rng.choice(items, size=2, replace=False))   # no repeats
print(rng.choice(items, size=6, replace=True))

# %% Shuffling
nums = np.arange(10)
rng.shuffle(nums)                       # in place
print(nums)
print(rng.permutation(10))              # new shuffled copy
print(rng.permutation(np.array([[1, 2], [3, 4], [5, 6]])))  # rows shuffled

# %% Reproducibility check
print(np.random.default_rng(1).random(3))
print(np.random.default_rng(1).random(3))   # exactly the same

# %% Fake dataset for practice
heights = rng.normal(170, 8, size=1000)
print(heights.mean(), heights.std())
print(np.percentile(heights, [5, 50, 95]))

# %% Simulations: roll two dice 10000 times
rolls = rng.integers(1, 7, size=(10000, 2)).sum(axis=1)
values, counts = np.unique(rolls, return_counts=True)
for value, count in zip(values, counts):
    print(value, count)

# %% Old style (you will see it in tutorials)
np.random.seed(0)
print(np.random.rand(2))
print(np.random.randn(2))
print(np.random.randint(0, 5, 3))
