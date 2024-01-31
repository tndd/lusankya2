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
        params=api_request.params,
        headers=api_request.header
    )
    return ApiResponse(
        api_request_id=api_request._id,
        status=response.status_code,
        header=dict(response.headers),
        body=response.json()
    )


def multi_requests_api(
        repo: DataBrokerApiRepository,
        api_requests: List[ApiRequest],
        n_max_worker: int = 8
    ) -> None:
    """
    並列で複数のAPIリクエストの内容を実行し、リクエストとその結果の保存を行う。
    """
    # TODO
    pass


def multi_requests_todo_api(repo: DataBrokerApiRepository) -> None:
    """
    未実行あるいは失敗したAPIの実行を行う。
    """
    todo_requests = repo.fetch_todo_requests()
    multi_requests_api(repo, todo_requests)
