
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect


# Locate the HTML file in the same directory as this test file.
HTML_FILE = Path(__file__).parent/"practice_store.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(HTML_FILE.as_uri())
    return page


# Part A: CSS Selectors

# CSS 1 - Main Heading Exist
def test_css_01_main_heading(store: Page):


    loc = store.locator("h1")

    expect(loc).to_have_text("Practice Store")


# CSS 2 - Email input using ID
def test_css_02_email_input(store: Page):

    loc = store.locator("#email")
    expect(loc).to_have_attribute("type", "email")


# CSS 3 - Password input using type attribute
def test_css_03_password_input(store: Page):

    loc = store.locator('input[type="password"]')
    expect(loc).to_have_attribute("placeholder", "Enter password")


# CSS 4 - Remember me checkbox using ID
def test_css_04_remember_checkbox(store: Page):

    loc = store.locator("#remember")
    expect(loc).not_to_be_checked()


# CSS 5 - Sign in button using type attribute
def test_css_05_sign_in_button(store: Page):

    loc = store.locator('button[type="submit"]')
    expect(loc).to_have_text("Sign in")


# CSS 6 - Logo using alt attribute
def test_css_06_logo(store: Page):

    loc = store.locator('img[alt="Practice Store logo"]')
    expect(loc).to_have_attribute("src", "logo.png")


# CSS 7 - All navigation links
def test_css_07_navigation_links(store: Page):

    loc = store.locator("nav a")
    expect(loc).to_have_text(["Home", "Products", "Contact us"])


# CSS 8 - Contact us link using href
def test_css_08_contact_link(store: Page):

    loc = store.locator('a[href="#contact"]')
    expect(loc).to_have_text("Contact us")


# CSS 9 - Shipping icon using partial title match
def test_css_09_shipping_icon(store: Page):

    loc = store.locator('span[title*="shipping"]')
    expect(loc).to_have_attribute(
        "title", "Free shipping on orders over $50"
    )


# CSS 10 - Checkout using data-testid
def test_css_10_checkout_button(store: Page):

    loc = store.locator('[data-testid="checkout-button"]')
    expect(loc).to_have_text("Checkout")


# CSS 11 - Check All Product Items 
def test_css_11_all_product_items(store: Page):

    product = store.locator(".product")
    expect(product).to_have_count(4)


# CSS 12 - Check All Product Prices
def test_css_12_all_product_prices(store: Page):

    product_price = store.locator(".price")
    expect(product_price).to_have_count(4)


# CSS 13 - Add to Cart Button Disabled
def test_css_13_add_to_cart_button_disabled(store: Page):

    cart_button = store.locator("button:disabled")
    expect(cart_button).to_be_disabled()


# CSS 14 - add to Cart Buttons Enabled
def test_css_13_add_to_cart_button_enabled(store: Page):

    cart_button = store.locator(".product button:not(:disabled)")
    expect(cart_button).to_have_count(3)



# CSS 15 - First product name
def test_css_15_first_product_name(store: Page):

    loc = store.locator(".product h3").first
    expect(loc).to_have_text("Backpack")


# CSS 16 - Third product price
def test_css_16_third_product_price(store: Page):

    loc = store.locator(".product:nth-child(3) .price")
    expect(loc).to_have_text("$15.99")


# CSS 17 - Last product stock
def test_css_17_last_product_stock(store: Page):
    
    loc = store.locator(".product:last-child .stock")
    expect(loc).to_have_text("In stock")


# CSS 18 - Direct child h2 headings of sections
def test_css_18_section_headings(store: Page):
    
    loc = store.locator("section > h2")
    expect(loc).to_have_text(["Sign in", "Products", "Recent orders"])


# CSS 19 - All order rows excluding header
def test_css_19_order_rows(store: Page):
    
    loc = store.locator("tbody tr")
    expect(loc).to_have_count(4)


# CSS 20 - Second order status
def test_css_20_second_order_status(store: Page):
    
    loc = store.locator("tbody tr:nth-child(2) td:nth-child(3)")
    expect(loc).to_have_text("Pending")




# Part B: XPath Selectors

# XPath 1 - Third link in navigation
def test_xpath_01_third_nav_link(store: Page):
    loc = store.locator("//nav/a[3]")
    expect(loc).to_have_text("Contact us")


# XPath 2 - Password input using ID
def test_xpath_02_password_input(store: Page):
    loc = store.locator("//input[@id='password']")
    expect(loc).to_have_attribute("type", "password")


# XPath 3 - Email input using placeholder
def test_xpath_03_email_input(store: Page):
    loc = store.locator("//input[@placeholder='you@example.com']")
    expect(loc).to_be_empty()


# XPath 4 - Home link using exact text
def test_xpath_04_home_link(store: Page):
    loc = store.locator("//a[text()='Home']")
    expect(loc).to_have_attribute("href", "#home")


# XPath 5 - Forgot password using partial text
def test_xpath_05_forgot_password(store: Page):
    loc = store.locator("//a[contains(text(), 'Forgot')]")
    expect(loc).to_have_text("Forgot password?")


# XPath 6 - Sign in button using text
def test_xpath_06_sign_in_button(store: Page):
    loc = store.locator("//button[text()='Sign in']")
    expect(loc).to_have_attribute("type", "submit")


# XPath 7 - Checkbox inside Remember me label
def test_xpath_07_remember_checkbox(store: Page):
    loc = store.locator("//label[contains(., 'Remember me')]//input")
    expect(loc).to_have_id("remember")


# XPath 8 - Checkout button using text
def test_xpath_08_checkout_button(store: Page):
    loc = store.locator("//button[text()='Checkout']")
    expect(loc).to_have_attribute("data-testid", "checkout-button")


# XPath 9 - All product li elements using class
def test_xpath_09_product_items(store: Page):
    loc = store.locator("//li[@class='product']")
    expect(loc).to_have_count(4)


# XPath 10 - Product heading Jacket
def test_xpath_10_jacket_heading(store: Page):
    loc = store.locator("//h3[text()='Jacket']")
    expect(loc).to_be_visible()


# XPath 11 - Bike Light price using following-sibling
def test_xpath_11_bike_light_price(store: Page):
    loc = store.locator(
        "//h3[text()='Bike Light']/following-sibling::p[@class='price']"
    )
    expect(loc).to_have_text("$9.99")


# XPath 12 - Name of Out of stock product
def test_xpath_12_out_of_stock_product(store: Page):
    loc = store.locator("//p[text()='Out of stock']/parent::li/h3")
    expect(loc).to_have_text("Bike Light")


# XPath 13 - T-Shirt Add to cart button
def test_xpath_13_tshirt_button(store: Page):
    loc = store.locator("//li[.//h3[text()='T-Shirt']]//button")
    expect(loc).to_be_enabled()


# XPath 14 - All disabled buttons
def test_xpath_14_disabled_buttons(store: Page):
    loc = store.locator("//button[@disabled]")
    expect(loc).to_have_count(1)


# XPath 15 - Second product heading using positional indexing
def test_xpath_15_second_product_heading(store: Page):
    loc = store.locator("(//li[@class='product']//h3)[2]")
    expect(loc).to_have_text("Bike Light")


# XPath 16 - Last price using last()
def test_xpath_16_last_price(store: Page):
    loc = store.locator("(//p[@class='price'])[last()]")
    expect(loc).to_have_text("$49.99")


# XPath 17 - All In stock paragraphs
def test_xpath_17_in_stock_paragraphs(store: Page):
    loc = store.locator("//p[@class='stock' and text()='In stock']")
    expect(loc).to_have_count(3)


# XPath 18 - Status of Chen Wei's order
def test_xpath_18_chen_wei_status(store: Page):
    loc = store.locator("//tr[td[2][text()='Chen Wei']]/td[3]")
    expect(loc).to_have_text("Shipped")


# XPath 19 - Order number of Pending order
def test_xpath_19_pending_order_number(store: Page):
    loc = store.locator("//td[text()='Pending']/preceding-sibling::td[2]")
    expect(loc).to_have_text("1002")


# XPath 20 - Total of Cancelled order
def test_xpath_20_cancelled_order_total(store: Page):
    loc = store.locator("//tr[td[text()='Cancelled']]/td[4]")
    expect(loc).to_have_text("$15.99")
