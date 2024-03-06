from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from domain.databroker.model.api import ApiResultMetadata


class Timeframe(Enum):
    """
    ローソク足の時間軸を表す列挙型。
    """
    MIN = "1T"
    HOUR = "1H"
    DAY = "1D"
    WEEK = "1W"
    MONTH = "1M"


class Adjustment(Enum):
    """
    ローソク足の調整方法を表す列挙型。
    """
    RAW = "raw"
    SPLIT = "split"
    DIVIDEND = "dividend"
    ALL = "all"


@dataclass
class Bar:
    """
    ローソク足の情報を表すモデル。

    注意:
        - ローソク足は自身の時間軸あるいはシンボルの情報を保持しない。
    """
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    trade_count: int
    vwap: float

    @staticmethod
    def from_json(data: dict) -> "Bar":
        """
        json形式のデータをBarモデルに変換

        Note:
            - 変換が失敗するのでZを+00:00に置き換える
        """
        ts = data["t"].replace("Z", "+00:00")
        return Bar(
            ts=datetime.fromisoformat(ts),
            open=data["o"],
            high=data["h"],
            low=data["l"],
            close=data["c"],
            volume=data["v"],
            trade_count=data["n"],
            vwap=data["vw"],
        )

    def to_parameter(self) -> dict:
        """
        クエリ用のパラメータに変換
        """
        return {
            "time_stamp": self.ts.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "trade_count": self.trade_count,
            "vwap": self.vwap,
        }


@dataclass
class Bars:
    """
    ローソク足の集合体を表すモデル。
    """
    symbol: str
    timeframe: Timeframe
    adjustment: Adjustment
    bars: List[Bar]

    @staticmethod
    def from_metadata_and_body(
        metadata: ApiResultMetadata,
        body: dict
    ) -> "Bars":
        return Bars(
            symbol=body['symbol'],
            timeframe=Timeframe(metadata.parameter['timeframe']),
            adjustment=Adjustment(metadata.parameter['adjustment']),
            bars=[Bar.from_json(data) for data in body['bars']],
        )
