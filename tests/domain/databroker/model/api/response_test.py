import json

from domain.databroker.model.api import ApiResponse


def test_to_query_parameter():
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
    assert response.to_query_parameter() == expected_param
