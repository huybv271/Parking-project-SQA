"""
WebDriver Factory module
Handles Chrome driver creation and management with webdriver-manager
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import HEADLESS, WINDOW_WIDTH, WINDOW_HEIGHT


class DriverFactory:
    """Factory for creating and managing WebDriver instances"""

    @staticmethod
    def create_driver():
        """
        Create and return a Chrome WebDriver instance
        
        Returns:
            webdriver.Chrome: Configured Chrome driver
        """
        # Create Chrome options
        chrome_options = Options()
        
        if HEADLESS:
            chrome_options.add_argument("--headless")
        
        # Common arguments for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Set window size
        chrome_options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
        
        # Disable notifications
        chrome_options.add_argument("--disable-notifications")
        
        # Setup service with webdriver-manager
        service = Service(ChromeDriverManager().install())
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Maximize window
        driver.maximize_window()
        
        return driver

    @staticmethod
    def close_driver(driver):
        """
        Close the WebDriver instance
        
        Args:
            driver (webdriver.Chrome): The driver to close
        """
        if driver:
            driver.quit()
