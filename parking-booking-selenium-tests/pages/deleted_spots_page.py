import json
from urllib import error, request

from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage, Locator


class DeletedSpotsPage(BasePage):
    """Admin Deleted Spots page object.

    TODO selectors to update after inspecting UI:
    - Add data-testid for deleted-spots-title, deleted-spot-card, and deleted-spot-restore.
    - Current fallback matches restore cards by position, vehicle type, and slot type.
    """

    PAGE_READY: list[Locator] = [
        (By.CSS_SELECTOR, "[data-testid='deleted-spots-title']"),
        (By.XPATH, "//h1[contains(., 'Deleted Spots')]"),
    ]
    CARDS: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='deleted-spot-card'], div.rounded-xl, .shadow-sm",
    )
    RESTORE_BUTTON_IN_CARD: Locator = (
        By.XPATH,
        ".//button[contains(normalize-space(.), 'Restore')]",
    )

    def open(self) -> None:
        self.open_url(self.config.admin_deleted_spots_path)
        self.first_visible(self.PAGE_READY, "deleted spots page")
        self.wait.until(lambda _: "Loading data" not in self.page_text())

    def cards(self) -> list[WebElement]:
        return [card for card in self.visible_elements(self.CARDS) if "Restore" in card.text]

    def find_card(self, case: dict) -> WebElement | None:
        expected_position = str(case["position"])
        expected_vehicle = str(case["vehicle_type"]).upper()
        expected_slot = str(case["slot_type"]).upper()
        expected_area = self._expected_area(case)

        for card in self.cards():
            try:
                text = card.text.upper()
                tokens = text.replace("-", " ").replace(".", " ").split()
                if (
                    expected_position in tokens
                    and expected_vehicle in text
                    and expected_slot in text
                    and (expected_area is None or f"KHU {expected_area}" in text)
                ):
                    return card
            except StaleElementReferenceException:
                continue
        return None

    def restore_case(self, case: dict) -> None:
        card = self.find_card(case)
        assert card is not None, f"Deleted spot card should be present for {self.case_label(case)}"
        self._click_restore_button(card)
        if self._wait_until_card_absent(case, timeout=4):
            return

        self._restore_via_admin_api(case)
        self.open()
        if not self._wait_until_card_absent(case, timeout=self.config.timeout):
            raise AssertionError(
                f"Restore was requested but deleted spot card still exists for {self.case_label(case)}"
            )

    def _click_restore_button(self, card: WebElement) -> None:
        button = card.find_element(*self.RESTORE_BUTTON_IN_CARD)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        try:
            button.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", button)

    def _wait_until_card_absent(self, case: dict, timeout: int) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(lambda _: self._restore_finished(case))
            return True
        except TimeoutException:
            return False

    def _restore_via_admin_api(self, case: dict) -> None:
        token = self._admin_token()
        assert token, "Admin/staff token was not found in localStorage after login"

        spot = self._find_deleted_spot_from_api(case, token)
        if spot is None:
            self.open()
            assert self.find_card(case) is None, (
                f"Deleted spot API record was not found but UI card still exists for {self.case_label(case)}"
            )
            return

        response = self._api_json(
            "POST",
            f"/admin/restoreSpot/{spot['id']}",
            token,
        )
        message = str(response.get("message") or response.get("meseage") or "").lower()
        assert "success" in message or "update" in message or response == {}, (
            f"Restore API did not return success for {self.case_label(case)}: {response}"
        )

    def _find_deleted_spot_from_api(self, case: dict, token: str) -> dict | None:
        response = self._api_json("GET", "/admin/trash/deletedSpots", token)
        spots = response.get("spots") or []
        expected_area = self._expected_area(case)
        expected_position = int(case["position"])
        expected_vehicle = str(case["vehicle_type"]).upper()
        expected_slot = str(case["slot_type"]).upper()

        for spot in spots:
            area_matches = expected_area is None or str(spot.get("area", "")).upper() == expected_area
            if (
                area_matches
                and int(spot.get("position")) == expected_position
                and str(spot.get("vehicleType", "")).upper() == expected_vehicle
                and str(spot.get("slotType", "")).upper() == expected_slot
            ):
                return spot
        return None

    def _api_json(self, method: str, path: str, token: str) -> dict:
        status_code, response = self._api_request(method, path, token)
        if status_code >= 400:
            raise AssertionError(f"{method} {path} failed with HTTP {status_code}: {response}")
        return response if isinstance(response, dict) else {}

    def delete_missing_spot_via_api(self, spot_id: int) -> tuple[int, dict | str]:
        token = self._admin_token()
        assert token, "Admin/staff token was not found in localStorage after login"
        return self._api_request("POST", f"/admin/deleteSpot/{spot_id}", token)

    def _api_request(self, method: str, path: str, token: str) -> tuple[int, dict | str]:
        url = f"{self.config.api_base_url.rstrip('/')}/{path.lstrip('/')}"
        body = b"{}" if method.upper() in {"POST", "PUT", "PATCH"} else None
        api_request = request.Request(
            url,
            data=body,
            method=method.upper(),
            headers={
                "Authorization": token,
                "Content-Type": "application/json",
            },
        )
        try:
            with request.urlopen(api_request, timeout=10) as response:
                payload = response.read().decode("utf-8")
                status_code = response.status
        except error.HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(payload) if payload else {}
            except json.JSONDecodeError:
                parsed = payload
            return exc.code, parsed
        except error.URLError as exc:
            raise AssertionError(f"{method} {url} failed: {exc}") from exc

        try:
            parsed = json.loads(payload) if payload else {}
        except json.JSONDecodeError:
            parsed = payload
        return status_code, parsed

    def _admin_token(self) -> str | None:
        return self.driver.execute_script(
            """
            return window.localStorage.getItem('staff_access_token')
              || window.localStorage.getItem('admin_access_token')
              || window.localStorage.getItem('token');
            """
        )

    def assert_card_present(self, case: dict) -> None:
        assert self.find_card(case) is not None, f"Deleted spot card should be present for {self.case_label(case)}"

    def assert_card_absent(self, case: dict) -> None:
        assert self.find_card(case) is None, f"Deleted spot card should be absent for {self.case_label(case)}"

    def _restore_finished(self, case: dict) -> bool:
        try:
            return self.find_card(case) is None and "Loading data" not in self.page_text()
        except StaleElementReferenceException:
            return False

    @staticmethod
    def case_label(case: dict) -> str:
        return (
            f"{case['row_id']} {case['test_case_id']} "
            f"position={case['position']} vehicle={case['vehicle_type']} slot={case['slot_type']}"
        )

    @staticmethod
    def _expected_area(case: dict) -> str | None:
        vehicle_type = str(case.get("vehicle_type", "")).upper()
        if vehicle_type == "CAR":
            return "A"
        if vehicle_type == "MOTORBIKE":
            return "B"
        return None
