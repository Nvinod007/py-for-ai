# 04 Undo and recover

Almost anything committed can be recovered. Uncommitted work can be lost, so commit often.

## Undo changes that are not committed

```bash
git restore file.py              # throw away edits to a file
git restore --staged file.py     # unstage (keep the edits)
git restore .                    # throw away ALL edits (careful)
git clean -n                     # preview untracked files that would be deleted
git clean -fd                    # actually delete untracked files and folders
```

## Fix the last commit

```bash
git commit --amend -m "better message"       # change the message
git add forgotten.py && git commit --amend --no-edit   # add a forgotten file
```

Only amend commits you have not pushed.

## Undo commits

| Goal | Command | Safe after push? |
|---|---|---|
| Add a new commit that cancels an old one | `git revert abc1234` | Yes |
| Move back, keep the changes staged | `git reset --soft HEAD~1` | No |
| Move back, keep the changes unstaged | `git reset HEAD~1` | No |
| Move back and delete the changes | `git reset --hard HEAD~1` | No, destructive |

When unsure, use `git revert`.

## Get a file from an older commit

```bash
git log --oneline -- file.py
git restore --source abc1234 file.py
```

## I lost a commit

```bash
git reflog                       # every place HEAD has been
git switch -c rescue abc1234     # make a branch pointing at the lost commit
```

## Committed a secret by mistake

1. Treat the key as stolen: **revoke it and create a new one right now**.
2. Remove it from the code, use an environment variable.
3. Cleaning history (`git filter-repo`) comes after, and does not make the old key safe.

## Compare and inspect

```bash
git diff main..feature/x         # difference between two branches
git diff --stat                  # summary only
git shortlog -sn                 # commits per author
git bisect start                 # binary search for the commit that broke things
```

## Tags and releases

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Practice

1. Edit a file, then undo it with `git restore`.
2. Make a bad commit, then undo it with `git revert`.
3. Make a commit, run `git reset --hard HEAD~1`, then recover it using `git reflog`.
