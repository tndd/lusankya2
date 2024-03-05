def get_query_insert_api_request() -> str:
    return """
    INSERT INTO databroker.api_request
    (id, time_stamp, endpoint, parameter, header)
    VALUES(%(id)s, %(time_stamp)s, %(endpoint)s, %(parameter)s, %(header)s)
    ON CONFLICT (id) DO NOTHING;
    """


def get_query_insert_api_response() -> str:
    return """
    INSERT INTO databroker.api_response
    (id, time_stamp, request_id, status, header, body)
    VALUES(%(id)s, %(time_stamp)s, %(request_id)s, %(status)s, %(header)s, %(body)s)
    ON CONFLICT (id) DO NOTHING;
    """