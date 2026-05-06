"""
Login Page Object Model
Handles customer and staff login pages
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    """Page Object for Customer Login"""

    # Locators
    USERNAME_INPUT = (By.ID, "phone")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Đăng nhập')]")
    STAFF_LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Đăng nhập cho nhân viên')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "text-red-600")
    
    def __init__(self, driver):
        """Initialize the login page"""
        super().__init__(driver)
        
    def navigate_to_customer_login(self):
        """Navigate to customer login page"""
        self.navigate_to(f"{BASE_URL}/auth/login")
        
    def navigate_to_staff_login(self):
        """Navigate to staff login page"""
        self.navigate_to(f"{BASE_URL}/staff/auth/login")

    def login_customer(self, username, password):
        """
        Perform customer login
        
        Args:
            username (str): Customer username/phone
            password (str): Customer password
        """
        self.fill_input(self.USERNAME_INPUT, username)
        self.fill_input(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        """
        Get error message if login fails
        
        Returns:
            str: Error message text or None
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        return None

    def is_login_successful(self, expected_url):
        """
        Check if login was successful by verifying URL
        
        Args:
            expected_url (str): Expected URL after successful login
            
        Returns:
            bool: True if redirected to expected URL
        """
        try:
            self.wait_for_url(expected_url)
            return True
        except:
            return False


class StaffLoginPage(BasePage):
    """Page Object for Staff/Admin Login"""

    # Locators for staff login (no explicit IDs, using CSS selectors)
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Tên đăng nhập']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Mật khẩu']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Đăng nhập')]")
    CUSTOMER_LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Quay lại đăng nhập Khách hàng')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "text-red-600")
    
    def __init__(self, driver):
        """Initialize the staff login page"""
        super().__init__(driver)
        
    def navigate_to_staff_login(self):
        """Navigate to staff login page"""
        self.navigate_to(f"{BASE_URL}/staff/auth/login")

    def login_staff(self, username, password):
        """
        Perform staff/admin login
        
        Args:
            username (str): Staff/Admin username
            password (str): Staff/Admin password
        """
        self.fill_input(self.USERNAME_INPUT, username)
        self.fill_input(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        """
        Get error message if login fails
        
        Returns:
            str: Error message text or None
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        return None

    def is_login_successful(self, expected_url):
        """
        Check if login was successful by verifying URL
        
        Args:
            expected_url (str): Expected URL after successful login
            
        Returns:
            bool: True if redirected to expected URL
        """
        try:
            self.wait_for_url(expected_url, timeout=15)
            return True
        except:
            return False
