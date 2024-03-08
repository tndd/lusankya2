from dataclasses import dataclass
from typing import Optional

from domain.dataset.model.chart import Adjustment, Bar, Chart, Timeframe
from infra.db.psql import PsqlClient
from infra.query.alpaca.insert import get_query_insert_bar
from infra.query.alpaca.select import get_query_select_bar


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
        query = get_query_insert_bar()
        bars_params = chart.to_parameter()
        self.db_cli.executemany(query, bars_params, parallel_mode=True)


    def fetch_chart(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> Chart:
        query = get_query_select_bar(start, end)
        param = {
            'symbol': symbol,
            'timeframe': timeframe.value,
            'adjustment': adjustment.value,
        }
        rows = self.db_cli.execute(query, param)
        bars = [Bar.from_row(row) for row in rows]
        return Chart(
            symbol=symbol,
            timeframe=timeframe,
            adjustment=adjustment,
            bars=bars
        )
