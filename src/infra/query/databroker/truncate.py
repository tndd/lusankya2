def get_query_truncate_api_request() -> str:
    return "TRUNCATE TABLE databroker.api_request CASCADE;"


def get_query_truncate_api_response() -> str:
    return "TRUNCATE TABLE databroker.api_response CASCADE;"
