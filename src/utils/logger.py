import logging
import os
import sys
import time
from colorlog import ColoredFormatter
from config import GlobalConfigs, LoggingConfigs


class Logger:
    _logger: logging.Logger | None = None

    # - - - Private plumbing - - -

    @staticmethod
    def _rotate_and_clean_logs() -> None:
        """Rotates the latest.txt file using a timestamp and limits the directory to 10 files."""
        os.makedirs(LoggingConfigs.LOG_DIR, exist_ok=True)
        path = os.path.join(LoggingConfigs.LOG_DIR, LoggingConfigs.LOG_FILE)

        # - - -1. Rotate current latest.txt if it exists
        if os.path.exists(path):
            timestamp = time.strftime(
                "%Y%m%d_%H%M%S", time.localtime(os.path.getctime(path))
            )
            rotated_path = os.path.join(LoggingConfigs.LOG_DIR, f"log_{timestamp}.txt")
            try:
                os.rename(path, rotated_path)
            except OSError:
                pass

        # - - - 2. Enforce the 10-file maximum limit
        all_files = [
            os.path.join(LoggingConfigs.LOG_DIR, f)
            for f in os.listdir(LoggingConfigs.LOG_DIR)
            if f.endswith(".txt")
        ]
        # - - - Sort by creation time (oldest first)
        all_files.sort(key=os.path.getmtime)

        # - - - If we exceed the max limit, delete the oldest historical files
        while len(all_files) > LoggingConfigs.MAX_LOG_FILES:
            oldest_file = all_files.pop(0)
            try:
                os.remove(oldest_file)
            except OSError:
                pass

    @staticmethod
    def _setup_logger() -> logging.Logger:
        if Logger._logger:
            return Logger._logger

        Logger._rotate_and_clean_logs()
        path = os.path.join(LoggingConfigs.LOG_DIR, LoggingConfigs.LOG_FILE)

        logger = logging.getLogger(LoggingConfigs.LOGGER_NAME)
        logger.setLevel(logging.DEBUG if GlobalConfigs.DEBUG else logging.INFO)
        logger.handlers.clear()

        # - - - Console (Colored output)
        console_formatter = ColoredFormatter(
            "%(log_color)s[%(levelname)s]%(reset)s %(message)s",
            log_colors=LoggingConfigs.LOG_COLORS,
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # - - - File (Standard output to latest.txt)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        Logger._logger = logger
        return logger

    # - - - Public Usage Interface - - -

    @staticmethod
    def log_debug(MESSAGE: str) -> None:
        """
        Logs a message if Debug is enabled

        Args:
            MESSAGE (str): The message to be logged
        """
        if GlobalConfigs.DEBUG:
            Logger._setup_logger().debug(MESSAGE)

    @staticmethod
    def log_info(MESSAGE: str) -> None:
        """
        Logs a message, use for generic Info, success messages

        Args:
            MESSAGE (str): The message to be logged
        """
        Logger._setup_logger().info(MESSAGE)

    @staticmethod
    def log_warn(MESSAGE: str) -> None:
        """
        Logs a message, use for warnings, which may or may not become errors

        Args:
            MESSAGE (str): The message to be logged
        """
        Logger._setup_logger().warning(MESSAGE)

    @staticmethod
    def log_error(MESSAGE: str) -> None:
        """
        Logs a message, used for errors committed

        Args:
            MESSAGE (str): The message to be logged
        """
        Logger._setup_logger().error(MESSAGE)

    @staticmethod
    def log_fatal(MESSAGE: str) -> None:
        """
        Logs a message, used for errors which shouldnt be possible, very very hazardous, or unrecoverable

        Args:
            MESSAGE (str): The message to be logged
        """
        Logger._setup_logger().critical(MESSAGE)
