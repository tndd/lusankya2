from domain.databroker.model.api import ApiRequest, ApiResponse


def api_request_to_param(request: ApiRequest) -> dict:
    """
    ApiRequestをクエリ用のパラメータ辞書に変換
    """
    return {
        'id': request.id_,
        'time_stamp': request.time_stamp,
        'endpoint': request.endpoint,
        'parameter': request.parameter,
        'header': request.header
    }


def api_response_to_param(response: ApiResponse) -> dict:
    """
    ApiResponseをクエリ用のパラメータ辞書に変換
    """
    return {
        'id': response.id_,
        'time_stamp': response.time_stamp,
        'request_id': response.request_id,
        'status': response.status,
        'header': response.header,
        'body': response.body
    }