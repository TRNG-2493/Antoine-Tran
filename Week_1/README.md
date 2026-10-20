# Week 1 Summary: Python Programming and Git Foundations

**Name:** Antoine Tran | **Cohort:** TRNG-2493 | **Tag:** `week1-complete`

## What this repo contains

| Day | Program / folder | What it does (one line) | Python topics used | Git skill practised |
|---|---|---|---|---|
| Mon | `Monday/` | Student Task Tracker for managing student tasks | variables, types, input/output | init, add, commit, log, pull request |
| Tue | `Tuesday/` | Number guessing game and log scanner | if/elif/else, conditionals, loops, break/continue | .gitignore, clone, push, pull, PR |
| Wed | `Wednesday/` | Test-Data Manager for organizing test data | lists, dicts, sets, collections | branch, merge |
| Thu | `Thursday/` | Collaborative reusable test utility library | functions, lambdas, decorators | Team branching, pull requests, driver/navigator |
| Fri | `Friday/` | Test-report system (TestResult, Suite, Reporter) | classes, encapsulation, inheritance | week-1 summary branch, PR, tag |

## How to run the Friday program

```bash
cd Week_1/Friday
py check_exercise.py     # expected: 24/24 checks passed
py run_report.py
```

Expected Checker Result: 24/24 checks passed

## What I learned this week

- Python: This week, I reviewed Python fundamentals such as variables, conditionals, loops, and collections while learning more about object-oriented programming. I gained a better understanding of classes, inheritance, properties, and methods, particularly when building the test-report system on Friday.
- Git: I learned how to manage my projects using Git and GitHub, including creating branches, making commits, pushing changes, and working with pull requests. I also gained experience collaborating with another developer through pair programming and managing changes in a shared repository.
- Testing mindset: I learned the importance of validating inputs and testing code regularly rather than waiting until the entire program is finished. For example, during Friday's exercise, the automated checker helped me identify mistakes in property setters, string formatting, and input validation.

## What was hardest, and what I would do differently

One of the more challenging parts of this week was understanding how different classes and methods interact, especially when using inheritance and properties. I occasionally made small mistakes with syntax and logic that required debugging. Going forward, I would focus on testing individual components more frequently and reviewing how each method works before combining everything.

## My commit history, honestly

- Best commit message I wrote this week: `Add TestResult with validation and alternative constructors`
- A vague message I wrote and the better version I would write now:
  `Add Suite with pass rate and failure` -> `Implement Suite with pass rate calculations and failure filtering`

## Next steps

- Continue practicing object-oriented programming, particularly inheritance, properties, and method overriding, while improving my ability to debug programs independently.