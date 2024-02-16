from infra.query.databroker.truncate import get_query_truncate_api_request, get_query_truncate_api_response
from domain.databroker.model.api import ApiRequest, ApiResponse


def test_store_request(psql_client, databroker_api_repository):
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
        SELECT id FROM databroker.api_request WHERE id = '{request_id}';
    """
    result = psql_client.execute(query_confirm_api_request)
    assert len(result) == 1


def test_store_response(psql_client, databroker_api_repository):
    """
    注意:
        api_responseの登録にはapi_requestを事前に登録する必要がある。
    """
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
    # api_responseを作成
    response_id = '4ae3bc1a-db11-14a3-8f35-75d112b8bd79'
    api_response = ApiResponse(
        request_id=request_id,
        status=200,
        header={'header_a': 'value_a'},
        body={'body_a': 'value_a'},
        id_=response_id,
        timestamp='2022-01-01 00:00:00'
    )
    # api_responseを保存
    databroker_api_repository.store_response(api_response)
    # api_requestが保存されたかの確認
    query_confirm_api_response = f"""
        SELECT id FROM databroker.api_response WHERE id = '{response_id}';
    """
    result = psql_client.execute(query_confirm_api_response)
    assert len(result) == 1


def test_store_request_and_response(psql_client, databroker_api_repository):
    # api_requestを作成
    request_id = '5473dd4e-be44-48a2-2f3b-58c99fd546c4'
    api_request = ApiRequest(
        endpoint='endpoint_a',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_=request_id,
        timestamp='2022-01-01 00:00:00'
    )
    # api_responseを作成
    response_id = '4178ccb9-bd28-a398-92a3-e38cfcb741d7'
    api_response = ApiResponse(
        request_id=request_id,
        status=200,
        header={'header_a': 'value_a'},
        body={'body_a': 'value_a'},
        id_=response_id,
        timestamp='2022-01-01 00:00:00'
    )
    # request,responseを同時に保存
    databroker_api_repository.store_request_and_response(api_request, api_response)
    # api_requestが保存されたかの確認
    query_confirm_api_request = f"""
        SELECT id FROM databroker.api_request WHERE id = '{request_id}';
    """
    result = psql_client.execute(query_confirm_api_request)
    assert len(result) == 1
    # api_requestが保存されたかの確認
    query_confirm_api_response = f"""
        SELECT id FROM databroker.api_response WHERE id = '{response_id}';
    """
    result = psql_client.execute(query_confirm_api_response)
    assert len(result) == 1
