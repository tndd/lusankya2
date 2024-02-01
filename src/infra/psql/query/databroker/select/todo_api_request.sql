-- 各requestごとの最新responseの日付
WITH latest_request_id_timestamps AS (
    SELECT api_request_id, MAX(time_stamp) AS latest_timestamp
    FROM databroker.api_response
    GROUP BY api_request_id
),
-- 各リクエストの最新のresponseの状態
latest_response as (
    select
        rs.id,
        rs.time_stamp,
        rs.api_request_id,
        rs.status,
        rs.resp_header,
        rs.body
    FROM databroker.api_response rs
    JOIN latest_request_id_timestamps lrt
    on rs."time_stamp" = lrt.latest_timestamp
)
-- 各リクエストの最新の結果。
-- 表示されるのは失敗あるいは未実行のもののみ。
select
    rq.id,
    rq."time_stamp" as timestamp_request,
    rq.endpoint,
    rq.params,
    rq.req_header,
    lr.id as response_id,
    lr.time_stamp  as "timestamp_response",
    lr.status,
    lr.resp_header,
    lr.body
from databroker.api_request rq
left join latest_response lr
on rq.id = lr.api_request_id
where lr.status is null
    or lr.status <> 200;