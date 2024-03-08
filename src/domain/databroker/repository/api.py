import re
from dataclasses import dataclass
from typing import List, Optional

from domain.databroker.model.api import (ApiRequest, ApiResponse,
                                         ApiResultMetadata)
from infra.db.psql import PsqlClient
from infra.query.databroker.insert import (get_query_insert_api_request,
                                           get_query_insert_api_response)
from infra.query.databroker.select import (
    get_query_select_api_response_body,
    get_query_select_api_result_metadata_should_be_moved,
    get_query_select_todo_api_request)


@dataclass
class DataBrokerApiRepository:
    db_cli: PsqlClient

    def store_request(self, request: ApiRequest) -> None:
        """
        APIリクエストの内容を保存する。

        Note:
            - 二重登録は防ぐようにする。
        """
        query = get_query_insert_api_request()
        param = request.to_query_parameter()
        self.db_cli.execute(query, param)


    def store_response(self, response: ApiResponse) -> None:
        """
        APIレスポンスの内容を保存する。
        """
        query = get_query_insert_api_response()
        param = response.to_query_parameter()
        self.db_cli.execute(query, param)


    def store_request_and_response(self, request: ApiRequest, response: ApiResponse) -> None:
        """
        APIリクエストとレスポンスの内容をトランザクション処理で確実に保存する。
        """
        # クエリとパラメータを用意
        query_rq = get_query_insert_api_request()
        param_rq = request.to_query_parameter()
        query_rs = get_query_insert_api_response()
        param_rs = response.to_query_parameter()
        # 引数用のペアを作成
        queries_with_params = [(query_rq, param_rq), (query_rs, param_rs)]
        # 実行
        self.db_cli.execute_queries(queries_with_params)


    def fetch_todo_requests(self, endpoint: Optional[str] = None) -> List[ApiRequest]:
        """
        未実行あるいは失敗したAPIのリクエスト一覧を取得する。
        """
        query = get_query_select_todo_api_request()
        fetched_data = self.db_cli.execute(query)
        api_requests = [ApiRequest.from_fetched_data(d) for d in fetched_data]
        # エンドポイント指定がある場合、絞り込みを行う
        if endpoint:
            api_requests = [r for r in api_requests if re.search(endpoint, r.endpoint)]
        return api_requests


    def fetch_api_result_metadata_should_be_moved(self, endpoint: Optional[str] = None) -> List[ApiResultMetadata]:
        """
        概要
            まだdatasetに未移動の成功したAPIレスポンスボディのメタデータの取得。
            このメタデータを元に適宜bodyをDBから取り出す用途で使用される。
        """
        query = get_query_select_api_result_metadata_should_be_moved()
        fetched_data = self.db_cli.execute(query)
        api_results_metadata = [ApiResultMetadata.from_fetched_data(d) for d in fetched_data]
        # エンドポイント指定がある場合、絞り込みを行う
        if endpoint:
            api_results_metadata = [rm for rm in api_results_metadata if re.search(endpoint, rm.endpoint)]
        return api_results_metadata


    def fetch_body(self, response_id: str) -> dict | None:
        """
        APIレスポンスidからボディを取得する。

        特殊な例:
            - レスポンスIDのbodyが空であった場合はNoneを返す。
            - 指定されたレスポンスID自体が存在しない場合もまたNoneを返す。

        警告:
            この実装ではIDは存在するがbodyが空の場合と、
            レスポンス自体が存在しない事例を区別できないので注意が必要。
        """
        query = get_query_select_api_response_body()
        param = (response_id,)
        fetched_data = self.db_cli.execute(query, param)
        # IDは存在するがbodyが空、あるいはレスポンス自体が存在しない場合はNoneを返す
        return fetched_data[0]['body'] if fetched_data else None
