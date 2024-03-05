import pytest

from domain.databroker.model.api import ApiRequest, ApiResponse
from domain.databroker.service.api import (multi_requests_api_and_store,
                                           multi_requests_todo_api_and_store,
                                           request_api)


@pytest.mark.ext
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
    assert response.body is not None
    assert response.body['url'] == 'https://httpbin.org/get?p1=param1&p2=param2'
    assert response.body['headers']['H1'] == 'header1'
    assert response.body['headers']['H2'] == 'header2'


@pytest.mark.ext
def test_multi_requests_api_and_store(databroker_api_repository):
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
    multi_requests_api_and_store(databroker_api_repository, api_requests)
    # リクエストとレスポンスがデータベースに保存されているかの検証
    r_req = databroker_api_repository.cli_db.execute('SELECT count(*) FROM databroker.api_request')
    assert r_req[0][0] == 2
    r_res = databroker_api_repository.cli_db.execute('SELECT count(*) FROM databroker.api_response')
    assert r_res[0][0] == 2


@pytest.mark.ext
def test_multi_requests_api_and_store_parallel(databroker_api_repository):
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
    multi_requests_api_and_store(databroker_api_repository, api_requests, parallel_mode=True)
    # リクエストとレスポンスがデータベースに保存されているかの検証
    r_req = databroker_api_repository.cli_db.execute('SELECT count(*) FROM databroker.api_request')
    assert r_req[0][0] == 2
    r_res = databroker_api_repository.cli_db.execute('SELECT count(*) FROM databroker.api_response')
    assert r_res[0][0] == 2


@pytest.mark.ext
def test_multi_requests_todo_api_and_store(databroker_api_repository):
    """
    概要:
        登録した条件から適切なリクエストのみが抽出され実行されたかのテスト

    条件:
        1. 未実行リクエスト
        2. 成功リクエスト
        3. 失敗リクエスト
        4. 失敗後、成功したリクエスト

     期待結果:
        1, 3のリクエストのみが実行される。
    """
    # リクエストの登録
    rq1 = ApiRequest(
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
    rq2 = ApiRequest(
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
    rq3 = ApiRequest(
        endpoint="https://httpbin.org/get",
        parameter={
            'pc1': 'param1',
            'pc2': 'param2'
        },
        header={
            'hc1': 'header1',
            'hc2': 'header2'
        }
    )
    rq4 = ApiRequest(
        endpoint="https://httpbin.org/get",
        parameter={
            'pd1': 'param1',
            'pd2': 'param2'
        },
        header={
            'hd1': 'header1',
            'hd2': 'header2'
        }
    )
    databroker_api_repository.store_request(rq1)
    databroker_api_repository.store_request(rq2)
    databroker_api_repository.store_request(rq3)
    databroker_api_repository.store_request(rq4)
    # レスポンスの登録
    rs2_success = ApiResponse(
        request_id=rq2.id_,
        status=200,
        header={},
        body={}
    )
    rs3_failed = ApiResponse(
        request_id=rq3.id_,
        status=400,
        header={},
        body={}
    )
    rs4_1_failed = ApiResponse(
        request_id=rq4.id_,
        status=400,
        header={},
        body={}
    )
    rs4_2_success = ApiResponse(
        request_id=rq4.id_,
        status=200,
        header={},
        body={}
    )
    databroker_api_repository.store_response(rs2_success)
    databroker_api_repository.store_response(rs3_failed)
    databroker_api_repository.store_response(rs4_1_failed)
    databroker_api_repository.store_response(rs4_2_success)
    # リクエストの実行
    multi_requests_todo_api_and_store(databroker_api_repository)
    """
    リクエストの結果確認

    確認事項:
        rs1:
            - １つのレスポンスが登録されている
            - （実行された１つ分）
        rs2:
            - １つのレスポンスが登録されている
            - （事前登録された成功分）
        rs3:
            - ２つのレスポンスが登録されている
            - （事前に登録した失敗分と、実行された成功分）
        rs4:
            - ２つのレスポンスが登録されている
            - （事前登録された失敗分および成功分の２つ）
    """
    r_rs1 = databroker_api_repository.cli_db.execute(
        f"SELECT count(*) FROM databroker.api_response where request_id = '{rq1.id_}'"
    )
    assert r_rs1[0][0] == 1
    r_rs2 = databroker_api_repository.cli_db.execute(
        f"SELECT count(*) FROM databroker.api_response where request_id = '{rq2.id_}'"
    )
    assert r_rs2[0][0] == 1
    r_rs3 = databroker_api_repository.cli_db.execute(
        f"SELECT count(*) FROM databroker.api_response where request_id = '{rq3.id_}'"
    )
    assert r_rs3[0][0] == 2
    r_rs4 = databroker_api_repository.cli_db.execute(
        f"SELECT count(*) FROM databroker.api_response where request_id = '{rq4.id_}'"
    )
    assert r_rs4[0][0] == 2
