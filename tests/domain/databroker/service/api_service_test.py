import pytest

from domain.databroker.model.api import ApiRequest, ApiResponse
from domain.databroker.service.api import request_api, requests_api_and_store


@pytest.mark.api
def test_request_api():
    """
    APIリクエストが正常に行われているのかのテスト
    """
    request = ApiRequest(
        endpoint="https://httpbin.org/get",
        parameter={
            'p1': 'param1',
            'p2': 'param2'
        },
        header={
            'h1': 'header1',
            'h2': 'header2'
        }
    )
    response = request_api(request)
    assert isinstance(response, ApiResponse)
    assert response.status == 200
    assert response.body['url'] == 'https://httpbin.org/get?p1=param1&p2=param2'
    assert response.body['headers']['H1'] == 'header1'
    assert response.body['headers']['H2'] == 'header2'


@pytest.mark.api
def test_requests_api_and_store(databroker_api_repository, psql_client):
    """
    2つのリクエストの処理が正常に行われたかの検証
    """
    # リクエストの準備
    request1 = ApiRequest(
        endpoint="https://httpbin.org/get",
        parameter={
            'pa1': 'param1',
            'pa2': 'param2'
        },
        header={
            'ha1': 'header1',
            'ha2': 'header2'
        }
    )
    request2 = ApiRequest(
        endpoint="https://httpbin.org/get",
        parameter={
            'pb1': 'param1',
            'pb2': 'param2'
        },
        header={
            'hb1': 'header1',
            'hb2': 'header2'
        }
    )
    api_requests = [request1, request2]
    requests_api_and_store(databroker_api_repository, api_requests)
    # リクエストとレスポンスがデータベースに保存されているかの検証
    r_req = psql_client.execute('SELECT count(*) FROM databroker.api_request')
    assert r_req[0][0] == 2
    r_res = psql_client.execute('SELECT count(*) FROM databroker.api_response')
    assert r_res[0][0] == 2


@pytest.mark.api
def test_requests_api_and_store_multi_process(databroker_api_repository, psql_client):
    """
    requests_api_and_storeの並列処理オプションが機能しているのかのテスト。
    """
    # リクエストの準備
    request1 = ApiRequest(
        endpoint="https://httpbin.org/get",
        parameter={
            'pa1': 'param1',
            'pa2': 'param2'
        },
        header={
            'ha1': 'header1',
            'ha2': 'header2'
        }
    )
    request2 = ApiRequest(
        endpoint="https://httpbin.org/get",
        parameter={
            'pb1': 'param1',
            'pb2': 'param2'
        },
        header={
            'hb1': 'header1',
            'hb2': 'header2'
        }
    )
    api_requests = [request1, request2]
    requests_api_and_store(databroker_api_repository, api_requests, parallel_mode=True)
    # リクエストとレスポンスがデータベースに保存されているかの検証
    r_req = psql_client.execute('SELECT count(*) FROM databroker.api_request')
    assert r_req[0][0] == 2
    r_res = psql_client.execute('SELECT count(*) FROM databroker.api_response')
    assert r_res[0][0] == 2
