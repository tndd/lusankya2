from domain.databroker.model.api import ApiRequest
from infra.api.alpaca.bar import QueryBar, convert_query_bar_to_api_request


def test_convert_query_bar_to_api_request():
    query_bar = QueryBar(
        symbol="AAPL",
        start="2021-01-01",
        end="2021-01-02",
        timeframe="1D",
    )
    request = convert_query_bar_to_api_request(query_bar)
    assert isinstance(request, ApiRequest)
