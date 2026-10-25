# Getting data in and out: CSV, Excel, JSON, and more.

from io import StringIO
from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
OUT = DATA / "output"
OUT.mkdir(exist_ok=True)

# %% Read a CSV
df = pd.read_csv(DATA / "03_employees.csv")
print(df.head())

# %% Useful read_csv options
print(pd.read_csv(DATA / "03_employees.csv", nrows=3))                      # only 3 rows
print(pd.read_csv(DATA / "03_employees.csv", usecols=["name", "salary"]).head(3))
print(pd.read_csv(DATA / "03_employees.csv", index_col="employee_id").head(3))
print(pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"]).dtypes)
print(pd.read_csv(DATA / "03_employees.csv", dtype={"age": "float64"}).dtypes["age"])
print(pd.read_csv(DATA / "03_employees.csv", skiprows=[1, 2]).head(2))
print(pd.read_csv(DATA / "03_employees.csv", header=0, names=list("ABCDEFGHI")).head(2))

# %% Missing value markers
text = "a,b\n1,NA\n2,-\n3,5\n"
print(pd.read_csv(StringIO(text)))
print(pd.read_csv(StringIO(text), na_values=["-"]))
print(pd.read_csv(StringIO(text), keep_default_na=False))

# %% Other separators and no header
tsv = "x\ty\n1\t2\n"
print(pd.read_csv(StringIO(tsv), sep="\t"))
print(pd.read_csv(StringIO("1,2\n3,4"), header=None))
print(pd.read_table(StringIO("a|b\n1|2"), sep="|"))

# %% Big files in chunks
total = 0
for chunk in pd.read_csv(DATA / "03_employees.csv", chunksize=10):
    total += chunk["salary"].sum()
print(total)

# %% Write CSV
df.head(5).to_csv(OUT / "employees_small.csv", index=False)
df.head(5).to_csv(OUT / "employees_small_semicolon.csv", index=False, sep=";")
df.head(5).to_csv(OUT / "employees_cols.csv", index=False, columns=["name", "salary"])
print(pd.read_csv(OUT / "employees_small.csv"))

# %% JSON
df.head(3).to_json(OUT / "employees.json", orient="records", indent=2)
print(pd.read_json(OUT / "employees.json"))
print(df.head(2).to_json(orient="split"))
print(df.head(2).to_json(orient="index"))

# %% Excel (needs openpyxl)
df.head(5).to_excel(OUT / "employees.xlsx", index=False, sheet_name="staff")
print(pd.read_excel(OUT / "employees.xlsx", sheet_name="staff"))
with pd.ExcelWriter(OUT / "multi.xlsx") as writer:
    df.head(3).to_excel(writer, sheet_name="first3", index=False)
    df.tail(3).to_excel(writer, sheet_name="last3", index=False)
print(pd.ExcelFile(OUT / "multi.xlsx").sheet_names)

# %% Other formats (just so you know they exist)
print(df.head(2).to_html(index=False)[:80])
print(df.head(2).to_markdown())              # needs the tabulate package
print(df.head(2).to_latex()[:60])
df.head(5).to_pickle(OUT / "employees.pkl")
print(pd.read_pickle(OUT / "employees.pkl").shape)
# df.to_parquet("file.parquet")   # needs pyarrow, popular for big data
# pd.read_sql(query, connection)  # databases
# pd.read_clipboard()             # copy a table from a web page, then call this

# %% From text in memory
print(pd.read_csv(StringIO("name,score\nAsha,90\nBen,80")))
