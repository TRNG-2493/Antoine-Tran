# ================= PART 3: Codegen answers =================
# Recorded with:
#   playwright codegen --target python-pytest -o homework/test_recorded.py "<file:/// URL>"
# Actions: log in as student / secret123, search "jacket" + Enter.
# The code below these comments is exactly what codegen generated.
#
# 1. Which locators did codegen choose for the username, password and Log in button?
#    All three are role-based locators with an accessible name:
#      username -> get_by_role("textbox", name="Username")
#      password -> get_by_role("textbox", name="Password")
#      Log in   -> get_by_role("button", name="Log in")
#    The names come from the <label for="..."> elements and the button text.
#    My hand-written tests use get_by_label("Username") for the fields;
#    both find the same <input>. Codegen also used
#    get_by_role("searchbox", name="Search products") for the search box
#    (<input type="search" aria-label="Search products">).
#
# 2. Which generated lines are unnecessary?
#    - The .click() on Username (right after goto) and on the search box:
#      fill() already focuses the field, so the clicks add nothing.
#    - .press("Tab") on Username: it only recorded me moving to the next
#      field. The next line fills Password directly, so the Tab isn't needed.
#    - "import re" and "expect" are imported but never used.
#
# 3. What important thing is missing from the recorded test?
#    Assertions. There is no expect(...) at all, so the test checks nothing:
#    it would still PASS if the password were wrong or the search did nothing.
#    (That's why it passed straight away: 11 passed with it included.)
#    It also never waits for "Welcome, student!" before moving on.
#
# 4. What would you change before using this as a real test?
#    - Add assertions: expect(#login-message).to_have_text("Welcome, student!"),
#      the URL contains "#dashboard", and #search-result says "Results for: jacket".
#    - Remove the extra click()/press("Tab") lines and unused imports.
#    - Replace the hard-coded file:///C:/Users/... path with
#      Path(__file__).parent / "actions_practice.html" (.as_uri()) so it works
#      on any machine, and reuse the `store` fixture / a log_in() helper.
#    - Rename test_example to something meaningful, e.g. test_login_then_search,
#      and split it into separate login and search tests.

import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("file:///C:/Users/g4fil/Documents/GitHub/Antoine-Tran/Week_4/Playwright/Lecture03_Homework/homework/actions_practice.html")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("student")
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_role("textbox", name="Password").fill("secret123")
    page.get_by_role("button", name="Log in").click()
    page.get_by_role("searchbox", name="Search products").click()
    page.get_by_role("searchbox", name="Search products").fill("jacket")
    page.get_by_role("searchbox", name="Search products").press("Enter")
