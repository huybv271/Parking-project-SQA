from selenium.webdriver.remote.webelement import WebElement


def assert_visible(element: WebElement, name: str) -> None:
    assert element.is_displayed(), f"{name} should be visible"


def assert_clickable(element: WebElement, name: str) -> None:
    assert element.is_displayed() and element.is_enabled(), f"{name} should be clickable"


def assert_text_not_blank(element: WebElement, name: str) -> None:
    assert element.text.strip(), f"{name} text should not be blank"


def assert_css_property_present(element: WebElement, css_name: str, name: str) -> None:
    value = element.value_of_css_property(css_name)
    assert value and value != "none", f"{name} should have CSS property {css_name}"


def assert_no_horizontal_overflow(driver) -> None:
    overflow = driver.execute_script(
        "return document.documentElement.scrollWidth > document.documentElement.clientWidth;"
    )
    assert not overflow, "Page should not have horizontal overflow"


def assert_no_text_overflows_viewport(driver) -> None:
    overflowing_count = driver.execute_script(
        """
        const elements = Array.from(document.querySelectorAll('body *'))
          .filter((el) => el.offsetParent !== null && (el.innerText || '').trim().length > 0);
        return elements.filter((el) => {
          const rect = el.getBoundingClientRect();
          return rect.left < -1 || rect.right > window.innerWidth + 1;
        }).length;
        """
    )
    assert overflowing_count == 0, f"{overflowing_count} text elements overflow viewport"


def assert_time_range_is_valid(time_text: str) -> None:
    numbers = [int(part[:-1]) for part in time_text.split() if part.endswith("h") and part[:-1].isdigit()]
    assert numbers, f"Could not parse hour values from history time text: {time_text!r}"
    for hour in numbers:
        assert 0 <= hour <= 24, f"Hour should not be formatted as invalid value such as 47h: {time_text!r}"
