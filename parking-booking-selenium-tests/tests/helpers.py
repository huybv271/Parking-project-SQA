from pages.history_page import HistoryPage
from pages.reservation_page import ReservationPage
import pytest


def case_by_id(test_data: dict, test_case_id: str) -> dict:
    for case in test_data["cases"]:
        if case["test_case_id"] == test_case_id:
            return case
    pytest.skip(f"Missing test case id {test_case_id} in current test data")


def cases_by_type(test_data: dict, test_type: str) -> list[dict]:
    return [case for case in test_data["cases"] if case["test_type"] == test_type]


def search_with_case(reservation_page: ReservationPage, case: dict) -> None:
    reservation_page.open()
    reservation_page.fill_search_form(case)
    reservation_page.search_spots()


def reserve_first_available_spot(reservation_page: ReservationPage, case: dict) -> None:
    search_with_case(reservation_page, case)
    reservation_page.wait_for_search_success_or_spots()
    reservation_page.select_first_spot()
    reservation_page.confirm_reservation()
    reservation_page.wait_for_reserve_success()


def assert_case_in_history(history_page: HistoryPage, case: dict) -> None:
    history_page.open()
    try:
        history_page.assert_history_contains_case(case)
    except AssertionError:
        if history_page.open_first_detail_if_available():
            history_page.assert_history_contains_case(case)
        else:
            raise
