from dataclasses import dataclass

from domain.dataset.model.chart import Adjustment, Chart, Timeframe
from infra.db.psql import PsqlClient


@dataclass
class ChartRepository:
    db_cli: PsqlClient

    def store_chart(self, chart: Chart) -> None:
        pass


    def fetch_chart(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: str,
        end: str
    ) -> Chart:
        pass
