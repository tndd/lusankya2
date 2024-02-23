import pytest

from domain.databroker.service.alpaca import chain_api_request
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
