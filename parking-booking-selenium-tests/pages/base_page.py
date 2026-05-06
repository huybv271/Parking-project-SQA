from typing import Iterable, Sequence, Tuple

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from utils.config import Config

Locator = Tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver, config: Config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config.timeout)

    def open_url(self, path: str) -> None:
        # Ghep base_url trong .env voi path cua tung man hinh can test.
        self.driver.get(self.config.url(path))

    def first_visible(self, locators: Sequence[Locator], name: str) -> WebElement:
        # Thu lan luot nhieu selector fallback de de doi selector khi UI thay doi.
        last_error = None
        for locator in locators:
            try:
                # Explicit wait: doi element hien thi, khong dung sleep cung.
                return self.wait.until(EC.visibility_of_element_located(locator))
            except TimeoutException as exc:
                # Luu loi cuoi cung de message fail co thong tin huu ich.
                last_error = exc
        raise TimeoutException(f"Could not find visible {name}. Tried: {locators}") from last_error

    def first_clickable(self, locators: Sequence[Locator], name: str) -> WebElement:
        # Thu lan luot nhieu selector fallback de tim element co the click.
        last_error = None
        for locator in locators:
            try:
                # Explicit wait: doi element clickable truoc khi click.
                return self.wait.until(EC.element_to_be_clickable(locator))
            except TimeoutException as exc:
                # Luu loi cuoi cung de debug selector nhanh hon.
                last_error = exc
        raise TimeoutException(f"Could not find clickable {name}. Tried: {locators}") from last_error

    def visible_elements(self, locator: Locator) -> list[WebElement]:
        # Lay danh sach element theo selector, sau do chi giu element dang hien thi.
        visible = []
        for element in self.driver.find_elements(*locator):
            try:
                # is_displayed co the nem stale neu React vua render lai DOM.
                if element.is_displayed():
                    visible.append(element)
            except StaleElementReferenceException:
                # Bo qua element cu va de lan wait tiep theo doc DOM moi.
                continue
        return visible

    def click(self, locators: Sequence[Locator], name: str) -> None:
        # Tim element clickable dau tien roi click.
        self.first_clickable(locators, name).click()

    def type_text(self, locators: Sequence[Locator], value: str, name: str) -> None:
        # Tim input dang hien thi.
        element = self.first_visible(locators, name)
        # Clear gia tri cu truoc khi nhap test data moi.
        element.clear()
        # Nhap text bang send_keys cho cac input binh thuong.
        element.send_keys(value)

    def set_input_value(self, element: WebElement, value: str | int) -> None:
        # Dung native setter de React/Next.js nhan dung thay doi value.
        self.driver.execute_script(
            """
            const element = arguments[0];
            const value = String(arguments[1]);
            const nativeSetter = Object.getOwnPropertyDescriptor(
              window.HTMLInputElement.prototype,
              'value'
            ).set;
            nativeSetter.call(element, value);
            element.dispatchEvent(new Event('input', { bubbles: true }));
            element.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value,
        )

    def select_by_visible_text_or_value(self, element: WebElement, value: str) -> None:
        # Selenium Select chi dung cho the select HTML native.
        select = Select(element)
        try:
            # Uu tien chon option theo text hien thi.
            select.select_by_visible_text(value)
        except Exception:
            # Neu text khong khop, fallback sang value attribute.
            select.select_by_value(value)

    def wait_for_any_text(self, expected_texts: Iterable[str]) -> str:
        # Chuyen expected text ve lowercase de so sanh khong phan biet hoa/thuong.
        expected = [text.lower() for text in expected_texts]

        def page_has_text(driver: WebDriver):
            # Lay toan bo body text hien tai.
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            # Tra ve text dau tien match; neu chua match thi False de WebDriverWait tiep tuc doi.
            return next((text for text in expected if text in body_text), False)

        return self.wait.until(page_has_text)

    def page_text(self) -> str:
        # Helper lay text cua body, dung cho assert message va wait loading.
        return self.driver.find_element(By.TAG_NAME, "body").text
