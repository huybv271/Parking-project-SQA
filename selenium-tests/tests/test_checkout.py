"""
Check-out Tests (Vehicle Exit with License Plate Recognition)
Tests for check-out functionality using image-based plate recognition via API
"""
import pytest
from utils.api_helper import (
    StaffAPIHelper,
    is_checkin_success_or_already_in_lot,
    is_checkout_success_response,
    is_no_active_session_response,
)
from utils.auth_helper import StaffAuthHelper
from utils.test_assets import (
    validate_test_assets_exist,
    get_checkout_image,
    get_checkout_fun09_images,
    CHECKOUT_ASSETS,
)
from utils.validators import (
    validate_co_fun_01,
    validate_co_fun_02_first_attempt,
    validate_co_fun_02_second_attempt,
    validate_co_fun_03,
    validate_co_fun_04,
    validate_co_fun_05,
    validate_co_fun_06,
    validate_co_fun_07,
    validate_co_fun_08_first_checkout,
    validate_co_fun_08_second_checkout,
    validate_co_fun_09_vehicle,
    validate_co_fun_09_uniqueness,
)


class TestCheckoutImageAPI:
    """
    Check-out tests using image upload API
    Uses test image assets to test check-out functionality without requiring camera
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

    def _ensure_active_session(self, image_path: str, tc_id: str):
        print(f"[{tc_id}] Preparing active session")
        checkin_response = self.api.checkin_image(image_path, tc_id=f"{tc_id}_checkin")
        print(f"[{tc_id}] Check-in response: {checkin_response}")
        assert is_checkin_success_or_already_in_lot(checkin_response), \
            f"[{tc_id}] Unable to prepare active session: {checkin_response}"
        return checkin_response

    @pytest.mark.CO_FUN_01
    def test_checkout_success_motorbike_plate(self):
        """
        TC_ID: CO_FUN_01
        Objective: Check Check-out success with valid plate from stream
        Test Data: Staff account, Camera: motorbike with plate visible
        Expected: Success message, plate recognized, bill calculated, images shown
        Validator: utils/validators.py::validate_co_fun_01
        """
        tc_id = "CO_FUN_01"
        print(f"\n[{tc_id}] Starting checkout success test")
        image_path = get_checkout_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        self._ensure_active_session(image_path, tc_id)
        response = self.api.checkout_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_co_fun_01(response, tc_id)
        print(f"[{tc_id}] Result: PASSED")

    @pytest.mark.CO_FUN_02
    def test_checkout_reject_no_active_session(self):
        """
        TC_ID: CO_FUN_02
        Objective: Check system rejects Check-out when vehicle no active session
        Test Data: Camera: plate 59-D2420.69, No pre-condition parking session
        Expected: System rejects, error message displayed
        Validator: utils/validators.py::validate_co_fun_02_first_attempt, validate_co_fun_02_second_attempt
        """
        tc_id = "CO_FUN_02"
        print(f"\n[{tc_id}] Starting no active session rejection test")

        image_path = get_checkout_image("CO_FUN_01")
        print(f"[{tc_id}] Image path: {image_path}")

        print(f"[{tc_id}] Attempt 1: Clear any active session")
        response1 = self.api.checkout_image(image_path, tc_id=f"{tc_id}_1")
        print(f"[{tc_id}] First response: {response1}")

        validate_co_fun_02_first_attempt(response1, tc_id)

        print(f"[{tc_id}] Attempt 2: Expect rejection for no active session")
        response2 = self.api.checkout_image(image_path, tc_id=f"{tc_id}_2")
        print(f"[{tc_id}] Second response: {response2}")

        validate_co_fun_02_second_attempt(response2, tc_id)
        print(f"[{tc_id}] Result: PASSED (no active session rejected correctly)")

    @pytest.mark.CO_FUN_03
    def test_checkout_reject_invalid_plate_format(self):
        """
        TC_ID: CO_FUN_03
        Objective: Check validate plate with invalid or partially obscured
        Test Data: Camera showing only 75-L1 (incomplete)
        Expected: System rejects, error about incomplete plate
        Validator: utils/validators.py::validate_co_fun_03
        """
        tc_id = "CO_FUN_03"
        print(f"\n[{tc_id}] Starting invalid plate format test")
        
        image_path = get_checkout_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        print(f"[{tc_id}] Image contains incomplete plate: 75L1")
        
        response = self.api.checkout_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_co_fun_03(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (invalid plate correctly rejected)")

    @pytest.mark.CO_FUN_04
    def test_checkout_no_plate_detected(self):
        """
        TC_ID: CO_FUN_04
        Objective: System behavior when no license plate in camera frame
        Test Data: Camera: no vehicle visible
        Expected: No plate detected, error message displayed
        Validator: utils/validators.py::validate_co_fun_04
        """
        tc_id = "CO_FUN_04"
        print(f"\n[{tc_id}] Starting no plate detected test")
        
        image_path = get_checkout_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        
        response = self.api.checkout_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_co_fun_04(response, tc_id)
        print(f"[{tc_id}] Result: PASSED (no plate handled correctly)")

    @pytest.mark.CO_FUN_05
    def test_checkout_car_long_plate(self):
        """
        TC_ID: CO_FUN_05
        Objective: System correctly recognizes and processes long car plate
        Test Data: Camera: car with plate 30E78777, Pre-condition: parking session
        Expected: Plate detected, normalized, bill calculated with times shown
        Validator: utils/validators.py::validate_co_fun_05
        """
        tc_id = "CO_FUN_05"
        print(f"\n[{tc_id}] Starting car long plate checkout test")
        image_path = get_checkout_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        self._ensure_active_session(image_path, tc_id)
        response = self.api.checkout_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_co_fun_05(response, tc_id)
        print(f"[{tc_id}] Result: PASSED")

    @pytest.mark.CO_FUN_06
    def test_checkout_government_vehicle_blue_plate(self):
        """
        TC_ID: CO_FUN_06
        Objective: System recognizes blue plate (government vehicle)
        Test Data: Camera: vehicle with blue plate 65B1-99999, Pre-condition: session
        Expected: Plate detected, normalized correctly
        Validator: utils/validators.py::validate_co_fun_06
        """
        tc_id = "CO_FUN_06"
        print(f"\n[{tc_id}] Starting blue plate checkout test")
        image_path = get_checkout_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        print(f"[{tc_id}] Preparing active session")
        checkin_response = self.api.checkin_image(image_path, tc_id=f"{tc_id}_checkin")
        print(f"[{tc_id}] Check-in response: {checkin_response}")
        if not is_checkin_success_or_already_in_lot(checkin_response):
            message = str(checkin_response.get("message", ""))
            if checkin_response.get("status_code") == 500 and "429" in message:
                print(f"[{tc_id}] Check-in rate limited; continuing to validate checkout with existing session state")
            else:
                assert False, f"[{tc_id}] Unable to prepare active session: {checkin_response}"
        response = self.api.checkout_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_co_fun_06(response, tc_id)
        print(f"[{tc_id}] Result: PASSED")

    @pytest.mark.CO_FUN_07
    def test_checkout_red_plate(self):
        """
        TC_ID: CO_FUN_07
        Objective: System recognizes red license plate during checkout
        Test Data: Camera: vehicle with red plate KC-88-88, Pre-condition: session
        Expected: Plate detected, normalized, bill shown with images
        Validator: utils/validators.py::validate_co_fun_07
        """
        tc_id = "CO_FUN_07"
        print(f"\n[{tc_id}] Starting red plate checkout test")
        image_path = get_checkout_image(tc_id)
        print(f"[{tc_id}] Image path: {image_path}")
        self._ensure_active_session(image_path, tc_id)
        response = self.api.checkout_image(image_path, tc_id=tc_id)
        print(f"[{tc_id}] API response: {response}")
        
        validate_co_fun_07(response, tc_id)
        print(f"[{tc_id}] Result: PASSED")

    @pytest.mark.CO_FUN_08
    def test_checkout_prevent_duplicate(self):
        """
        TC_ID: CO_FUN_08
        Objective: System prevents duplicate Check-out for same vehicle
        Test Data: Camera: plate 59-D2420.69, Pre-condition: already checked out
        Expected: Second checkout rejected, error message displayed
        Validator: utils/validators.py::validate_co_fun_08_first_checkout, validate_co_fun_08_second_checkout
        """
        tc_id = "CO_FUN_08"
        print(f"\n[{tc_id}] Starting duplicate checkout prevention test")

        image_path = get_checkout_image("CO_FUN_01")
        print(f"[{tc_id}] Image path: {image_path}")

        print(f"[{tc_id}] Step 1: Ensure active session exists")
        checkin_response = self.api.checkin_image(image_path, tc_id=f"{tc_id}_checkin")
        print(f"[{tc_id}] Check-in response: {checkin_response}")
        assert is_checkin_success_or_already_in_lot(checkin_response), \
            f"[{tc_id}] Unable to establish precondition: {checkin_response}"

        print(f"[{tc_id}] Step 2: First checkout should succeed")
        response1 = self.api.checkout_image(image_path, tc_id=f"{tc_id}_1")
        print(f"[{tc_id}] First checkout response: {response1}")
        
        validate_co_fun_08_first_checkout(response1, tc_id)

        print(f"[{tc_id}] Step 3: Second checkout should be rejected")
        response2 = self.api.checkout_image(image_path, tc_id=f"{tc_id}_2")
        print(f"[{tc_id}] Second checkout response: {response2}")

        validate_co_fun_08_second_checkout(response2, tc_id)
        print(f"[{tc_id}] Result: PASSED (duplicate checkout rejected correctly)")

    @pytest.mark.CO_FUN_09
    def test_checkout_multiple_vehicles_sequential(self):
        """
        TC_ID: CO_FUN_09
        Objective: System handles multiple vehicle checkouts sequentially
        Test Data: 3 plates: 59-D2420.69, 30E78777, 65B1-99999, all with sessions
        Expected: All checkout successfully, each plate/bill calculated correctly
        Validator: utils/validators.py::validate_co_fun_09_vehicle, validate_co_fun_09_uniqueness
        """
        tc_id = "CO_FUN_09"
        print(f"\n[{tc_id}] Starting sequential checkout test")

        image_paths = get_checkout_fun09_images()
        assert len(image_paths) == 3, f"[{tc_id}] Expected 3 checkout images, got {len(image_paths)}"

        print(f"[{tc_id}] Step 1: Preparing active sessions for all 3 vehicles")
        for index, image_path in enumerate(image_paths, 1):
            print(f"[{tc_id}] Pre-checkin {index}: {image_path}")
            checkin_response = self.api.checkin_image(image_path, tc_id=f"{tc_id}_checkin_{index}")
            print(f"[{tc_id}] Pre-checkin {index} response: {checkin_response}")
            if is_checkin_success_or_already_in_lot(checkin_response):
                continue
            assert False, f"[{tc_id}] Unable to prepare active session for vehicle {index}: {checkin_response}"

        print(f"[{tc_id}] Step 2: Checking out all 3 vehicles")
        responses = []
        plates = []
        bill_ids = []
        ticket_ids = []

        for index, image_path in enumerate(image_paths, 1):
            response = self.api.checkout_image(image_path, tc_id=f"{tc_id}_checkout_{index}")
            print(f"[{tc_id}] Checkout {index} response: {response}")
            responses.append(response)

            validate_co_fun_09_vehicle(response, index, tc_id)

            plate = response.get("plate")
            bill = response.get("bill")
            plates.append(plate)

            if isinstance(bill, dict):
                bill_id = bill.get("idBill") or bill.get("ticketId")
                ticket_id = bill.get("ticketId")
                if bill_id is not None:
                    bill_ids.append(bill_id)
                if ticket_id is not None:
                    ticket_ids.append(ticket_id)

        validate_co_fun_09_uniqueness(plates, bill_ids, ticket_ids, tc_id)
        print(f"[{tc_id}] Result: PASSED (all 3 vehicles checked out sequentially)")