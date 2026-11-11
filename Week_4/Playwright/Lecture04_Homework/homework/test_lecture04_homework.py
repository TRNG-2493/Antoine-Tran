import re
from pathlib import Path

import pytest  # type: ignore
from playwright.sync_api import Page, expect  # type: ignore

PRACTICE_PAGE = Path(__file__).parent / "forms_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


def suggestions(page: Page):
    """The options inside the city suggestions list only."""
    return page.get_by_role("listbox", name="Suggestions").get_by_role("option")


# ================= PART 1: Radio buttons and checkboxes =================

def test_01_overnight_shipping(store: Page):
    store.get_by_label("Overnight").check()
    expect(store.get_by_label("Overnight")).to_be_checked()
    expect(store.get_by_label("Standard")).not_to_be_checked()
    expect(store.locator("#shipping-summary")).to_have_text("Shipping: Overnight")


def test_02_two_interests(store: Page):
    store.get_by_label("Newsletter").check()
    store.get_by_label("SMS updates").check()
    expect(store.locator("#interests-summary")).to_have_text("Selected: Newsletter, SMS updates")


def test_03_select_all_then_untick_one(store: Page):
    select_all = store.get_by_label("Select all")
    select_all.check()
    store.get_by_label("SMS updates").uncheck()
    expect(select_all).not_to_be_checked()
    expect(store.locator("#interests-summary")).to_have_text("Selected: Newsletter, Special offers")


# ================= PART 2: Dropdowns =================

def test_04_country_by_label(store: Page):
    country = store.get_by_label("Country", exact=True)
    country.select_option(label="United States")
    expect(country).to_have_value("us")
    expect(store.locator("#country-summary")).to_have_text("Country: United States")


def test_05_sizes(store: Page):
    sizes = store.get_by_label("Sizes", exact=True)
    sizes.select_option(label=["M", "L", "XL"])
    # to_have_values checks ALL the selected values at once
    expect(sizes).to_have_values(["m", "l", "xl"])

    # select_option replaces the old selection, it doesn't add to it
    sizes.select_option(label="XS")
    expect(sizes).to_have_values(["xs"])


def test_06_custom_dropdown(store: Page):
    # Not a <select>: it's a button that shows a <ul role="listbox">,
    # so we click it open and click the option like a user would.
    store.get_by_role("button", name="Choose a colour").click()
    colours = store.get_by_role("listbox", name="Colours")
    colours.get_by_role("option", name="Green").click()

    expect(store.locator("#colour-button")).to_have_text("Colour: Green")
    expect(colours).to_be_hidden()


# ================= PART 3: Keyboard =================

def test_07_two_lines_of_notes(store: Page):
    notes = store.get_by_label("Notes")
    notes.press_sequentially("Line 1")
    notes.press("Enter")
    notes.press_sequentially("Line 2")
    expect(notes).to_have_value("Line 1\nLine 2")


def test_08_tab_between_fields(store: Page):
    store.get_by_label("First name").fill("Ben")
    store.keyboard.press("Tab")

    last_name = store.get_by_label("Last name")
    expect(last_name).to_be_focused()
    store.keyboard.type("Carter")
    expect(last_name).to_have_value("Carter")


def test_09_save_shortcut(store: Page):
    # "ControlOrMeta" is Ctrl on Windows/Linux and Cmd on macOS
    store.keyboard.press("ControlOrMeta+s")
    expect(store.locator("#shortcut-result")).to_have_text("Saved with keyboard shortcut")


# ================= PART 4: Mouse =================

def test_10_hover_and_log_out(store: Page):
    # The menu only opens on :hover, so hover first, then click
    store.get_by_role("button", name="Account").hover()
    store.get_by_role("link", name="Log out").click()
    expect(store).to_have_url(re.compile("#logout"))


def test_11_double_and_right_click(store: Page):
    editable = store.get_by_title("Double-click to edit")
    editable.dblclick()
    expect(editable).to_have_text("Edit mode")

    store.get_by_text("Right-click here").click(button="right")
    expect(store.get_by_role("menu").get_by_role("menuitem")).to_have_count(2)


def test_12_drag_and_drop(store: Page):
    store.get_by_text("Drag me").drag_to(store.get_by_text("Drop here"))
    expect(store.locator("#drop-result")).to_have_text("Dropped!")


# ================= PART 5: Auto-suggestions =================

def test_13_detroit_with_keyboard(store: Page):
    city = store.get_by_label("City")
    city.press_sequentially("de")
    expect(suggestions(store)).to_have_text(["Denver", "Detroit"])

    # Detroit is the 2nd suggestion: ArrowDown twice, then Enter
    city.press("ArrowDown")
    city.press("ArrowDown")
    city.press("Enter")
    expect(store.locator("#city-summary")).to_have_text("City: Detroit")


def test_14_san_jose_with_mouse(store: Page):
    city = store.get_by_label("City")
    city.press_sequentially("san")
    expect(suggestions(store)).to_have_count(3)

    suggestions(store).filter(has_text="San Jose").click()
    expect(city).to_have_value("San Jose")
    expect(suggestions(store)).to_have_count(0)
