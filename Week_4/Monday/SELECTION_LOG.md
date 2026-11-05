
# SELECTION_LOG.md (Task 7)

| Command | Selected | When would a team run this? |
|---|---:|---|
| `python -m pytest -m smoke` | 7 | To quickly verify critical functionality before committing changes. |
| `python -m pytest -m "regression and not slow"` | 19 | To run regression tests before a release while excluding slower tests. |
| `python -m pytest -m boundary` | 10 | To verify edge cases, limits, and input boundaries. |
| `python -m pytest -k username` | 7 | When modifying username validation and wanting to test related functionality. |
| `python -m pytest -k "grade and not raises"` | 4 | When testing normal grade mapping without exception tests. |
| `python -m pytest tests/test_cart.py::TestCartTotal::test_empty_cart_total_is_zero` | 1 | To isolate and debug a specific test. |

## Questions

1. Temporarily change one `@pytest.mark.smoke` to `@pytest.mark.smok` (typo) and run pytest. What happens and what exit code do you get? Why is that useful?

PyTest reports an error because the marker is not registered. The exit code is 2. This is useful because --strict-markers catches spelling mistakes and prevents tests from silently using incorrect markers.

2. What exit code did a run that selected zero tests give?

Exit code 5. PyTest uses this exit code when no tests are collected.

3. Which test is your xfail, and what would you see if the bug were fixed (strict=True)?

`test_truncate_text_exactly_max_len_is_unchanged` is the xfail test. If the bug were fixed, PyTest would report XPASS(strict), causing the test suite to fail until the xfail marker was removed.
