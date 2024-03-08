from domain.dataset.repository.chart import ChartRepository
from tests.tests_service.factory.domain.dataset.chart import factory_chart


def test_store_chart(chart_repository: ChartRepository):
    chart = factory_chart()
    chart_repository.store_chart(chart)
    # 保存されたデータの確認
    chart_repository.db_cli.execute(
        """
        INSERT INTO alpaca.bar ("time_stamp", timeframe, symbol, adjustment, "open", high, low, "close", trade_count, volume, vwap) VALUES('2024-02-21T05:00:01+00:00', '1M', 'AAPL', 'raw', 0, 0, 0, 0, 0, 0, 0);
        """
    )
    r = chart_repository.db_cli.execute(
        'select count(*) from alpaca.bar;'
    )
    # 注意: factoryの実装に依存したテスト
    assert r[0] == 3


def test_fetch_chart(chart_repository: ChartRepository):
    pass
