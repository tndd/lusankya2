import random
from datetime import datetime, timedelta
from random import choices
from string import ascii_uppercase
from uuid import uuid4

from domain.databroker.model.api import ApiRequest
from domain.databroker.repository.api import DataBrokerApiRepository
from infra.api.alpaca.bar import (Adjustment_Q, QueryBar, Timeframe_Q,
                                  convert_query_bar_to_api_request)
from infra.db.psql import PsqlClient


def factory_api_request_alpaca_bar(
        timeframe: Timeframe_Q = Timeframe_Q.DAY,
        adjustment: Adjustment_Q = Adjustment_Q.RAW,
) -> ApiRequest:
    """
    alpacaのbarリクエストを作成する。
    """
    symbol = ''.join(choices(ascii_uppercase, k=5))
    """
    日付の設定:
        2020-01-01からランダムな範囲が設定される。
        範囲は１~３０日の間。
    """
    start_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 365))
    end_date = start_date + timedelta(days=random.randint(1, 30))
    query = QueryBar(
        symbol=symbol,
        timeframe=timeframe,
        start=start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        end=end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        limit=5,
        adjustment=adjustment,
        asof=None,
        feed='iex',
        currency=None,
        page_token=None,
        sort='asc'
    )
    return convert_query_bar_to_api_request(query)


def factory_api_response():
    pass


def factroy_pair_api_request_and_response():
    pass


def factory_databroker_api_repository(psql_client: PsqlClient):
    return DataBrokerApiRepository(psql_client)
