"""
Pytest configuration and fixtures
Provides reusable fixtures for all tests
"""
import pytest
from utils.driver_factory import DriverFactory
from utils.screenshot_helper import ScreenshotHelper


@pytest.fixture(scope="function")
def driver():
    """
    Fixture that provides a WebDriver instance for each test
    
    Yields:
        webdriver.Chrome: The WebDriver instance
    """
    driver = DriverFactory.create_driver()
    yield driver
    
    # Cleanup after test
    DriverFactory.close_driver(driver)


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(driver, request):
    """
    Automatically take a screenshot if a test fails
    
    Args:
        driver: The WebDriver fixture
        request: The test request
    """
    yield
    
    # Take screenshot if test failed
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        test_name = request.node.name
        ScreenshotHelper.take_screenshot_on_failure(driver, test_name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to make test result available to fixtures
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
