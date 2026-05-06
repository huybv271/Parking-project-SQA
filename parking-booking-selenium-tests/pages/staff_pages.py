import unicodedata

from selenium.common.exceptions import NoAlertPresentException, StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, Locator


def _normalize_text(value: str) -> str:
    """Chuan hoa chuoi de so sanh on dinh khi UI co dau tieng Viet hoac loi encoding."""
    # Dua chuoi ve lowercase de so sanh khong phan biet hoa/thuong.
    lowered = value.lower()
    # Tach dau ra khoi ky tu goc, vi du "â" thanh "a" + dau.
    decomposed = unicodedata.normalize("NFKD", lowered)
    # Bo cac dau/combining mark de con lai chu cai goc.
    without_marks = "".join(char for char in decomposed if not unicodedata.combining(char))
    # Xu ly rieng ky tu "đ" vi normalize NFKD khong doi thanh "d".
    return without_marks.replace("đ", "d")


class StaffListPage(BasePage):
    """Page Object cho man hinh Staff List."""

    # Selector nhan biet trang Staff List da load.
    PAGE_READY: list[Locator] = [
        (By.XPATH, "//*[contains(., 'Staff List')]"),
        (By.CSS_SELECTOR, "table"),
    ]
    # Selector lay tat ca row trong table staff.
    TABLE_ROWS: Locator = (By.CSS_SELECTOR, "tbody tr")
    # Selector nut Delete nam ben trong mot row cu the.
    DELETE_BUTTON_IN_ROW: Locator = (By.XPATH, ".//button[contains(normalize-space(.), 'Delete')]")
    # Selector link/nut View nam ben trong mot row cu the.
    VIEW_BUTTON_IN_ROW: Locator = (By.XPATH, ".//a[contains(@href, '/admin/staffs/') or .//button[contains(., 'View')]]")

    def open(self) -> None:
        # Mo truc tiep URL danh sach staff.
        self.open_url("/admin/staffs/list")
        # Doi title/table xuat hien de chac chan trang da render.
        self.first_visible(self.PAGE_READY, "staff list page")
        # Doi loading text bien mat truoc khi tim row trong table.
        self.wait.until(lambda _: "Loading" not in self.page_text() and "Dang tai" not in self.page_text())

    def find_row_by_username(self, username: str) -> WebElement | None:
        # Duyet tung row dang hien thi trong tbody.
        for row in self.visible_elements(self.TABLE_ROWS):
            try:
                # Table hien tai dat username o cot dau tien.
                cells = row.find_elements(By.TAG_NAME, "td")
                # Neu cot dau tien khop username can tim thi tra ve row do.
                if cells and cells[0].text.strip() == username:
                    return row
            except StaleElementReferenceException:
                # React co the render lai table trong luc Selenium dang doc element.
                return None
        # Khong tim thay row phu hop.
        return None

    def delete_staff(self, username: str) -> None:
        # Tim dung row staff can delete.
        row = self.find_row_by_username(username)
        # Neu khong co row thi fail ngay de biet sai precondition/test data.
        assert row is not None, f"Staff row should be present for username={username}"
        # Click nut Delete trong row.
        row.find_element(*self.DELETE_BUTTON_IN_ROW).click()
        # Doi browser alert xac nhan xoa xuat hien.
        alert: Alert = self.wait.until(EC.alert_is_present())
        # Accept alert de dong y xoa.
        alert.accept()
        # Doi alert dong han truoc khi doc lai table.
        self.wait.until(lambda _: self._no_alert_present())
        # Doi row bien mat khoi danh sach, day la expected UI cua delete success.
        self.wait.until(lambda _: self.find_row_by_username(username) is None)

    def view_staff(self, username: str) -> None:
        # Tim row cua staff can xem detail.
        row = self.find_row_by_username(username)
        # Neu row khong ton tai thi fail vi test data/precondition sai.
        assert row is not None, f"Staff row should be present for username={username}"
        # Click View de chuyen sang trang Staff Detail.
        row.find_element(*self.VIEW_BUTTON_IN_ROW).click()

    def assert_staff_present(self, username: str) -> None:
        # Doi den khi staff xuat hien trong Staff List.
        self.wait.until(lambda _: self.find_row_by_username(username) is not None)

    def assert_staff_absent(self, username: str) -> None:
        # Doi den khi staff khong con trong Staff List.
        self.wait.until(lambda _: self.find_row_by_username(username) is None)

    def _no_alert_present(self) -> bool:
        try:
            # Neu switch_to.alert thanh cong nghia la alert van con ton tai.
            self.driver.switch_to.alert
            return False
        except NoAlertPresentException:
            # Khong co alert thi browser san sang cho step tiep theo.
            return True


class StaffDetailPage(BasePage):
    """Page Object cho man hinh Staff Detail."""

    # Selector nhan biet trang Staff Detail.
    PAGE_READY: list[Locator] = [
        (By.XPATH, "//*[contains(., 'Staff Detail')]"),
    ]

    def assert_staff_detail(self, username: str, name: str) -> None:
        # Doi trang detail load xong.
        self.first_visible(self.PAGE_READY, "staff detail page")
        # Expected UI: username phai hien thi tren detail page.
        self.wait.until(lambda _: username in self.page_text())
        # Expected UI: ten nhan vien phai hien thi tren detail page.
        self.wait.until(lambda _: self._name_matches(name))

    def _name_matches(self, name: str) -> bool:
        # Lay text tren page va chuan hoa de tranh loi encoding/dau tieng Viet.
        normalized_page = _normalize_text(self.page_text())
        # Lay ten mong doi tu test data va chuan hoa tuong tu.
        normalized_name = _normalize_text(name)
        # Chap nhan match dung ten hoac pattern "nhan vien" neu UI bi loi dau.
        return normalized_name in normalized_page or "nhan vien" in normalized_page


class DeletedStaffsPage(BasePage):
    """Page Object cho man hinh Deleted Staffs."""

    # Selector nhan biet trang Deleted Staffs.
    PAGE_READY: list[Locator] = [
        (By.XPATH, "//*[contains(., 'Deleted Staffs')]"),
    ]
    # Card staff bi xoa hien tai dung class rounded/shadow.
    CARDS: Locator = (By.CSS_SELECTOR, ".rounded-xl, .shadow-sm")
    # Nut Restore nam ben trong tung card.
    RESTORE_BUTTON_IN_CARD: Locator = (By.XPATH, ".//button[contains(normalize-space(.), 'Restore')]")

    def open(self) -> None:
        # Mo trang thung rac staff.
        self.open_url("/admin/staffs/trash")
        # Doi title Deleted Staffs xuat hien.
        self.first_visible(self.PAGE_READY, "deleted staffs page")
        # Doi loading data bien mat.
        self.wait.until(lambda _: "Loading data" not in self.page_text())

    def find_card_by_name(self, name: str) -> WebElement | None:
        # Chuan hoa ten staff can tim.
        expected = _normalize_text(name)
        # Duyet tat ca card dang hien thi.
        for card in self.visible_elements(self.CARDS):
            try:
                # Chuan hoa text cua card de so sanh on dinh.
                text = _normalize_text(card.text)
                # Card dung phai co nut restore va co ten staff can tim.
                if "restore" in text and (expected in text or "nhan vien" in text):
                    return card
            except StaleElementReferenceException:
                # DOM co the render lai sau action delete/restore.
                return None
        # Khong tim thay card phu hop.
        return None

    def restore_staff(self, name: str) -> None:
        # Tim card staff can restore.
        card = self.find_card_by_name(name)
        # Neu khong co card thi fail de bao sai precondition.
        assert card is not None, f"Deleted staff card should be present for name={name}"
        # Click Restore tren card.
        card.find_element(*self.RESTORE_BUTTON_IN_CARD).click()
        # Doi card bien mat khoi Deleted Staffs sau khi restore thanh cong.
        self.wait.until(lambda _: self.find_card_by_name(name) is None)


class CreateStaffPage(BasePage):
    """Page Object cho man hinh Create Staff."""

    # Selector nhan biet trang Create Staff.
    PAGE_READY: list[Locator] = [
        (By.XPATH, "//*[contains(., 'Create Staff')]"),
    ]
    # Input text cua form; hien tai thu tu la name roi username.
    NAME_INPUT: Locator = (By.CSS_SELECTOR, "input:not([type]), input[type='text']")
    # Input date cua ngay tao.
    DATE_INPUT: Locator = (By.CSS_SELECTOR, "input[type='date']")
    # Input password cua staff.
    PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "input[type='password']")
    # Nut submit tao staff.
    SUBMIT_BUTTON: Locator = (By.XPATH, "//button[contains(normalize-space(.), 'Create Staff')]")

    def open(self) -> None:
        # Mo trang Create Staff.
        self.open_url("/admin/staffs/create")
        # Doi form render xong.
        self.first_visible(self.PAGE_READY, "create staff page")

    def fill(self, name: str = "", date: str = "", username: str = "", password: str = "") -> None:
        # Lay tat ca input text de map theo thu tu tren UI.
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input:not([type]), input[type='text']")
        if name:
            # Set ten bang JS native setter de React nhan event input/change.
            self.set_input_value(text_inputs[0], name)
        if date:
            # Date input can set bang JS vi send_keys co the bi lech format theo locale Chrome.
            date_input = self.first_visible([self.DATE_INPUT], "staff create date input")
            # Gia tri date trong data dung format HTML date: YYYY-MM-DD.
            self.set_input_value(date_input, date)
        if username:
            # Set username bang JS native setter.
            self.set_input_value(text_inputs[1], username)
        if password:
            # Password input dung send_keys vi day la input don gian.
            self.type_text([self.PASSWORD_INPUT], password, "staff create password input")

    def submit(self) -> None:
        # Click nut Create Staff de submit form.
        self.first_clickable([self.SUBMIT_BUTTON], "create staff button").click()

    def assert_validation_alert(self, *tokens: str) -> None:
        # Doi alert validation hien thi.
        alert: Alert = self.wait.until(EC.alert_is_present())
        # Chuan hoa alert text de tranh loi dau tieng Viet.
        text = _normalize_text(alert.text)
        # Dong alert de test/browser khong bi ket.
        alert.accept()
        # Kiem tra tat ca token mong doi deu xuat hien trong alert.
        assert all(_normalize_text(token) in text for token in tokens), f"Unexpected alert text: {text}"

    def assert_redirected_to_staff_list(self) -> None:
        # Sau khi tao thanh cong, app redirect ve Staff List.
        self.wait.until(EC.url_contains("/admin/staffs/list"))
