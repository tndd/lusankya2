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


def multi_requests_api_and_store(
        repo: DataBrokerApiRepository,
        api_requests: List[ApiRequest],
        parallel_mode: bool = False
    ) -> None:
    """
    APIリクエストの内容を実行し、リクエストとその結果の保存を行う。

    parallel_modeが有効な場合、並列で処理が実行される。
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
    # 条件に応じてプロセス数を決定
    n_max_worker = 4
    n_process = 1
    if parallel_mode:
        n_process = min(len(api_requests), n_max_worker)
    # 処理
    with ThreadPoolExecutor(max_workers=n_process) as executor:
        for i in range(n_process):
            chunk_requests = api_requests[i::n_process]
            executor.submit(_serial_requests_api_and_store, repo, chunk_requests)


def multi_requests_todo_api_and_store(
        repo: DataBrokerApiRepository,
        parallel_mode: bool = False
    ) -> None:
    """
    未実行あるいは失敗したAPIの実行と保存を行う。

    並列処理モードも搭載されているが、基本的にはシリアル形式で実行する。
    """
    todo_requests = repo.fetch_todo_requests()
    multi_requests_api_and_store(repo, todo_requests, parallel_mode)
