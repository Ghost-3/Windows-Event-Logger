
from event_logger import Program

# .env file example
"""
LOG_FILE_PATH=app.log
LOG_LEVEL=INFO
LOG_FILE_ROTATION=50 MB

DB_HOST=localhost
DB_PORT=8123
DB_USERNAME=default
DB_PASSWORD=root
DB_DATABASE_NAME=default
DB_TABLE_NAME=event_log

EVENT_LOG_SERVER=localhost
EVENT_LOG_LOG_TYPE=Security
"""


if __name__ == "__main__":
    Program().run()
