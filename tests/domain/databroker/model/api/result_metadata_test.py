from domain.databroker.model.api import ApiResultMetadata


def test_from_fetched_data():
    fetched_data = {
        'request_id': '2d4eeca1-0efd-e9d4-2eba-d3b5efb0e775',
        'endpoint': 'http://test.endpoint',
        'parameter': {'key': 'value'},
        'request_header': {'Content-Type': 'application/json'},
        'response_id': '4857b290-9d39-fd7d-0c83-38da2714012b',
        'status': 200,
        'response_header': {'Content-Type': 'application/json'}
    }
    expected_result_metadata = ApiResultMetadata(
        request_id='2d4eeca1-0efd-e9d4-2eba-d3b5efb0e775',
        endpoint='http://test.endpoint',
        parameter={'key': 'value'},
        request_header={'Content-Type': 'application/json'},
        response_id='4857b290-9d39-fd7d-0c83-38da2714012b',
        status=200,
        response_header={'Content-Type': 'application/json'}
    )
    assert ApiResultMetadata.from_fetched_data(fetched_data) == expected_result_metadata # type: ignore