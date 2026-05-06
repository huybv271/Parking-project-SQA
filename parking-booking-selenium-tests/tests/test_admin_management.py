import json
from pathlib import Path

import pytest


# Đường dẫn tới file JSON chứa test data cho nhóm Admin Management.
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "admin_management_test_data.json"


def _load_cases() -> list[dict]:
    """Đọc toàn bộ test case từ file JSON để test code không hardcode dữ liệu."""
    with DATA_PATH.open(encoding="utf-8") as f:
        return json.load(f)["cases"]


# Load test data một lần khi pytest import file này.
CASES = _load_cases()


def _case(case_id: str) -> dict:
    """Lấy đúng test data theo TC_ID, ví dụ PRM_FUN_01 hoặc CS_FUN_01."""
    return next(case for case in CASES if case["test_case_id"] == case_id)


def _assert_parking_rate_error(parking_rate_page, *tokens: str) -> None:
    """Assert message lỗi theo token để tránh fail vì lỗi font/encoding tiếng Việt trên UI."""
    parking_rate_page.assert_message_contains(*tokens)


def _assert_staff_deleted_in_db(db, username: str) -> None:
    """Kiểm tra DB sau thao tác Delete Staff nếu DB_ENABLE=true."""
    if db.enabled:
        # Staff bị xóa mềm nên record vẫn còn, nhưng deletedAt phải có giá trị.
        staff = db.find_staff_by_username(username)
        assert staff is not None and staff["deletedAt"] is not None


def _assert_staff_active_in_db(db, username: str) -> None:
    """Kiểm tra DB sau thao tác Restore/Create Staff nếu DB_ENABLE=true."""
    if db.enabled:
        # Staff active nghĩa là record tồn tại và deletedAt phải rỗng/null.
        staff = db.find_staff_by_username(username)
        assert staff is not None and staff["deletedAt"] is None


def _restore_staff_if_missing_from_list(staff_list_page, deleted_staffs_page, case: dict) -> None:
    """Đưa staff về trạng thái active trước khi chạy case cần staff xuất hiện ở list."""
    staff_list_page.open()
    # Nếu staff không còn ở Staff List, staff có thể đang nằm trong Deleted Staffs.
    if staff_list_page.find_row_by_username(case["username"]) is None:
        deleted_staffs_page.open()
        # Restore để test có precondition sạch, chạy lại nhiều lần không bị fail giả.
        deleted_staffs_page.restore_staff(case["name"])
        staff_list_page.open()


def _delete_staff_if_still_active(staff_list_page, case: dict) -> None:
    """Đưa staff về trạng thái deleted trước khi chạy case restore."""
    staff_list_page.open()
    # Nếu staff vẫn còn active, xóa mềm trước để trang Deleted Staffs có dữ liệu restore.
    if staff_list_page.find_row_by_username(case["username"]) is not None:
        staff_list_page.delete_staff(case["username"])


@pytest.mark.admin
@pytest.mark.admin_management
def test_prm_fun_01_empty_data(logged_in_admin, parking_rate_page):
    """PRM_FUN_01: Save khi không nhập dữ liệu phải hiển thị lỗi thiếu giá."""
    case = _case("PRM_FUN_01")

    # Mở màn hình Parking Rate Management sau khi fixture đã login admin.
    parking_rate_page.open()

    # Không nhập vehicle type, ticket type, unit price theo đúng input test case.
    parking_rate_page.fill(case["vehicle_type"], case["ticket_type"], case["unit_price"])

    # Click Save để trigger validation phía UI/backend.
    parking_rate_page.save()

    # Expected: hiển thị thông báo thiếu dữ liệu/thiếu giá.
    _assert_parking_rate_error(parking_rate_page, "thi", "gi")


@pytest.mark.admin
@pytest.mark.admin_management
def test_prm_fun_02_missing_unit_price(logged_in_admin, parking_rate_page):
    """PRM_FUN_02: Chọn vehicle/ticket nhưng bỏ trống unit price phải báo thiếu giá."""
    case = _case("PRM_FUN_02")

    # Mở màn hình quản lý giá.
    parking_rate_page.open()

    # Nhập vehicle type và ticket type theo test data.
    parking_rate_page.fill(case["vehicle_type"], case["ticket_type"], case["unit_price"])

    # UI hiện tại tự load giá cũ khi chọn CAR/STANDARD, nên cần clear để giữ đúng precondition.
    parking_rate_page.clear_unit_price_after_autoload()

    # Submit form khi giá đang rỗng.
    parking_rate_page.save()

    # Expected: hệ thống báo thiếu dữ liệu/thiếu giá.
    _assert_parking_rate_error(parking_rate_page, "thi", "gi")


@pytest.mark.admin
@pytest.mark.admin_management
def test_prm_fun_03_missing_vehicle_and_ticket(logged_in_admin, parking_rate_page):
    """PRM_FUN_03: Chỉ nhập unit price, thiếu vehicle/ticket thì phải báo nhập đủ dữ liệu."""
    case = _case("PRM_FUN_03")

    # Mở màn hình quản lý giá.
    parking_rate_page.open()

    # Chỉ nhập unit price, không chọn vehicle type và ticket type.
    parking_rate_page.fill(case["vehicle_type"], case["ticket_type"], case["unit_price"])

    # Submit form để kiểm tra validation thiếu input.
    parking_rate_page.save()

    # Expected message có nội dung thất bại/nhập đầy đủ dữ liệu.
    _assert_parking_rate_error(parking_rate_page, "th", "b", "d", "li")


@pytest.mark.admin
@pytest.mark.admin_management
def test_prm_fun_04_save_parking_rate_success(logged_in_admin, parking_rate_page, db):
    """PRM_FUN_04: Nhập đủ dữ liệu thì lưu giá thành công và DB có giá active."""
    case = _case("PRM_FUN_04")

    # Mở màn hình quản lý giá.
    parking_rate_page.open()

    # Nhập đầy đủ vehicle type, ticket type và unit price.
    parking_rate_page.fill(case["vehicle_type"], case["ticket_type"], case["unit_price"])

    # Submit form thành công.
    parking_rate_page.save()

    # Expected UI: redirect về dashboard/management screen.
    parking_rate_page.assert_redirected_to_dashboard()

    # Expected DB: rate active mới nhất đúng vehicle/ticket có unitPrice như test data.
    if db.enabled:
        rate = db.find_active_parking_rate(case["vehicle_type"], case["ticket_type"])
        assert rate is not None and int(rate["unitPrice"]) == int(case["unit_price"])


@pytest.mark.admin
@pytest.mark.admin_management
def test_st_fun_01_delete_staff(logged_in_admin, staff_list_page, deleted_staffs_page, db):
    """ST_FUN_01: Xóa staff10 khỏi Staff List."""
    case = _case("ST_FUN_01")

    # Đảm bảo staff10 đang active trước khi test delete.
    _restore_staff_if_missing_from_list(staff_list_page, deleted_staffs_page, case)

    # Thực hiện click Delete và accept confirmation dialog.
    staff_list_page.delete_staff(case["username"])

    # Expected UI: staff10 không còn hiển thị trong Staff List.
    staff_list_page.assert_staff_absent(case["username"])

    # Expected DB: staff10 bị xóa mềm, deletedAt khác null.
    _assert_staff_deleted_in_db(db, case["username"])


@pytest.mark.admin
@pytest.mark.admin_management
def test_st_fun_02_view_staff(logged_in_admin, staff_list_page, staff_detail_page):
    """ST_FUN_02: View staff9 và kiểm tra trang detail hiển thị thông tin."""
    case = _case("ST_FUN_02")

    # Mở danh sách staff.
    staff_list_page.open()

    # Click View tại dòng username staff9.
    staff_list_page.view_staff(case["username"])

    # Expected UI: detail page chứa username và tên staff.
    staff_detail_page.assert_staff_detail(case["username"], case["name"])


@pytest.mark.admin
@pytest.mark.admin_management
def test_dt_fun_01_restore_staff(logged_in_admin, staff_list_page, deleted_staffs_page, db):
    """DT_FUN_01: Restore Nhân viên 10 từ Deleted Staffs."""
    case = _case("DT_FUN_01")

    # Đảm bảo staff10 đang ở trạng thái deleted để có thể restore.
    _delete_staff_if_still_active(staff_list_page, case)

    # Mở trang Deleted Staffs.
    deleted_staffs_page.open()

    # Click Restore tại card Nhân viên 10.
    deleted_staffs_page.restore_staff(case["name"])

    # Quay lại Staff List để kiểm tra staff đã xuất hiện lại.
    staff_list_page.open()

    # Expected UI: staff10 hiển thị lại trong Staff List.
    staff_list_page.assert_staff_present(case["username"])

    # Expected DB: staff10 active trở lại, deletedAt bằng null.
    _assert_staff_active_in_db(db, case["username"])


@pytest.mark.admin
@pytest.mark.admin_management
def test_cs_fun_01_create_staff_success(logged_in_admin, create_staff_page, staff_list_page, db):
    """CS_FUN_01: Tạo staff mới với đầy đủ dữ liệu."""
    case = _case("CS_FUN_01")

    # Rollback staff01 cũ do automation tạo ở lần chạy trước để test có thể chạy lại.
    db.rollback_staff_by_username(case["username"])

    # Mở màn hình Create Staff.
    create_staff_page.open()

    # Điền đầy đủ tên, ngày tạo, username và password.
    create_staff_page.fill(case["name"], case["date"], case["username"], case["password"])

    # Submit form tạo staff.
    create_staff_page.submit()

    # Expected UI: tạo thành công và redirect về Staff List.
    create_staff_page.assert_redirected_to_staff_list()

    # Expected UI: staff01 xuất hiện trong Staff List.
    staff_list_page.assert_staff_present(case["username"])

    # Expected DB: staff01 tồn tại và chưa bị xóa mềm.
    _assert_staff_active_in_db(db, case["username"])


@pytest.mark.admin
@pytest.mark.admin_management
def test_cs_fun_02_create_staff_missing_required_fields(logged_in_admin, create_staff_page):
    """CS_FUN_02: Chỉ nhập một field thì phải báo vui lòng nhập đầy đủ thông tin."""
    case = _case("CS_FUN_02")

    # Mở màn hình Create Staff.
    create_staff_page.open()

    # Theo test data, chỉ nhập tên nhân viên; date, username và password để rỗng.
    create_staff_page.fill(case["name"], case["date"], case["username"], case["password"])

    # Submit form thiếu dữ liệu.
    create_staff_page.submit()

    # Expected UI: alert báo cần nhập đầy đủ thông tin.
    create_staff_page.assert_validation_alert("vui", "long", "day", "du")
