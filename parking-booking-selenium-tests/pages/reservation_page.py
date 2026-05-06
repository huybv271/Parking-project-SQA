from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage, Locator


class ReservationPage(BasePage):
    """Reservation booking page object.

    TODO selectors to update after inspecting UI:
    - Add data-testid for reservation-form, date-in, date-out, time-in, time-out,
      vehicle-type, plate, search-spots, back-button, spot-card, reserve-button,
      toast-success, toast-error.
    - Current fallback uses input order and visible text from the current Next.js page.
    """

    PAGE_TITLE: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='reservation-title']"),
        (By.XPATH, "//h1[contains(., 'Đặt') or contains(., 'Reservation')]"),
    ]
    FORM_CONTAINER: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='reservation-form']"),
        (By.XPATH, "//button[contains(., 'Tìm') or contains(., 'Search')]/ancestor::div[contains(@class, 'space-y-6')][1]"),
        (By.CSS_SELECTOR, "form"),
    ]
    LABELS: Locator = (By.CSS_SELECTOR, "label")
    DATE_INPUTS: Locator = (By.CSS_SELECTOR, "input[type='date']")
    NUMBER_INPUTS: Locator = (By.CSS_SELECTOR, "input[type='number']")
    VEHICLE_SELECT: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='vehicle-type']"),
        (By.CSS_SELECTOR, "select"),
    ]
    PLATE_INPUT: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='plate']"),
        (By.CSS_SELECTOR, "input[placeholder*='30G']"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ]
    SEARCH_BUTTON: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='search-spots']"),
        (By.XPATH, "//button[contains(., 'Tìm chỗ') or contains(., 'Search spots') or contains(., 'Tìm')]"),
    ]
    BACK_BUTTON: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='reservation-back']"),
        (By.XPATH, "//button[contains(., 'Quay lại') or contains(., 'Back')]"),
    ]
    SPOT_CARDS: Locator = (By.CSS_SELECTOR, "[data-testid='spot-card'], button.rounded-lg.border")
    SUCCESS_MESSAGE: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='toast-success']"),
        (By.XPATH, "//*[contains(., 'Slot found') or contains(., 'Reservation created') or contains(., 'thành công')]"),
    ]
    ERROR_MESSAGE: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='toast-error']"),
        (By.XPATH, "//*[contains(., 'Please fill') or contains(., 'No slot') or contains(., 'Invalid') or contains(., 'Error') or contains(., 'không')]"),
    ]
    CONFIRM_BUTTON: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='confirm-reservation']"),
        (By.XPATH, "//button[contains(., 'Xác nhận đặt chỗ') or contains(., 'Confirm') or contains(., 'Reserve')]"),
    ]
    PAYMENT_CREATED_PANEL: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='payment-created']"),
        (By.XPATH, "//*[contains(., 'Reservation đã được tạo') or contains(., 'Thanh toán với VNPAY') or contains(., 'Reservation created')]"),
    ]

    def open(self) -> None:
        self.open_url(self.config.reservation_path)
        self.first_visible(self.PAGE_TITLE, "reservation page title")

    def labels(self) -> list[WebElement]:
        return self.visible_elements(self.LABELS)

    def form_container(self) -> WebElement:
        return self.first_visible(self.FORM_CONTAINER, "reservation form")

    def date_inputs(self) -> list[WebElement]:
        inputs = self.visible_elements(self.DATE_INPUTS)
        assert len(inputs) >= 2, "Reservation page should have date in and date out inputs"
        return inputs

    def number_inputs(self) -> list[WebElement]:
        inputs = self.visible_elements(self.NUMBER_INPUTS)
        assert len(inputs) >= 2, "Reservation page should have time in and time out inputs"
        return inputs

    def fill_search_form(self, case: dict) -> None:
        date_inputs = self.date_inputs()
        time_inputs = self.number_inputs()
        self.set_input_value(date_inputs[0], case["date_in"])
        self.set_input_value(date_inputs[1], case["date_out"])
        self.set_input_value(time_inputs[0], case["time_in"])
        self.set_input_value(time_inputs[1], case["time_out"])
        vehicle = self.first_visible(self.VEHICLE_SELECT, "vehicle type select")
        self.select_by_visible_text_or_value(vehicle, case["vehicle_type"])
        self.type_text(self.PLATE_INPUT, case["plate"], "plate input")

    def search_spots(self) -> None:
        self.click(self.SEARCH_BUTTON, "search spots button")

    def spot_cards(self) -> list[WebElement]:
        return self.visible_elements(self.SPOT_CARDS)

    def select_first_spot(self) -> None:
        cards = self.spot_cards()
        assert cards, "Expected at least one available spot to select"
        cards[0].click()

    def confirm_reservation(self) -> None:
        self.click(self.CONFIRM_BUTTON, "confirm reservation button")

    def wait_for_search_success_or_spots(self) -> None:
        def success_or_spots(driver):
            if self.spot_cards():
                return True
            text = self.page_text().lower()
            return "slot found" in text or "available" in text or "thành công" in text

        self.wait.until(success_or_spots)

    def wait_for_search_error_or_no_spots(self) -> None:
        def error_or_no_spots(driver):
            text = self.page_text().lower()
            return any(
                token in text
                for token in ["please fill", "no slot", "invalid", "error", "không", "lỗi"]
            )

        self.wait.until(error_or_no_spots)

    def wait_for_reserve_success(self) -> None:
        self.first_visible(self.PAYMENT_CREATED_PANEL, "reservation created/payment panel")

    def wait_for_reserve_error(self) -> None:
        self.first_visible(self.ERROR_MESSAGE, "reserve error message")
