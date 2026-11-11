from playwright.sync_api import Page, expect  # type: ignore

SITE = "https://the-internet.herokuapp.com"


def test_dropdown_option_2(page: Page):
    page.goto(f"{SITE}/dropdown")
    dropdown = page.locator("#dropdown")
    dropdown.select_option(label="Option 2")
    expect(dropdown).to_have_value("2")


def test_checkboxes(page: Page):
    page.goto(f"{SITE}/checkboxes")
    # No labels on these checkboxes, so we fall back to CSS + position
    boxes = page.locator("#checkboxes input[type='checkbox']")
    boxes.first.check()
    boxes.nth(1).uncheck()
    expect(boxes.first).to_be_checked()
    expect(boxes.nth(1)).not_to_be_checked()


def test_key_press_escape(page: Page):
    page.goto(f"{SITE}/key_presses")
    page.locator("#target").press("Escape")
    expect(page.locator("#result")).to_have_text("You entered: ESCAPE")


def test_hover_first_picture(page: Page):
    page.goto(f"{SITE}/hovers")
    page.locator(".figure").first.hover()
    expect(page.get_by_text("name: user1")).to_be_visible()


def test_drag_a_onto_b(page: Page):
    page.goto(f"{SITE}/drag_and_drop")
    page.locator("#column-a").drag_to(page.locator("#column-b"))
    expect(page.locator("#column-a header")).to_have_text("B")
