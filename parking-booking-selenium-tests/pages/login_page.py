from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator


class LoginPage(BasePage):
    """Customer login page object.

    TODO selectors to update after inspecting UI:
    - Prefer data-testid="login-username", data-testid="login-password", data-testid="login-submit".
    - Current fallback uses existing id="phone", id="password" and submit button text/type.
    """

    USERNAME_INPUT: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='login-username']"),
        (By.ID, "phone"),
        (By.NAME, "username"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ]
    PASSWORD_INPUT: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='login-password']"),
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]
    SUBMIT_BUTTON: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='login-submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(normalize-space(.), 'Đăng nhập') or contains(normalize-space(.), 'Login')]"),
    ]
    CUSTOMER_AREA: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='customer-dashboard']"),
        (By.XPATH, "//*[contains(@href, '/customer/reservation') or contains(normalize-space(.), 'Reservation')]"),
        (By.XPATH, "//*[contains(normalize-space(.), 'Dashboard') or contains(normalize-space(.), 'Xin chào')]"),
    ]

    def open(self) -> None:
        self.open_url(self.config.login_path)

    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME_INPUT, username, "username input")
        self.type_text(self.PASSWORD_INPUT, password, "password input")
        self.click(self.SUBMIT_BUTTON, "login submit button")

    def wait_until_customer_area_loaded(self) -> None:
        self.first_visible(self.CUSTOMER_AREA, "customer area after login")
