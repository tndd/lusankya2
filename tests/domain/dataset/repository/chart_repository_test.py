from domain.dataset.model.chart import Adjustment, Chart, Timeframe
from domain.dataset.repository.chart import ChartRepository
from tests.tests_service.factory.domain.dataset.chart import factory_chart


def test_store_chart(chart_repository: ChartRepository):
    chart = factory_chart()
    chart_repository.store_chart(chart)
    # 保存されたデータの確認
    r = chart_repository.db_cli.execute(
        'select count(*) from alpaca.bar;'
    )
    # 注意: factoryの実装に依存したテスト
    assert r[0][0] == 3


def test_fetch_chart(chart_repository: ChartRepository):
    # 取得のためのデータ取得
    chart = factory_chart()
    chart_repository.store_chart(chart)
    # 取得
    fetched_chart = chart_repository.fetch_chart(
        symbol='AAPL',
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW
    )
    assert isinstance(Chart, fetched_chart)
