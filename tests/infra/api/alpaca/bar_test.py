from domain.databroker.model.api import ApiRequest
from infra.api.alpaca.bar import QueryBar, make_request_alpaca_bar


def test_make_request_alpaca_bar():
    query_bar = QueryBar(
        symbol="AAPL",
        start="2021-01-01",
        end="2021-01-02",
        timeframe="1D",
    )
    request = make_request_alpaca_bar(query_bar)
    assert isinstance(request, ApiRequest)
