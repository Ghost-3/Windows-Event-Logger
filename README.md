# Windows Event Logger

Данный проект представляет собой программу для чтения журнала событий Windows и отправки логов в базу данных.

Проект разработан на Python 3.12 под базу данных ClickHouse 24.3.1.537.

## Установка

Клонируйте репозиторий с помощью команды:

```sh
git clone https://github.com/Ghost-3/Windows-Event-Logger.git
```

Установите необходимые зависимости с помощью команды:

```sh
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` для хранения конфигурационных переменных.
Добавьте в файл `.env` следующие переменные и укажите соответствующие значения:
```ini
LOG_FILE_PATH=app.log
LOG_LEVEL=INFO
LOG_FILE_ROTATION=50 MB

DB_HOST=localhost
DB_PORT=8123
DB_USERNAME=default
DB_PASSWORD=
DB_DATABASE_NAME=default
DB_TABLE_NAME=event_log

EVENT_LOG_SERVER=localhost
EVENT_LOG_LOG_TYPE=Security
```

## Использование

Запустите программу с помощью команды:

```sh
python main.py
```

Программа начнёт чтение логов из журнала событий Windows и отправку их в указанную базу данных.
