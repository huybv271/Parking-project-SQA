"""
Screenshot utility module
Handles capturing screenshots on test failure or demand
"""
import os
from datetime import datetime
from utils.config import SCREENSHOT_DIR, SCREENSHOT_ON_FAILURE


class ScreenshotHelper:
    """Helper class for taking and managing screenshots"""

    @staticmethod
    def ensure_screenshot_dir():
        """Create screenshot directory if it doesn't exist"""
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)

    @staticmethod
    def take_screenshot(driver, test_name):
        """
        Take a screenshot and save it
        
        Args:
            driver (webdriver.Chrome): The WebDriver instance
            test_name (str): Name of the test (used for filename)
            
        Returns:
            str: Path to the saved screenshot file, or None if not taken
        """
        if not SCREENSHOT_ON_FAILURE:
            return None
            
        ScreenshotHelper.ensure_screenshot_dir()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        try:
            driver.save_screenshot(filepath)
            print(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None

    @staticmethod
    def take_screenshot_on_failure(driver, test_name):
        """
        Take a screenshot after a test failure
        
        Args:
            driver (webdriver.Chrome): The WebDriver instance
            test_name (str): Name of the test
            
        Returns:
            str: Path to the screenshot
        """
        return ScreenshotHelper.take_screenshot(driver, f"{test_name}_FAILURE")
