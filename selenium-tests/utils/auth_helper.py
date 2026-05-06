"""
Authentication Helper
Reuses existing UI login flow and extracts auth token from browser storage
"""
from pages.login_page import StaffLoginPage
from utils.config import STAFF_USERNAME, STAFF_PASSWORD


class StaffAuthHelper:
    """Helper for staff UI login and token extraction"""
    
    def __init__(self, driver):
        """
        Initialize auth helper
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.token = None
    
    def login_and_get_token(self, username: str = STAFF_USERNAME, password: str = STAFF_PASSWORD) -> str:
        """
        Perform UI login and extract auth token from browser storage
        
        Args:
            username: Staff username
            password: Staff password
            
        Returns:
            str: Auth token if found, None otherwise
        """
        try:
            # Use existing UI login flow
            login_page = StaffLoginPage(self.driver)
            login_page.navigate_to_staff_login()
            
            print(f"[DEBUG] Navigated to staff login page")
            
            # Perform login
            login_page.login_staff(username, password)
            
            print(f"[DEBUG] Submitted login form")
            
            # Wait for successful login redirect
            if not login_page.is_login_successful("staff/dashboard"):
                print(f"[ERROR] Login redirect failed - not at staff/dashboard")
                return None
            
            print(f"[DEBUG] Login successful - at staff/dashboard")
            
            # Extract token from browser storage
            token = self._extract_token_from_storage()
            
            if token:
                self.token = token
                print(f"[DEBUG] Token extracted: key found in browser storage")
                return token
            else:
                print(f"[ERROR] Token not found in browser storage after successful login")
                return None
                
        except Exception as e:
            print(f"[ERROR] Login/token extraction failed: {e}")
            return None
    
    def _extract_token_from_storage(self) -> str:
        """
        Extract auth token from browser localStorage or sessionStorage
        
        Returns:
            str: Auth token if found, None otherwise
        """
        # Common token key names to check (in order of likelihood)
        token_keys = [
            "staff_access_token",
            "accessToken",
            "access_token",
            "token",
            "staffToken",
            "authToken",
            "jwt",
            "auth_token",
        ]
        
        try:
            # Check localStorage
            for key in token_keys:
                try:
                    token = self.driver.execute_script(f"return localStorage.getItem('{key}');")
                    if token:
                        print(f"[DEBUG] Found token in localStorage.{key}")
                        return token
                except:
                    pass
            
            # Check sessionStorage
            for key in token_keys:
                try:
                    token = self.driver.execute_script(f"return sessionStorage.getItem('{key}');")
                    if token:
                        print(f"[DEBUG] Found token in sessionStorage.{key}")
                        return token
                except:
                    pass
            
            # Debug: list all keys in storage
            print(f"[DEBUG] Token not found. Checking available storage keys...")
            try:
                ls_keys = self.driver.execute_script(
                    "return Object.keys(localStorage);"
                )
                print(f"[DEBUG] localStorage keys: {ls_keys}")
            except:
                pass
            
            try:
                ss_keys = self.driver.execute_script(
                    "return Object.keys(sessionStorage);"
                )
                print(f"[DEBUG] sessionStorage keys: {ss_keys}")
            except:
                pass
            
            return None
            
        except Exception as e:
            print(f"[ERROR] Error extracting token: {e}")
            return None
    
    def get_token(self) -> str:
        """Get the cached token"""
        return self.token
