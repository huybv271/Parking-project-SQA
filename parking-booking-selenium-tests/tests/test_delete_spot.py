import json
from pathlib import Path

import pytest


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "reservation_test_data.json"


def _load_delete_spot_cases() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return [case for case in data["cases"] if case["feature"] == "Delete spot"]


DELETE_SPOT_CASES = _load_delete_spot_cases()


def _case_id(case: dict) -> str:
    return f"{case['row_id']}-{case['test_case_id']}-{case['objective']}-{case['expected_result']}"


@pytest.mark.admin
@pytest.mark.delete_spot
def test_admin_delete_restore_spot_manual_cases(logged_in_admin, spot_area_page, deleted_spots_page, db):
    failures = []

    for case in DELETE_SPOT_CASES:
        try:
            _run_case(spot_area_page, deleted_spots_page, db, case)
        except AssertionError as exc:
            failures.append(f"{_case_id(case)}: {exc}")

    assert not failures, "Delete Spot failures:\n" + "\n".join(failures)


def _run_case(spot_area_page, deleted_spots_page, db, case):
    action = str(case["action"]).strip().lower()
    expected = str(case["expected_result"]).strip().lower()

    if action == "delete":
        _run_delete_case(spot_area_page, deleted_spots_page, db, case, expected)
        return

    if action == "restore":
        _run_restore_case(spot_area_page, deleted_spots_page, db, case)
        return

    if action == "cancel delete":
        _run_cancel_delete_case(spot_area_page, deleted_spots_page, db, case)
        return

    if action in {"delete nonexistent", "delete non-existent", "delete missing spot"}:
        _run_delete_nonexistent_spot_case(deleted_spots_page, db, case)
        return

    raise AssertionError(f"Unsupported action: {case['action']}")


def _run_delete_case(spot_area_page, deleted_spots_page, db, case, expected):
    _ensure_spot_active(spot_area_page, deleted_spots_page, case)
    _, row = spot_area_page.find_row_across_configured_areas(case)

    assert row is not None, f"Precondition failed: active spot row not found for {spot_area_page.case_label(case)}"
    spot_area_page.delete_row(row, accept_confirmation=True)

    if expected == "delete success":
        spot_area_page.assert_row_absent(case)
        deleted_spots_page.open()
        deleted_spots_page.assert_card_present(case)
        if db.enabled:
            spot = db.find_spot_by_position(case["position"], case["vehicle_type"], case["slot_type"])
            assert spot is not None and spot["deletedAt"] is not None
        return

    if expected == "delete fail":
        spot_area_page.assert_row_present(case)
        if db.enabled:
            spot = db.find_spot_by_position(case["position"], case["vehicle_type"], case["slot_type"])
            assert spot is not None and spot["deletedAt"] is None
        return

    raise AssertionError(f"Unsupported delete expected_result: {case['expected_result']}")


def _run_restore_case(spot_area_page, deleted_spots_page, db, case):
    _ensure_spot_deleted(spot_area_page, deleted_spots_page, case)
    deleted_spots_page.open()
    deleted_spots_page.restore_case(case)
    deleted_spots_page.assert_card_absent(case)
    spot_area_page.assert_row_present(case)
    if db.enabled:
        spot = db.find_spot_by_position(case["position"], case["vehicle_type"], case["slot_type"])
        assert spot is not None and spot["deletedAt"] is None


def _run_cancel_delete_case(spot_area_page, deleted_spots_page, db, case):
    # Cancel case only proves the confirmation dialog keeps the spot active.
    # It should not depend on a spot left deleted by a previous run.
    _ensure_spot_active(spot_area_page, deleted_spots_page, case)
    _, row = spot_area_page.find_row_across_configured_areas(case)
    assert row is not None, f"Precondition failed: active spot row not found for {spot_area_page.case_label(case)}"

    spot_area_page.delete_row(row, accept_confirmation=False)
    spot_area_page.assert_row_present(case)
    if db.enabled:
        spot = db.find_spot_by_position(case["position"], case["vehicle_type"], case["slot_type"])
        assert spot is not None and spot["deletedAt"] is None


def _run_delete_nonexistent_spot_case(deleted_spots_page, db, case):
    spot_id = int(case["spot_id"])
    status_code, response = deleted_spots_page.delete_missing_spot_via_api(spot_id)
    assert status_code == 404, f"Expected 404 for missing spot id={spot_id}, got {status_code}: {response}"
    response_text = str(response).lower()
    assert "spot" in response_text, f"Missing spot response should mention spot: {response}"
    if db.enabled:
        assert db.find_spot_by_id(spot_id) is None, f"Spot id={spot_id} should not exist in DB"


def _ensure_spot_active(spot_area_page, deleted_spots_page, case):
    _, row = spot_area_page.find_row_across_configured_areas(case)
    if row is not None:
        return

    deleted_spots_page.open()
    if deleted_spots_page.find_card(case) is not None:
        deleted_spots_page.restore_case(case)
        spot_area_page.assert_row_present(case)
        return

    raise AssertionError(f"Precondition failed: spot not found in active list or trash for {spot_area_page.case_label(case)}")


def _ensure_spot_deleted(spot_area_page, deleted_spots_page, case):
    deleted_spots_page.open()
    if deleted_spots_page.find_card(case) is not None:
        return

    _, row = spot_area_page.find_row_across_configured_areas(case)
    assert row is not None, f"Precondition failed: active spot row not found for restore setup {spot_area_page.case_label(case)}"
    spot_area_page.delete_row(row, accept_confirmation=True)
    deleted_spots_page.open()
    deleted_spots_page.assert_card_present(case)
