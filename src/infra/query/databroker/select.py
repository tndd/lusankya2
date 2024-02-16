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