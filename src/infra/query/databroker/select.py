def get_query_select_todo_api_request() -> str:
    """
    view_latest_api_resultからApiRequestの要素を取得する。
    
    条件:
        1. 通信がまだ行われていない（つまりstatusがNone）
        2. 通信が失敗（statusが成功の200以外）
    """
    return """
    select
        id,
        timestamp_request,
        endpoint,
        parameter,
        request_header as header
    from databroker.view_latest_api_result v
    where v.status is null
        or v.status <> 200;
"""


def get_query_select_api_result_metadata_should_be_moved() -> str:
    return """
    select
        id as request_id,
        endpoint,
        parameter,
        request_header,
        response_id,
        status,
        response_header
    from databroker.view_latest_api_result v
    where status = 200
        and v.body is not null;
"""