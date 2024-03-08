from functools import wraps

from infra.db.psql import PsqlClient


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
    全ての対象テーブルの初期化を行う
    """
    # 対象スキーマの指定
    target_tables = [
        'databroker',
        'alpaca'
    ]
    for table_name in target_tables:
        clear_tables_by_schema(db_cli, table_name)


@test_only
def clear_tables_by_schema(db_cli: PsqlClient, schema: str):
    """
    指定スキーマのテーブルをすべてtruncateする。
    """
    query_get_tables = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' AND table_type = 'BASE TABLE';"
    tables = db_cli.execute(query_get_tables)
    # スキーマ名を動的に挿入するように修正
    queries_truncate = [f"TRUNCATE TABLE {schema}.{table[0]} CASCADE;" for table in tables]
    db_cli.execute_queries(queries_truncate)
