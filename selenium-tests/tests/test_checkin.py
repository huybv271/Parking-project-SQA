"""
Check-in Tests (Vehicle Entry with License Plate Recognition)
Tests for check-in functionality using image-based plate recognition via API
"""
import pytest
from utils.api_helper import StaffAPIHelper
from utils.auth_helper import StaffAuthHelper
from utils.test_assets import (
    validate_test_assets_exist,
    get_checkin_image,
    get_checkin_fun09_images,
    CHECKIN_ASSETS,
)
from utils.validators import (
    validate_ci_fun_01,
    validate_ci_fun_02_first_attempt,
    validate_ci_fun_02_second_attempt,
    validate_ci_fun_03,
    validate_ci_fun_04,
    validate_ci_fun_05,
    validate_ci_fun_06,
    validate_ci_fun_07,
    validate_ci_fun_08,
    validate_ci_fun_09_vehicle,
    validate_ci_fun_09_uniqueness,
)


class TestCheckinImageAPI:
    """
    Check-in tests using image upload API
    Uses test image assets to test check-in functionality without requiring camera
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup UI login and API helper before each test"""
        # Validate assets exist
        validate_test_assets_exist()
        
        # Perform UI login and extract token
        auth_helper = StaffAuthHelper(driver)
        token = auth_helper.login_and_get_token()
        
        if not token:
            pytest.skip("UI login succeeded but auth token was not found in browser storage.")
        
        # Create API helper with extracted token
        self.api = StaffAPIHelper()
        self.api.set_token(token)
        
        yield
        
        # Cleanup
        self.api.close()

    @pytest.mark.CI_FUN_01
    def test_checkin_success_motorbike_plate(self):
        """
        TC_ID: CI_FUN_01
        Objective: Check check-in success with valid plate from stream
        Test Data: Staff account, Camera stream: motorbike with visible plate 59-D2420.69
        Expected: Success message, plate recognized, area/position assigned
        Validator: utils/validators.py::validate_ci_fun_01
        """
        tc_id = "CI_FUN_01"
        print(f"\n[{tc_id}] Starting check-in success test")
        
        image_path = get_checkin_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        
        response = self.api.checkin_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_ci_fun_01(response, tc_id)
        print(f"[{tc_id}] Result: PASSED")

    @pytest.mark.CI_FUN_02
    def test_checkin_reject_duplicate_vehicle(self):
        """
        TC_ID: CI_FUN_02
        Objective: Check system rejects check-in when vehicle already has active session
        Test Data: Staff account, Camera: plate 59-D2420.69, Pre-condition: vehicle already parked
        Expected: Second check-in rejected, no duplicate ticket created
        Validator: utils/validators.py::validate_ci_fun_02_first_attempt, validate_ci_fun_02_second_attempt
        """
        tc_id = "CI_FUN_02"
        print(f"\n[{tc_id}] Starting duplicate vehicle check-in test")
        
        image_path = get_checkin_image("CI_FUN_01")  # Use CI_FUN_01 image (same plate)
        print(f"[{tc_id}] Using image: {image_path}")
        
        # First check-in
        print(f"[{tc_id}] Attempt 1: First check-in")
        response1 = self.api.checkin_image(image_path, tc_id=f"{tc_id}_1")
        print(f"[{tc_id}] First response status: {response1.get('status_code')}")
        print(f"[{tc_id}] First response: {response1}")
        
        validate_ci_fun_02_first_attempt(response1, tc_id)
        
        # Second check-in - must be rejected
        print(f"[{tc_id}] Attempt 2: Second check-in (should be rejected)")
        response2 = self.api.checkin_image(image_path, tc_id=f"{tc_id}_2")
        print(f"[{tc_id}] Second response status: {response2.get('status_code')}")
        print(f"[{tc_id}] Second response: {response2}")
        
        validate_ci_fun_02_second_attempt(response2, tc_id)
        print(f"[{tc_id}] Result: PASSED (duplicate rejected correctly)")

    @pytest.mark.CI_FUN_03
    def test_checkin_reject_invalid_plate_format(self):
        """
        TC_ID: CI_FUN_03
        Objective: Check validate plate format with invalid plate
        Test Data: Camera stream showing only 75-L1 (incomplete plate)
        Expected: System rejects check-in, error message about invalid/incomplete plate
        Validator: utils/validators.py::validate_ci_fun_03
        """
        tc_id = "CI_FUN_03"
        print(f"\n[{tc_id}] Starting invalid plate format test")
        
        image_path = get_checkin_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        print(f"[{tc_id}] Image contains incomplete plate: 75L1")
        
        response = self.api.checkin_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_ci_fun_03(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (invalid plate correctly rejected)")

    @pytest.mark.CI_FUN_04
    def test_checkin_no_plate_detected(self):
        """
        TC_ID: CI_FUN_04
        Objective: Check system behavior when no license plate present
        Test Data: Camera stream with no vehicle visible
        Expected: System does not detect plate, error message displayed
        Validator: utils/validators.py::validate_ci_fun_04
        """
        tc_id = "CI_FUN_04"
        print(f"\n[{tc_id}] Starting no plate detected test")
        
        image_path = get_checkin_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        
        response = self.api.checkin_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_ci_fun_04(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (no plate detection correct)")

    @pytest.mark.CI_FUN_05
    def test_checkin_car_long_plate(self):
        """
        TC_ID: CI_FUN_05
        Objective: Check system can recognize long license plate of a car
        Test Data: Camera: car with plate 51H64427
        Expected: System correctly detects full plate, plate normalized, ticket created
        Validator: utils/validators.py::validate_ci_fun_05
        """
        tc_id = "CI_FUN_05"
        print(f"\n[{tc_id}] Starting car long plate test")
        
        image_path = get_checkin_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        
        response = self.api.checkin_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_ci_fun_05(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (car plate recognized)")

    @pytest.mark.CI_FUN_06
    def test_checkin_government_vehicle_blue_plate(self):
        """
        TC_ID: CI_FUN_06
        Objective: Check system recognizes blue plate (government vehicle)
        Test Data: Camera: vehicle with blue plate 65B1-99999
        Expected: System detects full plate, normalizes correctly, ticket created
        Validator: utils/validators.py::validate_ci_fun_06
        """
        tc_id = "CI_FUN_06"
        print(f"\n[{tc_id}] Starting government vehicle blue plate test")
        
        image_path = get_checkin_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        
        response = self.api.checkin_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_ci_fun_06(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (blue plate recognized)")

    @pytest.mark.CI_FUN_07
    def test_checkin_red_plate(self):
        """
        TC_ID: CI_FUN_07
        Objective: Check system recognizes red license plate
        Test Data: Camera: vehicle with red plate KC-88-88
        Expected: System correctly detects, normalizes, creates ticket
        Validator: utils/validators.py::validate_ci_fun_07
        """
        tc_id = "CI_FUN_07"
        print(f"\n[{tc_id}] Starting red plate test")
        
        image_path = get_checkin_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        
        response = self.api.checkin_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_ci_fun_07(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (red plate recognized)")

    @pytest.mark.CI_FUN_08
    def test_checkin_slot_full(self):
        """
        TC_ID: CI_FUN_08
        Objective: Check system rejects check-in when parking slot is full
        Pre-condition: Slot at capacity
        Expected: System rejects check-in, error message about full slot
        Validator: utils/validators.py::validate_ci_fun_08
        """
        tc_id = "CI_FUN_08"
        print(f"\n[{tc_id}] Starting slot full rejection test")
        
        # First, check slot capacity
        print(f"[{tc_id}] Checking slot capacity...")
        lot_status = self.api.get_lot_status(tc_id=tc_id)
        print(f"[{tc_id}] Slot status: {lot_status}")
        
        available_spots = lot_status.get("availableSpots", 1)
        total_spots = lot_status.get("totalSpots", 1)
        
        if available_spots > 0:
            pytest.skip(
                f"[{tc_id}] Full slot precondition requires parking area/slot capacity setup. "
                f"(available: {available_spots}/{total_spots})"
            )
        
        # Slot is full - attempt check-in
        print(f"[{tc_id}] Slot is full. Attempting check-in...")
        image_path = get_checkin_image("CI_FUN_01")  # Use any valid image
        
        response = self.api.checkin_image(image_path, tc_id=f"{tc_id}_fullCheck")
        print(f"[{tc_id}] Response: {response}")
        
        validate_ci_fun_08(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (full slot rejection confirmed)")

    @pytest.mark.CI_FUN_09
    def test_checkin_multiple_vehicles_sequential(self):
        """
        TC_ID: CI_FUN_09
        Objective: System handles multiple vehicles check-in sequentially without data loss
        Test Data: 3 different plates: 59-D2420.69, 51H64427, 65B1-99999
        Expected: System creates 3 separate records in this run, all recognized correctly
        Validator: utils/validators.py::validate_ci_fun_09_vehicle, validate_ci_fun_09_uniqueness
        """
        tc_id = "CI_FUN_09"
        print(f"\n[{tc_id}] Starting multiple vehicles sequential test")
        
        # Test data: use images from previous tests
        test_images = [
            ("CI_FUN_01", "59-D2420.69"),    # motorbike
            ("CI_FUN_05", "51H64427"),       # car
            ("CI_FUN_06", "65B1-99999")      # government vehicle
        ]
        
        # STEP 1: Cleanup - attempt checkout for all 3 images to remove pre-existing sessions
        print(f"[{tc_id}] Step 1: Cleanup - attempting checkout for all 3 vehicles")
        for i, (image_tc, plate) in enumerate(test_images, 1):
            try:
                image_path = get_checkin_image(image_tc)
                response = self.api.checkout_image(image_path, tc_id=f"{tc_id}_cleanup_{i}")
                print(f"[{tc_id}] Cleanup {i} ({plate}): status {response.get('status_code')}")
                # Cleanup success or vehicle not found (404) - both OK
                if response.get("status_code") in [200, 404, 400]:
                    print(f"[{tc_id}] Cleanup {i}: OK")
                else:
                    print(f"[{tc_id}] Cleanup {i}: unexpected status {response.get('status_code')}")
            except Exception as e:
                print(f"[{tc_id}] Cleanup {i}: error (acceptable) - {e}")
        
        print(f"[{tc_id}] Step 1 complete, proceeding with check-ins")
        
        # STEP 2: Check-in all 3 vehicles - ALL MUST SUCCEED
        print(f"[{tc_id}] Step 2: Check-in all 3 vehicles sequentially")
        tickets_created = []
        plates_recognized = []
        
        for i, (image_tc, expected_plate) in enumerate(test_images, 1):
            print(f"[{tc_id}] Check-in {i}: {expected_plate}")
            
            image_path = get_checkin_image(image_tc)
            response = self.api.checkin_image(image_path, tc_id=f"{tc_id}_vehicle{i}")
            print(f"[{tc_id}] Check-in {i} response status: {response.get('status_code')}")
            print(f"[{tc_id}] Check-in {i} response: {response}")
            
            validate_ci_fun_09_vehicle(response, i, tc_id)
            
            tickets_created.append(response.get("ticketId"))
            plates_recognized.append(response.get("plate"))
            
            print(f"[{tc_id}] Vehicle {i} OK: ticket={response.get('ticketId')}, plate={response.get('plate')}")
        
        # STEP 3: Verify all 3 are unique
        print(f"[{tc_id}] Step 3: Verifying uniqueness")
        validate_ci_fun_09_uniqueness(tickets_created, plates_recognized, tc_id)
        
        print(f"[{tc_id}] Result: PASSED (all 3 vehicles checked in sequentially with unique tickets and plates)")