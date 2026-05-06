from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator


class AdminLoginPage(BasePage):
    """Admin/staff login page object.

    TODO selectors to update after inspecting UI:
    - Prefer data-testid="admin-login-username", data-testid="admin-login-password",
      data-testid="admin-login-submit", data-testid="admin-dashboard".
    - Current fallback uses input type and submit button from /staff/auth/login.
    """

    USERNAME_INPUT: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='admin-login-username']"),
        (By.NAME, "username"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ]
    PASSWORD_INPUT: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='admin-login-password']"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]
    SUBMIT_BUTTON: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='admin-login-submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(., 'Đăng nhập') or contains(., 'Login')]"),
    ]
    ADMIN_AREA: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='admin-dashboard']"),
        (By.XPATH, "//*[contains(@href, '/admin/spots') or contains(., 'Dashboard') or contains(., 'Spots')]"),
        (By.XPATH, "//*[contains(., 'Quản lý Spot') or contains(., 'Spots Area') or contains(., 'Deleted Spots')]"),
    ]

    def open(self) -> None:
        self.open_url(self.config.admin_login_path)

    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME_INPUT, username, "admin username input")
        self.type_text(self.PASSWORD_INPUT, password, "admin password input")
        self.click(self.SUBMIT_BUTTON, "admin login submit button")

    def wait_until_admin_area_loaded(self) -> None:
        self.wait.until(lambda driver: "/admin" in driver.current_url)
        self.first_visible(self.ADMIN_AREA, "admin area after login")
