from domain.databroker.model.api import ApiRequest, ApiResponse


def api_request_to_query_parameter(request: ApiRequest) -> dict:
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


def api_response_to_query_parameter(response: ApiResponse) -> dict:
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


def api_request_from_query_result(fetched_data: dict) -> ApiRequest:
    """
    DBからフェッチしてきたデータをApiRequestモデルに変換
    """
    return ApiRequest(
        endpoint=fetched_data[2],
        parameter=fetched_data[3],
        header=fetched_data[4],
        id_=fetched_data[0],
        timestamp=fetched_data[1]
    )