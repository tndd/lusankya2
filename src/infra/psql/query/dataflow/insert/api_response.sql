INSERT INTO dataflow.api_response
(time_stamp, api_request_id, status, resp_header, body)
VALUES(%(time_stamp)s, %(api_request_id)s, %(status)s, %(resp_header)s, %(body)s);