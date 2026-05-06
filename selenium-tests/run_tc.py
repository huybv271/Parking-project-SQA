"""
Run test case(s) by TC_ID marker.

Usage:
  Single TC:    python run_tc.py CI_FUN_01
  Multiple TCs: python run_tc.py CI_FUN_01 CI_FUN_03 CO_FUN_04
  All checkin:  python run_tc.py checkin
  All checkout: python run_tc.py checkout
  All tests:    python run_tc.py all

The script validates TC_IDs, creates the reports/ folder if needed,
prints the exact pytest command, and returns the pytest exit code.
"""
import os
import sys
import subprocess

VALID_TC_IDS = [
    "CI_FUN_01", "CI_FUN_02", "CI_FUN_03", "CI_FUN_04",
    "CI_FUN_05", "CI_FUN_06", "CI_FUN_07", "CI_FUN_08", "CI_FUN_09",
    "CO_FUN_01", "CO_FUN_02", "CO_FUN_03", "CO_FUN_04",
    "CO_FUN_05", "CO_FUN_06", "CO_FUN_07", "CO_FUN_08", "CO_FUN_09",
]

CI_TC_IDS = [tc for tc in VALID_TC_IDS if tc.startswith("CI_")]
CO_TC_IDS = [tc for tc in VALID_TC_IDS if tc.startswith("CO_")]

GROUPS = {
    "checkin": CI_TC_IDS,
    "checkout": CO_TC_IDS,
    "all": VALID_TC_IDS,
}


def build_pytest_args(tc_ids, report_name):
    """Build pytest command arguments for given TC_IDs."""
    marker_expr = " or ".join(tc_ids)
    report_path = os.path.join("reports", f"{report_name}_report.html")
    return [
        sys.executable, "-m", "pytest",
        "-m", marker_expr,
        "-v", "-s",
        f"--html={report_path}",
        "--self-contained-html",
    ]


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single TC:    python run_tc.py CI_FUN_01")
        print("  Multiple TCs: python run_tc.py CI_FUN_01 CI_FUN_03 CO_FUN_04")
        print("  All checkin:  python run_tc.py checkin")
        print("  All checkout: python run_tc.py checkout")
        print("  All tests:    python run_tc.py all")
        print(f"\nValid TC_IDs: {', '.join(VALID_TC_IDS)}")
        sys.exit(1)

    args = [a.strip().upper() for a in sys.argv[1:]]

    # Create reports directory if missing
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Check if it's a group keyword
    if len(args) == 1 and args[0].lower() in GROUPS:
        group_name = args[0].lower()
        tc_ids = GROUPS[group_name]
        report_name = group_name
        cmd = build_pytest_args(tc_ids, report_name)
        print(f"Running group '{group_name}' with {len(tc_ids)} TC_IDs")
    else:
        # Validate all TC_IDs
        for tc_id in args:
            if tc_id not in VALID_TC_IDS:
                print(f"Error: '{tc_id}' is not a valid TC_ID.")
                print(f"Valid TC_IDs: {', '.join(VALID_TC_IDS)}")
                print(f"Group keywords: {', '.join(GROUPS.keys())}")
                sys.exit(1)

        if len(args) == 1:
            report_name = args[0]
        else:
            report_name = "_".join(args)

        cmd = build_pytest_args(args, report_name)

    print(f"Running command: {' '.join(cmd)}")
    print("-" * 60)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
