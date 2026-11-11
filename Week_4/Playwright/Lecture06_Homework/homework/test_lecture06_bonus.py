from pathlib import Path

from playwright.sync_api import Page, expect  # type: ignore

SITE = "https://the-internet.herokuapp.com"


def test_js_prompt(page: Page):
    page.goto(f"{SITE}/javascript_alerts")
    page.once("dialog", lambda dialog: dialog.accept("hello"))
    page.get_by_role("button", name="Click for JS Prompt").click()
    expect(page.locator("#result")).to_have_text("You entered: hello")


def test_nested_frames_middle(page: Page):
    page.goto(f"{SITE}/nested_frames")
    # Old-style <frame> elements with name attributes, nested two deep
    middle = (page.frame_locator("frame[name='frame-top']")
                  .frame_locator("frame[name='frame-middle']"))
    expect(middle.locator("body")).to_have_text("MIDDLE")


def test_new_window(page: Page):
    page.goto(f"{SITE}/windows")
    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="Click Here").click()
    new_window = popup_info.value
    expect(new_window.get_by_role("heading")).to_have_text("New Window")


def test_upload_file(page: Page, tmp_path: Path):
    upload = tmp_path / "notes.txt"
    upload.write_text("hello from playwright")

    page.goto(f"{SITE}/upload")
    page.locator("#file-upload").set_input_files(upload)
    page.get_by_role("button", name="Upload").click()

    expect(page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
    expect(page.locator("#uploaded-files")).to_have_text("notes.txt")
