from domain.databroker.model.api import ApiRequest
from infra.api.alpaca.bar import (QueryBar, Timeframe_Q,
                                  convert_query_bar_to_api_request,
                                  make_query_bars_from_symbols)


def test_convert_query_bar_to_api_request():
    query_bar = QueryBar(
        symbol="AAPL",
        start="2021-01-01",
        end="2021-01-02",
        timeframe=Timeframe_Q.DAY,
    )
    request = convert_query_bar_to_api_request(query_bar)
    assert isinstance(request, ApiRequest)


def test_make_query_bars_from_symbols():
    query_bars = make_query_bars_from_symbols(
        symbols=["AAPL", "GOOGL"],
        timeframe=Timeframe_Q.DAY,
        start="2021-01-01",
        end="2022-01-02",
    )
    assert isinstance(query_bars, list)
    assert len(query_bars) == 2
    assert isinstance(query_bars[0], QueryBar)
