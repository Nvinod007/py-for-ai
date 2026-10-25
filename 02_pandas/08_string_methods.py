# The .str accessor: text tools that work on a whole column.

import pandas as pd

names = pd.Series(["  Alice Johnson ", "bob SMITH", "Carol-Ann White", None, "dave brown"])

# %% Case and spaces
print(names.str.lower())
print(names.str.upper())
print(names.str.title())
print(names.str.capitalize())
print(names.str.swapcase())
print(names.str.strip())
print(names.str.lstrip(), names.str.rstrip())
print(names.str.strip().str.strip("-"))

# %% Length and counting
print(names.str.len())
print(names.str.count("a"))
print(names.str.count(r"[aeiou]"))

# %% Searching
print(names.str.contains("bob", case=False))
print(names.str.contains("Alice|Carol", na=False))
print(names.str.startswith("  A"))
print(names.str.endswith("n"))
print(names.str.find("o"))
print(names.str.match(r"\s*[A-Z]"))              # regex at the start

# %% Replacing
print(names.str.replace("-", " ", regex=False))
print(names.str.replace(r"\s+", " ", regex=True))   # many spaces -> one
print(names.str.strip().str.replace(" ", "_"))
print(names.str.removeprefix("  "))
print(names.str.removesuffix(" "))

# %% Splitting and joining
clean = names.dropna().str.strip()
print(clean.str.split(" "))
print(clean.str.split(" ", expand=True))               # into columns
print(clean.str.split(" ").str[0])                     # first word
print(clean.str.split(" ").str[-1])                    # last word
print(clean.str.split(" ").str.join("_"))
print(clean.str.rsplit(" ", n=1, expand=True))
print(clean.str.partition(" "))
print(clean.str.cat(sep=" | "))
print(clean.str.cat(clean.str.upper(), sep=" / "))

# %% Slicing and padding
print(clean.str[0:3])
print(clean.str.slice(0, 3))
print(clean.str.slice_replace(0, 1, "*"))
print(pd.Series(["7", "42"]).str.zfill(4))
print(pd.Series(["a", "bb"]).str.pad(4, side="left", fillchar="."))
print(pd.Series(["a", "bb"]).str.center(5, "*"))
print(clean.str.ljust(20, "."))
print(pd.Series(["ab", "c"]).str.repeat(2))

# %% Regex extraction
emails = pd.Series(["alice@mail.com", "bob@work.org", "bad-email", "carol@school.edu"])
print(emails.str.extract(r"(\w+)@(\w+)\.(\w+)"))
print(emails.str.extract(r"@(?P<domain>[\w.]+)"))
print(emails.str.contains("@"))
print(emails.str.findall(r"[a-z]+"))
print(emails.str.extractall(r"(\w)@"))
print(emails[emails.str.fullmatch(r"\w+@\w+\.\w+")])

# %% Character tests
mixed = pd.Series(["123", "abc", "a1", "  ", "ABC"])
print(mixed.str.isdigit(), mixed.str.isalpha(), mixed.str.isalnum())
print(mixed.str.isspace(), mixed.str.isupper(), mixed.str.islower())
print(mixed.str.isnumeric(), mixed.str.istitle())

# %% Dummies from tags
tags = pd.Series(["a|b", "b|c", "a"])
print(tags.str.get_dummies(sep="|"))

# %% Other helpers
print(pd.Series(["Straße"]).str.casefold())
print(pd.Series(["café"]).str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("ascii"))
print(pd.Series(["a b c d"]).str.wrap(3))
print(pd.Series(["abc"]).str.translate(str.maketrans("abc", "xyz")))
print(pd.Series(["ab", "cd"]).str.get(0))
print(pd.Series(["x"]).str.len().dtype)

# %% Real use: clean city names
cities = pd.Series(["new york", "NEW YORK ", "New  York", "NYC"])
cleaned = cities.str.strip().str.replace(r"\s+", " ", regex=True).str.title()
cleaned = cleaned.replace({"Nyc": "New York"})
print(cleaned.value_counts())
