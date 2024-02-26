from datetime import datetime, timedelta

import pytest

from domain.databroker.model.api import ApiRequest, ApiResponse
from domain.databroker.service.alpaca import (
    chain_api_request, multi_requests_todo_api_alpaca_bar)
from infra.api.alpaca.bar import QueryBar, make_request_alpaca_bar


@pytest.mark.ext
def test_chain_api_request(databroker_api_repository):
    """
    alpacaのbarデータの取得を行いテストする。
    """
    # リクエスト作成
    """
    日足、１月分のデータを取得する。

    １度の取得数を5にすることで、
    next_page_tokenによるロールオーバーを引き起こさせる。
    """
    query = QueryBar(
        symbol='AAPL',
        timeframe='1Day',
        start='2023-01-01T00:00:00Z',
        end='2023-01-31T00:00:00Z',
        limit=5,
        adjustment='raw',
        asof=None,
        feed='iex',
        currency=None,
        page_token=None,
        sort='asc'
    )
    rq = make_request_alpaca_bar(query)
    # chain_api_requestの実行
    chain_api_request(databroker_api_repository, rq, 3)
    """
    レスポンスの確認

    確認事項:
        - リクエスト回数は4個登録されていることを確認
            リクエストのループを３回で強制終了しているため、
            未実行の１回分が余計に存在するのが正しい挙動。

        - 3回分のレスポンスが実行されていることを確認する
            レスポンスの個数は、指定通り３個であるのが正しい挙動。

        - 各レスポンスのnext_page_tokenが連鎖していることも確認
            レスポンスの'next_page_token'が、
            次のリクエストの'page_token'になっていることを確認する。
    """
    # リクエスト数の確認
    r_req = databroker_api_repository.cli_db.execute(
        'SELECT * FROM databroker.api_request'
    )
    assert len(r_req) == 4
    # レスポンス数の確認
    r_res = databroker_api_repository.cli_db.execute(
        'SELECT * FROM databroker.api_response'
    )
    assert len(r_res) == 3
    # next_page_tokenのチェック
    assert r_res[0]['body']['next_page_token'] == r_req[1]['parameter']['page_token']
    assert r_res[1]['body']['next_page_token'] == r_req[2]['parameter']['page_token']
    assert r_res[2]['body']['next_page_token'] == r_req[3]['parameter']['page_token']


# @pytest.mark.ext
def test_multi_requests_todo_api_alpaca_bar(databroker_api_repository):
    """
    概要:
        登録されたリクエストから、
        実行すべきリクエストのみが抽出され実行されているのかを確認する

    登録リクエスト:
        1. 未実行
        2. 失敗
        3. 成功
        4. 失敗のち成功
        5. 失敗のち失敗
        6. 未実行（ただし無関係なエンドポイントA）
        7. 失敗（ただし無関係なエンドポイントB）

    抽出され実行されるべきリクエスト:
        1, 2, 5
    """
    # リクエストの登録１（正規エンドポイント）
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB']
    rq_ids = [
        '1c25f217-86cc-476c-90e7-fa20ff600e79',
        '4c40d425-a503-4bc1-b090-85f464287c03',
        '83797f3a-c2d0-4a07-a73f-03f85d6c219f',
        'c27b4b93-9371-4df4-8705-70e3a58e6847',
        'c67d9bb0-1c6f-44a6-9c18-441868a4f3a2'
    ]
    for id_, symbol in zip(rq_ids, symbols):
        q = QueryBar(
            symbol=symbol,
            timeframe='1Day',
            start=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT00:00:00Z'),
            end=datetime.now().strftime('%Y-%m-%dT00:00:00Z'),
            limit=5,
            adjustment='raw',
            asof=None,
            feed='iex',
            currency=None,
            page_token=None,
            sort='asc'
        )
        rq = make_request_alpaca_bar(q)
        # デバッグしやすいように固定IDにする
        rq.id_ = id_
        # リクエスト保存
        databroker_api_repository.store_request(rq)
    # リクエストの登録２（非対象エンドポイント）
    rq6 = ApiRequest(
        endpoint='https://data.lama.markets/v2/stocks/{symbol}/bar',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_='1c25f217-86cc-476c-90e7-fa20ff600e79'
    )
    rq7 = ApiRequest(
        endpoint='https://data.alpaca.markets/v1/stocks/{symbol}/bar',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_='4c40d425-a503-4bc1-b090-85f464287c03'
    )
    databroker_api_repository.store_request(rq6)
    databroker_api_repository.store_request(rq7)
    # テスト用にレスポンスを事前登録
    rs2 = ApiResponse(
        request_id=rq_ids[1],
        status=400,
        header={'header': 'h2'},
        body={'body': 'failed'}
    )
    rs3 = ApiResponse(
        request_id=rq_ids[2],
        status=200,
        header={'header': 'h3'},
        body={'body': 'succeed'}
    )
    rs4a = ApiResponse(
        request_id=rq_ids[3],
        status=400,
        header={'header': 'h4a'},
        body={'body': 'failed'}
    )
    rs4b = ApiResponse(
        request_id=rq_ids[3],
        status=200,
        header={'header': 'h4b'},
        body={'body': 'succeed'}
    )
    rs5a = ApiResponse(
        request_id=rq_ids[4],
        status=400,
        header={'header': 'h5a'},
        body={'body': 'failed'}
    )
    rs5b = ApiResponse(
        request_id=rq_ids[4],
        status=400,
        header={'header': 'h5b'},
        body={'body': 'failed'}
    )
    rs7 = ApiResponse(
        request_id=rq7.id_,
        status=400,
        header={'header': 'h7'},
        body={'body': 'failed'}
    )
    # レスポンス保存
    databroker_api_repository.store_response(rs2)
    databroker_api_repository.store_response(rs3)
    databroker_api_repository.store_response(rs4a)
    databroker_api_repository.store_response(rs4b)
    databroker_api_repository.store_response(rs5a)
    databroker_api_repository.store_response(rs5b)
    databroker_api_repository.store_response(rs7)
    """
    現状確認:
        リクエストとレスポンスが、テスト条件に従って登録されていることを確認する。
        そのために以下の２条件の観点から登録状況の確認を行う。
    条件1:
        todoリクエストとして以下のリクエストが抽出されているか
            * 1
            * 2
            * 5
            * 6
            * 7
    条件2:
        対象エンドポイントを指定した際
            * 1
            * 2
            * 5
    """
    # 条件1の確認
    requests_cond1 = databroker_api_repository.fetch_todo_requests()
    todo_request_ids = [request.id_ for request in requests_cond1]
    expect_ids_cond1 = [rq_ids[0], rq_ids[1], rq_ids[4], rq6.id_, rq7.id_]
    assert set(expect_ids_cond1) == set(todo_request_ids)
    # 条件2の確認
    endpoint = r'https://data.alpaca.markets/v2/stocks/.+/bars'
    requests_cond2 = databroker_api_repository.fetch_todo_requests(endpoint)
    todo_request_ids = [request.id_ for request in requests_cond2]
    expect_ids_cond2 = [rq_ids[0], rq_ids[1], rq_ids[4]]
    assert set(expect_ids_cond2) == set(todo_request_ids)
    # リクエストの実行
    # multi_requests_todo_api_alpaca_bar(databroker_api_repository)
    # """
    # リクエスト実行後の状態確認:
    #     リクエストが実行されたならば、1,2,5のリクエストが実行されているはずだ。
    #     リクエスト実行後、fetch_todo_requestsの結果は0となっていることが期待される。
    # """
    # assert len(databroker_api_repository.fetch_todo_requests(endpoint)) == 0
