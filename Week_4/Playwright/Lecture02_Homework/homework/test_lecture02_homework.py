from pathlib import Path

import pytest # type: ignore
from playwright.sync_api import Page, expect # type: ignore

PRACTICE_PAGE = Path(__file__).parent / "locators_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


# ================= PART 1: Built-in locators =================
# Rule: use ONLY get_by_role, get_by_label, get_by_placeholder,
#       get_by_text, get_by_alt_text, get_by_title or get_by_test_id.
#       No page.locator() in Part 1!

def test_01_products_link(store: Page):
    # TODO: the "Products" LINK in the navigation is visible
    link = store.get_by_role("link", name="Products")
    expect(link).to_be_visible()


def test_02_recent_orders_heading(store: Page):
    # TODO: the "Recent orders" heading is visible
    heading = store.get_by_role("heading", name="Recent orders")
    expect(heading).to_be_visible()


def test_03_password_by_label(store: Page):
    # TODO: find the Password field by its label; check it is empty
    # Hint: expect(...).to_be_empty()
    label = store.get_by_label("Password")
    expect(label).to_be_empty()


def test_04_email_by_placeholder(store: Page):
    # TODO: find the Email field by its placeholder; check it is visible
    email = store.get_by_placeholder("you@example.com")
    expect(email).to_be_visible()


def test_05_remember_me_checkbox(store: Page):
    # TODO: the "Remember me" checkbox is NOT checked
    # Hint: expect(...).not_to_be_checked()
    checkbox = store.get_by_label("Remember me")
    expect(checkbox).not_to_be_checked()


def test_06_logo_by_alt_text(store: Page):
    # TODO: find the logo image by its alt text; check it is attached
    # Hint: expect(...).to_be_attached()
    logo = store.get_by_alt_text("Practice Store logo")
    expect(logo).to_be_attached()


def test_07_shipping_icon_by_title(store: Page):
    # TODO: find the shipping icon by its title; check it is visible
    icon = store.get_by_title("Free shipping on orders over $50")
    expect(icon).to_be_visible()


def test_08_checkout_by_test_id(store: Page):
    # TODO: find the Checkout button by its test id; check it is visible
    button = store.get_by_test_id("checkout-button")
    expect(button).to_be_visible()


def test_09_copyright_text(store: Page):
    # TODO: the footer text "2026 Practice Store" is visible
    footer = store.get_by_text("2026 Practice Store")
    expect(footer).to_be_visible()


def test_10_privacy_link(store: Page):
    # TODO: the "Privacy policy" link is visible
    link = store.get_by_role("link", name="Privacy policy")
    expect(link).to_be_visible()


# ================= PART 2: Filtering and chaining =================
# You may use page.locator(".product") as a starting point here.

def test_a_tshirt_price(store: Page):
    # TODO: in the T-Shirt product card, the price is "$15.99"
    # Hint: filter(has_text=...) then find ".price" inside it
    price = store.locator(".product").filter(has_text="T-Shirt").locator(".price")
    expect(price).to_have_text("$15.99")


def test_b_in_stock_count(store: Page):
    # TODO: exactly 3 products are "In stock"
    # Hint: expect(...).to_have_count(3)
    products = store.locator(".product").filter(has_text="In stock")
    expect(products).to_have_count(3)


def test_c_order_status(store: Page):
    # TODO: in the orders table, Ben Carter's order status is "Pending"
    # Hint: find the row, then the cells inside it. Which nth() is Status?
    status = store.locator("tbody tr").filter(has_text="Ben Carter").locator("td").nth(2)
    expect(status).to_have_text("Pending")



def test_d_first_and_last(store: Page):
    # TODO: the LAST product name is "Jacket"
    # TODO: the FIRST product price is "$29.99"
    products = store.locator(".product")

    last_product = products.last.locator("h3")
    expect(last_product).to_have_text("Jacket")
    
    first_price = products.first.locator(".price")
    expect(first_price).to_have_text("$29.99")


def test_e_bike_light_disabled(store: Page):
    # TODO: the Bike Light's "Add to cart" button is disabled
    # Hint: expect(...).to_be_disabled()
    button = store.locator(".product").filter(has_text="Bike Light").locator("button")
    expect(button).to_be_disabled()

# ================= PART 2 QUESTION =================
# Answer as a comment:
# What happens if you run
#     store.get_by_role("button", name="Add to cart").click()
# and how would you change it to click ONLY the Jacket's button?

# It causes a strict mode violation because multiple buttons
# match the locator. Playwright doesn't know which one to click.

# To click only the Jacket button:
# store.locator(".product").filter(has_text="Jacket").get_by_role("button", name="Add to cart").click()