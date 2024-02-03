INSERT INTO databroker.api_request
(id, time_stamp, endpoint, params, req_header)
VALUES(%(id)s, %(time_stamp)s, %(endpoint)s, %(params)s, %(req_header)s)
ON CONFLICT (id) DO NOTHING;