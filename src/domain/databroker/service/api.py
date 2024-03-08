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
    def _serial_requests_api_and_store(
            repo: DataBrokerApiRepository,
            api_requests: List[ApiRequest]
    ) -> None:
        for req in api_requests:
            res = request_api(req)
            repo.store_request_and_response(req, res)

    if parallel_mode:
        # 並列処理を行う
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(_serial_requests_api_and_store, repo, [request])
                for request in api_requests
            ]
            for future in futures:
                future.result()  # 各タスクが完了するのを待つ
    else:
        # シリアル処理を行う
        _serial_requests_api_and_store(repo, api_requests)


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
