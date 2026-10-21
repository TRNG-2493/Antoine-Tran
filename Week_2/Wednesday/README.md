# Week 2 — Wednesday: Debugging and Testing Foundations

**Training:** Revature QE Foundations  
**Topic:** Python Debugging, Logging, Unit Testing, and Git Merge Conflicts  
**Status:** In Progress

## Completed Work

### Part A — Debugging
- Investigated and fixed seven reported bugs in `run_stats.py`.
- Practiced using Python's Pdb debugger and reading tracebacks.
- Fixed issues involving list slicing, mutability, nested dictionaries, variable scope, and empty inputs.
- Completed `debug_log.md` with debugging evidence.

**Automated checks: 10/10 passed.**

### Part B — Logging (In Progress)
- Added a module-level logger.
- Implemented DEBUG logging for report IDs, median calculations, and slowest durations.
- Added INFO logging for flaky test tracking.
- Worked on WARNING logging for missing suites.

## Remaining Work

- Complete Part B logging configuration.
- Part C — Automated unit tests.
- Part D — Git merge conflict exercise.
- Part E — Logging and tests for the QE Foundations ingestion module.

## GitHub Repository

[Wednesday Debugging and Testing Exercise](https://github.com/InstinctWorks/week2-wed-debugging-testing)

**Latest checkpoint commit:** `e4456e3`

## Key Takeaways

Practiced identifying the root causes of Python bugs before implementing fixes. Learned how mutable objects, variable scope, and list operations can affect other parts of a program. Began using structured logging to capture diagnostic information during execution.