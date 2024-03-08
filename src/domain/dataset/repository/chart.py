from dataclasses import dataclass

from domain.dataset.model.chart import Adjustment, Chart, Timeframe
from infra.db.psql import PsqlClient
from infra.query.alpaca.insert import get_query_insert_bar


@dataclass
class ChartRepository:
    db_cli: PsqlClient

    def store_chart(
        self,
        chart: Chart
    ) -> None:
        """
        Chartモデルを保存する。

        Memo:
            parallel_modeが有効である場合、並列でinsertが実行される。
            デフォルトではTrueとする。
        """
        # BUG: 情報が保存されない
        query = get_query_insert_bar()
        bars_params = chart.to_parameter()
        self.db_cli.executemany(query, bars_params, parallel_mode=True)


    def fetch_chart(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: str,
        end: str
    ) -> Chart:
        pass
