from infra.db.psql import PsqlClient
from infra.query.databroker.truncate import (
    get_query_truncate_api_request,
    get_query_truncate_api_response
)
from tests._test_service.decorator import test_only


@test_only
def clear_tables(db_cli: PsqlClient):
    """
    全てのテーブルの初期化
    """
    clear_tables_databroker(db_cli)


@test_only
def clear_tables_databroker(db_cli: PsqlClient):
    """
    databrokerにまつわるテーブルを全てtruncateする。
    """
    queries_truncate = [
        get_query_truncate_api_response() +
        get_query_truncate_api_request()
    ]
    db_cli.execute_queries(queries_truncate)
