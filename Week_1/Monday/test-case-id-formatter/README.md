# Test-Case ID Formatter

A small command-line program that collects a module prefix, test number, test title, and test counts. It formats a test-case ID, calculates the number of failed tests and the pass rate, and reports whether the results meet the 90% release threshold.

## Run

From this project folder, run:

```text
python test_case_id_formatter.py
```

Enter the requested values when prompted.

## Example

Example input: `login`, `42`, `Valid login`, `40`, and `34`.

```text
=== Test-Case ID Formatter ===
Module prefix (e.g. login): login
Test number: 42
Test title: Valid login
Tests executed: 40
Tests passed: 34
Generated ID: LOGIN-0042
Title: Valid login
Failed: 6
Pass rate: 85.0%
Release ready: False
```
