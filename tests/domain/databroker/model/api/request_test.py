import json

from domain.databroker.model.api import ApiRequest


def test_to_query_parameter():
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
    assert request.to_query_parameter() == expected_param


def test_from_fetched_data():
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
    assert ApiRequest.from_fetched_data(fetched_data) == expected_request # type: ignore
