# 03 Branches, merging, and pull requests

A branch is a separate line of work. `main` stays safe while you experiment.

## Branch commands

```bash
git branch                       # list branches
git switch -c feature/sql-lessons   # create and move to a new branch
git switch main                  # go back
git branch -d feature/sql-lessons   # delete after merging
```

## Typical team flow

1. `git switch main && git pull`
2. `git switch -c feature/my-change`
3. Edit, then `git add` and `git commit` (small commits)
4. `git push -u origin feature/my-change`
5. Open a **pull request** (PR) on GitHub
6. Teammates review, you fix comments, then it is merged
7. `git switch main && git pull`, delete the old branch

## Branch names

`feature/add-rag-demo`, `fix/null-rating`, `docs/readme`, `chore/update-deps`.

## Merge vs rebase

```bash
git merge main                   # bring main into your branch (adds a merge commit)
git rebase main                  # replay your commits on top of main (straight history)
```

- Merge is safer for beginners.
- Never rebase a branch other people already use.

## Merge conflicts

Two people edit the same lines. Git marks the file:

```text
<<<<<<< HEAD
your version
=======
their version
>>>>>>> main
```

Fix it:
1. Open the file, keep the correct text, delete the three marker lines.
2. `git add file.py`
3. `git commit` (merge) or `git rebase --continue` (rebase)

## Stash: park work for later

```bash
git stash                        # hide uncommitted changes
git stash list
git stash pop                    # bring them back
```

## Good pull requests

- Small (under about 400 changed lines).
- Title says what and why.
- Description: what changed, how to try it, screenshots if visual.
- Respond to every comment.

## Practice

1. Create a branch, add a file, commit, switch to `main`, merge the branch.
2. Make a conflict on purpose: edit the same line on two branches, merge, fix it.
