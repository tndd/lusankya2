from functools import wraps

from infra.db.psql import PsqlClient
from infra.query.databroker.truncate import (get_query_truncate_api_request,
                                             get_query_truncate_api_response)


### Decorator ###
def test_only(f):
    """
    関数をテストモード時のみ実行可能にするデコレータ
    """
    @wraps(f)
    def wrapper(db_cli: PsqlClient, *args, **kwargs):
        if not db_cli.is_test_mode():
            raise ValueError("この関数はテストモード時のみ実行可能です。")
        return f(db_cli, *args, **kwargs)
    return wrapper


### Test only ###
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
