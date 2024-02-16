from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class ApiRequest:
    endpoint: str
    parameter: dict
    header: dict
    id_: str = field(default_factory=lambda: str(uuid4()))
    time_stamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ApiResponse:
    request_id: str
    status: int
    header: dict
    body: dict
    id_: str = field(default_factory=lambda: str(uuid4()))
    time_stamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ApiResponseMetdata:
    """
    ApiResponseのbodyには非常に大きなデータが格納されていることがある。
    そのため、ApiResponseのbodyにはデータのメタデータのみを格納し、
    bodyの情報をこのクラスの情報をもとに適宜引き出せるようにする。
    """
    response_id: str
    endpoint: str


@dataclass
class ApiResult:
    endpoint: str
    parameter: dict
    request_header: dict
    status: int
    response_header: dict
    body: str
    id_: str = field(default_factory=lambda: str(uuid4()))
    time_stamp: str = field(default_factory=lambda: datetime.now().isoformat())