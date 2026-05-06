# Parking Booking Selenium Tests

Automation project for Booking Spot and Reservation History system tests.

`test.json` in the repository currently contains Delete Spot cases, so this project uses the Booking Spot requirements from the chat as the source and converts them to `data/reservation_test_data.json`.

## Understanding

The customer logs in, opens Reservation, enters date/time/vehicle/plate, searches spots, selects one spot, reserves it, then verifies the reservation in History. The suite covers GUI checks, date/time/plate validation, reservation success/failure, duplicate conflict, same plate on different dates, and history display including invalid `47h`-style time formatting.

GUI checks automate measurable points only: visible elements, clickable back button, non-empty labels/headers, CSS font/color presence, no horizontal overflow, and no text overflowing the viewport.

## Structure

```text
parking-booking-selenium-tests/
├── README.md
├── requirements.txt
├── .env.example
├── pytest.ini
├── conftest.py
├── data/
│   ├── reservation_test_data.json
│   └── reservation_test_data.csv
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── reservation_page.py
│   └── history_page.py
├── tests/
│   ├── test_reservation_gui.py
│   ├── test_reservation_validation.py
│   ├── test_reservation_booking.py
│   └── test_reservation_history.py
├── utils/
│   ├── config.py
│   ├── driver_factory.py
│   ├── database.py
│   └── assertions.py
└── postman/
    ├── parking_booking_api_collection.json
    └── parking_booking_api_environment.json
```

## Setup

```powershell
cd D:\ThucHanh\packing-project\parking-booking-selenium-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`:

```env
BASE_URL=http://localhost:3000
CUSTOMER_USERNAME=your_customer_username
CUSTOMER_PASSWORD=your_customer_password
ADMIN_USERNAME=admin
ADMIN_PASSWORD=123456
API_BASE_URL=http://localhost:3001
```

Keep `DB_ENABLE=false` until the database credentials and table names are confirmed. When enabled, the suite can assert reservations in DB and rollback records with plate prefix `AUTO`.

## Run Selenium Tests

Run all tests and generate HTML report:

```powershell
pytest
```

Run by group:

```powershell
pytest -m gui
pytest -m validation
pytest -m booking
pytest -m history
pytest -m "admin and delete_spot"
pytest -m admin_management
pytest -m smoke
```

Run one file:

```powershell
pytest tests/test_reservation_booking.py
```

Run one Admin Management test case after the cleanup/refactor:

```powershell
pytest tests/test_admin_management.py::test_prm_fun_01_empty_data
pytest tests/test_admin_management.py::test_st_fun_01_delete_staff
pytest tests/test_admin_management.py::test_dt_fun_01_restore_staff
pytest tests/test_admin_management.py::test_cs_fun_01_create_staff_success
```

Report output:

```text
reports/report.html
logs/test-run.log
screenshots/*.png
```

Screenshots are captured for failed Selenium tests.

## Run Postman API Tests

Open `postman/parking_booking_api_collection.json` and `postman/parking_booking_api_environment.json` in Postman, update environment values, then run the collection.

Newman command with report:

```powershell
npm install -g newman newman-reporter-htmlextra
newman run postman/parking_booking_api_collection.json `
  -e postman/parking_booking_api_environment.json `
  -r cli,htmlextra,json `
  --reporter-htmlextra-export reports/postman-report.html `
  --reporter-json-export reports/postman-report.json
```

The collection covers login, available spot search, invalid time validation, create reservation, duplicate overlap rejection, VNPay payment creation, reservation history, and active reservation count.

Admin Delete Spot API collection:

```powershell
newman run postman/parking_delete_spot_admin_api_collection.json `
  -e postman/parking_booking_api_environment.json `
  -r cli,htmlextra,json `
  --reporter-htmlextra-export reports/postman-delete-spot-report.html `
  --reporter-json-export reports/postman-delete-spot-report.json
```

Set `admin_spot_id` in the Postman environment to a safe test spot. The API collection is intentionally small and checks login, get spots by area, delete, get deleted spots, and restore.

## Delete Spot Selenium Tests

The Delete Spot data is in:

```text
data/reservation_test_data.json
data/reservation_test_data.csv
```

The filename is kept because it already existed, but the content now contains the 21 `DS_FUN_*` Delete/Restore Spot cases. Duplicate manual IDs are preserved; use `row_id` for unique reporting.

Run:

```powershell
pytest tests/test_delete_spot.py
pytest -m "admin and delete_spot"
```

The test logs in with:

```text
ADMIN_USERNAME=admin
ADMIN_PASSWORD=123456
```

Expected behavior:

- `Delete success`: row disappears from Spot Area and appears in Deleted Spots.
- `Delete Fail`: row remains in Spot Area.
- `Restore Success`: card disappears from Deleted Spots and row appears in Spot Area.
- `No Delete`: canceling browser confirmation keeps row in Spot Area.

Do not run these tests in parallel because the manual cases mutate the same spot records and are intended to run in file order.

## Selectors To Update

Add stable `data-testid` attributes in the UI when possible, then update only these Page Object files:

`pages/login_page.py`:

- `login-username`
- `login-password`
- `login-submit`

`pages/reservation_page.py`:

- `reservation-title`
- `reservation-form`
- `date-in`
- `date-out`
- `time-in`
- `time-out`
- `vehicle-type`
- `plate`
- `search-spots`
- `reservation-back`
- `spot-card`
- `confirm-reservation`
- `payment-created`
- `toast-success`
- `toast-error`

`pages/history_page.py`:

- `history-title`
- `history-table`
- `history-row`
- `history-header`
- `history-back`
- `history-detail`
- `history-empty`

`pages/admin_login_page.py`:

- `admin-login-username`
- `admin-login-password`
- `admin-login-submit`
- `admin-dashboard`

`pages/spot_area_page.py`:

- `spot-area-title`
- `spot-area-select`
- `spot-row`
- `spot-position`
- `spot-vehicle-type`
- `spot-slot-type`
- `spot-active-toggle`
- `spot-delete`

`pages/deleted_spots_page.py`:

- `deleted-spots-title`
- `deleted-spot-card`
- `deleted-spot-info`
- `deleted-spot-restore`
- `deleted-spots-empty`

No selectors are hardcoded in test files.

## Tests Likely To Expose Current Bugs

These tests are written against expected behavior and should fail if the system still has the current implementation gaps:

- `RS_VAL_PLATE_003`: whitespace-only plate should be rejected.
- `RS_VAL_PLATE_004`: special-character-only plate should be rejected.
- `RS_VAL_PLATE_005`: too-short plate should be rejected.
- `RS_VAL_PLATE_006`: too-long plate should be rejected.
- `RH_FUN_002`: overnight history must not show invalid hour values such as `25h` or `47h`.
- `RH_FUN_001` / `RH_FUN_002`: history should show enough date in/date out/time in/time out/plate information, or provide a detail view.

Do not change expected results to match actual bugs. If these fail, keep them failing and log defects.

## Rollback Notes

Automation-created plates use the `AUTO` prefix. With `DB_ENABLE=true`, `utils/database.py` deletes matching rows from `Payments`, `ReservationBlocks`, and `Reservations` after the pytest session.

If your database uses singular or lowercase table names, update only `utils/database.py`.
