# 01 Terminal basics

The terminal is how you run Python, git, uv, docker, and servers. Type each command and watch what happens.

## Where am I?

| Command | Meaning |
|---|---|
| `pwd` | print the current folder |
| `ls` | list files |
| `ls -la` | list with details and hidden files |
| `cd folder` | go into a folder |
| `cd ..` | go up one level |
| `cd ~` | go to your home folder |
| `cd -` | go back to the previous folder |

## Files and folders

```bash
mkdir demo                  # make a folder
mkdir -p a/b/c              # make nested folders
touch notes.txt             # create an empty file
cp notes.txt copy.txt       # copy
cp -r demo demo_backup      # copy a folder
mv copy.txt renamed.txt     # rename or move
rm renamed.txt              # delete a file (no recycle bin!)
rm -r demo_backup           # delete a folder
```

## Reading files

```bash
cat notes.txt               # print the whole file
head -n 5 data/03_employees.csv      # first 5 lines
tail -n 5 data/03_employees.csv      # last 5 lines
tail -f app.log             # follow a log live (Ctrl+C to stop)
wc -l data/03_employees.csv # count lines
less bigfile.txt            # scroll (q to quit)
```

## Searching

```bash
rg "salary" data/            # fastest text search (ripgrep)
grep -rn "salary" data/      # same idea, built in
find . -name "*.py"          # find files by name
```

## Pipes and redirects

```bash
ls | wc -l                          # pipe: output of one command into the next
cat data/03_employees.csv | head -3
echo "hello" > file.txt             # write (overwrite)
echo "more" >> file.txt             # append
python script.py > out.txt 2> err.txt   # save output and errors separately
python script.py 2>&1 | tee run.log     # see it AND save it
```

## Running Python

```bash
python hello.py                     # run a file
python -c "print(2 + 2)"            # run one line
python -m http.server 8000          # tiny web server for the current folder
uv run python hello.py              # run inside the project environment
uv add requests                     # add a package
```

## Environment variables

```bash
echo $HOME
export OPENAI_API_KEY="paste-here"      # lasts for this terminal window only
echo $OPENAI_API_KEY | head -c 5        # check without printing everything
env | rg OPENAI                         # list matching variables
```

Never paste real keys into files that go to git. Keep a `.env.example` with fake values.

## Processes

```bash
ps aux | rg python          # find running Python programs
lsof -i :8000               # who is using port 8000?
kill 12345                  # stop a process by id
kill -9 12345               # force stop
Ctrl+C                      # stop the running program
Ctrl+Z                      # pause it
```

## Useful shortcuts

| Keys | Action |
|---|---|
| `Tab` | auto-complete a name |
| `Up arrow` | previous command |
| `Ctrl+R` | search command history |
| `Ctrl+A` / `Ctrl+E` | jump to start / end of line |
| `Ctrl+L` | clear the screen |

## Network quick checks

```bash
curl https://api.github.com                          # GET a URL
curl -s https://api.github.com | python -m json.tool # pretty print JSON
curl -X POST localhost:8000/items -H "Content-Type: application/json" -d '{"name":"pen"}'
ping -c 3 google.com
```

## Practice

1. Make a folder `playground`, go inside, create three files.
2. Count the lines of `data/03_employees.csv`.
3. Find every `.py` file under `02_pandas`.
4. Print the 5 highest salaries using `sort`: `sort -t, -k6 -n -r data/03_employees.csv | head -5`.
