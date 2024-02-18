from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Optional


@dataclass
class ApiRequest:
    endpoint: str
    parameter: dict
    header: dict
    id_: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ApiResponse:
    request_id: str
    status: int
    header: dict
    body: Optional[dict]
    id_: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ApiResultMetadata:
    """
    ApiRequestとそれに対応するApiResponseの情報をまとめたもの。
    なおbodyについてはサイズが巨大であるため、このクラスには含めない。

    もしbodyが必要である場合は、response_idから適宜引き出すように。
    """
    request_id: str
    endpoint: str
    parameter: dict
    request_header: dict
    response_id: str
    status: int
    response_header: dict
