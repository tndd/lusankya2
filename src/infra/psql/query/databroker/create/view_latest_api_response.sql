-- 各リクエストの最新のresponseの状態
CREATE OR REPLACE VIEW databroker.view_latest_api_response AS
select
    rs.id,
    rs.time_stamp,
    rs.api_request_id,
    rs.status,
    rs.resp_header,
    rs.body
FROM databroker.api_response rs
JOIN databroker.view_latest_request_timestamp vlrt
on rs.api_request_id = vlrt.api_request_id
and rs."time_stamp" = vlrt.latest_timestamp;