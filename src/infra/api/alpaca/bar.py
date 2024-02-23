from dataclasses import dataclass
from typing import Optional

from domain.databroker.model.api import ApiRequest
from infra.api.alpaca.common import APCA_ENDPOINT, APCA_HEADER


@dataclass
class QueryBar:
    symbol: str
    timeframe: str
    start: str
    end: str
    limit: int = 10000
    adjustment: str = 'raw'
    asof: Optional[str] = None
    feed: str = 'iex'
    currency: Optional[str] = None
    page_token: Optional[str] = None
    sort: str = 'asc'

    def to_params(self) -> dict:
        """
        要素をApiリクエストのためのパラメータに変換する。

        symbolについてはエンドポイント部分に直接含まれるので、
        パラメータには含めない。
        """
        params = {
            'timeframe': self.timeframe,
            'start': self.start,
            'end': self.end,
            'limit': self.limit,
            'adjustment': self.adjustment,
            'asof': self.asof,
            'feed': self.feed,
            'currency': self.currency,
            'page_token': self.page_token,
            'sort': self.sort,
        }
        return {k: v for k, v in params.items() if v is not None}


def make_request_alpaca_bar(query: QueryBar) -> ApiRequest:
    """
    クエリの情報を元にAPIリクエストを作成する。
    """
    return ApiRequest(
        endpoint=APCA_ENDPOINT['bar'].format(symbol=query.symbol),
        header=APCA_HEADER,
        parameter=query.to_params()
    )
