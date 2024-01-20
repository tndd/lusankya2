DROP VIEW IF EXISTS databroker.latest_api_response;
CREATE VIEW databroker.latest_api_response AS
WITH max_timestamps_snapshot AS (
  SELECT api_request_id, MAX(time_stamp) AS max_timestamp
  FROM databroker.api_response
  GROUP BY api_request_id
),
latest_snapshots AS (
  SELECT s.*
  FROM databroker.api_response s
  JOIN max_timestamps_snapshot mts
    ON s.api_request_id = mts.api_request_id
   AND s.time_stamp = mts.max_timestamp
)
SELECT *
FROM latest_snapshots;