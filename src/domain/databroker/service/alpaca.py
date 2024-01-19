from domain.databroker.model.api import ApiRequest
from domain.databroker.repository import DataBrokerApiRepository
from infra.api.alpaca.bar import ENDPOINT as EP_APCA_BAR


def chain_request(api_request: ApiRequest) -> None:
    """
    クエリの情報を元にAPIリクエストを作成する。
    next_page_tokenのみを書き換えて連鎖的に再実行する。
    """
    # TODO
    pass


def multi_requests_todo_api_alpaca_bar(
        rp: DataBrokerApiRepository,
        n_max_worker: int = 8
    ) -> None:
    """
    alpacaのbarエンドポイントについての未実行、あるいは失敗したリクエストを連鎖実行する。
    """
    todo_bar_requests = rp.fetch_todo_requests_for_endpoint(EP_APCA_BAR)
    # TODO 並列実行
    for request in todo_bar_requests:
        chain_request(request)
