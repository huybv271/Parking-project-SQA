"""
Authentication Tests
Tests for staff/admin and customer login functionality
"""
import pytest
from pages.login_page import StaffLoginPage, LoginPage
from utils.config import (
    STAFF_USERNAME, STAFF_PASSWORD, 
    CUSTOMER_USERNAME, CUSTOMER_PASSWORD,
    BASE_URL
)


class TestStaffLogin:
    """Test cases for staff/admin login"""
    
    def test_staff_login_valid_credentials(self, driver):
        """
        TC_ID: AUTH_STAFF_01
        Test staff login with valid credentials
        Expected: User redirected to staff dashboard
        """
        login_page = StaffLoginPage(driver)
        login_page.navigate_to_staff_login()
        
        # Perform login
        login_page.login_staff(STAFF_USERNAME, STAFF_PASSWORD)
        
        # Verify successful login
        assert login_page.is_login_successful("staff/dashboard"), \
            "User should be redirected to staff dashboard after successful login"
        
    def test_staff_login_invalid_password(self, driver):
        """
        TC_ID: AUTH_STAFF_02
        Test staff login with invalid password
        Expected: Error message displayed, user remains on login page
        """
        login_page = StaffLoginPage(driver)
        login_page.navigate_to_staff_login()
        
        # Try login with wrong password
        login_page.login_staff(STAFF_USERNAME, "wrongpassword")
        
        # Should see error or remain on login page
        import time
        time.sleep(2)  # Wait for response
        
        current_url = login_page.get_current_url()
        assert "staff/auth/login" in current_url or "staff/dashboard" not in current_url, \
            "User should remain on login page or see error with invalid credentials"
        
    def test_staff_login_empty_fields(self, driver):
        """
        TC_ID: AUTH_STAFF_03
        Test staff login with empty credentials
        Expected: Validation error or submission prevented
        """
        login_page = StaffLoginPage(driver)
        login_page.navigate_to_staff_login()
        
        # Try to submit empty form
        login_page.click_element(StaffLoginPage.LOGIN_BUTTON)
        
        # Wait and verify user stays on login page
        import time
        time.sleep(2)
        
        current_url = login_page.get_current_url()
        assert "staff/auth/login" in current_url, \
            "User should remain on login page with empty credentials"
        

class TestCustomerLogin:
    """Test cases for customer login"""
    
    def test_customer_login_navigation(self, driver):
        """
        TC_ID: AUTH_CUSTOMER_01
        Test customer login page navigation
        Expected: Customer login page loads successfully
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_customer_login()
        
        # Verify page loaded
        assert login_page.is_element_visible(LoginPage.USERNAME_INPUT, timeout=5), \
            "Username input should be visible on customer login page"
        
    def test_customer_login_valid_flow(self, driver):
        """
        TC_ID: AUTH_CUSTOMER_02
        Test customer login with valid credentials
        Expected: User redirected to customer dashboard
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_customer_login()
        
        # Perform login
        login_page.login_customer(CUSTOMER_USERNAME, CUSTOMER_PASSWORD)
        
        # Verify successful login
        assert login_page.is_login_successful("customer/dashboard"), \
            "User should be redirected to customer dashboard after successful login"


class TestLoginPageElements:
    """Test login page UI elements"""
    
    def test_staff_login_page_elements_visible(self, driver):
        """
        TC_ID: AUTH_UI_01
        Verify staff login page has all required elements
        Expected: Username, password inputs and login button visible
        """
        login_page = StaffLoginPage(driver)
        login_page.navigate_to_staff_login()
        
        assert login_page.is_element_visible(StaffLoginPage.USERNAME_INPUT, timeout=5), \
            "Username input should be visible"
        assert login_page.is_element_visible(StaffLoginPage.PASSWORD_INPUT, timeout=5), \
            "Password input should be visible"
        assert login_page.is_element_visible(StaffLoginPage.LOGIN_BUTTON, timeout=5), \
            "Login button should be visible"
        
    def test_customer_login_page_elements_visible(self, driver):
        """
        TC_ID: AUTH_UI_02
        Verify customer login page has all required elements
        Expected: Username, password inputs and login button visible
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_customer_login()
        
        assert login_page.is_element_visible(LoginPage.USERNAME_INPUT, timeout=5), \
            "Username input should be visible"
        assert login_page.is_element_visible(LoginPage.PASSWORD_INPUT, timeout=5), \
            "Password input should be visible"
        assert login_page.is_element_visible(LoginPage.LOGIN_BUTTON, timeout=5), \
            "Login button should be visible"
