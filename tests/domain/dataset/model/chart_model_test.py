from datetime import datetime

from domain.databroker.model.api import ApiResultMetadata
from domain.dataset.model.chart import Adjustment, Bar, Chart, Timeframe
from tests.tests_service.factory.domain.dataset.chart import factory_chart


def test_bar_from_api_data():
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
    bar = Bar.from_api_data(data)
    # 時間がきちんとpythonに則った形に変換されているかを確認(Z => +00:00)
    assert bar.time_stamp == datetime.fromisoformat("2024-02-20T05:00:00+00:00")
    assert bar.open == 139.63


def test_bar_from_row():
    row = {
        "time_stamp": datetime.fromisoformat("2024-02-20T05:00:00+00:00"),
        "open": 139.63,
        "high": 142.075,
        "low": 139.55,
        "close": 141.15,
        "volume": 485786,
        "trade_count": 6395,
        "vwap": 140.9291
    }
    bar = Bar.from_row(row)
    assert isinstance(bar, Bar)
    assert bar.time_stamp == datetime.fromisoformat("2024-02-20T05:00:00+00:00")
    assert bar.open == 139.63


def test_bar_to_parameter():
    """
    パラメータに変換できていることを確認
    """
    bar = Bar(
        time_stamp=datetime.fromisoformat("2024-02-20T05:00:00+00:00"),
        open=139.63,
        high=142.075,
        low=139.55,
        close=141.15,
        volume=485786,
        trade_count=6395,
        vwap=140.9291
    )
    assert bar.to_parameter() == {
        "time_stamp": "2024-02-20T05:00:00+00:00",
        "open": 139.63,
        "high": 142.075,
        "low": 139.55,
        "close": 141.15,
        "volume": 485786,
        "trade_count": 6395,
        "vwap": 140.9291
    }


def test_chart_from_metadata_and_body():
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
    bars = Chart.from_metadata_and_body(metadata, body)
    assert bars.symbol == "GOOGL"
    assert bars.timeframe == Timeframe.DAY
    assert bars.adjustment == Adjustment.RAW
    assert len(bars.bars) == 4


def test_chart_to_parameter():
    bars = factory_chart()
    # 注意: factoryの実装に依存したテスト
    assert bars.to_parameter() == [
        {
            'adjustment': 'raw',
            'close': 141.15,
            'high': 142.075,
            'low': 139.55,
            'open': 139.63,
            'symbol': 'AAPL',
            'time_stamp': '2024-02-20T05:00:00+00:00',
            'timeframe': '1D',
            'trade_count': 6395,
            'volume': 485786,
            'vwap': 140.9291
        },
        {
            'adjustment': 'raw',
            'close': 142.54,
            'high': 142.68,
            'low': 140.7,
            'open': 141.37,
            'symbol': 'AAPL',
            'time_stamp': '2024-02-21T05:00:00+00:00',
            'timeframe': '1D',
            'trade_count': 5835,
            'volume': 386976,
            'vwap': 141.990892
        },
        {
            'adjustment': 'raw',
            'close': 144.02,
            'high': 145,
            'low': 142.8,
            'open': 144.96,
            'symbol': 'AAPL',
            'time_stamp': '2024-02-22T05:00:00+00:00',
            'timeframe': '1D',
            'trade_count': 6183,
            'volume': 538093,
            'vwap': 143.926125
        }
    ]
