# Short ways to build collections, and lazy sequences that save memory.

import itertools

# %% List comprehension
squares = [n * n for n in range(6)]
evens = [n for n in range(10) if n % 2 == 0]
labels = ["big" if n > 2 else "small" for n in range(5)]
print(squares, evens, labels)
pairs = [(x, y) for x in range(3) for y in range(2)]
print(pairs)
matrix = [[r * c for c in range(1, 4)] for r in range(1, 4)]
print(matrix)
flat = [value for row in matrix for value in row]
print(flat)

# %% Dict, set comprehension
words = ["apple", "banana", "cherry"]
print({w: len(w) for w in words})
print({w[0] for w in words})
print({v: k for k, v in {"a": 1, "b": 2}.items()})     # swap keys and values
print({k: v for k, v in {"a": 1, "b": 5}.items() if v > 2})

# %% Generator expression: like a list, but made one item at a time
total = sum(n * n for n in range(1_000_000))
print(total)
gen = (n * n for n in range(3))
print(next(gen), next(gen), next(gen))
print(list(gen))                         # already used up -> []

# %% Generator function with yield
def countdown(n):
    while n > 0:
        yield n
        n -= 1


print(list(countdown(4)))
for number in countdown(2):
    print(number)


def read_in_chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


print(list(read_in_chunks(list(range(7)), 3)))

# %% Infinite generator, take what you need
def counter():
    n = 0
    while True:
        yield n
        n += 1


from_gen = counter()
print([next(from_gen) for _ in range(5)])

# %% Useful built-ins
names = ["Asha", "Ben", "Chen"]
ages = [25, 32, 47]
print(list(zip(names, ages)))
print(dict(zip(names, ages)))
for index, name in enumerate(names, start=1):
    print(index, name)
print(list(map(str.upper, names)))
print(list(filter(lambda a: a > 30, ages)))
print(sorted(names, key=len, reverse=True))
print(any(a > 40 for a in ages), all(a > 20 for a in ages))
print(max(names, key=len), min(ages), sum(ages))
print(list(reversed(names)))

# %% itertools
print(list(itertools.chain([1, 2], [3])))
print(list(itertools.islice(counter(), 3)))
print(list(itertools.combinations("abc", 2)))
print(list(itertools.permutations("ab")))
print(list(itertools.product("ab", [1, 2])))
print([(k, list(g)) for k, g in itertools.groupby("aabbbc")])
print(list(itertools.accumulate([1, 2, 3, 4])))
