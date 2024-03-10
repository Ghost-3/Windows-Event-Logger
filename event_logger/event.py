from typing import TYPE_CHECKING

from .data_types import EventData
from .utils import Utils

# A way to get types from a .pyi file.
if TYPE_CHECKING:
    from _win32typing import PyEventLogRecord  # type: ignore reportMissingModuleSource


class Event(EventData):
    def __init__(self, event: "PyEventLogRecord") -> None:
        """
        Initialize the Event object with data from PyEventLogRecord.

        :param event: The PyEventLogRecord object containing event data.
        """
        super().__init__(
            event.ClosingRecordNumber,
            event.ComputerName,
            str(event.Data) if event.Data else None,
            event.EventCategory,
            event.EventID,
            event.EventType,
            event.RecordNumber,
            event.Reserved,
            event.ReservedFlags,
            event.Sid,
            event.SourceName,
            event.StringInserts,
            Utils.pytime2datetime(event.TimeGenerated),
            Utils.pytime2datetime(event.TimeWritten),
        )
