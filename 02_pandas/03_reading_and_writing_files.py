# Getting data in and out: CSV, Excel, JSON, and more.
# Each line has a short comment saying WHAT the function is.

from io import StringIO
from pathlib import Path

import pandas as pd

# Path("data"): a folder path; .exists(): True if it is there. Picks the data folder that exists.
DATA = Path("data") if Path("data").exists() else Path("../data")
OUT = DATA / "output"            # path / "name": adds a sub-folder or file name to a path
OUT.mkdir(exist_ok=True)         # .mkdir(): creates the folder; exist_ok=True: no error if already there

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Read a CSV
# pd.read_csv(path): reads a CSV (comma-separated text table) file into a DataFrame.
df = pd.read_csv(DATA / "03_employees.csv")
print(df.head())                 # .head(): first 5 rows

# %% Useful read_csv options
print(pd.read_csv(DATA / "03_employees.csv", nrows=3))                      # nrows=3: read only 3 rows
# usecols=: read only these columns.
print(pd.read_csv(DATA / "03_employees.csv", usecols=["name", "salary"]).head(3))
# index_col=: use this column as the row labels.
print(pd.read_csv(DATA / "03_employees.csv", index_col="employee_id").head(3))
# parse_dates=: read this column as real dates; .dtypes: type of each column.
print(pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"]).dtypes)
# dtype={col: type}: force a column's data type.
print(pd.read_csv(DATA / "03_employees.csv", dtype={"age": "float64"}).dtypes["age"])

# %% Missing value markers
text = "a,b\n1,NA\n2,-\n3,5\n"        # \n = new line
# StringIO(text): makes text act like a file so read_csv can read it.
print(pd.read_csv(StringIO(text)))
print(pd.read_csv(StringIO(text), na_values=["-"]))            # na_values=: extra texts to treat as missing
print(pd.read_csv(StringIO(text), keep_default_na=False))      # keep_default_na=False: do not treat "NA" as missing

# %% Other separators and no header
tsv = "x\ty\n1\t2\n"                                           # \t = tab
print(pd.read_csv(StringIO(tsv), sep="\t"))                    # sep=: the character that splits columns
print(pd.read_csv(StringIO("1,2\n3,4"), header=None))          # header=None: file has no header line
print(pd.read_table(StringIO("a|b\n1|2"), sep="|"))            # pd.read_table(): like read_csv but tab-separated by default

# %% Write CSV
# df.to_csv(path): saves the table as a CSV file; index=False: do not save the row numbers.
df.head(5).to_csv(OUT / "employees_small.csv", index=False)
df.head(5).to_csv(OUT / "employees_small_semicolon.csv", index=False, sep=";")        # sep=";": separate with ;
df.head(5).to_csv(OUT / "employees_cols.csv", index=False, columns=["name", "salary"])  # columns=: save only these
print(pd.read_csv(OUT / "employees_small.csv"))

# %% JSON
# .to_json(path): saves as JSON (text format used by web apps); orient="records": list of rows; indent=2: neat spacing.
df.head(3).to_json(OUT / "employees.json", orient="records", indent=2)
print(pd.read_json(OUT / "employees.json"))      # pd.read_json(): reads a JSON file

# %% Excel (needs openpyxl)
# .to_excel(path): saves as an Excel file; sheet_name=: the tab name.
df.head(5).to_excel(OUT / "employees.xlsx", index=False, sheet_name="staff")
print(pd.read_excel(OUT / "employees.xlsx", sheet_name="staff"))     # pd.read_excel(): reads an Excel sheet

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Rare read_csv options
# skiprows=[1, 2]: skip those lines of the file.
print(pd.read_csv(DATA / "03_employees.csv", skiprows=[1, 2]).head(2))
# header=0: line 0 is the header; names=: use these column names; list("ABC"): splits text into letters.
print(pd.read_csv(DATA / "03_employees.csv", header=0, names=list("ABCDEFGHI")).head(2))

# %% Big files in chunks
total = 0
# chunksize=10: reads 10 rows at a time instead of everything.
for chunk in pd.read_csv(DATA / "03_employees.csv", chunksize=10):
    total += chunk["salary"].sum()          # chunk["col"]: one column; .sum(): adds it up
print(total)

# %% JSON orient variants
print(df.head(2).to_json(orient="split"))        # without a path, returns the JSON text; "split": columns, index, data apart
print(df.head(2).to_json(orient="index"))        # "index": one entry per row label

# %% Excel: several sheets
with pd.ExcelWriter(OUT / "multi.xlsx") as writer:    # pd.ExcelWriter: lets you write several sheets into one file
    df.head(3).to_excel(writer, sheet_name="first3", index=False)
    df.tail(3).to_excel(writer, sheet_name="last3", index=False)     # .tail(3): last 3 rows
print(pd.ExcelFile(OUT / "multi.xlsx").sheet_names)   # pd.ExcelFile: opens an Excel file; .sheet_names: the tab names

# %% Other formats (just so you know they exist)
print(df.head(2).to_html(index=False)[:80])    # .to_html(): table as web-page HTML; [:80]: first 80 characters
print(df.head(2).to_markdown())              # .to_markdown(): table as Markdown text; needs the tabulate package
print(df.head(2).to_latex()[:60])            # .to_latex(): table as LaTeX (paper-writing format)
df.head(5).to_pickle(OUT / "employees.pkl")  # .to_pickle(): saves in Python's own binary format
print(pd.read_pickle(OUT / "employees.pkl").shape)   # pd.read_pickle(): loads it back; .shape: (rows, columns)
# df.to_parquet("file.parquet")   # needs pyarrow, popular for big data
# pd.read_sql(query, connection)  # databases
# pd.read_clipboard()             # copy a table from a web page, then call this

# %% From text in memory
print(pd.read_csv(StringIO("name,score\nAsha,90\nBen,80")))
