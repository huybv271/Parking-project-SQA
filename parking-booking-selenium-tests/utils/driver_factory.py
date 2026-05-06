from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from utils.config import Config


def create_driver(config: Config) -> webdriver.Chrome:
    if config.browser.strip().lower() != "chrome":
        raise ValueError("Only Chrome is configured. Set BROWSER=chrome.")

    options = ChromeOptions()
    if config.headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={config.window_width},{config.window_height}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(config.timeout * 2)
    driver.implicitly_wait(0)
    return driver
