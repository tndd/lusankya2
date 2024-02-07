def test_execute(psql_client):
    """
    以下２点の要素を確認する。
        1. 単発のクエリを実行出来ていること
        2. クエリの結果が取得できていること
    """
    assert psql_client.execute('SELECT 1') == [(1,)]


def test_execute_queries(psql_client):
    table_name_a = 'afxntedq'
    table_name_b = 'svknpbmf'
    table_name_c = 'dnavrupe'
    try:
        # テスト用のテーブルの作成
        queries_with_params = [
            (f"CREATE TABLE IF NOT EXISTS {table_name_a} (column1 varchar(255), column2 varchar(255))", ()),
            (f"CREATE TABLE IF NOT EXISTS {table_name_b} (column1 varchar(255), column2 varchar(255))", ()),
            (f"CREATE TABLE IF NOT EXISTS {table_name_c} (column1 varchar(255), column2 varchar(255))", ())
        ]
        psql_client.execute_queries(queries_with_params)
        # テーブルが正しく作成されたことを確認
        for table_name in [table_name_a, table_name_b, table_name_c]:
            rows = psql_client.execute(f"SELECT to_regclass('{table_name}')")
            assert rows[0][0] == table_name
    finally:
        # テスト用テーブルは必ず削除しておく
        psql_client.execute(f"DROP TABLE IF EXISTS {table_name_a}")
        psql_client.execute(f"DROP TABLE IF EXISTS {table_name_b}")
        psql_client.execute(f"DROP TABLE IF EXISTS {table_name_c}")


def test_executemany(psql_client):
    table_name = 'usksxcdw'
    try:
        # テスト用の一時的なテーブルを作成
        psql_client.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (column1 varchar(255), column2 varchar(255))")
        # テスト用投入データを作成
        query = f"INSERT INTO {table_name} (column1, column2) VALUES (%s, %s)"
        data = [(f"value1_{i}", f"value2_{i}") for i in range(10)]
        # executemanyの動作確認
        assert psql_client.executemany(query, data) == None
        # テーブルにデータが入っていることを確認
        rows = psql_client.execute(f'select * from {table_name}')
        assert len(rows) == 10
    finally:
        # テスト用テーブルは必ず削除しておく
        psql_client.execute(f"DROP TABLE IF EXISTS {table_name}")


def test_parallel_executemany(psql_client):
    table_name = 'crtdzgur'
    try:
        # テスト用の一時的なテーブルを作成
        psql_client.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (column1 varchar(255), column2 varchar(255))")
        # テスト用投入データを作成
        query = f"INSERT INTO {table_name} (column1, column2) VALUES (%s, %s)"
        data = [(f"value1_{i}", f"value2_{i}") for i in range(10)]
        # parallel_executemanyの動作確認
        assert psql_client.parallel_executemany(query, data) == None
        # テーブルにデータが入っていることを確認
        rows = psql_client.execute(f'select * from {table_name}')
        assert len(rows) == 10
    finally:
        # テスト用テーブルは必ず削除しておく
        psql_client.execute(f"DROP TABLE IF EXISTS {table_name}")
