from domain.databroker.model.api import ApiRequest, ApiResponse, ApiResultMetadata


def transform_api_request_to_query_parameter(request: ApiRequest) -> dict:
    """
    ApiRequestをクエリ用のパラメータ辞書に変換
    """
    return {
        'id': request.id_,
        'time_stamp': request.timestamp,
        'endpoint': request.endpoint,
        'parameter': request.parameter,
        'header': request.header
    }


def transform_api_request_from_fetched_data(fetched_data: dict) -> ApiRequest:
    """
    "view_latest_api_result"からフェッチしてきたデータをApiRequestモデルに変換
    """
    return ApiRequest(
        endpoint=fetched_data[2],
        parameter=fetched_data[3],
        header=fetched_data[4],
        id_=fetched_data[0],
        timestamp=fetched_data[1]
    )


def transform_api_response_to_query_parameter(response: ApiResponse) -> dict:
    """
    ApiResponseをクエリ用のパラメータ辞書に変換
    """
    return {
        'id': response.id_,
        'time_stamp': response.timestamp,
        'request_id': response.request_id,
        'status': response.status,
        'header': response.header,
        'body': response.body
    }


def transform_api_result_metadata_from_fetched_data(fetched_data: dict) -> ApiResultMetadata:
    """
    "view_latest_api_result"からフェッチしてきたデータをApiResultMetadataモデルに変換
    """
    return ApiResultMetadata(
        request_id=fetched_data[0],
        endpoint=fetched_data[2],
        parameter=fetched_data[3],
        request_header=fetched_data[4],
        response_id=fetched_data[5],
        status=fetched_data[7],
        response_header=fetched_data[8]
    )
