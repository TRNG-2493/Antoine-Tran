# Commands Used

This reference collects the terminal commands from the Test-Case ID Formatter exercise.

## Open and initialize the project

```text
code .
git init
git status
```

Run `code .` from the project folder to open it in VS Code.

## Run the formatter and self-check

```text
python test_case_id_formatter.py
python check_exercise.py
```

## Part 1 — commit the prompts and input handling

```text
git status
git add test_case_id_formatter.py check_exercise.py
git commit -m "Add prompts for module, number, title and test counts"
git status
```

## Part 2 — commit the generated ID output

```text
git status
git diff
git add test_case_id_formatter.py
git commit -m "Add zero-padded test-case ID output"
git status
```

## Part 3 — commit the test summary and release decision

```text
git status
git add test_case_id_formatter.py
git commit -m "Add failed count, pass rate and release decision"
git status
```

## Part 4 — add the README and verify the repository

```text
python check_exercise.py
git status
git add README.md
git commit -m "Add README with usage instructions"
git status
python check_exercise.py
git log --oneline
```
