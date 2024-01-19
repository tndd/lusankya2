from dataclasses import dataclass

from domain.databroker.model.api import ApiRequest
from infra.api.alpaca.common import HEADER
from infra.api.value import ApiQuery

ENDPOINT = 'https://data.alpaca.markets/v2/stocks/bars'


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
    return ApiRequest(
        endpoint=ENDPOINT,
        header=HEADER,
        params=query.to_params()
    )
