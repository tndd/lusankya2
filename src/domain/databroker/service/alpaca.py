from domain.databroker.model.api import ApiRequest
from domain.databroker.repository.api import DataBrokerApiRepository
from domain.databroker.service.api import request_api
from infra.api.alpaca.bar import ENDPOINT as EP_APCA_BAR


def chain_request(
        rp: DataBrokerApiRepository,
        request: ApiRequest
    ) -> None:
    """
    クエリの情報を元にAPIリクエストを作成する。
    next_page_tokenのみを書き換えて連鎖的に再実行する。

    Note:
        - このメソッドはリクエストが未登録の状態でいきなり実行されることを想定している。
        - todoリクエストとして取得された登録済みリクエストとして実行されうることもあるため注意。
    """
    NEXT_PAGE_TOKEN = 'next_page_token'
    # これから実行するAPIリクエストの情報を保存
    rp.store_request(request)
    # 引数のrequestを元にAPIを連鎖実行
    while True:
        # データ取得
        response = request_api(request)
        # 次のページ(next_page_token)がない場合は終了
        if not NEXT_PAGE_TOKEN in response.body:
            break
        # api_requestのnext_page_tokenを更新して再実行
        request.body[NEXT_PAGE_TOKEN] = response.body[NEXT_PAGE_TOKEN]
        """
        取得したレスポンスと、
        その結果を元にnext_page_tokenを更新し作成した新リクエストを保存する。

        Note:
            - これは次のリクエストの登録情報が不慮の事故で消滅する事態を予防するために必要。
            - store_request_and_responseは、本来想定された使い方である
                "request->response"という並びではなく、
                "response->request"というペアを保存している点に注意。
        """
        rp.store_request_and_response(request, response)


def multi_requests_todo_api_alpaca_bar(
        rp: DataBrokerApiRepository,
        n_max_worker: int = 8
    ) -> None:
    """
    alpacaのbarエンドポイントについての未実行、あるいは失敗したリクエストを連鎖実行する。
    """
    todo_bar_requests = rp.fetch_todo_requests_by_endpoint(EP_APCA_BAR)
    # TODO 並列実行
    for request in todo_bar_requests:
        chain_request(request)
