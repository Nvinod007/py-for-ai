# Reading and writing files. Use pathlib for paths, "with" so files always close.
# Each line has a short comment saying WHAT it is.

import tempfile  # import: loads a library; tempfile makes temporary files/folders
from pathlib import Path  # Path: an object that represents a file or folder path

work = Path(tempfile.mkdtemp())         # mkdtemp(): makes a new empty temp folder; Path(...) wraps its location
print(work)  # print(x): shows x on screen

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Write and read text
note = work / "note.txt"  # "/" between Paths joins them into a longer path
note.write_text("line one\nline two\nline three\n")  # write_text(s): saves text s into the file (replaces old content); \n = new line
print(note.read_text())  # read_text(): returns the whole file as one string
print(note.read_text().splitlines())  # splitlines(): cuts a string into a list of lines

# %% open() with "with": closes the file for you
with open(note, "w", encoding="utf-8") as f:  # with: auto-closes when block ends; open(path, mode): "w" = write (overwrite); encoding="utf-8" = normal text format; "as f" names the file object
    f.write("first\n")  # f.write(s): writes text s into the file
    f.writelines(["second\n", "third\n"])  # writelines(list): writes each string in the list, no extra newlines added

with open(note, encoding="utf-8") as f:  # no mode given = "r" (read only)
    for line in f:                      # for: loops; a file gives one line at a time (good for big files)
        print(line.strip())  # strip(): removes spaces/newline from both ends of a string

with open(note, "a", encoding="utf-8") as f:    # "a" = append (add to end, keep old content)
    f.write("fourth\n")
print(note.read_text())

# %% pathlib basics
p = Path("data") / "03_employees.csv"  # builds the path data/03_employees.csv
print(p, p.name, p.stem, p.suffix, p.parent)  # name = file name, stem = name without extension, suffix = extension, parent = folder
print(p.with_suffix(".json"), p.with_name("other.csv"))  # with_suffix: swaps extension; with_name: swaps whole file name
print(p.exists(), p.is_file(), p.is_dir())  # exists(): is there anything at this path; is_file(): is it a file; is_dir(): is it a folder
print(Path.cwd(), Path.home())  # cwd(): folder you are running from; home(): your home folder
print(Path("a/b/../c").resolve().name)  # resolve(): turns a path into a clean absolute path ("../" goes up one folder)

# %% Folders
(work / "reports" / "2024").mkdir(parents=True, exist_ok=True)  # mkdir: makes a folder; parents=True also makes missing parent folders; exist_ok=True = no error if it exists
(work / "reports" / "2024" / "a.txt").write_text("a")  # write a small file
(work / "reports" / "b.txt").write_text("b")
print(sorted(p.name for p in work.iterdir()))  # iterdir(): lists items in a folder; sorted(): puts in order; "x for p in ..." is a generator expression (a compact loop)
print([p.name for p in work.rglob("*.txt")])      # [... for ...]: list comprehension; rglob(pattern): finds matches in all sub folders; * = anything
print([p.name for p in work.glob("*.txt")])  # glob(pattern): finds matches in this folder only
print((work / "note.txt").stat().st_size)  # stat().st_size: file size in bytes

# %% Rename, copy, delete
note.rename(work / "renamed.txt")  # rename(new): moves/renames the file
(work / "renamed.txt").unlink()                    # unlink(): deletes a file
print((work / "renamed.txt").exists())

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Modes: r read, w overwrite, a append, x create new only, b binary
data = bytes([72, 105, 33])  # bytes(list): raw bytes made from numbers (72=H, 105=i, 33=!)
(work / "raw.bin").write_bytes(data)  # write_bytes(b): saves raw bytes into the file
print((work / "raw.bin").read_bytes())  # read_bytes(): reads the file as raw bytes

# %% Check before you write
target = work / "once.txt"
if not target.exists():  # if not ...: runs the block only when the test is False
    target.write_text("created")
try:  # try: run code that might fail
    with open(target, "x") as f:                   # "x" = create new only; fails if it exists
        f.write("again")
except FileExistsError as error:  # except: catches that error type; "as error" names it
    print("Already there:", error.filename == str(target))  # error.filename: the path that caused it; str(): turns a Path into text

# %% Temporary files that clean up themselves
with tempfile.TemporaryDirectory() as tmp:  # TemporaryDirectory(): a temp folder deleted when the with-block ends
    temp_file = Path(tmp) / "x.txt"
    temp_file.write_text("gone soon")
    print(temp_file.exists())
print(temp_file.exists())
