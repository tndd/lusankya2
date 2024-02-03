-- 各リクエストの最新のレスポンスの結果のみを表示する
CREATE OR REPLACE VIEW databroker.view_latest_api_result AS
select
	rq.id,
    rq.time_stamp as timestamp_request,
    rq.endpoint,
    rq.params,
    rq.req_header,
    lr.id as response_id,
    lr.time_stamp as timestamp_response,
    lr.status,
    lr.resp_header,
    lr.body
from databroker.api_request rq
left join databroker.view_latest_api_response lr
on rq.id = lr.api_request_id;