from dataclasses import dataclass
from typing import List, Optional

from domain.databroker.model.api import ApiRequest, ApiResponse
from infra.adapter.databroker.api import (api_request_to_param,
                                          api_response_to_param)
from infra.db.psql import PsqlClient
from infra.query.databroker.insert import (insert_api_request,
                                           insert_api_response)
from infra.query.databroker.select import select_todo_api_request


@dataclass
class DataBrokerApiRepository:
    cli_db: PsqlClient

    def store_request(self, request: ApiRequest) -> None:
        """
        APIリクエストの内容を保存する。

        Note:
            - 二重登録は防ぐようにする。
        """
        query = insert_api_response()
        param = api_request_to_param(request)
        self.cli_db.execute(query, param)

    def store_response(self, response: ApiResponse) -> None:
        """
        APIレスポンスの内容を保存する。
        """
        query = insert_api_response()
        param = api_response_to_param(response)
        self.cli_db.execute(query, param)

    def store_request_and_response(self, request: ApiRequest, response: ApiResponse) -> None:
        """
        APIリクエストとレスポンスの内容をトランザクション処理で確実に保存する。
        """
        # クエリとパラメータを用意
        query_rq = insert_api_request()
        param_rq = api_request_to_param(request)
        query_rs = insert_api_response()
        param_rs = api_response_to_param(response)
        # 引数用のペアを作成
        queries_with_params = [(query_rq, param_rq), (query_rs, param_rs)]
        # 実行
        self.cli_db.execute_queries(queries_with_params)

    def fetch_todo_requests(self, endpoint: Optional[str] = None) -> List[ApiRequest]:
        """
        未実行あるいは失敗したAPIのリクエスト一覧を取得する。
        """
        query = select_todo_api_request()
        result = self.cli_db.execute(query)
        if endpoint:
            """
            エンドポイント指定がある場合、
            そのエンドポイントの未実行あるいは失敗したAPIリクエストのみ取得する。
            """
            return [
                ApiRequest(
                    endpoint=r[2],
                    params=r[3],
                    header=r[4],
                    id_=r[0],
                    time_stamp=r[1]
                )
                for r in result
                if r[2] == endpoint
            ]
        else:
            """
            デフォルト動作。
            すべての未実行あるいは失敗したAPIリクエストを取得する。
            """
            return [
                ApiRequest(
                    endpoint=r[2],
                    params=r[3],
                    header=r[4],
                    id_=r[0],
                    time_stamp=r[1]
                )
                for r in result
            ]

    def fetch_success_results_unmoved(self) -> List[ApiResponse]:
        """
        まだdatasetに未移動の成功したAPIのレスポンス一覧を取得する。
        """
        # TODO
        pass
