from dataclasses import dataclass
from typing import List

from domain.databroker.model.api import ApiRequest, ApiResponse
from infra.adapter.databroker.api import (api_request_to_param,
                                          api_response_to_param)
from infra.psql.client import PsqlClient
from infra.psql.service.load_query import Command, Schema, load_query


@dataclass
class DataBrokerApiRepository:
    cli_db: PsqlClient

    def store_request(self, request: ApiRequest) -> None:
        """
        APIリクエストの内容を保存する。

        Note:
            - 二重登録は防ぐようにする。
        """
        query = load_query(Schema.DATABROKER, Command.INSERT, 'api_request')
        param = api_request_to_param(request)
        self.cli_db.execute(query, param)

    def store_response(self, response: ApiResponse) -> None:
        """
        APIレスポンスの内容を保存する。
        """
        query = load_query(Schema.DATABROKER, Command.INSERT, 'api_response')
        param = api_response_to_param(response)
        self.cli_db.execute(query, param)

    def store_request_and_response(self, request: ApiRequest, response: ApiResponse) -> None:
        """
        APIリクエストとレスポンスの内容をトランザクション処理で確実に保存する。
        """
        query_rq = load_query(Schema.DATABROKER, Command.INSERT, 'api_request')
        param_rq = api_request_to_param(request)
        query_rs = load_query(Schema.DATABROKER, Command.INSERT, 'api_response')
        param_rs = api_response_to_param(response)
        queries_with_params = [(query_rq, param_rq), (query_rs, param_rs)]
        self.cli_db.execute_queries(queries_with_params)

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
