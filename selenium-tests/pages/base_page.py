"""
Base Page Object Model
Provides common functionality for all page objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.config import DEFAULT_WAIT
from utils.screenshot_helper import ScreenshotHelper


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        """
        Initialize the base page
        
        Args:
            driver (webdriver.Chrome): The WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT)

    def wait_for_element(self, locator, timeout=None):
        """
        Wait for an element to be present
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
            timeout (int): Timeout in seconds, defaults to DEFAULT_WAIT
            
        Returns:
            WebElement: The found element
        """
        if timeout is None:
            timeout = DEFAULT_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for an element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
            timeout (int): Timeout in seconds
            
        Returns:
            WebElement: The found element
        """
        if timeout is None:
            timeout = DEFAULT_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def find_element(self, locator):
        """
        Find a single element
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
            
        Returns:
            WebElement: The found element
        """
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            return None

    def find_elements(self, locator):
        """
        Find multiple elements
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
            
        Returns:
            list: List of found elements
        """
        return self.driver.find_elements(*locator)

    def click_element(self, locator):
        """
        Click an element after waiting for it to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
        """
        element = self.wait_for_element_clickable(locator)
        element.click()

    def fill_input(self, locator, text):
        """
        Fill an input field with text
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
            text (str): Text to fill
        """
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """
        Get text from an element
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
            
        Returns:
            str: The element's text
        """
        element = self.wait_for_element(locator)
        return element.text

    def is_element_visible(self, locator, timeout=5):
        """
        Check if an element is visible
        
        Args:
            locator (tuple): Locator tuple (By.XXX, value)
            timeout (int): Timeout in seconds
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url(self, partial_url, timeout=None):
        """
        Wait for the URL to contain a specific string
        
        Args:
            partial_url (str): Partial URL to wait for
            timeout (int): Timeout in seconds
        """
        if timeout is None:
            timeout = DEFAULT_WAIT
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url)
        )

    def get_current_url(self):
        """
        Get the current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url

    def navigate_to(self, url):
        """
        Navigate to a URL
        
        Args:
            url (str): URL to navigate to
        """
        self.driver.get(url)

    def screenshot(self, name):
        """
        Take a screenshot
        
        Args:
            name (str): Name for the screenshot
        """
        ScreenshotHelper.take_screenshot(self.driver, name)
