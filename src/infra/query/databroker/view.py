def get_query_create_view_latest_api_request_timestamp() -> str:
    """
    各requestごとの最新responseの日付
    """
    return """
    CREATE OR REPLACE VIEW databroker.view_latest_request_timestamp AS
    SELECT request_id, MAX(time_stamp) AS latest_timestamp
    FROM databroker.api_response
    GROUP BY request_id;
    """


def get_query_view_latest_api_response() -> str:
    """
    各リクエストの最新のresponseの状態
    """
    return """
    CREATE OR REPLACE VIEW databroker.view_latest_api_response AS
    select
        rs.id,
        rs.time_stamp,
        rs.request_id,
        rs.status,
        rs.resp_header,
        rs.body
    FROM databroker.api_response rs
    JOIN databroker.view_latest_request_timestamp vlrt
    on rs.request_id = vlrt.request_id
    and rs.time_stamp = vlrt.latest_timestamp;
    """


def get_query_view_latest_api_result() -> str:
    """
    各リクエストの最新のレスポンスの結果のみを表示する
    """
    return """
    CREATE OR REPLACE VIEW databroker.view_latest_api_result AS
    select
        rq.id,
        rq.time_stamp as timestamp_request,
        rq.endpoint,
        rq.parameter,
        rq.req_header,
        lr.id as response_id,
        lr.time_stamp as timestamp_response,
        lr.status,
        lr.resp_header,
        lr.body
    from databroker.api_request rq
    left join databroker.view_latest_api_response lr
    on rq.id = lr.request_id;
    """