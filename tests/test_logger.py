import os
import sys
import time

# 1. Fix python path so the test script can find the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from config import LoggingConfigs
from utils.logger import Logger


def test_logger_functionality():
    print("--- Running Logger Formatting Test ---")
    Logger.log_info("Testing standard info message.")
    Logger.log_debug("Testing debug message (visible if GlobalConfigs.DEBUG is True).")
    Logger.log_warn("Testing a warning alert.")
    Logger.log_error("Testing a caught exception error state.")

    print("\n--- Running Log Rotation and 10-File Limit Test ---")
    print(f"Simulating multiple sessions to verify file cap...")

    # We run a loop 12 times. This should create 1 'latest.txt' and 11 backups.
    # Because our limit is 10, the oldest 2 backups should be automatically deleted.
    for i in range(12):
        print(f"  Simulating application boot cycle #{i + 1}...")

        # Reset the singleton internal logger variable to force a fresh boot cycle sequence
        Logger._logger = None
        Logger.log_info(f"Log data generated during simulated session #{i + 1}")

        # Sleep briefly so the operating system records slightly different modification timestamps
        time.sleep(0.1)

    # 2. Count the files left in the directory to verify success
    log_files = [
        f
        for f in os.listdir(LoggingConfigs.LOG_DIR)
        if f.endswith(".txt") or f.endswith(".log")
    ]

    print("\n--- Test Verification Results ---")
    print(f"Total log files found in directory: {len(log_files)}")
    print(f"Expected limit: {LoggingConfigs.MAX_LOG_FILES}")
    print("\nFiles currently in logs folder:")
    for file in sorted(log_files):
        print(f" - {file}")

    if len(log_files) <= LoggingConfigs.MAX_LOG_FILES:
        print("\n SUCCESS: Log file count is strictly controlled and capped!")
    else:
        print("\n FAILURE: Log rotation allowed too many files to accumulate.")


if __name__ == "__main__":
    test_logger_functionality()
