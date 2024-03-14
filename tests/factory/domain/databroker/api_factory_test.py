from domain.databroker.model.api import ApiRequest
from infra.api.alpaca.bar import Adjustment_Q, Timeframe_Q
from tests.tests_service.factory.domain.databroker.api import \
    factory_alpaca_bar_api_request


def test_factory_alpaca_bar_api_request():
    api_request_alpaca_bar = factory_alpaca_bar_api_request()
    assert isinstance(api_request_alpaca_bar, ApiRequest)
    assert api_request_alpaca_bar.parameter['timeframe'] == Timeframe_Q.DAY.value
    assert api_request_alpaca_bar.parameter['adjustment'] == Adjustment_Q.RAW.value
