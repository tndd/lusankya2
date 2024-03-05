from dataclasses import dataclass
from datetime import datetime
from typing import List


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
    symbol: str
    timeframe: str
    bars: List[Bar]
