import csv
import re
from pathlib import Path

import pytest  # type: ignore
from playwright.sync_api import BrowserContext, Dialog, Page, expect  # type: ignore

PRACTICE_PAGE = Path(__file__).parent / "events_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


# ================= PART 1: Dialogs =================
# Every handler is registered BEFORE the click that opens the dialog.

def test_01_alert_message(store: Page):
    messages = []

    def handle(dialog: Dialog):
        messages.append(dialog.message)
        dialog.accept()

    store.once("dialog", handle)
    store.get_by_role("button", name="Show alert").click()

    assert messages == ["Your order has been placed!"]
    expect(store.locator("#dialog-result")).to_have_text("Alert closed")


def test_02_accept_confirm(store: Page):
    types = []

    def handle(dialog: Dialog):
        types.append(dialog.type)
        dialog.accept()

    store.once("dialog", handle)
    store.get_by_role("button", name="Delete account").click()

    assert types == ["confirm"]
    expect(store.locator("#dialog-result")).to_have_text("Account deleted")


def test_03_prompt_with_text(store: Page):
    store.once("dialog", lambda dialog: dialog.accept("FREESHIP"))
    store.get_by_role("button", name="Enter coupon").click()
    expect(store.locator("#dialog-result")).to_have_text("Coupon applied: FREESHIP")


def test_04_cancel_prompt(store: Page):
    store.once("dialog", lambda dialog: dialog.dismiss())
    store.get_by_role("button", name="Enter coupon").click()
    expect(store.locator("#dialog-result")).to_have_text("No coupon entered")


# ================= PART 2: Frames and Shadow DOM =================

def test_05_profile_frame(store: Page):
    profile = store.frame_locator("iframe[title='Profile form']")
    profile.get_by_label("Name").fill("Ben Carter")
    profile.get_by_role("button", name="Save").click()
    expect(profile.get_by_text("Saved: Ben Carter")).to_be_visible()


def test_06_nested_newsletter_frame(store: Page):
    # The Newsletter frame is INSIDE the Profile form frame, so chain them
    newsletter = (store.frame_locator("iframe[title='Profile form']")
                       .frame_locator("iframe[title='Newsletter']"))
    newsletter.get_by_label("Newsletter email").fill("ben@example.com")
    newsletter.get_by_role("button", name="Subscribe").click()
    expect(newsletter.get_by_text("Subscribed: ben@example.com")).to_be_visible()


def test_07_shadow_dom_follow(store: Page):
    # Playwright's CSS and role locators pierce OPEN shadow roots automatically
    # (XPath does not, and nothing can see inside a CLOSED shadow root).
    card = store.locator("#open-card")
    expect(card.locator(".name")).to_have_text("Asha Patel")
    card.get_by_role("button", name="Follow").click()
    expect(card.locator(".status")).to_have_text("Following")


# ================= PART 3: Navigation, tabs and pop-ups =================

def test_08_navigate_and_go_back(store: Page):
    store.get_by_role("link", name="Help page").click()
    expect(store).to_have_title("Help Centre")

    store.get_by_role("link", name="Back to the store").click()
    expect(store).to_have_title("Practice Store - Events")

    store.go_back()
    expect(store).to_have_title("Help Centre")


def test_09_new_tab_then_close(store: Page, context: BrowserContext):
    with context.expect_page() as new_page_info:
        store.get_by_role("link", name="Open help in a new tab").click()
    help_tab = new_page_info.value

    expect(help_tab.get_by_role("heading", level=1)).to_have_text("Help Centre")
    help_tab.close()
    assert len(context.pages) == 1


def test_10_chat_popup(store: Page):
    with store.expect_popup() as popup_info:
        store.get_by_role("button", name="Open chat window").click()
    chat = popup_info.value

    expect(chat).to_have_url(re.compile("from=chat"))
    expect(chat).to_have_title("Help Centre")


def test_11_delayed_redirect(store: Page):
    store.get_by_role("button", name="Go to help in 1 second").click()
    expect(store).to_have_url(re.compile("from=redirect"))
    expect(store).to_have_title("Help Centre")


# ================= PART 4: Upload and download =================

def test_12_upload_resume(store: Page, tmp_path: Path):
    resume = tmp_path / "cv.pdf"
    resume.write_bytes(b"x" * 1024)

    store.get_by_label("Resume").set_input_files(resume)
    expect(store.locator("#resume-result")).to_have_text("Uploaded: cv.pdf (1024 bytes)")


def test_13_upload_photos_from_memory(store: Page):
    store.get_by_label("Photos").set_input_files([
        {"name": "cat.png", "mimeType": "image/png", "buffer": b"fake cat image"},
        {"name": "dog.png", "mimeType": "image/png", "buffer": b"fake dog image"},
    ])
    expect(store.locator("#photos-result")).to_have_text("2 photos: cat.png, dog.png")


def test_14_avatar_file_chooser(store: Page, tmp_path: Path):
    avatar = tmp_path / "profile.jpg"
    avatar.write_bytes(b"fake jpg")

    # The real <input type="file"> is hidden, so catch the file chooser
    # that opens when the button is clicked.
    with store.expect_file_chooser() as chooser_info:
        store.get_by_role("button", name="Choose avatar").click()
    chooser_info.value.set_files(avatar)

    expect(store.locator("#avatar-result")).to_have_text("Avatar: profile.jpg")


def test_15_download_and_read_csv(store: Page, tmp_path: Path):
    with store.expect_download() as download_info:
        store.get_by_role("button", name="Export orders as CSV").click()
    download = download_info.value

    saved = tmp_path / download.suggested_filename
    download.save_as(saved)

    with saved.open(newline="") as f:
        rows = list(csv.DictReader(f))

    assert [row["customer"] for row in rows] == ["Asha", "Ben"]
    assert sum(float(row["total"]) for row in rows) == 27.5
