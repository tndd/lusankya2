from domain.databroker.model.api import ApiRequest
from infra.api.alpaca.bar import Adjustment_Q, Timeframe_Q
from tests.tests_service.factory.domain.databroker.api import \
    factory_api_request_alpaca_bar


def test_factory_api_request_alpaca_bar():
    api_request_alpaca_bar = factory_api_request_alpaca_bar()
    assert isinstance(api_request_alpaca_bar, ApiRequest)
    assert api_request_alpaca_bar.parameter['timeframe'] == Timeframe_Q.DAY.value
    assert api_request_alpaca_bar.parameter['adjustment'] == Adjustment_Q.RAW.value
