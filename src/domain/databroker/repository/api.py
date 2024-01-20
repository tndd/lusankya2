from dataclasses import dataclass
from typing import List

from domain.databroker.model.api import ApiRequest, ApiResponse
from infra.psql.client import PsqlClient


@dataclass
class DataBrokerApiRepository:
    cli_db: PsqlClient

    def store_request(self, api_request: ApiRequest) -> None:
        """
        APIリクエストの内容を保存する。

        Note:
            - 二重登録は防ぐようにする。
        """
        # TODO
        pass

    def store_response(self, api_response: ApiResponse) -> None:
        """
        APIレスポンスの内容を保存する。
        """
        # TODO
        pass

    def store_request_and_response(self, api_request: ApiRequest, api_response: ApiResponse) -> None:
        """
        APIリクエストとレスポンスの内容をトランザクション処理で確実に保存する。
        """
        # TODO
        pass

    def fetch_todo_requests(self) -> List[ApiRequest]:
        """
        未実行あるいは失敗したAPIのリクエスト一覧を取得する。
        """
        # TODO
        pass

    def fetch_todo_requests_by_endpoint(self, endpoint: str) -> List[ApiRequest]:
        """
        特定エンドポイントの未実行あるいは失敗したAPIのリクエスト一覧を取得する。
        """
        todo_api_requests = self.fetch_todo_requests()
        return [r for r in todo_api_requests if r.endpoint == endpoint]

    def fetch_success_results_unmoved(self) -> List[ApiResponse]:
        """
        まだdatasetに未移動の成功したAPIのレスポンス一覧を取得する。
        """
        # TODO
        pass
