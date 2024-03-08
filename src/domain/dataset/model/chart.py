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


def parse_timestamp(time_stamp: str) -> datetime:
    """
    概要:
        ISOフォーマットのタイムスタンプ文字列をdatetimeオブジェクトに変換する。
        'Z'が含まれている場合は'+00:00'に置き換える。

    注意:
        この置き換えしなければ、datetimeがエラーになってしまう。
        pythonはデフォルトで'Z'という表記に対応していないようだ。

    引数:
        ts_str (str): ISOフォーマットのタイムスタンプ文字列。
    """
    return datetime.fromisoformat(time_stamp.replace("Z", "+00:00"))


@dataclass
class Bar:
    """
    ローソク足の情報を表すモデル。

    注意:
        - ローソク足は自身の時間軸あるいはシンボルの情報を保持しない。
    """
    time_stamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    trade_count: int
    vwap: float

    @staticmethod
    def from_api_data(data: dict) -> "Bar":
        """
        apiの生形式のデータをBarモデルに変換
        """
        return Bar(
            time_stamp=parse_timestamp(data["t"]),
            open=data["o"],
            high=data["h"],
            low=data["l"],
            close=data["c"],
            volume=data["v"],
            trade_count=data["n"],
            vwap=data["vw"],
        )


    @staticmethod
    def from_row(row: dict) -> "Bar":
        """
        dbから取得してきた1行のデータをBarモデルに変換
        """
        return Bar(
            time_stamp=parse_timestamp(row["time_stamp"]),
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume'],
            trade_count=row['trade_count'],
            vwap=row['vwap'],
        )


    def to_parameter(self) -> dict:
        """
        クエリ用のパラメータに変換
        """
        return {
            "time_stamp": self.time_stamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "trade_count": self.trade_count,
            "vwap": self.vwap,
        }


@dataclass
class Chart:
    """
    ローソク足の集合体であるチャートを表すモデル
    """
    symbol: str
    timeframe: Timeframe
    adjustment: Adjustment
    bars: List[Bar]

    @staticmethod
    def from_metadata_and_body(
        metadata: ApiResultMetadata,
        body: dict
    ) -> "Chart":
        return Chart(
            symbol=body['symbol'],
            timeframe=Timeframe(metadata.parameter['timeframe']),
            adjustment=Adjustment(metadata.parameter['adjustment']),
            bars=[Bar.from_api_data(data) for data in body['bars']],
        )

    def to_parameter(self) -> List[dict]:
        return [
            {
                **bar.to_parameter(),
                "symbol": self.symbol,
                "timeframe": self.timeframe.value,
                "adjustment": self.adjustment.value,
            }
            for bar in self.bars
        ]

    @staticmethod
    def from_rows(rows: List[dict]) -> "Chart":
        return Chart(
            symbol=rows[0]['symbol'],
            timeframe=Timeframe(rows[0]['timeframe']),
            adjustment=Adjustment(rows[0]['adjustment']),
            bars=[Bar.from_api_data(r['']) for r in rows],
        )
