WITH max_timestamps_snapshot AS (
  SELECT api_request_id, MAX(time_stamp) AS max_timestamp
  FROM api_response
  GROUP BY api_request_id
),
latest_snapshots AS (
  SELECT s.*
  FROM api_response s
  JOIN max_timestamps_snapshot mts
    ON s.api_request_id = mts.api_request_id
   AND s.time_stamp = mts.max_timestamp
)
SELECT *
FROM api_request sch
LEFT JOIN latest_snapshots lt_s
  ON sch.id = lt_s.api_request_id
WHERE lt_s.status IS NULL OR lt_s.status <> 200;