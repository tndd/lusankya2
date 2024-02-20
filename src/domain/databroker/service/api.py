from concurrent.futures import ThreadPoolExecutor
from typing import List

from requests import get

from domain.databroker.model.api import ApiRequest, ApiResponse
from domain.databroker.repository.api import DataBrokerApiRepository


def request_api(api_request: ApiRequest) -> ApiResponse:
    """
    APIリクエストを実行し、レスポンスを返す。
    """
    response = get(
        api_request.endpoint,
        params=api_request.parameter,
        headers=api_request.header
    )
    return ApiResponse(
        request_id=api_request.id_,
        status=response.status_code,
        header=dict(response.headers),
        body=response.json()
    )


def requests_api_and_store(
        repo: DataBrokerApiRepository,
        api_requests: List[ApiRequest],
        n_max_worker: int = 1
    ) -> None:
    """
    APIリクエストの内容を実行し、リクエストとその結果の保存を行う。

    n_max_workerを1以外に指定すると、並列で処理が実行される。
    """
    def _serial_requests_api_and_store(
            repo: DataBrokerApiRepository,
            api_requests: List[ApiRequest]
    ) -> None:
        """
        単純な、リクエストを実行し結果を保存する関数。
        これを呼び出し側で利用することで並列処理を実現する。
        """
        for req in api_requests:
            res = request_api(req)
            repo.store_request_and_response(req, res)
    # api_requestsをスレッド数に応じて分割
    with ThreadPoolExecutor(max_workers=n_max_worker) as executor:
        for i in range(n_max_worker):
            chunk_requests = api_requests[i::n_max_worker]
            executor.submit(_serial_requests_api_and_store, repo, chunk_requests)


def multi_requests_todo_api(repo: DataBrokerApiRepository) -> None:
    """
    未実行あるいは失敗したAPIの実行を行う。
    """
    todo_requests = repo.fetch_todo_requests()
    requests_api_and_store(repo, todo_requests)
