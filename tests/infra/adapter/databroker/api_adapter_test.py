from domain.databroker.model.api import ApiRequest, ApiResponse
from infra.adapter.databroker.api import (api_request_to_param,
                                          api_response_to_param)


def test_api_request_to_param():
    request = ApiRequest(
        _id='test_id',
        time_stamp='2021-01-01T00:00:00Z',
        endpoint='http://test.endpoint',
        params={'key': 'value'},
        header={'Content-Type': 'application/json'}
    )
    expected_param = {
        'id': 'test_id',
        'time_stamp': '2021-01-01T00:00:00Z',
        'endpoint': 'http://test.endpoint',
        'params': {'key': 'value'},
        'req_header': {'Content-Type': 'application/json'}
    }
    assert api_request_to_param(request) == expected_param


def test_api_response_to_param():
    response = ApiResponse(
        _id='response_id',
        time_stamp='2021-01-01T00:00:00Z',
        api_request_id='test_id',
        status=200,
        header={'Content-Type': 'application/json'},
        body={'data': 'test'}
    )
    expected_param = {
        'id': 'response_id',
        'time_stamp': '2021-01-01T00:00:00Z',
        'api_request_id': 'test_id',
        'status': 200,
        'resp_header': {'Content-Type': 'application/json'},
        'body': {'data': 'test'}
    }
    assert api_response_to_param(response) == expected_param
