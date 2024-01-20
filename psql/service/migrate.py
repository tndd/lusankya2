from typing import List

from infra.psql.client import PsqlClient
from infra.psql.service.load_query import Command, Schema, load_query


def migrate(cli: PsqlClient):
    q = queries_extension() + queries_schema() + queries_table() + queries_view()
    cli.execute_queries(q)


def queries_extension() -> List[str]:
    return [
        load_query(Schema.DATABROKER, Command.CREATE, 'extension_uuid')
    ]


def queries_schema() -> List[str]:
    return [
        load_query(Schema.DATABROKER, Command.CREATE, 'schema_dataflow'),
        load_query(Schema.ALPACA, Command.CREATE, 'schema_alpaca')
    ]


def queries_table() -> List[str]:
    return [
        load_query(Schema.DATABROKER, Command.CREATE, 'table_api_request'),
        load_query(Schema.DATABROKER, Command.CREATE, 'table_api_response'),
        load_query(Schema.ALPACA, Command.CREATE, 'table_bar')
    ]


def queries_view() -> List[str]:
    return [
        load_query(Schema.DATABROKER, Command.CREATE, 'view_latest_api_response'),
    ]
