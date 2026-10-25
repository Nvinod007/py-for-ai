# The .str accessor: text tools that work on a whole column.
# Each line has a short comment saying WHAT the function is.

import pandas as pd

# pd.Series(list): one column of values; None = a missing item.
names = pd.Series(["  Alice Johnson ", "bob SMITH", "Carol-Ann White", None, "dave brown"])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Case and spaces
print(names.str.lower())          # .str.lower(): all small letters
print(names.str.upper())          # .str.upper(): ALL CAPITALS
print(names.str.title())          # .str.title(): Capital First Letter Of Each Word

# %% Length and counting
print(names.str.len())                  # .str.len(): number of characters

# %% Searching
print(names.str.contains("bob", case=False))          # .str.contains(x): True if x is inside; case=False: ignore capitals
print(names.str.contains("Alice|Carol", na=False))    # "|" means or; na=False: missing counts as False
print(names.str.startswith("  A"))                    # .str.startswith(x): True if text begins with x
print(names.str.endswith("n"))                        # .str.endswith(x): True if text ends with x

# %% Replacing
print(names.str.replace("-", " ", regex=False))     # .str.replace(a, b): swaps a for b; regex=False: plain text
print(names.str.replace(r"\s+", " ", regex=True))   # regex=True: a is a pattern; \s+ = one or more spaces -> one
print(names.str.strip().str.replace(" ", "_"))

# %% Splitting and joining
clean = names.dropna().str.strip()                  # .dropna(): removes missing items
print(clean.str.split(" "))                            # .str.split(x): cuts text into a list at each x
print(clean.str.split(" ", expand=True))               # expand=True: into columns
print(clean.str.split(" ").str[0])                     # .str[0]: first item of each list = first word
print(clean.str.split(" ").str[-1])                    # last word
print(clean.str.split(" ").str.join("_"))              # .str.join(x): glues list items together with x

# %% Slicing and padding
print(clean.str[0:3])                         # .str[a:b]: characters from a up to (not incl.) b

# %% Regex extraction
emails = pd.Series(["alice@mail.com", "bob@work.org", "bad-email", "carol@school.edu"])
print(emails.str.extract(r"(\w+)@(\w+)\.(\w+)"))     # .str.extract(pattern): each (...) group becomes a column; \w+ = letters/digits
print(emails.str.extract(r"@(?P<domain>[\w.]+)"))    # ?P<name>: names the column
print(emails.str.contains("@"))                      # True if "@" is inside

# %% Real use: clean city names
cities = pd.Series(["new york", "NEW YORK ", "New  York", "NYC"])
cleaned = cities.str.strip().str.replace(r"\s+", " ", regex=True).str.title()
cleaned = cleaned.replace({"Nyc": "New York"})     # .replace({old: new}): swaps whole values
print(cleaned.value_counts())                      # .value_counts(): how many times each value appears

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Rare case and strip helpers
print(names.str.capitalize())     # .str.capitalize(): only the first letter capital
print(names.str.swapcase())       # .str.swapcase(): flips small <-> capital
print(names.str.strip())          # .str.strip(): removes spaces at both ends
print(names.str.lstrip(), names.str.rstrip())      # lstrip: left end only; rstrip: right end only
print(names.str.strip().str.strip("-"))            # strip("-"): removes "-" characters at the ends

# %% Counting characters
print(names.str.count("a"))             # .str.count(x): how many times x appears
print(names.str.count(r"[aeiou]"))      # [aeiou] is a pattern meaning "any vowel"

# %% Searching (less common)
print(names.str.find("o"))                            # .str.find(x): position of first x (-1 if none)
print(names.str.match(r"\s*[A-Z]"))              # .str.match(pattern): regex (text pattern) at the start; \s = space, [A-Z] = capital

# %% Replacing (less common)
print(names.str.removeprefix("  "))                 # .str.removeprefix(x): cuts x off the start
print(names.str.removesuffix(" "))                  # .str.removesuffix(x): cuts x off the end

# %% Splitting and joining (less common)
print(clean.str.rsplit(" ", n=1, expand=True))         # .str.rsplit(x, n=1): split from the right, at most 1 cut
print(clean.str.partition(" "))                        # .str.partition(x): 3 parts: before, x, after
print(clean.str.cat(sep=" | "))                        # .str.cat(sep=): joins all items into one text
print(clean.str.cat(clean.str.upper(), sep=" / "))     # cat(other): joins item-by-item with another column

# %% Slicing and padding (less common)
print(clean.str.slice(0, 3))                  # .str.slice(a, b): same as above
print(clean.str.slice_replace(0, 1, "*"))     # .str.slice_replace(a, b, x): swaps characters a..b for x
print(pd.Series(["7", "42"]).str.zfill(4))    # .str.zfill(4): pads with 0 on the left to length 4
print(pd.Series(["a", "bb"]).str.pad(4, side="left", fillchar="."))   # .str.pad(width): pads to that length; side=: which end; fillchar=: pad character
print(pd.Series(["a", "bb"]).str.center(5, "*"))    # .str.center(width, char): pads both sides
print(clean.str.ljust(20, "."))                     # .str.ljust(width, char): pads on the right
print(pd.Series(["ab", "c"]).str.repeat(2))         # .str.repeat(2): repeats text 2 times

# %% Regex extraction (less common)
print(emails.str.findall(r"[a-z]+"))                 # .str.findall(pattern): list of all matches
print(emails.str.extractall(r"(\w)@"))               # .str.extractall(pattern): every match, one row each
print(emails[emails.str.fullmatch(r"\w+@\w+\.\w+")])   # .str.fullmatch(pattern): True if the whole text fits; keeps those rows

# %% Character tests
mixed = pd.Series(["123", "abc", "a1", "  ", "ABC"])
# .str.isdigit(): only digits; isalpha(): only letters; isalnum(): letters or digits only.
print(mixed.str.isdigit(), mixed.str.isalpha(), mixed.str.isalnum())
# isspace(): only spaces; isupper(): all capitals; islower(): all small letters.
print(mixed.str.isspace(), mixed.str.isupper(), mixed.str.islower())
# isnumeric(): looks like a number; istitle(): Like This Title Case.
print(mixed.str.isnumeric(), mixed.str.istitle())

# %% Dummies from tags
tags = pd.Series(["a|b", "b|c", "a"])
print(tags.str.get_dummies(sep="|"))     # .str.get_dummies(sep=): one 0/1 column per tag

# %% Other helpers
print(pd.Series(["Straße"]).str.casefold())    # .str.casefold(): strong lower-case (ß -> ss)
# .str.normalize("NFKD"): splits accents from letters; .encode("ascii", errors="ignore"): drops non-English characters; .decode(): back to text.
print(pd.Series(["café"]).str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("ascii"))
print(pd.Series(["a b c d"]).str.wrap(3))      # .str.wrap(3): breaks long text into lines of about 3 characters
# str.maketrans("abc", "xyz"): letter swap table (a->x...); .str.translate(table): applies it.
print(pd.Series(["abc"]).str.translate(str.maketrans("abc", "xyz")))
print(pd.Series(["ab", "cd"]).str.get(0))      # .str.get(0): character at position 0
print(pd.Series(["x"]).str.len().dtype)        # .dtype: the data type of the result
