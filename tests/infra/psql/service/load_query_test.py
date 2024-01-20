from infra.psql.service.load_query import Command, Schema, load_query


def test_load_query():
    query = load_query(Schema.DATABROKER, Command.CREATE, 'schema_databroker')
    assert query == 'CREATE SCHEMA IF NOT EXISTS databroker AUTHORIZATION postgres;'