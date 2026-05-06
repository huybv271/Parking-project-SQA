import pytest

from tests.helpers import case_by_id
from utils.assertions import (
    assert_clickable,
    assert_css_property_present,
    assert_no_horizontal_overflow,
    assert_no_text_overflows_viewport,
    assert_text_not_blank,
    assert_visible,
)


@pytest.mark.gui
def test_reservation_booking_form_layout(logged_in_customer, reservation_page, test_data):
    case_by_id(test_data, "RS_GUI_001")

    reservation_page.open()
    form = reservation_page.form_container()
    assert_visible(form, "reservation form")
    assert_css_property_present(form, "font-size", "reservation form")
    assert_css_property_present(form, "color", "reservation form")

    labels = reservation_page.labels()
    assert len(labels) >= 5, "Reservation form should show labels for date/time/vehicle/plate"
    for index, label in enumerate(labels, start=1):
        assert_text_not_blank(label, f"reservation label #{index}")
        assert_css_property_present(label, "font-size", f"reservation label #{index}")
        assert_css_property_present(label, "color", f"reservation label #{index}")

    assert len(reservation_page.date_inputs()) >= 2
    assert len(reservation_page.number_inputs()) >= 2
    assert_clickable(
        reservation_page.first_clickable(reservation_page.SEARCH_BUTTON, "search spots button"),
        "search spots button",
    )
    assert_clickable(
        reservation_page.first_clickable(reservation_page.BACK_BUTTON, "reservation back button"),
        "reservation back button",
    )
    assert_no_horizontal_overflow(reservation_page.driver)
    assert_no_text_overflows_viewport(reservation_page.driver)


@pytest.mark.gui
def test_reservation_history_layout(logged_in_customer, history_page, test_data):
    case_by_id(test_data, "RH_GUI_001")

    history_page.open()
    assert_visible(history_page.first_visible(history_page.PAGE_TITLE, "history title"), "history title")
    assert_clickable(history_page.back_button(), "history back button")

    headers = history_page.headers()
    rows = history_page.rows()
    if headers:
        for index, header in enumerate(headers, start=1):
            assert_text_not_blank(header, f"history header #{index}")
            assert_css_property_present(header, "font-size", f"history header #{index}")
            assert_css_property_present(header, "color", f"history header #{index}")
    else:
        assert history_page.first_visible(history_page.EMPTY_MESSAGE, "history empty message")

    for index, row in enumerate(rows, start=1):
        assert_text_not_blank(row, f"history row #{index}")

    assert_no_horizontal_overflow(history_page.driver)
    assert_no_text_overflows_viewport(history_page.driver)
