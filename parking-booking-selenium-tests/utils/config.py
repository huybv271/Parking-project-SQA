from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Config:
    base_url: str
    api_base_url: str
    login_path: str
    reservation_path: str
    history_path: str
    username: str
    password: str
    admin_username: str
    admin_password: str
    admin_login_path: str
    admin_spot_area_path: str
    admin_deleted_spots_path: str
    admin_spot_areas: tuple[str, ...]
    browser: str
    headless: bool
    window_width: int
    window_height: int
    timeout: int
    db_enable: bool
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    db_dialect: str
    test_plate_prefix: str

    def url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"


def get_config() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL", "http://localhost:3000"),
        api_base_url=os.getenv("API_BASE_URL", "http://localhost:8081"),
        login_path=os.getenv("LOGIN_PATH", "/auth/login"),
        reservation_path=os.getenv("RESERVATION_PATH", "/customer/reservation"),
        history_path=os.getenv("HISTORY_PATH", "/customer/history"),
        username=os.getenv("CUSTOMER_USERNAME", ""),
        password=os.getenv("CUSTOMER_PASSWORD", ""),
        admin_username=os.getenv("ADMIN_USERNAME", "admin"),
        admin_password=os.getenv("ADMIN_PASSWORD", "123456"),
        admin_login_path=os.getenv("ADMIN_LOGIN_PATH", "/staff/auth/login"),
        admin_spot_area_path=os.getenv("ADMIN_SPOT_AREA_PATH", "/admin/spots/A"),
        admin_deleted_spots_path=os.getenv("ADMIN_DELETED_SPOTS_PATH", "/admin/spots/trash"),
        admin_spot_areas=tuple(
            area.strip()
            for area in os.getenv("ADMIN_SPOT_AREAS", "A,B").split(",")
            if area.strip()
        ),
        browser=os.getenv("BROWSER", "chrome"),
        headless=_bool_env("HEADLESS", False),
        window_width=int(os.getenv("WINDOW_WIDTH", "1440")),
        window_height=int(os.getenv("WINDOW_HEIGHT", "900")),
        timeout=int(os.getenv("SELENIUM_TIMEOUT", "15")),
        db_enable=_bool_env("DB_ENABLE", False),
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "3306")),
        db_name=os.getenv("DB_NAME", "parking"),
        db_user=os.getenv("DB_USER", "root"),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_dialect=os.getenv("DB_DIALECT", "mysql"),
        test_plate_prefix=os.getenv("TEST_PLATE_PREFIX", "AUTO"),
    )
