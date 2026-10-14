# Git Beginner Lab — Student Task Tracker

A quick-reference guide to the Git commands used during the Revature **Student Task Tracker** exercise. 

## Part 1 — Create a local repository


mkdir student-task-tracker
cd student-task-tracker
git init -b main
git config user.name
git config user.email


- `mkdir`: Create a folder.
- `cd`: Change folders.
- `git init -b main`: Initialize a Git repository with `main` as the starting branch. If you already initialized with `master`, rename it using `git branch -m main`.
- `git config user.name` / `git config user.email`: Check the identity Git uses for commits.

Create `README.md` with a project description, then:

git status


## Part 2 — Stage, commit, and inspect history

After creating `tasks.txt` with at least three sample tasks:


git status
git add README.md tasks.txt
git status
git commit -m "Add project documentation and task list"
git log --oneline


After adding the fourth task:


git status
git diff
git add tasks.txt
git commit -m "Add fourth task to task list"
git log --oneline
git status


- `git status`: Show staged, modified, and untracked files.
- `git add`: Stage changes for the next commit.
- `git diff`: Show **unstaged** changes. Use `git diff --staged` to inspect staged changes.
- `git commit -m "..."`: Record the staged changes in history.
- `git log --oneline`: Display a concise commit history (newest first).

## Part 3 — Ignore files with `.gitignore`

Create `.gitignore` in the repository root:

gitignore
*.log
.env


Create `app.log` and `.env` containing **dummy data only**, then check the rules:


git status
git check-ignore -v app.log .env
git status --ignored
git add .gitignore
git commit -m "Add Git ignore rules"
git status


- `*.log`: Ignore untracked log files.
- `.env`: Ignore files named `.env` (often used for local configuration and secrets).
- `git check-ignore -v`: Explain which ignore rule matches a path.
- `git status --ignored`: Show ignored files as well.
- **Important:** `.gitignore` does not stop tracking a file already committed. To untrack it while preserving your local copy, use `git rm --cached FILE` and commit the removal. If a real secret was exposed, rotate/revoke it.

## Part 4 — Publish, clone, and synchronize

After creating an **empty** `student-task-tracker` repository on GitHub:


git remote add origin https://github.com/InstinctWorks/student-task-tracker.git
git remote -v
git push -u origin main


If `origin` already exists but its URL is wrong, **change** it rather than adding it again:


git remote set-url origin https://github.com/InstinctWorks/student-task-tracker.git
git remote -v


From your original `student-task-tracker` directory, move up one level and clone into a **separate** folder:


cd ..
git clone https://github.com/InstinctWorks/student-task-tracker.git student-task-tracker-clone
cd student-task-tracker-clone


Edit `README.md` inside the **clone**, then:


git status
git diff
git add README.md
git commit -m "Update project README"
git push
git log --oneline
git status


- `origin`: Conventional nickname for a remote repository.
- `git remote add`: Register a remote URL.
- `git remote set-url`: Correct an existing remote URL.
- `git push -u origin main`: Publish local `main` and set its upstream.
- `git clone`: Create another full working copy of a repository.
- `git push`: Publish commits from the current branch to its upstream (when configured).

## Part 5 — Fetch, pull, branch, and open a PR

Return to the **original** repository from the clone:


cd ..\student-task-tracker
git log --oneline
git fetch origin
git log --oneline --all --decorate
git pull origin main
git log --oneline
git status


- `git fetch origin`: Download new Git objects and update remote-tracking references such as `origin/main`, **without** integrating into your current branch.
- `git pull origin main`: Fetch and then integrate the remote `main` into the current branch (often a fast-forward).

Create a feature branch, add a priority section to `tasks.txt`, and commit:


git switch -c feature/add-priority
git branch
git status
git diff
git add tasks.txt
git commit -m "Add task priorities"
git log --oneline -3
git status
git push -u origin feature/add-priority


On GitHub, open a Pull Request with **base `main`** and **compare `feature/add-priority`**. Review the `Files changed` tab, then merge when permitted.

After the PR is merged on GitHub, update your original repository:


git switch main
git pull origin main
git log --oneline --graph --all --decorate
git status


- `git switch -c`: Create and switch to a branch.
- `git branch`: List local branches; `*` marks your current one.
- `git switch main`: Switch back to `main`.
- `git log --oneline --graph --all --decorate`: Display branch/merge structure and reference names.

## Part 6 — Verify final state


git check-ignore -v app.log .env
git status
git log --oneline --graph --all --decorate


Confirm that `tasks.txt` has priorities, `.gitignore` is tracked, ignored files were not accidentally committed, and the pull request was reviewed/merged as required.

## Extra exercise — Resolve a merge conflict

This was practiced in the **original** repository. Two branches deliberately changed the same README line differently.


git switch -c practice/merge-conflict


Edit an existing line in `README.md`, then:


git add README.md
git commit -m "Update README description on practice branch"
git switch main


Change **the same line** differently on `main`, then:


git add README.md
git commit -m "Revise README description on main"
git merge practice/merge-conflict


Git reports `CONFLICT (content)` because it cannot choose between the two edits. Open `README.md` and resolve the section with markers like:


<<<<<<< HEAD
Current branch version
=======
Incoming branch version
>>>>>>> practice/merge-conflict


Keep the desired final wording and **remove all conflict markers**. Save the file, then:


git status
git add README.md
git commit -m "Resolve README merge conflict"
git status
git log --oneline --graph --all --decorate


git push origin main

