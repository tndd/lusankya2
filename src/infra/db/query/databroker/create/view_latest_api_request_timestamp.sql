-- 各requestごとの最新responseの日付
CREATE OR REPLACE VIEW databroker.view_latest_request_timestamp AS
SELECT api_request_id, MAX(time_stamp) AS latest_timestamp
FROM databroker.api_response
GROUP BY api_request_id;