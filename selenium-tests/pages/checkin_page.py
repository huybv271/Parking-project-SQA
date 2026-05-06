"""
Check-in Page Object Model
Handles the check-in (ticket creation) page with camera
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class CheckinPage(BasePage):
    """
    Page Object for Check-in Page (/staff/(dashboard)/ticket/create)
    
    NOTE: This page uses camera stream and requires physical camera access
    or mocked camera for Selenium automation. Most test cases using this page
    will be skipped unless a test mode is available.
    """

    # Locators
    VIDEO_ELEMENT = (By.TAG_NAME, "video")
    SCAN_BUTTON = (By.XPATH, "//button[contains(text(), 'Quét biển số')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'Quay lại')]")
    SUCCESS_MESSAGE = (By.XPATH, "//h3[contains(text(), 'Tạo vé thành công')]")
    PLATE_TEXT = (By.XPATH, "//*[contains(text(), 'Biển số:')]")
    VEHICLE_TYPE = (By.XPATH, "//*[contains(text(), 'Loại xe:')]")
    AREA_TEXT = (By.XPATH, "//*[contains(text(), 'Khu vực:')]")
    POSITION_TEXT = (By.XPATH, "//*[contains(text(), 'Vị trí:')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "text-red-600")
    
    def __init__(self, driver):
        """Initialize the check-in page"""
        super().__init__(driver)
        
    def navigate_to_checkin(self):
        """Navigate to check-in page"""
        self.navigate_to(f"{BASE_URL}/staff/dashboard/ticket/create")

    def is_camera_visible(self):
        """
        Check if camera video element is visible
        
        Returns:
            bool: True if camera is visible
        """
        return self.is_element_visible(self.VIDEO_ELEMENT, timeout=5)

    def click_scan_button(self):
        """
        Click the scan/capture button
        
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

    def get_vehicle_type(self):
        """
        Get the detected vehicle type
        
        Returns:
            str: Vehicle type or None
        """
        try:
            element = self.wait_for_element(self.VEHICLE_TYPE, timeout=5)
            text = element.text
            if ":" in text:
                return text.split(":")[-1].strip()
            return text
        except:
            return None

    def get_area(self):
        """
        Get the parking area
        
        Returns:
            str: Area or None
        """
        try:
            element = self.wait_for_element(self.AREA_TEXT, timeout=5)
            text = element.text
            if ":" in text:
                return text.split(":")[-1].strip()
            return text
        except:
            return None

    def get_position(self):
        """
        Get the parking position/spot
        
        Returns:
            str: Position or None
        """
        try:
            element = self.wait_for_element(self.POSITION_TEXT, timeout=5)
            text = element.text
            if ":" in text:
                return text.split(":")[-1].strip()
            return text
        except:
            return None

    def get_error_message(self):
        """
        Get error message if check-in fails
        
        Returns:
            str: Error message text or None
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        return None

    # ===== API-BASED TESTING HELPERS (for image-based tests) =====
    
    def is_page_loaded(self):
        """
        Check if check-in page is loaded (camera or title visible)
        
        Returns:
            bool: True if page loaded
        """
        try:
            # Check if page has loaded by looking for main heading
            heading = self.driver.find_elements(By.XPATH, "//h1[contains(text(), 'Check-in')]")
            return len(heading) > 0
        except:
            return False
