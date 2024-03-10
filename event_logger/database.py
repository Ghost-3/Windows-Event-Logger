import sys

from clickhouse_connect import get_client
from clickhouse_connect.driver.exceptions import ClickHouseError

from .event import Event
from .utils import Utils


class DataBase:
    def __init__(self, host: str, port: int, username: str, password: str, database: str, table: str) -> None:
        """
        Initialize the DataBase class.

        :param host: The host name of the database.
        :param port: The port number for the database connection.
        :param username: The username for accessing the database.
        :param password: The password for the specified username.
        :param database: The name of the database to connect to.
        :param table: The name of the table in the database.
        """
        Utils.LOGGER.info("Init database connection")
        Utils.LOGGER.debug(
            f"Connect to database with: (host: {host}:{port}, "
            f"username: {username}, database: {database}, table: {table})"
        )
        try:
            self._client = get_client(host=host, port=port, username=username, password=password)
        except ClickHouseError as e:
            Utils.LOGGER.error(f"{type(e)}: {e}")
            sys.exit(-1)

        self._database = database
        self._table = table

        self._create_database()
        self._create_table()

    @property
    def max_record_number(self) -> int:
        """
        Get the maximum record number from the database table.

        :return: The maximum record number.
        """
        return self._client.query(f"select max(record_number) from {self._database}.{self._table}").first_item.get(
            "max(record_number)", 0
        )

    def _create_database(self) -> None:
        """Create a database if it does not exist."""
        Utils.LOGGER.debug(f"Create database if not exists with: (name: {self._database})")
        self._client.query("CREATE DATABASE IF NOT EXISTS main;")

    def _create_table(self) -> None:
        """Create a table in the database if it does not exist."""
        Utils.LOGGER.debug(f"Create table if not exists with: (name: {self._table})")
        self._client.query(
            f"CREATE TABLE IF NOT EXISTS {self._database}.{self._table} (\n"
            "    closing_record_number UInt32,\n"
            "    computer_name         String,\n"
            "    data                  String NULL,\n"
            "    event_category        UInt32,\n"
            "    event_id              UInt32,\n"
            "    event_type            UInt32,\n"
            "    record_number         UInt32,\n"
            "    reserved              UInt32,\n"
            "    reserved_flags        UInt32,\n"
            "    sid                   String NULL,\n"
            "    source_name           String,\n"
            "    string_inserts        String NULL,\n"
            "    time_generated        DateTime,\n"
            "    time_written          DateTime)\n"
            "ENGINE = MergeTree()\n"
            "ORDER BY (record_number);"
        )

    def _event_to_insert(self, event: Event) -> str:
        """
        Convert an event into an SQL insert statement.

        :param event: The event to be inserted.

        :return: The SQL insert statement.
        """
        data = f"'{event.data}'" if event.data else "NULL"
        sid = f"'{event.sid}'" if event.sid else "NULL"
        string_inserts = f"'{' | '.join(event.string_inserts)}'" if event.string_inserts else "NULL"

        return (
            f"INSERT INTO {self._database}.{self._table}\n"
            f"VALUES ("
            f"{event.closing_record_number}, "
            f"'{event.computer_name}', "
            f"{data}, "
            f"{event.event_category}, "
            f"{event.event_id}, "
            f"{event.event_type}, "
            f"{event.record_number}, "
            f"{event.reserved}, "
            f"{event.reserved_flags}, "
            f"{sid}, "
            f"'{event.source_name}', "
            f"{string_inserts}, "
            f"'{event.time_generated}', "
            f"'{event.time_written}');"
        )

    def insert_event(self, event: Event) -> None:
        """
        Insert an event into the database.

        :param event: The event to be inserted.
        """
        Utils.LOGGER.info(f"Insert event: {event.record_number}")
        self._client.query(self._event_to_insert(event))
