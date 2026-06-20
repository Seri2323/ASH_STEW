import sys
from config import GlobalConfigs
from utils.logger import Logger


class DevTools:
    """Provides internal contract validations and code diagnostics."""

    @staticmethod
    def assert_that(CONDITION: bool, MESSAGE: str = "") -> None:
        """
        Validates operational assumptions during debug mode executions.

        Args:
            CONDITIONS (bool): the condition that ought to be true
            MESSAGE (str): Optional message to be logged, in case the condition is false

        Raises:
            AssertionError: If condition evaluates to False.
        """
        if GlobalConfigs.DEBUG and not CONDITION:
            Logger.log_fatal(f"Assertion failed: {MESSAGE}")
            raise AssertionError(MESSAGE)

    @staticmethod
    def todo(MESSAGE: str = "Not implemented") -> None:
        """
        Acts as a compilation/runtime placeholder for unmapped logical sections.

        Args:
            MESSAGE (str): Optional message to be logged in case runtime hits todo
        """
        Logger.log_fatal(f"TODO: {MESSAGE}")
        sys.exit(1)

    @staticmethod
    def type_check(VARIABLE: object, EXPECTED_TYPE: type) -> None:
        """
        Enforces runtime type-safety evaluations during development phases.

        Args:
            VARIABLE (object): The object whose type is to be checked
            EXPECTED_TYPE (type): The type which the object ought to be
        """
        if not GlobalConfigs.DEBUG:
            return

        if isinstance(VARIABLE, EXPECTED_TYPE):
            return

        # - - - Abstract int matching standard float properties seamlessly
        if EXPECTED_TYPE is float and isinstance(VARIABLE, int):
            return

        Logger.log_error(
            f"TypeCheck failed: Expected {EXPECTED_TYPE.__name__}, "
            f"got {type(VARIABLE).__name__}"
        )
        sys.exit(1)
