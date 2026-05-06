from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, Locator


class SpotAreaPage(BasePage):
    """Admin Spot Area page object.

    TODO selectors to update after inspecting UI:
    - Add data-testid for spot-area-title, spot-area-select, spot-row, and spot-delete.
    - Area B is selected by the dropdown. Do not navigate directly to /admin/spots/B.
    """

    PAGE_READY: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='spot-area-title']"),
        (By.CSS_SELECTOR, "table"),
        (By.XPATH, "//*[contains(., 'Loading spots')]"),
    ]
    AREA_SELECT: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='spot-area-select']"),
        (By.CSS_SELECTOR, "select"),
    ]
    TABLE_ROWS: Locator = (By.CSS_SELECTOR, "[data-testid='spot-row'], tbody tr")
    DELETE_BUTTON_IN_ROW: Locator = (
        By.XPATH,
        ".//button[contains(normalize-space(.), 'Delete')]",
    )

    def open(self, area: str | None = None) -> None:
        self.open_url(self.config.admin_spot_area_path)
        self.first_visible(self.PAGE_READY, "spot area page")
        self.wait.until(lambda _: self.page_has_finished_loading())
        if area:
            self.select_area(area)

    def select_area(self, area: str) -> None:
        select = self.first_visible(self.AREA_SELECT, "spot area select")
        current_value = (select.get_attribute("value") or "").strip()
        if current_value != area:
            self.select_by_visible_text_or_value(select, area)
        self.wait.until(lambda _: self.page_has_finished_loading())

    def page_has_finished_loading(self) -> bool:
        return "Loading spots" not in self.page_text()

    def rows(self) -> list[WebElement]:
        return [
            row
            for row in self.visible_elements(self.TABLE_ROWS)
            if row.find_elements(By.TAG_NAME, "td") and "spot" not in row.text.lower()
        ]

    def find_row(self, case: dict) -> WebElement | None:
        expected_position = str(case["position"])
        expected_vehicle = str(case["vehicle_type"]).upper()
        expected_slot = self._normalize_slot_type(case["slot_type"]).upper()

        for row in self.rows():
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                continue
            position = cells[0].text.strip()
            vehicle = cells[1].text.upper()
            slot_type = cells[2].text.upper()
            if position == expected_position and expected_vehicle in vehicle and expected_slot in slot_type:
                return row
        return None

    def find_row_across_configured_areas(self, case: dict) -> tuple[str, WebElement] | tuple[None, None]:
        for area in self._candidate_areas(case):
            if not self._is_on_spot_area_page():
                self.open()
            try:
                self.select_area(area)
            except TimeoutException:
                continue
            row = self.find_row(case)
            if row is not None:
                return area, row
        return None, None

    def delete_row(self, row: WebElement, accept_confirmation: bool = True) -> None:
        row.find_element(*self.DELETE_BUTTON_IN_ROW).click()
        alert: Alert = self.wait.until(EC.alert_is_present())
        if accept_confirmation:
            alert.accept()
        else:
            alert.dismiss()
        self.wait.until(lambda _: self._no_alert_present())

    def assert_row_present(self, case: dict) -> None:
        _, row = self.find_row_across_configured_areas(case)
        assert row is not None, f"Spot row should be present for {self.case_label(case)}"

    def assert_row_absent(self, case: dict) -> None:
        _, row = self.find_row_across_configured_areas(case)
        assert row is None, f"Spot row should be deleted/absent for {self.case_label(case)}"

    @staticmethod
    def case_label(case: dict) -> str:
        return (
            f"{case['row_id']} {case['test_case_id']} "
            f"position={case['position']} vehicle={case['vehicle_type']} slot={case['slot_type']}"
        )

    @staticmethod
    def _normalize_slot_type(slot_type: str) -> str:
        normalized = str(slot_type).strip().upper()
        if normalized == "OFFLINE":
            return "Offline"
        if normalized == "ONLINE":
            return "Online"
        return str(slot_type)

    def _candidate_areas(self, case: dict) -> tuple[str, ...]:
        vehicle_type = str(case.get("vehicle_type", "")).upper()
        if vehicle_type == "CAR" and "A" in self.config.admin_spot_areas:
            return ("A",)
        if vehicle_type == "MOTORBIKE" and "B" in self.config.admin_spot_areas:
            return ("B",)
        return self.config.admin_spot_areas

    def _is_on_spot_area_page(self) -> bool:
        return "/admin/spots" in self.driver.current_url and "/trash" not in self.driver.current_url

    def _no_alert_present(self) -> bool:
        try:
            self.driver.switch_to.alert
            return False
        except NoAlertPresentException:
            return True
