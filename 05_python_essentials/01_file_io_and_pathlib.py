# Reading and writing files. Use pathlib for paths, "with" so files always close.

import tempfile
from pathlib import Path

work = Path(tempfile.mkdtemp())         # a safe scratch folder
print(work)

# %% Write and read text
note = work / "note.txt"
note.write_text("line one\nline two\nline three\n")
print(note.read_text())
print(note.read_text().splitlines())

# %% open() with "with": closes the file for you
with open(note, "w", encoding="utf-8") as f:
    f.write("first\n")
    f.writelines(["second\n", "third\n"])

with open(note, encoding="utf-8") as f:
    for line in f:                      # one line at a time (good for big files)
        print(line.strip())

with open(note, "a", encoding="utf-8") as f:    # "a" = append
    f.write("fourth\n")
print(note.read_text())

# %% Modes: r read, w overwrite, a append, x create new only, b binary
data = bytes([72, 105, 33])
(work / "raw.bin").write_bytes(data)
print((work / "raw.bin").read_bytes())

# %% pathlib basics
p = Path("data") / "03_employees.csv"
print(p, p.name, p.stem, p.suffix, p.parent)
print(p.with_suffix(".json"), p.with_name("other.csv"))
print(p.exists(), p.is_file(), p.is_dir())
print(Path.cwd(), Path.home())
print(Path("a/b/../c").resolve().name)

# %% Folders
(work / "reports" / "2024").mkdir(parents=True, exist_ok=True)
(work / "reports" / "2024" / "a.txt").write_text("a")
(work / "reports" / "b.txt").write_text("b")
print(sorted(p.name for p in work.iterdir()))
print([p.name for p in work.rglob("*.txt")])      # search all sub folders
print([p.name for p in work.glob("*.txt")])
print((work / "note.txt").stat().st_size)

# %% Rename, copy, delete
note.rename(work / "renamed.txt")
(work / "renamed.txt").unlink()                    # delete a file
print((work / "renamed.txt").exists())

# %% Check before you write
target = work / "once.txt"
if not target.exists():
    target.write_text("created")
try:
    with open(target, "x") as f:                   # fails if it exists
        f.write("again")
except FileExistsError as error:
    print("Already there:", error.filename == str(target))

# %% Temporary files that clean up themselves
with tempfile.TemporaryDirectory() as tmp:
    temp_file = Path(tmp) / "x.txt"
    temp_file.write_text("gone soon")
    print(temp_file.exists())
print(temp_file.exists())
