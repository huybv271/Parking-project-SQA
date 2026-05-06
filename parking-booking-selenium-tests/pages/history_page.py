from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage, Locator


class HistoryPage(BasePage):
    """Reservation history page object.

    TODO selectors to update after inspecting UI:
    - Add data-testid for history-title, history-table, history-row, history-back,
      history-detail-button, and cells date-in/date-out/time-in/time-out/plate.
    - Current fallback uses table rows/cells and page text.
    """

    PAGE_TITLE: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='history-title']"),
        (By.XPATH, "//h1[contains(., 'Lịch sử') or contains(., 'History')]"),
    ]
    BACK_BUTTON: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='history-back']"),
        (By.XPATH, "//button[contains(., 'Quay lại') or contains(., 'Back')]"),
    ]
    TABLE: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='history-table']"),
        (By.CSS_SELECTOR, "table"),
    ]
    HEADERS: Locator = (By.CSS_SELECTOR, "thead th, [data-testid='history-header']")
    ROWS: Locator = (By.CSS_SELECTOR, "[data-testid='history-row'], tbody tr")
    DETAIL_BUTTONS: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='history-detail'], button[aria-label*='detail'], a[href*='history']",
    )
    EMPTY_MESSAGE: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='history-empty']"),
        (By.XPATH, "//*[contains(., 'Chưa có') or contains(., 'No history')]"),
    ]

    def open(self) -> None:
        self.open_url(self.config.history_path)
        self.first_visible(self.PAGE_TITLE, "history page title")

    def rows(self) -> list[WebElement]:
        return self.visible_elements(self.ROWS)

    def headers(self) -> list[WebElement]:
        return self.visible_elements(self.HEADERS)

    def back_button(self) -> WebElement:
        return self.first_clickable(self.BACK_BUTTON, "history back button")

    def find_row_by_plate(self, plate: str) -> WebElement | None:
        expected = plate.strip().upper()
        for row in self.rows():
            if expected in row.text.upper():
                return row
        return None

    def assert_history_contains_case(self, case: dict) -> None:
        row = self.find_row_by_plate(case["plate"])
        assert row is not None, f"History should contain reservation plate {case['plate']}"
        row_text = row.text.upper()
        assert case["plate"].upper() in row_text
        assert case["vehicle_type"].upper() in row_text
        assert str(case["time_in"]) in row_text
        assert str(case["time_out"]) in row_text
        assert self._date_visible(row_text, case["date_in"]), f"History should show date in {case['date_in']}"
        assert self._date_visible(row_text, case["date_out"]), f"History should show date out {case['date_out']}"

    def open_first_detail_if_available(self) -> bool:
        buttons = self.visible_elements(self.DETAIL_BUTTONS)
        if not buttons:
            return False
        buttons[0].click()
        return True

    @staticmethod
    def _date_visible(text: str, iso_date: str) -> bool:
        year, month, day = iso_date.split("-")
        candidates = {
            iso_date,
            f"{int(month)}/{int(day)}/{year}",
            f"{int(day)}/{int(month)}/{year}",
            f"{day}/{month}/{year}",
            f"{month}/{day}/{year}",
        }
        return any(candidate.upper() in text for candidate in candidates)
