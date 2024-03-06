from datetime import datetime

from domain.databroker.model.api import ApiResultMetadata
from domain.dataset.model.bar import Adjustment, Bar, Bars, Timeframe


def test_bar_from_json():
    """
    bodyの要素Barsの１要素が変換できていることを確認
    """
    data = {
        "c": 141.15,
        "h": 142.075,
        "l": 139.55,
        "n": 6395,
        "o": 139.63,
        "t": "2024-02-20T05:00:00Z",
        "v": 485786,
        "vw": 140.9291
    }
    bar = Bar.from_json(data)
    # 時間がきちんとpythonに則った形に変換されているかを確認(Z => +00:00)
    assert bar.ts == datetime.fromisoformat("2024-02-20T05:00:00+00:00")
    assert bar.open == 139.63


def test_bars_from_metadata_and_body():
    metadata = ApiResultMetadata(
        request_id='aa8fcbe8-1820-49b7-aa4a-4cd96453d6b9',
        endpoint='https://data.alpaca.markets/v2/stocks/AAPL/bars',
        parameter={"timeframe": "1D", "start": "2023-01-01T00:00:00Z", "end": "2023-01-31T00:00:00Z", "limit": 5, "adjustment": "raw", "feed": "iex", "sort": "asc"},
        request_header={"APCA-API-KEY-ID": "XXXXX", "APCA-API-SECRET-KEY": "YYYYY"},
        response_id='934fe9d3-7750-426b-8490-4e24f2794085',
        status=200,
        response_header={"Date": "Wed, 06 Mar 2024 05:33:50 GMT", "Content-Type": "application/json; charset=UTF-8", "Transfer-Encoding": "chunked", "Connection": "keep-alive", "Vary": "Accept-Encoding", "X-Ratelimit-Limit": "200", "X-Ratelimit-Remaining": "199", "X-Ratelimit-Reset": "1709703230", "Strict-Transport-Security": "max-age=15724800; includeSubDomains", "X-Request-ID": "d263f5a6f6904a6201b6b0b0738f93e4", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": "true", "Access-Control-Allow-Methods": "GET, OPTIONS", "Access-Control-Allow-Headers": "Apca-Api-Key-Id, Apca-Api-Secret-Key, Authorization", "Access-Control-Max-Age": "1728000", "Content-Encoding": "gzip"}
    )
    body = {
        "bars": [
            {"c": 141.15, "h": 142.075, "l": 139.55, "n": 6395, "o": 139.63, "t": "2024-02-20T05:00:00Z", "v": 485786, "vw": 140.9291},
            {"c": 142.54, "h": 142.68, "l": 140.7, "n": 5835, "o": 141.37, "t": "2024-02-21T05:00:00Z", "v": 386976, "vw": 141.990892},
            {"c": 144.02, "h": 145, "l": 142.8, "n": 6183, "o": 144.96, "t": "2024-02-22T05:00:00Z", "v": 538093, "vw": 143.926125},
            {"c": 143.94, "h": 144.665, "l": 143.445, "n": 5352, "o": 143.645, "t": "2024-02-23T05:00:00Z", "v": 382390, "vw": 143.969119}
        ],
        "next_page_token": None,
        "symbol": "GOOGL"
    }
    bars = Bars.from_metadata_and_body(metadata, body)
    assert bars.symbol == "GOOGL"
    assert bars.timeframe == Timeframe.DAY
    assert bars.adjustment == Adjustment.RAW
    assert len(bars.bars) == 4
