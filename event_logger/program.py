import os
import sys
from pathlib import Path
from warnings import warn

from dotenv import load_dotenv

from .database import DataBase
from .event_logger import EventLogger
from .utils import Utils


class Program:
    def __init__(self) -> None:
        """
        Initialize the program by loading environment variables from a .env file if it exists.

        If the file does not exist, a warning is issued.
        """
        file_path = Path(__file__) / ".." / ".." / ".env"
        if file_path.exists():
            load_dotenv(file_path)
        else:
            warn(".env file does not exist", stacklevel=1)

        loguru_config = {
            "log_file_path": os.getenv("LOG_FILE_PATH", "app.log"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "log_file_rotation": os.getenv("LOG_FILE_ROTATION", "50 MB"),
        }

        database_config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "0")),
            "username": os.getenv("DB_USERNAME"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_DATABASE_NAME"),
            "table": os.getenv("DB_TABLE_NAME"),
        }

        event_logger_config = {
            "server": os.getenv("EVENT_LOG_SERVER"),
            "log_type": os.getenv("EVENT_LOG_LOG_TYPE", "Security")
        }

        self._init_loguru(**loguru_config)
        Utils.LOGGER.info("Init program")
        self._event_logger = EventLogger(**event_logger_config)
        self._database = DataBase(**database_config)

    @staticmethod
    def _init_loguru(log_file_path: str, log_level: str, log_file_rotation: str) -> None:
        """
        Initialize the loguru logger with the specified parameters.

        :param log_file_path: The path for the log file.
        :param log_level: The logging level.
        :param log_file_rotation: The log file rotation scheme.
        """
        Utils.LOGGER.remove()
        # The argument type is always correct.
        Utils.LOGGER.add(sys.stderr, level=log_level)
        Utils.LOGGER.add(log_file_path, level=log_level, rotation=log_file_rotation)

    def run(self) -> None:
        """Run the program by triggering the event logger with the database."""
        self._event_logger.run(self._database)
