select
    id,
    timestamp_request,
    endpoint,
    params,
    req_header,
    response_id,
    timestamp_response,
    status,
    resp_header,
    body
from databroker.view_latest_api_result v
where v.status is null
    or v.status <> 200;