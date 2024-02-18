import json
from dataclasses import dataclass
from typing import List, Optional

from domain.databroker.model.api import (ApiRequest, ApiResponse,
                                         ApiResultMetadata)
from infra.adapter.databroker.api import (
    transform_api_request_from_fetched_data,
    transform_api_request_to_query_parameter,
    transform_api_response_to_query_parameter,
    transform_api_result_metadata_from_fetched_data)
from infra.db.psql import PsqlClient
from infra.query.databroker.insert import (get_query_insert_api_request,
                                           get_query_insert_api_response)
from infra.query.databroker.select import (
    get_query_select_api_response_body,
    get_query_select_api_result_metadata_should_be_moved,
    get_query_select_todo_api_request)


@dataclass
class DataBrokerApiRepository:
    cli_db: PsqlClient

    def store_request(self, request: ApiRequest) -> None:
        """
        APIリクエストの内容を保存する。

        Note:
            - 二重登録は防ぐようにする。
        """
        query = get_query_insert_api_request()
        param = transform_api_request_to_query_parameter(request)
        self.cli_db.execute(query, param)


    def store_response(self, response: ApiResponse) -> None:
        """
        APIレスポンスの内容を保存する。
        """
        query = get_query_insert_api_response()
        param = transform_api_response_to_query_parameter(response)
        self.cli_db.execute(query, param)


    def store_request_and_response(self, request: ApiRequest, response: ApiResponse) -> None:
        """
        APIリクエストとレスポンスの内容をトランザクション処理で確実に保存する。
        """
        # クエリとパラメータを用意
        query_rq = get_query_insert_api_request()
        param_rq = transform_api_request_to_query_parameter(request)
        query_rs = get_query_insert_api_response()
        param_rs = transform_api_response_to_query_parameter(response)
        # 引数用のペアを作成
        queries_with_params = [(query_rq, param_rq), (query_rs, param_rs)]
        # 実行
        self.cli_db.execute_queries(queries_with_params)


    def fetch_todo_requests(self, endpoint: Optional[str] = None) -> List[ApiRequest]:
        """
        未実行あるいは失敗したAPIのリクエスト一覧を取得する。
        """
        query = get_query_select_todo_api_request()
        fetched_data = self.cli_db.execute(query)
        api_requests = [transform_api_request_from_fetched_data(d) for d in fetched_data]
        # エンドポイント指定がある場合、絞り込みを行う
        if endpoint:
            api_requests = [r for r in api_requests if r.endpoint == endpoint]
        return api_requests


    def fetch_api_result_metadata_should_be_moved(self, endpoint: Optional[str] = None) -> List[ApiResultMetadata]:
        """
        概要
            まだdatasetに未移動の成功したAPIレスポンスボディのメタデータの取得。
            このメタデータを元に適宜bodyをDBから取り出す用途で使用される。
        """
        query = get_query_select_api_result_metadata_should_be_moved()
        fetched_data = self.cli_db.execute(query)
        api_results_metadata = [transform_api_result_metadata_from_fetched_data(d) for d in fetched_data]
        # エンドポイント指定がある場合、絞り込みを行う
        if endpoint:
            api_results_metadata = [rm for rm in api_results_metadata if rm.endpoint == endpoint]
        return api_results_metadata


    def fetch_body(self, response_id: str) -> dict | None:
        """
        APIレスポンスidからボディを取得する。

        レスポンスが見つからなかった場合はNoneを返す。
        """
        query = get_query_select_api_response_body()
        param = (response_id,)
        fetched_data = self.cli_db.execute(query, param)
        # WARN: ここの変換はadapter無しに直接やっているので注意
        if fetched_data[0]['body'] is not None:
            result = json.loads(fetched_data[0]['body'])
        else:
            result = None
        return result
