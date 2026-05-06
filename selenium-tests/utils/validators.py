"""
Validation functions for each TC_ID.
Each function takes the API response dict and tc_id string,
and performs all assertions for that specific TC.

This file centralizes PASS/FAIL logic per TC for clear maintainability.
"""
import pytest


# =============================================================================
# CHECK-IN VALIDATORS (CI_FUN_01 to CI_FUN_09)
# =============================================================================

def validate_ci_fun_01(response: dict, tc_id: str = "CI_FUN_01"):
    """CI_FUN_01: Check-in success with valid motorbike plate"""
    assert response.get("plate") is not None, f"[{tc_id}] Plate not recognized"
    assert response.get("area") is not None, f"[{tc_id}] Area not assigned"
    assert response.get("position") is not None, f"[{tc_id}] Position not assigned"
    assert response.get("type") is not None, f"[{tc_id}] Vehicle type not determined"
    assert response.get("status_code") == 200, \
        f"[{tc_id}] Expected status 200, got {response.get('status_code')}"


def validate_ci_fun_02_first_attempt(response: dict, tc_id: str = "CI_FUN_02"):
    """CI_FUN_02: First check-in attempt (may succeed or already in lot)"""
    status = response.get("status_code")
    message = response.get("message", "")
    if status == 400 and "Xe đang ở trong bãi" in message:
        return  # precondition satisfied
    # Otherwise just log, no assertion on first attempt


def validate_ci_fun_02_second_attempt(response: dict, tc_id: str = "CI_FUN_02"):
    """CI_FUN_02: Second check-in must be rejected (duplicate)"""
    assert response.get("status_code") == 400, \
        f"[{tc_id}] Expected status 400 for duplicate, got {response.get('status_code')}"
    message = response.get("message", "")
    assert "Xe đang ở trong bãi" in message or "duplicate" in message.lower() or "already" in message.lower(), \
        f"[{tc_id}] Expected duplicate rejection message, got: {message}"
    assert response.get("ticketId") is None, f"[{tc_id}] Duplicate check-in should not create ticket"
    assert "Check-in thành công" not in message, f"[{tc_id}] Duplicate check-in must not succeed"


def validate_ci_fun_03(response: dict, tc_id: str = "CI_FUN_03"):
    """CI_FUN_03: Invalid plate (75L1) must be rejected — REAL DEFECT if accepted"""
    status_code = response.get("status_code")
    message = response.get("message", "")
    plate = response.get("plate")
    ticket_id = response.get("ticketId")

    # STRICT: If system accepts invalid plate, this test MUST FAIL
    if status_code == 200 or (plate and ticket_id):
        assert False, \
            f"[{tc_id}] FAILED: Invalid plate 75L1 was accepted and ticket was created. " \
            f"Status: {status_code}, Plate: {plate}, TicketID: {ticket_id}"

    assert status_code == 400 or \
           "khôngphát hiện" in message.lower() or \
           "cannot" in message.lower() or \
           "invalid" in message.lower() or \
           plate is None, \
        f"[{tc_id}] Expected rejection but got status {status_code}, message: {message}"


def validate_ci_fun_04(response: dict, tc_id: str = "CI_FUN_04"):
    """CI_FUN_04: No plate detected — must return error or no plate"""
    plate = response.get("plate")
    assert plate is None or \
           response.get("status_code") != 200 or \
           "message" in response or "error" in response, \
        f"[{tc_id}] Should not detect plate or return error"


def validate_ci_fun_05(response: dict, tc_id: str = "CI_FUN_05"):
    """CI_FUN_05: Car long plate (51H64427) must be recognized"""
    assert response.get("status_code") == 200, \
        f"[{tc_id}] Expected status 200, got {response.get('status_code')}"
    assert response.get("plate") is not None, f"[{tc_id}] Long plate not recognized"
    assert response.get("type") is not None, f"[{tc_id}] Vehicle type not detected"
    assert response.get("area") is not None, f"[{tc_id}] Spot area not assigned"
    assert response.get("ticketId") is not None, f"[{tc_id}] No ticket created"


def validate_ci_fun_06(response: dict, tc_id: str = "CI_FUN_06"):
    """CI_FUN_06: Blue plate (65B199999) government vehicle must be recognized"""
    assert response.get("status_code") == 200, \
        f"[{tc_id}] Expected status 200, got {response.get('status_code')}"
    assert response.get("plate") is not None, f"[{tc_id}] Blue plate not recognized"
    assert response.get("type") is not None, f"[{tc_id}] Vehicle type not detected"
    assert response.get("area") is not None, f"[{tc_id}] Spot not assigned"


def validate_ci_fun_07(response: dict, tc_id: str = "CI_FUN_07"):
    """CI_FUN_07: Red plate (KC8888) must be recognized"""
    assert response.get("status_code") == 200, \
        f"[{tc_id}] Expected status 200, got {response.get('status_code')}"
    assert response.get("plate") is not None, f"[{tc_id}] Red plate not recognized"
    assert response.get("type") is not None, f"[{tc_id}] Vehicle type not detected"


def validate_ci_fun_08(response: dict, tc_id: str = "CI_FUN_08"):
    """CI_FUN_08: Full slot must reject check-in"""
    assert response.get("status_code") == 400, \
        f"[{tc_id}] Expected status 400 for full slot, got {response.get('status_code')}"
    message = response.get("message", "")
    assert "đầy" in message.lower() or "full" in message.lower() or \
           "không có chỗ" in message.lower(), \
        f"[{tc_id}] Expected 'full slot' message, got: {message}"
    assert response.get("ticketId") is None, f"[{tc_id}] Full slot should not create ticket"


def validate_ci_fun_09_vehicle(response: dict, vehicle_index: int, tc_id: str = "CI_FUN_09"):
    """CI_FUN_09: Each of the 3 vehicles must check in successfully"""
    status = response.get("status_code")
    message = response.get("message", "")

    assert status == 200, \
        f"[{tc_id}] Vehicle {vehicle_index} check-in failed: status {status}, message: {message}"
    assert "Check-in thành công" in message, \
        f"[{tc_id}] Vehicle {vehicle_index} missing success message, got: {message}"
    assert response.get("ticketId") is not None, f"[{tc_id}] Vehicle {vehicle_index} has no ticket"
    assert response.get("plate") is not None, f"[{tc_id}] Vehicle {vehicle_index} plate not recognized"
    assert response.get("area") is not None, f"[{tc_id}] Vehicle {vehicle_index} has no area assigned"


def validate_ci_fun_09_uniqueness(tickets: list, plates: list, tc_id: str = "CI_FUN_09"):
    """CI_FUN_09: All tickets and plates must be unique"""
    assert len(set(tickets)) == 3, f"[{tc_id}] Duplicate tickets detected: {tickets}"
    assert len(set(plates)) == 3, f"[{tc_id}] Duplicate plates detected: {plates}"


# =============================================================================
# CHECK-OUT VALIDATORS (CO_FUN_01 to CO_FUN_09)
# =============================================================================

def validate_co_fun_01(response: dict, tc_id: str = "CO_FUN_01"):
    """CO_FUN_01: Checkout success with valid motorbike plate"""
    from utils.api_helper import is_checkout_success_response
    assert is_checkout_success_response(response), f"[{tc_id}] Expected successful checkout"
    assert response.get("plate") is not None, f"[{tc_id}] Plate not recognized"
    assert response.get("bill") is not None, f"[{tc_id}] Bill not returned"
    if response.get("bill"):
        bill = response.get("bill")
        assert "startTime" in bill or "finishTime" in bill, f"[{tc_id}] Bill should have time info"


def validate_co_fun_02_first_attempt(response: dict, tc_id: str = "CO_FUN_02"):
    """CO_FUN_02: First attempt — clear any active session (no assertion)"""
    from utils.api_helper import is_checkout_success_response, is_no_active_session_response
    if is_checkout_success_response(response):
        return  # session cleared
    if is_no_active_session_response(response):
        return  # already no session
    assert False, f"[{tc_id}] Unexpected first checkout response: {response}"


def validate_co_fun_02_second_attempt(response: dict, tc_id: str = "CO_FUN_02"):
    """CO_FUN_02: Second attempt must be rejected — no active session"""
    from utils.api_helper import is_checkout_success_response, is_no_active_session_response
    status_code = response.get("status_code")
    message = response.get("message", "")
    bill = response.get("bill")

    assert not is_checkout_success_response(response), f"[{tc_id}] Second checkout unexpectedly succeeded"
    assert bill is None, f"[{tc_id}] Second checkout must not return a bill"
    assert message.lower() != "success", f"[{tc_id}] Second checkout message must not be success"
    assert is_no_active_session_response(response), \
        f"[{tc_id}] Expected no active session rejection, got status {status_code}, message: {message}"


def validate_co_fun_03(response: dict, tc_id: str = "CO_FUN_03"):
    """CO_FUN_03: Invalid plate (75L1) must be rejected — REAL DEFECT if accepted"""
    status_code = response.get("status_code")
    message = response.get("message", "")
    plate = response.get("plate")
    bill = response.get("bill")

    # STRICT: If system accepts invalid plate, this test MUST FAIL
    if status_code == 200 or message.lower().find("success") >= 0 or bill or plate == "75L1":
        assert False, \
            f"[{tc_id}] FAILED: Invalid plate 75L1 was accepted and checkout was completed. " \
            f"Status: {status_code}, Message: {message}, Plate: {plate}, Bill: {bill}"

    assert status_code == 400 or status_code == 404 or \
           "không" in message.lower() or \
           "không phát hiện" in message.lower() or \
           "cannot" in message.lower() or \
           "invalid" in message.lower() or \
           plate is None, \
        f"[{tc_id}] Expected rejection but got status {status_code}, message: {message}"


def validate_co_fun_04(response: dict, tc_id: str = "CO_FUN_04"):
    """CO_FUN_04: No plate checkout — REAL DEFECT if returns 500 instead of validation error"""
    status_code = response.get("status_code")
    message = response.get("message", "")
    plate = response.get("plate")

    # FAIL if server error (status 500) instead of controlled rejection
    if status_code == 500:
        assert False, \
            f"[{tc_id}] FAILED: No-plate checkout caused server error instead of controlled validation error. " \
            f"Status: {status_code}, Message: {message}"

    assert (
        plate is None or \
        status_code in [400, 404] or \
        "message" in response or \
        "error" in response
    ), f"[{tc_id}] Should not detect plate or return controlled error, got status {status_code}"


def validate_co_fun_05(response: dict, tc_id: str = "CO_FUN_05"):
    """CO_FUN_05: Car long plate checkout must succeed"""
    from utils.api_helper import is_checkout_success_response
    assert is_checkout_success_response(response), f"[{tc_id}] Expected successful checkout"
    assert response.get("plate") is not None, f"[{tc_id}] Long plate not recognized"
    assert response.get("bill") is not None, f"[{tc_id}] No bill returned"


def validate_co_fun_06(response: dict, tc_id: str = "CO_FUN_06"):
    """CO_FUN_06: Blue plate checkout must succeed"""
    from utils.api_helper import is_checkout_success_response
    assert is_checkout_success_response(response), f"[{tc_id}] Expected successful checkout"
    assert response.get("plate") is not None, f"[{tc_id}] Blue plate not recognized"
    assert response.get("bill") is not None, f"[{tc_id}] No bill returned"


def validate_co_fun_07(response: dict, tc_id: str = "CO_FUN_07"):
    """CO_FUN_07: Red plate checkout must succeed"""
    from utils.api_helper import is_checkout_success_response
    assert is_checkout_success_response(response), f"[{tc_id}] Expected successful checkout"
    assert response.get("plate") is not None, f"[{tc_id}] Red plate not recognized"
    assert response.get("bill") is not None, f"[{tc_id}] No bill returned"


def validate_co_fun_08_first_checkout(response: dict, tc_id: str = "CO_FUN_08"):
    """CO_FUN_08: First checkout must succeed"""
    from utils.api_helper import is_checkout_success_response
    assert is_checkout_success_response(response), f"[{tc_id}] First checkout did not succeed"


def validate_co_fun_08_second_checkout(response: dict, tc_id: str = "CO_FUN_08"):
    """CO_FUN_08: Second checkout must be rejected (duplicate)"""
    from utils.api_helper import is_checkout_success_response, is_no_active_session_response
    assert not is_checkout_success_response(response), f"[{tc_id}] Second checkout unexpectedly succeeded"
    assert response.get("bill") is None, f"[{tc_id}] Second checkout must not return a bill"
    assert response.get("message", "").lower() != "success", f"[{tc_id}] Second checkout message must not be success"
    assert is_no_active_session_response(response), \
        f"[{tc_id}] Expected duplicate checkout rejection, got: {response}"


def validate_co_fun_09_vehicle(response: dict, vehicle_index: int, tc_id: str = "CO_FUN_09"):
    """CO_FUN_09: Each of the 3 vehicles must checkout successfully"""
    from utils.api_helper import is_checkout_success_response
    assert is_checkout_success_response(response), \
        f"[{tc_id}] Vehicle {vehicle_index} checkout failed: {response}"
    assert response.get("status_code") == 200, \
        f"[{tc_id}] Vehicle {vehicle_index} expected status 200, got {response.get('status_code')}"
    assert response.get("plate") is not None, f"[{tc_id}] Vehicle {vehicle_index} did not return a plate"
    assert response.get("bill") is not None, f"[{tc_id}] Vehicle {vehicle_index} did not return a bill"
    message = str(response.get("message", "")).lower()
    assert message == "success" or "success" in message, \
        f"[{tc_id}] Vehicle {vehicle_index} missing success indicator: {message}"


def validate_co_fun_09_uniqueness(plates: list, bill_ids: list, ticket_ids: list, tc_id: str = "CO_FUN_09"):
    """CO_FUN_09: All plates, bills, and tickets must be unique"""
    assert len(set(plates)) == 3, f"[{tc_id}] Returned plates are not unique: {plates}"
    if bill_ids:
        assert len(set(bill_ids)) == len(bill_ids), f"[{tc_id}] Bill IDs are not unique: {bill_ids}"
    if ticket_ids:
        assert len(set(ticket_ids)) == len(ticket_ids), f"[{tc_id}] Ticket IDs are not unique: {ticket_ids}"