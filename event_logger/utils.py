from datetime import datetime
from typing import TYPE_CHECKING

from loguru import logger

# A way to get types from a .pyi file.
if TYPE_CHECKING:
    from _win32typing import PyTime  # type: ignore reportMissingModuleSource


class Utils:
    """A class containing utility methods."""

    LOGGER = logger
    """Logger instance"""

    @staticmethod
    def pytime2datetime(win_dt: "PyTime") -> datetime:
        """
        Convert PyTime to datetime.

        :param win_dt: The PyTime object to be converted.
        :return: The equivalent datetime object.
        """
        return datetime(
            win_dt.year,
            win_dt.month,
            win_dt.day,
            win_dt.hour,
            win_dt.minute,
            win_dt.second,
            # Incorrect attribute name in _win32typing.
            win_dt.microsecond  # type: ignore reportAttributeAccessIssue
        )
