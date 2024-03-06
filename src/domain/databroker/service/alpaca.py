from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import List, Optional

from domain.databroker.model.api import ApiRequest
from domain.databroker.repository.api import DataBrokerApiRepository
from domain.databroker.service.api import request_api
from infra.api.alpaca.common import APCA_ENDPOINT
from src.infra.api.alpaca.bar import (Timeframe_Q,
                                      convert_query_bar_to_api_request,
                                      make_query_bars_from_symbols)


def chain_api_request(
        databroker_api_repository: DataBrokerApiRepository,
        api_request: ApiRequest,
        chain_limit_num: Optional[int] = None
    ) -> None:
    """
    クエリの情報を元にAPIリクエストを作成する。
    next_page_tokenのみを書き換えて連鎖的に再実行する。

    引数:
        databroker_api_repository:
            - リクエストとレスポンスの保存用リポジトリ
        api_request:
            - 連鎖実行するAPIリクエストの火種
            - これを起点に連鎖実行を行う
        chain_limit_num:
            - 連鎖回数に制限をかける場合は、その回数を指定する。
            - Noneであれば連鎖回数は無制限。これがデフォルト動作。

    Note:
        - このメソッドはリクエストが未登録の状態でいきなり実行されることを想定している。
        - todoリクエストとして取得された登録済みリクエストとして実行されうることもあるため注意。
    """
    # 定数
    NEXT_PAGE_TOKEN = 'next_page_token'

    # これから実行するAPIリクエストの情報を保存
    databroker_api_repository.store_request(api_request)
    # 引数のrequestを元にAPIを連鎖実行
    while True:
        # データ取得
        response = request_api(api_request)
        """
        強制終了条件:
            1. レスポンスボディが存在しない
            2. next_page_tokenが存在しない
            3. next_page_tokenが空
        """
        if (
            response.body is None
            or NEXT_PAGE_TOKEN not in response.body
            or response.body[NEXT_PAGE_TOKEN] == None
        ):
            # レスポンスを保存して終了
            databroker_api_repository.store_response(response)
            break
        """
        api_requestのheaderを、取得したnext_page_tokenで更新

        注意:
            response側のbodyのトークン名'next_page_token'だが、
            request側のparameterのトークン名'page_token'であるため注意が必要。
        """
        api_request.parameter['page_token'] = response.body[NEXT_PAGE_TOKEN]
        api_request = ApiRequest(
            endpoint=api_request.endpoint,
            parameter=api_request.parameter,
            header=api_request.header,
        )
        """
        取得したレスポンスと、
        その結果を元にnext_page_tokenを更新し作成した新リクエストを保存する。

        Note:
            - これは次のリクエストの登録情報が不慮の事故で消滅する事態を予防するために必要。
            - store_request_and_responseは、本来想定された使い方である、
                "request->response"という並びではなく、
                "response->request"というペアを保存している点に注意。
        """
        databroker_api_repository.store_request_and_response(api_request, response)
        # 連鎖実行制限時、ここで処理を強制終了する必要がある
        if chain_limit_num is not None:
            chain_limit_num -= 1
            if chain_limit_num <= 0:
                break


def multi_requests_todo_api_alpaca_bar(
        repo: DataBrokerApiRepository,
        parallel_mode: bool = False
    ) -> None:
    """
    alpacaのbarエンドポイントについての未実行、あるいは失敗したリクエストを連鎖実行する。
    """
    # 対象エンドポイント絞り込み用のパターン作成
    pattern = APCA_ENDPOINT['bar'].replace('{symbol}', '.+')
    # 対象エンドポイントのリクエストを取得
    todo_bar_requests = repo.fetch_todo_requests(pattern)
    # リクエスト実行
    if parallel_mode:
        with ThreadPoolExecutor(max_workers=4) as executor:
            for request in todo_bar_requests:
                executor.submit(chain_api_request, repo, request)
    else:
        for request in todo_bar_requests:
            chain_api_request(repo, request)



def regist_schedule_bars(
        repo: DataBrokerApiRepository,
        symbols: List[str],
        timeframe: Timeframe_Q,
        start: str = (datetime.now() - timedelta(days=7*365)).strftime('%Y-%m-%dT00:00:00Z'),
        end: str = datetime.now().strftime('%Y-%m-%dT00:00:00Z'),
) -> None:
    """
    barエンドポイントのリクエストをスケジュールする。

    時間幅は、デフォルトで今日の日付から過去7年間を設定する。
    """
    # シンボルごとにクエリを作成
    query_bars = make_query_bars_from_symbols(symbols, timeframe, start, end)
    # クエリをAPIリクエストに変換
    api_requests = [
        convert_query_bar_to_api_request(query_bar)
        for query_bar in query_bars
    ]
    # APIリクエストを保存
    for api_request in api_requests:
        repo.store_request(api_request)
