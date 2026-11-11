from datetime import date, datetime, timedelta
from pathlib import Path

import pytest  # type: ignore
from playwright.sync_api import Locator, Page, expect  # type: ignore

PRACTICE_PAGE = Path(__file__).parent / "widgets_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


# ---------- Helpers (already done) ----------

def column_index(table: Locator, header: str) -> int:
    headers = [h.strip() for h in table.get_by_role("columnheader").all_text_contents()]
    return headers.index(header)


def column_values(table: Locator, header: str) -> list[str]:
    index = column_index(table, header)
    return [row.get_by_role("cell").nth(index).text_content()
            for row in table.locator("tbody tr").all()]


def to_number(money: str) -> int:
    """'$95,000' -> 95000"""
    return int(money.replace("$", "").replace(",", ""))


def go_to_next_page(page: Page) -> None:
    page_info = page.locator("#page-info")
    before = page_info.text_content()
    page.get_by_role("button", name="Next", exact=True).click()
    expect(page_info).not_to_have_text(before)


def pick_calendar_date(page: Page, target: date) -> None:
    page.get_by_label("Delivery date").click()
    header = page.locator("#month-year")
    target_month = target.replace(day=1)
    while True:
        shown = datetime.strptime(header.text_content(), "%B %Y").date()
        if shown == target_month:
            break
        if shown < target_month:
            page.get_by_role("button", name="Next month").click()
        else:
            page.get_by_role("button", name="Previous month").click()
    page.get_by_role("button", name=f"{target:%B} {target.day}, {target.year}", exact=True).click()


# ---------- My helpers ----------

def employees_table(page: Page) -> Locator:
    return page.get_by_role("table", name="Employees")


def orders_table(page: Page) -> Locator:
    return page.get_by_role("table", name="Orders")


def cell_for(table: Locator, row_text: str, header: str) -> Locator:
    """The cell in the `header` column of the row containing `row_text`."""
    row = table.locator("tbody tr").filter(has_text=row_text)
    return row.get_by_role("cell").nth(column_index(table, header))


def first_day_of_next_month(today: date) -> date:
    # Day 28 + 4 days always lands in next month (works in December too:
    # it rolls over into January of next year).
    return (today.replace(day=28) + timedelta(days=4)).replace(day=1)


# ================= PART 1: Tables (Employees) =================

def test_01_fatima_department(store: Page):
    expect(cell_for(employees_table(store), "Fatima Khan", "Department")).to_have_text("HR")


def test_02_ethan_start_date(store: Page):
    expect(cell_for(employees_table(store), "Ethan Brown", "Start date")).to_have_text("2023-05-22")


def test_03_sales_count(store: Page):
    departments = column_values(employees_table(store), "Department")
    assert departments.count("Sales") == 2


def test_04_total_salary(store: Page):
    salaries = column_values(employees_table(store), "Salary")
    assert sum(to_number(s) for s in salaries) == 458000


def test_05_started_before_2021(store: Page):
    table = employees_table(store)
    names = column_values(table, "Name")
    starts = column_values(table, "Start date")
    early = [name for name, start in zip(names, starts) if start < "2021-01-01"]
    assert early == ["Ben Carter", "Chen Wei", "Fatima Khan"]


def test_06_delete_all_sales(store: Page):
    table = employees_table(store)
    dept = column_index(table, "Department")
    sales_rows = table.locator("tbody tr").filter(
        has=store.locator(f"td:nth-child({dept + 1})", has_text="Sales")
    )

    # The delete-loop trap: every Delete re-renders the table, so a list from
    # .all() or nth(i) points at the wrong rows after the first delete.
    # Instead, re-find the FIRST Sales row each time until none are left.
    for _ in range(sales_rows.count()):
        before = table.locator("tbody tr").count()
        sales_rows.first.get_by_role("button", name="Delete").click()
        expect(table.locator("tbody tr")).to_have_count(before - 1)

    expect(sales_rows).to_have_count(0)
    expect(table.locator("tbody tr")).to_have_count(4)
    expect(store.locator("#employee-count")).to_have_text("4 employees")


def test_07_sort_salary_descending(store: Page):
    table = employees_table(store)
    salary_header = table.get_by_role("button", name="Salary")
    first_row = table.locator("tbody tr").first

    salary_header.click()  # ascending
    expect(first_row).to_contain_text("Ethan Brown")
    salary_header.click()  # descending
    expect(first_row).to_contain_text("Chen Wei")

    salaries = [to_number(s) for s in column_values(table, "Salary")]
    assert salaries == sorted(salaries, reverse=True)


# ================= PART 2: Pagination (Orders) =================

def test_08_find_order_2008(store: Page):
    table = orders_table(store)
    order_col = column_index(table, "Order")
    row = table.locator("tbody tr").filter(
        has=store.locator(f"td:nth-child({order_col + 1})", has_text="2008")
    )
    while row.count() == 0:
        go_to_next_page(store)

    expect(row.get_by_role("cell")).to_have_text(["2008", "Ben", "Cancelled", "$62.50"])
    expect(store.locator("#page-info")).to_have_text("Page 2 of 3")


def test_09_count_pending_orders(store: Page):
    # Counting straight after clicking Next would read the OLD page (the next
    # page loads after 300 ms). go_to_next_page waits for "Page x of y" to change.
    table = orders_table(store)
    next_button = store.get_by_role("button", name="Next", exact=True)
    pending = column_values(table, "Status").count("Pending")
    while next_button.is_enabled():
        go_to_next_page(store)
        pending += column_values(table, "Status").count("Pending")
    assert pending == 3


def test_10_previous_button(store: Page):
    go_to_next_page(store)
    go_to_next_page(store)
    expect(store.locator("#page-info")).to_have_text("Page 3 of 3")

    store.get_by_role("button", name="Previous", exact=True).click()
    expect(store.locator("#page-info")).to_have_text("Page 2 of 3")
    expect(store.get_by_role("button", name="Next", exact=True)).to_be_enabled()


# ================= PART 3: Date pickers =================

def test_11_native_birthday(store: Page):
    birthday = date(2001, 1, 31)
    # <input type="date"> always takes YYYY-MM-DD, which is what isoformat() gives
    store.get_by_label("Birthday").fill(birthday.isoformat())
    expect(store.locator("#birthday-summary")).to_have_text("Birthday: 2001-01-31")


def test_12_new_years_eve(store: Page):
    pick_calendar_date(store, date(2026, 12, 31))
    expect(store.get_by_label("Delivery date")).to_have_value("12/31/2026")


def test_13_one_week_from_today(store: Page):
    target = date.today() + timedelta(days=7)
    pick_calendar_date(store, target)
    expect(store.locator("#delivery-summary")).to_have_text(
        f"Delivery: {target:%B} {target.day}, {target.year}"
    )


def test_14_first_of_next_month(store: Page):
    target = first_day_of_next_month(date.today())
    pick_calendar_date(store, target)
    expect(store.get_by_label("Delivery date")).to_have_value(f"{target:%m/%d/%Y}")


def test_first_of_next_month_in_december():
    """The helper itself: December must roll over to January next year."""
    assert first_day_of_next_month(date(2026, 12, 15)) == date(2027, 1, 1)
    assert first_day_of_next_month(date(2026, 1, 31)) == date(2026, 2, 1)
