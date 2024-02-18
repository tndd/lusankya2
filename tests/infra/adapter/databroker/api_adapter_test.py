from domain.databroker.model.api import ApiRequest, ApiResponse
from infra.adapter.databroker.api import (transform_api_request_to_query_parameter,
                                          transform_api_response_to_query_parameter, 
                                          transform_api_request_from_fetched_data,
                                          transform_api_result_metadata_from_fetched_data)
import json
from psycopg2.extras import DictRow


def test_transform_api_request_to_query_parameter():
    request = ApiRequest(
        id_='test_id',
        timestamp='2021-01-01T00:00:00Z',
        endpoint='http://test.endpoint',
        parameter={'key': 'value'},
        header={'Content-Type': 'application/json'}
    )
    expected_param = {
        'id': 'test_id',
        'time_stamp': '2021-01-01T00:00:00Z',
        'endpoint': 'http://test.endpoint',
        'parameter': json.dumps({'key': 'value'}),
        'header': json.dumps({'Content-Type': 'application/json'})
    }
    assert transform_api_request_to_query_parameter(request) == expected_param


def test_transform_api_request_from_fetched_data():
    fetched_data = {
        'id': 'c0fe6a69-aca7-4680-b29f-84788dc637d6',
        'timestamp_request': '2021-01-01T00:00:00Z',
        'endpoint': 'http://test.endpoint',
        'parameter': {'key': 'value'},
        'header': {'Content-Type': 'application/json'}
    }
    expected_request = ApiRequest(
        id_='c0fe6a69-aca7-4680-b29f-84788dc637d6',
        timestamp='2021-01-01T00:00:00Z',
        endpoint='http://test.endpoint',
        parameter={'key': 'value'},
        header={'Content-Type': 'application/json'}
    )
    assert transform_api_request_from_fetched_data(fetched_data) == expected_request


def test_transform_api_response_to_query_parameter():
    response = ApiResponse(
        id_='response_id',
        timestamp='2021-01-01T00:00:00Z',
        request_id='test_id',
        status=200,
        header={'Content-Type': 'application/json'},
        body={'data': 'test'}
    )
    expected_param = {
        'id': 'response_id',
        'time_stamp': '2021-01-01T00:00:00Z',
        'request_id': 'test_id',
        'status': 200,
        'header': json.dumps({'Content-Type': 'application/json'}),
        'body': json.dumps({'data': 'test'})
    }
    assert transform_api_response_to_query_parameter(response) == expected_param


def test_transform_api_result_metadata_from_fetched_data():
    pass
