import os

# - - - Project Roots
SRC_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR: str = os.path.dirname(SRC_DIR)


class GlobalConfigs:
    """Global flags controlling application execution state."""

    DEBUG: bool = True


class LoggingConfigs:
    """Parameters governing log storage, formats, and console visualization."""

    LOG_DIR: str = os.path.join(PROJECT_DIR, "logs")
    LOG_FILE: str = "latest.txt"
    LOGGER_NAME: str = "InterviewAnalyzerLogger"
    MAX_LOG_FILES: int = 10
    LOG_COLORS: dict[str, str] = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    }
