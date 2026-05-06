import json
import logging
from pathlib import Path
import sys

import pytest

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from pages.history_page import HistoryPage
from pages.admin_login_page import AdminLoginPage
from pages.deleted_spots_page import DeletedSpotsPage
from pages.login_page import LoginPage
from pages.parking_rate_page import ParkingRatePage
from pages.reservation_page import ReservationPage
from pages.spot_area_page import SpotAreaPage
from pages.staff_pages import CreateStaffPage, DeletedStaffsPage, StaffDetailPage, StaffListPage
from utils.config import get_config
from utils.database import DatabaseClient
from utils.driver_factory import create_driver


def pytest_configure(config):
    log_dir = ROOT_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_dir / "test-run.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


@pytest.fixture(scope="session")
def app_config():
    return get_config()


@pytest.fixture(scope="session")
def test_data():
    data_path = ROOT_DIR / "data" / "reservation_test_data.json"
    with data_path.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def db(app_config):
    return DatabaseClient(app_config)


@pytest.fixture(scope="session", autouse=True)
def rollback_automation_data_after_session(db, app_config):
    yield
    db.rollback_reservations_by_plate_prefix(app_config.test_plate_prefix)


@pytest.fixture()
def driver(app_config, request):
    driver_instance = create_driver(app_config)
    yield driver_instance
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        screenshot_dir = ROOT_DIR / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        safe_name = request.node.nodeid.replace("/", "_").replace("::", "__").replace("[", "_").replace("]", "_")
        driver_instance.save_screenshot(str(screenshot_dir / f"{safe_name}.png"))
    driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture()
def login_page(driver, app_config):
    return LoginPage(driver, app_config)


@pytest.fixture()
def reservation_page(driver, app_config):
    return ReservationPage(driver, app_config)


@pytest.fixture()
def history_page(driver, app_config):
    return HistoryPage(driver, app_config)


@pytest.fixture()
def admin_login_page(driver, app_config):
    return AdminLoginPage(driver, app_config)


@pytest.fixture()
def spot_area_page(driver, app_config):
    return SpotAreaPage(driver, app_config)


@pytest.fixture()
def deleted_spots_page(driver, app_config):
    return DeletedSpotsPage(driver, app_config)


@pytest.fixture()
def parking_rate_page(driver, app_config):
    return ParkingRatePage(driver, app_config)


@pytest.fixture()
def staff_list_page(driver, app_config):
    return StaffListPage(driver, app_config)


@pytest.fixture()
def staff_detail_page(driver, app_config):
    return StaffDetailPage(driver, app_config)


@pytest.fixture()
def deleted_staffs_page(driver, app_config):
    return DeletedStaffsPage(driver, app_config)


@pytest.fixture()
def create_staff_page(driver, app_config):
    return CreateStaffPage(driver, app_config)


@pytest.fixture()
def logged_in_customer(login_page, app_config):
    if not app_config.username or not app_config.password:
        pytest.skip("CUSTOMER_USERNAME/CUSTOMER_PASSWORD are not configured for customer reservation tests")
    login_page.open()
    login_page.login(app_config.username, app_config.password)
    login_page.wait_until_customer_area_loaded()
    return login_page


@pytest.fixture()
def logged_in_admin(admin_login_page, app_config):
    assert app_config.admin_username, "ADMIN_USERNAME must be configured in .env"
    assert app_config.admin_password, "ADMIN_PASSWORD must be configured in .env"
    admin_login_page.open()
    admin_login_page.login(app_config.admin_username, app_config.admin_password)
    admin_login_page.wait_until_admin_area_loaded()
    return admin_login_page
