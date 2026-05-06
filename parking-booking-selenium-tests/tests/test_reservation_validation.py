import pytest

from tests.helpers import case_by_id, search_with_case


VALIDATION_CASE_IDS = [
    "RS_VAL_DATE_001",
    "RS_VAL_DATE_002",
    "RS_VAL_TIME_001",
    "RS_VAL_TIME_002",
    "RS_VAL_PLATE_001",
    "RS_VAL_PLATE_002",
    "RS_VAL_PLATE_003",
    "RS_VAL_PLATE_004",
    "RS_VAL_PLATE_005",
    "RS_VAL_PLATE_006",
]


@pytest.mark.validation
@pytest.mark.parametrize("test_case_id", VALIDATION_CASE_IDS)
def test_reservation_search_validation(logged_in_customer, reservation_page, test_data, test_case_id):
    case = case_by_id(test_data, test_case_id)

    search_with_case(reservation_page, case)

    if case["expected_search_result"] == "Find empty spots successfully":
        reservation_page.wait_for_search_success_or_spots()
        assert reservation_page.spot_cards() or "slot found" in reservation_page.page_text().lower()
    else:
        reservation_page.wait_for_search_error_or_no_spots()
