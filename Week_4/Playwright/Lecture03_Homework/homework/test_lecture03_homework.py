import re
from pathlib import Path

import pytest  # type: ignore
from playwright.sync_api import Page, expect  # type: ignore

PRACTICE_PAGE = Path(__file__).parent / "actions_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


def log_in(page: Page, username: str, password: str) -> None:
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Log in").click()


# ================= PART 1: Actions and assertions =================

def test_01_successful_login(store: Page):
    log_in(store, "student", "secret123")
    message = store.locator("#login-message")
    expect(message).to_have_text("Welcome, student!")
    expect(message).to_have_class("success")
    expect(store).to_have_url(re.compile("#dashboard"))


def test_02_failed_login(store: Page):
    log_in(store, "student", "wrong-password")
    message = store.locator("#login-message")
    # Check the message FIRST: it only appears after the 1 second check is done.
    # If we checked the URL first, it would pass straight away (the URL hasn't
    # changed YET), even if the page was about to redirect to #dashboard.
    expect(message).to_have_text("Invalid username or password")
    expect(message).to_have_class("error")
    expect(store).not_to_have_url(re.compile("#dashboard"))


def test_03_empty_login(store: Page):
    store.get_by_role("button", name="Log in").click()
    expect(store.locator("#login-message")).to_have_text("Invalid username or password")


def test_04_search_with_enter(store: Page):
    search = store.get_by_placeholder("Search products")
    search.fill("bike light")
    search.press("Enter")
    expect(store.locator("#search-result")).to_have_text("Results for: bike light")


def test_05_add_five_items(store: Page):
    add_button = store.get_by_role("button", name="Add item")
    for _ in range(5):
        add_button.click()
    expect(store.locator("#cart-count")).to_have_text("Items: 5")


def test_06_terms_toggle(store: Page):
    agree = store.get_by_label("I agree to the terms")
    continue_button = store.get_by_role("button", name="Continue")

    expect(continue_button).to_be_disabled()
    agree.check()
    expect(continue_button).to_be_enabled()
    agree.uncheck()
    expect(continue_button).to_be_disabled()


# ================= PART 2: Dynamic elements =================

def test_07_load_products(store: Page):
    store.get_by_role("button", name="Load products").click()
    spinner = store.get_by_text("Loading...")
    expect(spinner).to_be_visible()
    expect(spinner).to_be_hidden()

    products = store.locator("#product-list li")
    expect(products).to_have_count(3)
    expect(products.last).to_have_text("Jacket")


def test_08_process_order(store: Page):
    store.get_by_role("button", name="Process order").click()
    expect(store.locator("#order-status")).to_have_text("Complete")


def test_09_slow_report(store: Page):
    store.get_by_role("button", name="Generate report").click()
    # The default expect timeout is 5 s and the report takes 7 s, so raise it.
    expect(store.locator("#report-result")).to_have_text("Report ready", timeout=10_000)


# ================= PART 5: Bonus - fix a flaky test =================
# The original test_flaky_login (kept here as a comment so it doesn't run):
#
#     def test_flaky_login(page: Page):
#         page.goto(PRACTICE_PAGE.as_uri())
#         page.locator("#username").fill("student")
#         page.locator("#password").fill("secret123")
#         page.locator("#login-button").click()
#         time.sleep(1)
#         assert page.locator("#login-message").text_content() == "Welcome, student!"
#
# What's wrong with it:
# 1. time.sleep(1) is a guess. The page also waits exactly 1 second, so it's a
#    race: sometimes the message has changed, sometimes it still says "Checking...".
#    On a slow machine it fails more often; on a fast one it just wastes time.
# 2. text_content() reads the text ONCE, and a plain assert never retries.
#    expect(...).to_have_text() keeps retrying until the text matches or times out.
# 3. (Smaller) It uses CSS ids instead of user-facing locators (label / role).

def test_fixed_flaky_login(page: Page):
    page.goto(PRACTICE_PAGE.as_uri())
    log_in(page, "student", "secret123")
    expect(page.locator("#login-message")).to_have_text("Welcome, student!")


# ================= PART 4: Trace Viewer answers =================
# (from: pytest homework -k successful_login --tracing on)
# 1. 7 actions from my test: goto, fill Username, fill Password, click Log in,
#    and 3 expects (text, class, URL). Trace Viewer also shows "New page"
#    from the fixture's setup.
# 2. In the "After" tab of the Log in click, the message says "Checking...".
#    The click finished, but the page's 1 second check hadn't finished yet.
# 3. The to_have_text assertion waited about 1.3 seconds (it kept retrying
#    until "Welcome, student!" appeared). The next two expects took ~10 ms each.
