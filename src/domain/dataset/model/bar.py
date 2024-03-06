from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from domain.dataset.model.asset import Asset


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


@dataclass
class Bars:
    """
    ローソク足の集合体を表すモデル。
    """
    asset: Asset
    timeframe: Timeframe
    adjustment: Adjustment
    bars: List[Bar]
