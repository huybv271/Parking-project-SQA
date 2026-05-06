"""
Configuration module for Selenium tests
Loads environment variables and default settings
"""
import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Base URL for the application (frontend)
BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")

# Base URL for the backend API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")

# Staff/Admin credentials
STAFF_USERNAME = os.getenv("STAFF_USERNAME", "staff2")
STAFF_PASSWORD = os.getenv("STAFF_PASSWORD", "123456")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "123456")

# Customer credentials
CUSTOMER_USERNAME = os.getenv("CUSTOMER_USERNAME", "0987654321")
CUSTOMER_PASSWORD = os.getenv("CUSTOMER_PASSWORD", "123456abcd")

# Browser settings
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))

# Timeouts (in seconds)
DEFAULT_WAIT = int(os.getenv("DEFAULT_WAIT", "10"))
PAGE_LOAD_WAIT = int(os.getenv("PAGE_LOAD_WAIT", "30"))

# Screenshot settings
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

# PlateRecognizer API (optional for automated tests)
PLATE_RECOGNIZER_API_KEY = os.getenv("PLATE_RECOGNIZER_API_KEY", "")

# Test data
TEST_PLATE_MOTORBIKE = os.getenv("TEST_PLATE_MOTORBIKE", "59D2420.69")
TEST_PLATE_CAR = os.getenv("TEST_PLATE_CAR", "30F78777")
TEST_PLATE_GOVERNMENT = os.getenv("TEST_PLATE_GOVERNMENT", "65B1-99999")
TEST_PLATE_RED = os.getenv("TEST_PLATE_RED", "KC-88-88")
