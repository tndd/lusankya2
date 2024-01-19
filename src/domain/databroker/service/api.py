from typing import List

from domain.databroker.model import ApiRequest
from domain.databroker.repository.api import ApiRepository


def request_api(repo: ApiRepository, api_request: ApiRequest) -> None:
    """
    APIリクエストの内容を実行し、リクエストとその結果の保存を行う。
    """
    # TODO
    pass


def multi_requests_api(repo: ApiRepository, api_requests: List[ApiRequest]) -> None:
    """
    複数のAPIリクエストの内容を実行し、リクエストとその結果の保存を行う。
    """
    # TODO
    pass


def multi_requests_todo_api(repo: ApiRepository) -> None:
    """
    未実行あるいは失敗したAPIの実行を行う。
    """
    todo_requests = repo.fetch_todo_requests()
    multi_requests_api(repo, todo_requests)
