# 02 Git basics

Git saves snapshots of your project so you can go back, compare, and share.

## One-time setup

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --list
```

## Start or copy a project

```bash
git init                         # make this folder a repo
git clone <url>                  # copy a repo from GitHub
```

## The daily loop

Three areas: **working folder** -> **staging area** -> **history**.

```bash
git status                       # what changed?
git diff                         # unstaged changes
git add file.py                  # stage one file
git add .                        # stage everything
git diff --staged                # what will be committed
git commit -m "add pandas lessons"
git log --oneline                # short history
```

Commit message tips:
- Start with a verb: `add`, `fix`, `remove`, `rename`.
- One idea per commit.
- Say what changed and why, not "stuff" or "update".

## .gitignore: what git should never track

```gitignore
.venv/
__pycache__/
*.pyc
.env
.env.local
data/output/
.DS_Store
```

Share a `.env.example` (fake values), never the real `.env`.

## Look at history

```bash
git log --oneline --graph --all  # branches as a picture
git show abc1234                 # one commit
git log -p file.py               # history of one file
git blame file.py                # who changed each line
git diff HEAD~1                  # compare with the previous commit
```

## Remotes (GitHub, GitLab, Bitbucket)

```bash
git remote -v
git remote add origin <url>
git push -u origin main          # first push, remembers the branch
git push                         # later pushes
git pull                         # fetch and merge new changes
git fetch                        # fetch only, do not merge yet
```

## Practice

1. Make a new folder, run `git init`, add a `hello.py`, commit it.
2. Change the file, look at `git diff`, commit again.
3. Run `git log --oneline` and read your history.
