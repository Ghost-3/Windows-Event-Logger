from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional

# A way to get types from a .pyi file.
if TYPE_CHECKING:
    from _win32typing import PySID  # type: ignore reportMissingModuleSource


@dataclass
class EventData:
    """A class to represent event data."""

    closing_record_number: int
    computer_name: str
    data: Optional[str]
    event_category: int
    event_id: int
    event_type: int
    record_number: int
    reserved: int
    reserved_flags: int
    sid: Optional["PySID"]
    source_name: str
    string_inserts: Optional[tuple[str, ...]]
    time_generated: datetime
    time_written: datetime
