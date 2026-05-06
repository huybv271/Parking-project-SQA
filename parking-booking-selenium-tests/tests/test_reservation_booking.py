import pytest

from tests.helpers import case_by_id, reserve_first_available_spot, search_with_case


@pytest.mark.booking
@pytest.mark.smoke
def test_find_select_and_reserve_spot_success(logged_in_customer, reservation_page, history_page, db, test_data):
    case = case_by_id(test_data, "RS_BOOK_001")

    reserve_first_available_spot(reservation_page, case)

    if db.enabled:
        reservation = db.find_latest_reservation_by_plate(case["plate"])
        assert reservation is not None, "Reservation should be created in database"
        assert reservation["plate"] == case["plate"]

    history_page.open()
    assert history_page.find_row_by_plate(case["plate"]) is not None


@pytest.mark.booking
def test_reserve_duplicate_plate_and_overlapping_time_fails(logged_in_customer, reservation_page, test_data):
    case = case_by_id(test_data, "RS_BOOK_002")

    reserve_first_available_spot(reservation_page, case)

    search_with_case(reservation_page, case)
    reservation_page.wait_for_search_success_or_spots()
    reservation_page.select_first_spot()
    reservation_page.confirm_reservation()
    reservation_page.wait_for_reserve_error()


@pytest.mark.booking
def test_same_plate_can_reserve_on_different_dates(logged_in_customer, reservation_page, history_page, test_data):
    first_case = case_by_id(test_data, "RS_BOOK_003")
    second_case = case_by_id(test_data, "RS_BOOK_004")

    reserve_first_available_spot(reservation_page, first_case)
    reserve_first_available_spot(reservation_page, second_case)

    history_page.open()
    assert history_page.find_row_by_plate(first_case["plate"]) is not None
