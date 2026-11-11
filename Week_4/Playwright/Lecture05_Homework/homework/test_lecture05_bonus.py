from playwright.sync_api import Locator, Page, expect  # type: ignore

TABLES_PAGE = "https://the-internet.herokuapp.com/tables"


def column_index(table: Locator, header: str) -> int:
    # These headers are <th> elements with extra spans, so read them directly
    headers = [h.strip() for h in table.locator("thead th").all_text_contents()]
    return headers.index(header)


def column_values(table: Locator, header: str) -> list[str]:
    index = column_index(table, header)
    return [row.locator("td").nth(index).text_content().strip()
            for row in table.locator("tbody tr").all()]


def test_highest_amount_due(page: Page):
    page.goto(TABLES_PAGE)
    table = page.locator("#table1")
    dues = [float(d.replace("$", "")) for d in column_values(table, "Due")]
    first_names = column_values(table, "First Name")
    last_names = column_values(table, "Last Name")

    top = dues.index(max(dues))
    assert f"{first_names[top]} {last_names[top]}" == "Jason Doe"


def test_sort_by_last_name(page: Page):
    page.goto(TABLES_PAGE)
    table = page.locator("#table1")
    table.locator("thead th").filter(has_text="Last Name").click()
    # After sorting, Bach (alphabetically first) is in the first row
    expect(table.locator("tbody tr").first).to_contain_text("Bach")

    last_names = column_values(table, "Last Name")
    assert last_names == sorted(last_names)
