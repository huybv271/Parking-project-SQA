"""
Test assets configuration
Manages paths to test image files for check-in and check-out tests
"""
import os
from pathlib import Path


# Get the selenium-tests root directory
SELENIUM_TESTS_ROOT = Path(__file__).parent.parent.absolute()
TEST_ASSETS_DIR = SELENIUM_TESTS_ROOT / "test_assets"

# Check-in test images
CHECKIN_ASSETS = {
    "CI_FUN_01": TEST_ASSETS_DIR / "checkin" / "CI_FUN_01_59D242069.jpg",
    "CI_FUN_03": TEST_ASSETS_DIR / "checkin" / "CI_FUN_03_invalid_75L1.jpg",
    "CI_FUN_04": TEST_ASSETS_DIR / "checkin" / "CI_FUN_04_no_plate.jpg",
    "CI_FUN_05": TEST_ASSETS_DIR / "checkin" / "CI_FUN_05_51H64427.jpg",
    "CI_FUN_06": TEST_ASSETS_DIR / "checkin" / "CI_FUN_06_65B199999_blue.jpg",
    "CI_FUN_07": TEST_ASSETS_DIR / "checkin" / "CI_FUN_07_KC8888_red.jpg",
    "CI_FUN_08": TEST_ASSETS_DIR / "checkin" / "CI_FUN_08_lot_full_30G49344.jpg",
    "CI_FUN_09_1": TEST_ASSETS_DIR / "checkin" / "CI_FUN_09_51H64427.jpg",
    "CI_FUN_09_2": TEST_ASSETS_DIR / "checkin" / "CI_FUN_09_59D242069.jpg",
    "CI_FUN_09_3": TEST_ASSETS_DIR / "checkin" / "CI_FUN_09_65B199999_blue.jpg",
}

# Check-out test images
CHECKOUT_ASSETS = {
    "CO_FUN_01": TEST_ASSETS_DIR / "checkout" / "CO_FUN_01_59D242069.jpg",
    "CO_FUN_03": TEST_ASSETS_DIR / "checkout" / "CO_FUN_03_invalid_75L1.jpg",
    "CO_FUN_04": TEST_ASSETS_DIR / "checkout" / "CO_FUN_04_no_plate.jpg",
    "CO_FUN_05": TEST_ASSETS_DIR / "checkout" / "CO_FUN_05_30F78777.jpg",
    "CO_FUN_06": TEST_ASSETS_DIR / "checkout" / "CO_FUN_06_65B199999_blue.jpg",
    "CO_FUN_07": TEST_ASSETS_DIR / "checkout" / "CO_FUN_07_KC8888_red.jpg",
    "CO_FUN_09_VEHICLE_1": TEST_ASSETS_DIR / "checkout" / "CO_FUN_09_51H64427.jpg",
    "CO_FUN_09_VEHICLE_2": TEST_ASSETS_DIR / "checkout" / "CO_FUN_09_59D242069.jpg",
    "CO_FUN_09_VEHICLE_3": TEST_ASSETS_DIR / "checkout" / "CO_FUN_09_65B199999_blue.jpg",
}


def validate_test_assets_exist():
    """
    Validate that all required test image files exist.
    
    Raises:
        FileNotFoundError: If any required image file is missing
        
    Returns:
        dict: Summary of validation results
    """
    missing_files = []
    found_files = []
    
    # Check checkin assets
    for tc_id, path in CHECKIN_ASSETS.items():
        if path.exists():
            found_files.append(f"✓ {tc_id}: {path}")
        else:
            missing_files.append(f"✗ {tc_id}: {path}")
    
    # Check checkout assets
    for tc_id, path in CHECKOUT_ASSETS.items():
        if path.exists():
            found_files.append(f"✓ {tc_id}: {path}")
        else:
            missing_files.append(f"✗ {tc_id}: {path}")
    
    result = {
        "found_count": len(found_files),
        "missing_count": len(missing_files),
        "found_files": found_files,
        "missing_files": missing_files,
        "all_valid": len(missing_files) == 0,
    }
    
    if missing_files:
        error_msg = f"Missing {len(missing_files)} test image files:\n"
        error_msg += "\n".join(missing_files)
        raise FileNotFoundError(error_msg)
    
    return result


def get_checkin_image(tc_id):
    """Get path to check-in test image by TC_ID"""
    if tc_id not in CHECKIN_ASSETS:
        raise ValueError(f"Unknown check-in TC_ID: {tc_id}")
    path = CHECKIN_ASSETS[tc_id]
    if not path.exists():
        raise FileNotFoundError(f"Check-in image not found: {path}")
    return str(path)


def get_checkout_image(tc_id):
    """Get path to check-out test image by TC_ID"""
    if tc_id not in CHECKOUT_ASSETS:
        raise ValueError(f"Unknown check-out TC_ID: {tc_id}")
    path = CHECKOUT_ASSETS[tc_id]
    if not path.exists():
        raise FileNotFoundError(f"Check-out image not found: {path}")
    return str(path)


def get_checkin_fun09_images():
    """Get list of 3 check-in images for CI_FUN_09 (multiple vehicles sequentially)"""
    tc_ids = ["CI_FUN_09_1", "CI_FUN_09_2", "CI_FUN_09_3"]
    images = []
    for tc_id in tc_ids:
        if tc_id not in CHECKIN_ASSETS:
            raise ValueError(f"CI_FUN_09 image not found: {tc_id}")
        path = CHECKIN_ASSETS[tc_id]
        if not path.exists():
            raise FileNotFoundError(f"CI_FUN_09 image not found: {path}")
        images.append(str(path))
    return images


def get_checkout_fun09_images():
    """Get list of 3 check-out images for CO_FUN_09 (multiple vehicles sequentially)"""
    tc_ids = ["CO_FUN_09_VEHICLE_1", "CO_FUN_09_VEHICLE_2", "CO_FUN_09_VEHICLE_3"]
    images = []
    for tc_id in tc_ids:
        if tc_id not in CHECKOUT_ASSETS:
            raise ValueError(f"CO_FUN_09 image not found: {tc_id}")
        path = CHECKOUT_ASSETS[tc_id]
        if not path.exists():
            raise FileNotFoundError(f"CO_FUN_09 image not found: {path}")
        images.append(str(path))
    return images
