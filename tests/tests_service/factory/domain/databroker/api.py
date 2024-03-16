from datetime import datetime, timedelta
from random import choices, randint
from string import ascii_uppercase

from domain.databroker.model.api import ApiRequest
from domain.databroker.repository.api import DataBrokerApiRepository
from infra.api.alpaca.bar import (Adjustment_Q, QueryBar, Timeframe_Q,
                                  convert_query_bar_to_api_request)
from infra.db.psql import PsqlClient


def factory_api_request(
        endpoint: str | None = None,
        parameter: dict | None = None,
        header: dict | None = None
) -> ApiRequest:
    """
    汎用的なApiRequestを作成する。

    endpointの形式:
        endpoint/{ランダムな文字列8~16}/{ランダムな数字4~8桁}

    parameterの形式:
        要素の数は4~8個
        keyはp_{n}という形式
        valueの値はランダムな英数字8桁

    headerの形式:
        基本的にparameterと同様。
        要素の数は4~8個
        keyはh_{n}という形式
        valueの値はランダムな英数字8桁
    """
    if endpoint is None:
        random_chars = "".join(choices(ascii_uppercase, k=randint(8, 16)))
        random_digits = "".join(choices(ascii_uppercase + "0123456789", k=randint(4, 8)))
        endpoint = f'endpoint/{random_chars}/{random_digits}'
    if parameter is None:
        random_parameter = {}
        for i in range(randint(4, 8)):
            random_parameter[f'p_{i}'] = ''.join(choices(ascii_uppercase + "0123456789", k=randint(4, 8)))
        parameter = random_parameter
    if header is None:
        random_header = {}
        for i in range(randint(4, 8)):
            random_header[f'h_{i}'] = ''.join(choices(ascii_uppercase + "0123456789", k=randint(4, 8)))
        header = random_header
    return ApiRequest(
        endpoint=endpoint,
        parameter=parameter,
        header=header
    )


def factory_alpaca_bar_api_request(
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
    start_date = datetime(2020, 1, 1) + timedelta(days=randint(0, 365))
    end_date = start_date + timedelta(days=randint(1, 30))
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


def factory_api_response_alpaca_bar():
    pass


def factroy_pair_api_request_and_response():
    pass


def factory_databroker_api_repository(psql_client: PsqlClient):
    return DataBrokerApiRepository(psql_client)
