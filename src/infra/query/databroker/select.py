def get_query_select_latest_api_result_metadata() -> str:
    return """
    select
        id as request_id,
        endpoint,
        parameter,
        request_header,
        response_id,
        status,
        response_header
    from databroker.view_latest_api_result;
"""


def get_query_select_todo_api_request() -> str:
    return """
    select
        id,
        timestamp_request,
        endpoint,
        parameter,
        header
    from databroker.view_latest_api_result v
    where v.status is null
        or v.status <> 200;
"""