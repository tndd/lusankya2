import json

from psycopg2.extras import DictRow

from domain.databroker.model.api import (ApiRequest, ApiResponse,
                                         ApiResultMetadata)


def transform_api_request_to_query_parameter(request: ApiRequest) -> dict:
    """
    ApiRequestをクエリ用のパラメータ辞書に変換
    """
    return {
        'id': request.id_,
        'time_stamp': request.timestamp,
        'endpoint': request.endpoint,
        'parameter': json.dumps(request.parameter),
        'header': json.dumps(request.header)
    }


def transform_api_request_from_fetched_data(fetched_data: DictRow) -> ApiRequest:
    """
    "get_query_select_todo_api_request"からフェッチしてきたデータをApiRequestモデルに変換
    """
    return ApiRequest(
        endpoint=fetched_data['endpoint'],
        parameter=fetched_data['parameter'],
        header=fetched_data['header'],
        id_=fetched_data['id'],
        timestamp=fetched_data['timestamp_request']
    )


def transform_api_response_to_query_parameter(response: ApiResponse) -> dict:
    """
    ApiResponseをクエリ用のパラメータ辞書に変換

    警告:
        json.dumpsにNoneを渡すと文字列で'null'という値を返してしまう。
        そのため、bodyにNoneを渡す場合には特別な処理が必要となる。
    """
    return {
        'id': response.id_,
        'time_stamp': response.timestamp,
        'request_id': response.request_id,
        'status': response.status,
        'header': json.dumps(response.header),
        'body': json.dumps(response.body) if response.body is not None else None
    }


def transform_api_result_metadata_from_fetched_data(fetched_data: DictRow) -> ApiResultMetadata:
    """
    "get_query_select_api_result_metadata_should_be_moved"からフェッチしてきたデータを、
    ApiResultMetadataモデルに変換
    """
    return ApiResultMetadata(
        request_id=fetched_data['request_id'],
        endpoint=fetched_data['endpoint'],
        parameter=fetched_data['parameter'],
        request_header=fetched_data['request_header'],
        response_id=fetched_data['response_id'],
        status=fetched_data['status'],
        response_header=fetched_data['response_header']
    )
