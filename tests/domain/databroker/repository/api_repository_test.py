from infra.query.databroker.truncate import get_query_truncate_api_request
from domain.databroker.model.api import ApiRequest


def test_store_request(psql_client, databroker_api_repository):
    # api_requestのテーブルを初期化
    query_truncate_api_request = get_query_truncate_api_request()
    psql_client.execute(query_truncate_api_request)
    # api_requestを作成
    request_id = 'b90287e9-5478-f434-8eff-20613ae0d1c1'
    api_request = ApiRequest(
        endpoint='endpoint_a',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_=request_id,
        timestamp='2022-01-01 00:00:00'
    )
    # api_requestを保存
    databroker_api_repository.store_request(api_request)
    # api_requestが保存されたかの確認
    query_confirm_api_request = f"""
        SELECT id FROM api_request WHERE id = '{request_id}';
    """
    result = psql_client.execute(query_confirm_api_request)
    assert result.fetchone() is not None

