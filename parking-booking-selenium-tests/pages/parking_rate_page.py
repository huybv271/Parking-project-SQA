from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import unicodedata

from pages.base_page import BasePage, Locator


class ParkingRatePage(BasePage):
    # Các selector của trang Parking Rate Management được gom tại Page Object,
    # nhờ vậy test file không phải hardcode selector rải rác.
    PAGE_READY: list[Locator] = [
        (By.XPATH, "//*[contains(., 'Parking Rate Management')]"),
    ]
    VEHICLE_SELECT: Locator = (By.CSS_SELECTOR, "select")
    TICKET_SELECT: Locator = (By.CSS_SELECTOR, "select:nth-of-type(2)")
    UNIT_PRICE_INPUT: Locator = (By.CSS_SELECTOR, "input[type='number']")
    SAVE_BUTTON: Locator = (By.XPATH, "//button[contains(normalize-space(.), 'Save')]")

    def open(self) -> None:
        # Mở đúng URL của màn hình quản lý giá gửi xe.
        self.open_url("/admin/parking-rate-management")
        # Đợi title/nội dung chính xuất hiện để chắc chắn page đã render xong.
        self.first_visible(self.PAGE_READY, "parking rate management page")

    def fill(self, vehicle_type: str = "", ticket_type: str = "", unit_price: str = "") -> None:
        # Trang hiện tại dùng 2 thẻ select: select đầu là vehicle type, select thứ hai là ticket type.
        selects = self.driver.find_elements(By.CSS_SELECTOR, "select")
        if vehicle_type:
            # Chọn loại xe theo text hiển thị hoặc value HTML.
            self.select_by_visible_text_or_value(selects[0], vehicle_type)
        if ticket_type:
            # Chọn loại vé theo text hiển thị hoặc value HTML.
            self.select_by_visible_text_or_value(selects[1], ticket_type)
        if unit_price:
            # Nhập đơn giá nếu test data có truyền unit_price.
            self.type_text([self.UNIT_PRICE_INPUT], unit_price, "unit price input")

    def clear_unit_price_after_autoload(self) -> None:
        # Một số combination như CAR/STANDARD tự load giá cũ vào input.
        input_element = self.first_visible([self.UNIT_PRICE_INPUT], "unit price input")
        try:
            # Đợi tối đa 5 giây để giá cũ load vào input trước khi clear.
            WebDriverWait(self.driver, 5).until(
                lambda _: (input_element.get_attribute("value") or "").strip() != ""
            )
        except TimeoutException:
            # Nếu không có giá tự load thì bỏ qua, test vẫn tiếp tục với input rỗng.
            pass
        # Clear bằng JS native setter để React nhận event input/change đúng.
        self.set_input_value(input_element, "")

    def save(self) -> None:
        # Click nút Save để submit form.
        self.first_clickable([self.SAVE_BUTTON], "parking rate save button").click()

    def assert_message_contains(self, *tokens: str) -> None:
        # Normalize text để giảm lỗi do dấu tiếng Việt hoặc encoding khi assert message.
        expected = [self._normalize(token) for token in tokens]
        # Đợi đến khi tất cả token mong đợi xuất hiện trong body text.
        self.wait.until(lambda _: all(token in self._normalize(self.page_text()) for token in expected))

    def assert_redirected_to_dashboard(self) -> None:
        # Sau khi lưu thành công, app redirect về dashboard admin.
        self.wait.until(EC.url_contains("/admin/dashboard"))

    @staticmethod
    def _normalize(value: str) -> str:
        # Bỏ dấu tiếng Việt và chuyển lowercase để assert ổn định hơn.
        return "".join(
            char for char in unicodedata.normalize("NFKD", value.lower()) if not unicodedata.combining(char)
        )
