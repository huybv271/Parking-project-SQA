import pytest

from tests.helpers import assert_case_in_history, case_by_id, reserve_first_available_spot
from utils.assertions import assert_time_range_is_valid


@pytest.mark.history
def test_history_displays_reservation_information_after_reserve(
    logged_in_customer, reservation_page, history_page, test_data
):
    case = case_by_id(test_data, "RH_FUN_001")

    reserve_first_available_spot(reservation_page, case)
    assert_case_in_history(history_page, case)


@pytest.mark.history
def test_history_time_out_is_not_formatted_as_invalid_47h(
    logged_in_customer, reservation_page, history_page, test_data
):
    case = case_by_id(test_data, "RH_FUN_002")

    reserve_first_available_spot(reservation_page, case)
    history_page.open()
    row = history_page.find_row_by_plate(case["plate"])
    assert row is not None, f"History should contain reservation plate {case['plate']}"
    assert "47h" not in row.text.lower(), "History must not display invalid 47h time format"
    assert_time_range_is_valid(row.text)

    try:
        history_page.assert_history_contains_case(case)
    except AssertionError:
        if history_page.open_first_detail_if_available():
            history_page.assert_history_contains_case(case)
        else:
            raise
