import sys
from typing import TYPE_CHECKING

from win32evtlog import (
    EVENTLOG_FORWARDS_READ,
    EVENTLOG_SEEK_READ,
    EVENTLOG_SEQUENTIAL_READ,
    OpenEventLog,
    ReadEventLog,
)

from .database import DataBase
from .event import Event
from .utils import Utils

# A way to get types from a .pyi file.
if TYPE_CHECKING:
    from _win32typing import PyEventLogRecord, PyEVTLOG_HANDLE  # type: ignore reportMissingModuleSource


class EventLogger:
    """Class for logging events."""

    INIT_FLAGS: int = EVENTLOG_FORWARDS_READ | EVENTLOG_SEQUENTIAL_READ
    """Flags for initializing event log."""

    DEFAULT_FLAGS: int = EVENTLOG_FORWARDS_READ | EVENTLOG_SEEK_READ
    """Default flags for event log."""

    def __init__(self, server: str, log_type: str) -> None:
        """
        Initialize EventLogger.

        :param server: The server name.
        :param log_type: The type of log.
        """
        Utils.LOGGER.info("Init event logger")
        Utils.LOGGER.debug(f"Open event log with: (server: {server}, log_type: {log_type})")
        try:
            self.hand: "PyEVTLOG_HANDLE" = OpenEventLog(server, log_type)
        # Unable to use the error type from _win32typing.
        except Exception as e:  # noqa: BLE001
            args_len = 3
            if e.args and len(e.args) == args_len:
                error_id, error_name, error_desc = e.args
                Utils.LOGGER.error(f"<{error_id} '{error_name}'>: {error_desc}")
            else:
                Utils.LOGGER.error(f"{type(e)}: {e}")
            sys.exit(-1)

    def _get_raw_events(self, flags: int, offset: int) -> list["PyEventLogRecord"]:
        """
        Get raw events from the event log.

        :param flags: Flags for reading event log.
        :param offset: The offset for reading event log.

        :return: List of raw event log records.
        """
        try:
            return ReadEventLog(self.hand, flags, offset)
        # Unable to use the error type from _win32typing.
        except Exception as e:  # noqa: BLE001
            error_id = 87
            if e.args[0] == error_id:  # reinit if last record number not in log
                Utils.LOGGER.debug("Unable to read event log. Try to reinit...")
                return self._get_raw_events(self.INIT_FLAGS, 0)
            return list()

    def _get_new_events(self, database: DataBase) -> tuple[Event, ...]:
        """
        Get new events from the event log.

        :param database: The database to compare and fetch new events.

        :return: Tuple of new events.
        """
        offset: int = database.max_record_number
        Utils.LOGGER.debug(f"offset from DB: {offset}")
        flags: int = self.INIT_FLAGS if offset == 0 else self.DEFAULT_FLAGS

        events: list["PyEventLogRecord"] = self._get_raw_events(flags, offset)

        if not events:
            return tuple()

        if flags == self.DEFAULT_FLAGS:
            events.pop(0)  # Skips an already logged event

        return tuple(map(Event, events))

    def run(self, database: DataBase) -> None:
        """
        Start event logger and continuously fetch new events.

        :param database: The database to store the events.
        """
        Utils.LOGGER.info("Start event logger")
        try:
            while True:
                for event in self._get_new_events(database):
                    database.insert_event(event)
        except KeyboardInterrupt:
            pass
        # Top-level exception logger.
        except Exception as idf:  # noqa: BLE001
            Utils.LOGGER.error(f"{type(idf)}: {idf}")
            self.run()
