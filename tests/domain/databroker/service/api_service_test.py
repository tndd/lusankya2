import pytest

from domain.databroker.model.api import ApiRequest, ApiResponse
from domain.databroker.service.api import request_api


@pytest.mark.api
def test_request_api():
    """
    APIリクエストが正常に行われているのかのテスト
    """
    request = ApiRequest(
        endpoint="https://httpbin.org/get",
        params={
            'p1': 'param1',
            'p2': 'param2'
        },
        header={
            'h1': 'header1',
            'h2': 'header2'
        }
    )
    response = request_api(request)
    assert isinstance(response, ApiResponse)
    assert response.status == 200
    assert response.body['url'] == 'https://httpbin.org/get?p1=param1&p2=param2'
    assert response.body['headers']['H1'] == 'header1'
    assert response.body['headers']['H2'] == 'header2'
