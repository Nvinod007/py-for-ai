# Short ways to build collections, and lazy sequences that save memory.
# Each line has a short comment saying WHAT it is.

import itertools  # import: loads a library; itertools has tools for looping

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% List comprehension
squares = [n * n for n in range(6)]  # [expr for n in ...]: list comprehension = build a list in one line; range(6) = 0..5
evens = [n for n in range(10) if n % 2 == 0]  # "if" at the end keeps only matching items; % = remainder after division
labels = ["big" if n > 2 else "small" for n in range(5)]  # "A if test else B": picks A or B for each item
print(squares, evens, labels)  # print: shows values
pairs = [(x, y) for x in range(3) for y in range(2)]  # two "for"s = loop inside a loop; (x, y) = a tuple (fixed pair)
print(pairs)
matrix = [[r * c for c in range(1, 4)] for r in range(1, 4)]  # a list of lists (rows); range(1, 4) = 1..3
print(matrix)
flat = [value for row in matrix for value in row]  # flattens rows into one list
print(flat)

# %% Dict, set comprehension
words = ["apple", "banana", "cherry"]
print({w: len(w) for w in words})  # {k: v for ...}: dict comprehension; len(x): how many items/characters
print({w[0] for w in words})  # {x for ...}: set comprehension (unique values); w[0] = first letter
print({v: k for k, v in {"a": 1, "b": 2}.items()})     # .items(): gives (key, value) pairs; here swap keys and values
print({k: v for k, v in {"a": 1, "b": 5}.items() if v > 2})  # keep only pairs where value > 2

# %% Generator expression: like a list, but made one item at a time
total = sum(n * n for n in range(1_000_000))  # (expr for ...) with () = generator, makes items one by one; sum(): adds them; 1_000_000 = one million
print(total)
gen = (n * n for n in range(3))  # generator expression stored in a variable
print(next(gen), next(gen), next(gen))  # next(g): gets the next item from a generator
print(list(gen))                         # list(x): turns items into a list; already used up -> []

# %% Generator function with yield
def countdown(n):  # def: makes a function
    while n > 0:  # while: repeats as long as the test is True
        yield n  # yield: hands out one value and pauses here (makes this a generator)
        n -= 1  # -= : subtract 1


print(list(countdown(4)))
for number in countdown(2):  # for: takes items from the generator one at a time
    print(number)


def read_in_chunks(items, size):
    for i in range(0, len(items), size):  # range(start, stop, step): counts in jumps of size
        yield items[i : i + size]  # items[a:b]: slice = part of the list from a up to (not including) b


print(list(read_in_chunks(list(range(7)), 3)))

# %% Useful built-ins
names = ["Asha", "Ben", "Chen"]
ages = [25, 32, 47]
print(list(zip(names, ages)))  # zip(a, b): pairs items from two lists
print(dict(zip(names, ages)))  # dict(pairs): builds a dict from pairs
for index, name in enumerate(names, start=1):  # enumerate(list, start=1): gives (counter, item); start sets first number
    print(index, name)
print(list(map(str.upper, names)))  # map(func, list): applies func to each item; str.upper: makes text capital
print(list(filter(lambda a: a > 30, ages)))  # filter(func, list): keeps items where func is True; lambda: tiny one-line function
print(sorted(names, key=len, reverse=True))  # sorted(list): new sorted list; key=len sorts by length; reverse=True = biggest first
print(any(a > 40 for a in ages), all(a > 20 for a in ages))  # any(): True if at least one is True; all(): True only if every one is True
print(max(names, key=len), min(ages), sum(ages))  # max/min: biggest/smallest; sum: total
print(list(reversed(names)))  # reversed(list): items in backwards order

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Infinite generator, take what you need
def counter():
    n = 0
    while True:  # while True: loops forever (generator pauses at each yield)
        yield n
        n += 1  # += : add 1


from_gen = counter()
print([next(from_gen) for _ in range(5)])  # _ = a throwaway name when you don't need the value

# %% itertools
print(list(itertools.chain([1, 2], [3])))  # chain(a, b): joins lists one after another
print(list(itertools.islice(counter(), 3)))  # islice(gen, 3): takes only the first 3 items
print(list(itertools.combinations("abc", 2)))  # combinations(x, 2): all pairs, order doesn't matter
print(list(itertools.permutations("ab")))  # permutations(x): all orderings
print(list(itertools.product("ab", [1, 2])))  # product(a, b): every pairing of a with b
print([(k, list(g)) for k, g in itertools.groupby("aabbbc")])  # groupby(x): groups neighbouring equal items
print(list(itertools.accumulate([1, 2, 3, 4])))  # accumulate(x): running total
