"""
API helper for direct API testing
Provides methods to call backend endpoints for check-in and check-out
"""
import requests
from typing import Optional, Dict, Any
from utils.config import API_BASE_URL, STAFF_USERNAME, STAFF_PASSWORD


def _normalize_message(response: Dict[str, Any]) -> str:
    message = response.get("message", "")
    return str(message).lower()


def is_checkout_success_response(response: Dict[str, Any]) -> bool:
    status_code = response.get("status_code")
    message = _normalize_message(response)
    return status_code == 200 and (
        message == "success"
        or "success" in message
        or response.get("bill") is not None
    )


def is_no_active_session_response(response: Dict[str, Any]) -> bool:
    status_code = response.get("status_code")
    message = _normalize_message(response)
    return status_code in {400, 404, 409, 422} or any(
        phrase in message
        for phrase in [
            "không có trong bãi",
            "không tìm thấy",
            "không tồn tại",
            "đã ra",
            "already checked out",
            "no active session",
            "not in parking lot",
            "vehicle is not in parking lot",
            "vehicle not found",
            "already out",
        ]
    )


def is_checkin_success_or_already_in_lot(response: Dict[str, Any]) -> bool:
    status_code = response.get("status_code")
    message = _normalize_message(response)
    return status_code == 200 or any(
        phrase in message
        for phrase in [
            "check-in thành công",
            "xe đang ở trong bãi",
            "already in lot",
            "already parked",
            "already exists",
        ]
    )


class StaffAPIHelper:
    """Helper class for calling staff API endpoints"""
    
    def __init__(self, api_base_url: str = API_BASE_URL):
        """
        Initialize API helper
        
        Args:
            api_base_url: Base URL of the backend API (e.g., http://localhost:8080)
        """
        self.api_base = api_base_url.rstrip('/') + "/staff"
        self.token = None
        self.session = requests.Session()
    
    def login(self, username: str = STAFF_USERNAME, password: str = STAFF_PASSWORD) -> bool:
        """
        Login to staff account and get JWT token.
        """
        try:
            login_url = f"{self.api_base}/auth/login"

            print(f"[DEBUG] Login URL: {login_url}")
            print(f"[DEBUG] Username present: {bool(username)}")
            print(f"[DEBUG] Password present: {bool(password)}")

            response = self.session.post(
                login_url,
                json={"username": username, "password": password},
                timeout=10
            )

            print(f"[DEBUG] Login status: {response.status_code}")
            print(f"[DEBUG] Login response: {response.text[:500]}")

            if response.status_code == 200:
                data = response.json()
                self.token = (
                    data.get("token")
                    or data.get("accessToken")
                    or data.get("access_token")
                    or data.get("data", {}).get("token")
                    or data.get("data", {}).get("accessToken")
                )
                print(f"[DEBUG] Token received: {bool(self.token)}")
                return bool(self.token)

            return False

        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def set_token(self, token: str):
        """
        Set auth token for API calls (e.g., from UI login)
        
        Args:
            token: JWT token from browser storage after UI login
        """
        self.token = token
        token_preview = token[:20] + "..." if len(token) > 20 else token
        print(f"[DEBUG] Token set in StaffAPIHelper: {token_preview} (length: {len(token)})")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        headers = {}
        if self.token:
            # Backend expects raw token in Authorization header (no Bearer prefix)
            headers["Authorization"] = self.token
        return headers
    
    def checkin_image(self, image_path: str, tc_id: str = None) -> Dict[str, Any]:
        """
        Send check-in image to API
        
        Args:
            image_path: Path to image file
            tc_id: Test case ID for logging
            
        Returns:
            Response data with status_code always included
        """
        if not self.token:
            raise ValueError("Not authenticated. Call login() first or use set_token()")
        
        tc_prefix = f"[{tc_id}]" if tc_id else "[API]"
        
        with open(image_path, 'rb') as f:
            files = {'image': f}
            headers = self._get_headers()
            
            print(f"{tc_prefix} POST {self.api_base}/ticket-entry")
            print(f"{tc_prefix} image path: {image_path}")
            
            response = self.session.post(
                f"{self.api_base}/ticket-entry",
                files=files,
                headers=headers
            )
            
            print(f"{tc_prefix} Response status: {response.status_code}")
            print(f"{tc_prefix} Response body: {response.text}")
            
            # Always include status_code in response
            if response.status_code == 200:
                result = response.json()
                result['status_code'] = response.status_code
                return result
            else:
                # Error response
                try:
                    result = response.json()
                    result['status_code'] = response.status_code
                    return result
                except:
                    return {"error": response.text, "status_code": response.status_code}
    
    def checkout_image(self, image_path: str, tc_id: str = None) -> Dict[str, Any]:
        """
        Send check-out image to API
        
        Args:
            image_path: Path to image file
            tc_id: Test case ID for logging
            
        Returns:
            Response data with status_code always included
        """
        if not self.token:
            raise ValueError("Not authenticated. Call login() first or use set_token()")
        
        tc_prefix = f"[{tc_id}]" if tc_id else "[API]"
        
        with open(image_path, 'rb') as f:
            files = {'image': f}
            headers = self._get_headers()
            
            print(f"{tc_prefix} POST {self.api_base}/free-endtry")
            print(f"{tc_prefix} image path: {image_path}")
            
            response = self.session.post(
                f"{self.api_base}/free-endtry",
                files=files,
                headers=headers
            )
            
            print(f"{tc_prefix} Response status: {response.status_code}")
            print(f"{tc_prefix} Response body: {response.text}")
            
            # Always include status_code in response
            if response.status_code == 200:
                result = response.json()
                result['status_code'] = response.status_code
                return result
            else:
                # Error response
                try:
                    result = response.json()
                    result['status_code'] = response.status_code
                    return result
                except:
                    return {"error": response.text, "status_code": response.status_code}
    
    def get_lot_status(self, tc_id: str = None) -> Dict[str, Any]:
        """
        Get current parking lot status (capacity, available spots, etc.)
        
        Args:
            tc_id: Test case ID for logging
            
        Returns:
            Lot status data with availableSpots and totalSpots
        """
        if not self.token:
            raise ValueError("Not authenticated. Call login() first or use set_token()")
        
        tc_prefix = f"[{tc_id}]" if tc_id else "[API]"
        
        try:
            headers = self._get_headers()
            
            # Try multiple possible endpoints for lot status
            endpoints = [
                f"{self.api_base}/status",
                f"{self.api_base}/lot-status",
                f"{self.api_base}/parking-status",
                f"{self.api_base}/dashboard/status",
            ]
            
            for endpoint in endpoints:
                try:
                    print(f"{tc_prefix} GET {endpoint}")
                    response = self.session.get(endpoint, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"{tc_prefix} Lot status: {result}")
                        
                        # Extract lot capacity info
                        return {
                            "availableSpots": result.get("availableSpots") or result.get("available_spots") or 0,
                            "totalSpots": result.get("totalSpots") or result.get("total_spots") or result.get("capacity") or 1,
                            "status_code": response.status_code,
                            "raw": result
                        }
                except requests.exceptions.RequestException:
                    continue
            
            # If no endpoint succeeded, assume lot has availability (conservative default)
            print(f"{tc_prefix} Could not get lot status from any endpoint, assuming available")
            return {
                "availableSpots": 1,
                "totalSpots": 1,
                "status_code": 503,
                "error": "Lot status endpoint unreachable"
            }
            
        except Exception as e:
            print(f"{tc_prefix} Error getting lot status: {e}")
            return {
                "availableSpots": 1,
                "totalSpots": 1,
                "status_code": 500,
                "error": str(e)
            }
    
    def close(self):
        """Close session"""
        self.session.close()
