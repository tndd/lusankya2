from enum import Enum
from os.path import abspath, dirname


class Schema(str, Enum):
    DATABROKER = "databroker"
    ALPACA = "alpaca"


class Command(str, Enum):
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    CREATE = "create"
    DROP = "drop"


def load_query(schema: Schema, command: Command, name: str) -> str:
    QUERY_DIR = "query"
    current_dir = dirname(abspath(__file__))
    infra_dir = dirname(current_dir)

    with open(f'{infra_dir}/{QUERY_DIR}/{schema.value}/{command.value}/{name}.sql', 'r') as file:
        query = file.read()
    return query
