from dataclasses import dataclass
from os import getenv

from domain.databroker.model.api import ApiRequest
from domain.databroker.service.value import ApiQuery


@dataclass
class QueryBar(ApiQuery):
    symbol: str
    timeframe: str
    start: str
    end: str
    limit: int = 10000
    adjustment: str = 'raw'
    asof: str = None
    feed: str = 'iex'
    currency: str = None
    page_token: str = None
    sort: str = 'asc'


def make_request_alpaca_bar(query: QueryBar) -> ApiRequest:
    """
    クエリの情報を元にAPIリクエストを作成する。
    """
    ENDPOINT = 'https://data.alpaca.markets/v2/stocks/bars'
    HEADER = {
        "APCA-API-KEY-ID": getenv('APCA_KEY_ID'),
        "APCA-API-SECRET-KEY": getenv('APCA_SECRET')
    }
    return ApiRequest(
        endpoint=ENDPOINT,
        header=HEADER,
        params=query.to_params()
    )
