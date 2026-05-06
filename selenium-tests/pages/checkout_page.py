"""
Check-out Page Object Model
Handles the check-out page with camera
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class CheckoutPage(BasePage):
    """
    Page Object for Check-out Page (/staff/(dashboard)/ticket/checkout)
    
    NOTE: This page uses camera stream and requires physical camera access
    or mocked camera for Selenium automation. Most test cases using this page
    will be skipped unless a test mode is available.
    """

    # Locators
    VIDEO_ELEMENT = (By.TAG_NAME, "video")
    SCAN_BUTTON = (By.XPATH, "//button[contains(text(), 'Quét & Checkout')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'Quay lại')]")
    SUCCESS_MESSAGE = (By.XPATH, "//h3[contains(text(), 'Checkout thành công')]")
    PLATE_TEXT = (By.XPATH, "//*[contains(text(), 'Biển số:')]")
    START_TIME = (By.XPATH, "//*[contains(text(), 'Bắt đầu:')]")
    FINISH_TIME = (By.XPATH, "//*[contains(text(), 'Kết thúc:')]")
    PAID_MONEY = (By.XPATH, "//*[contains(text(), 'Đã thanh toán online:')]")
    TOTAL_PRICE = (By.XPATH, "//*[contains(text(), 'Phí cần trả thêm:')]")
    CHECKIN_IMAGE = (By.XPATH, "//img[@alt='Check-in']")
    CHECKOUT_IMAGE = (By.XPATH, "//img[@alt='Check-out']")
    ERROR_MESSAGE = (By.CLASS_NAME, "text-red-600")
    
    def __init__(self, driver):
        """Initialize the check-out page"""
        super().__init__(driver)
        
    def navigate_to_checkout(self):
        """Navigate to check-out page"""
        self.navigate_to(f"{BASE_URL}/staff/dashboard/ticket/checkout")

    def is_camera_visible(self):
        """
        Check if camera video element is visible
        
        Returns:
            bool: True if camera is visible
        """
        return self.is_element_visible(self.VIDEO_ELEMENT, timeout=5)

    def click_scan_button(self):
        """
        Click the scan/checkout button
        
        NOTE: This will try to capture a frame from the camera stream
        """
        self.click_element(self.SCAN_BUTTON)

    def click_back_button(self):
        """Click the back button"""
        self.click_element(self.BACK_BUTTON)

    def is_success_message_visible(self):
        """
        Check if success message is displayed
        
        Returns:
            bool: True if success message is visible
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=10)

    def get_recognized_plate(self):
        """
        Get the recognized plate number from success message
        
        Returns:
            str: Plate number or None if not found
        """
        try:
            element = self.wait_for_element(self.PLATE_TEXT, timeout=5)
            text = element.text
            # Extract plate from "Biển số: XXXXX" format
            if ":" in text:
                return text.split(":")[-1].strip()
            return text
        except:
            return None

    def get_start_time(self):
        """
        Get the check-in start time
        
        Returns:
            str: Start time or None
        """
        try:
            element = self.wait_for_element(self.START_TIME, timeout=5)
            text = element.text
            if ":" in text:
                return text.split(":", 1)[-1].strip()
            return text
        except:
            return None

    def get_finish_time(self):
        """
        Get the check-out finish time
        
        Returns:
            str: Finish time or None
        """
        try:
            element = self.wait_for_element(self.FINISH_TIME, timeout=5)
            text = element.text
            if ":" in text:
                return text.split(":", 1)[-1].strip()
            return text
        except:
            return None

    def get_paid_money(self):
        """
        Get the amount already paid online
        
        Returns:
            str: Paid amount or None
        """
        try:
            element = self.wait_for_element(self.PAID_MONEY, timeout=5)
            text = element.text
            if ":" in text:
                return text.split(":")[-1].strip()
            return text
        except:
            return None

    def get_total_price(self):
        """
        Get the remaining fee to pay
        
        Returns:
            str: Total price or None
        """
        try:
            element = self.wait_for_element(self.TOTAL_PRICE, timeout=5)
            text = element.text
            if ":" in text:
                return text.split(":")[-1].strip()
            return text
        except:
            return None

    def are_images_visible(self):
        """
        Check if both check-in and check-out images are visible
        
        Returns:
            bool: True if both images are visible
        """
        return (
            self.is_element_visible(self.CHECKIN_IMAGE, timeout=5) and
            self.is_element_visible(self.CHECKOUT_IMAGE, timeout=5)
        )

    def get_error_message(self):
        """
        Get error message if check-out fails
        
        Returns:
            str: Error message text or None
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        return None

    # ===== API-BASED TESTING HELPERS (for image-based tests) =====
    
    def is_page_loaded(self):
        """
        Check if check-out page is loaded (camera or title visible)
        
        Returns:
            bool: True if page loaded
        """
        try:
            # Check if page has loaded by looking for main heading
            heading = self.driver.find_elements(By.XPATH, "//h1[contains(text(), 'Check-out')]")
            return len(heading) > 0
        except:
            return False
