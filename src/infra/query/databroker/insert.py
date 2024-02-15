def get_query_insert_api_request() -> str:
    return """
    INSERT INTO databroker.api_request
    (id, time_stamp, endpoint, parameter, req_header)
    VALUES(%(id)s, %(time_stamp)s, %(endpoint)s, %(parameter)s, %(req_header)s)
    ON CONFLICT (id) DO NOTHING;
    """


def get_query_insert_api_response() -> str:
    return """
    INSERT INTO databroker.api_response
    (time_stamp, request_id, status, resp_header, body)
    VALUES(%(id)s, %(time_stamp)s, %(request_id)s, %(status)s, %(resp_header)s, %(body)s)
    ON CONFLICT (id) DO NOTHING;
    """