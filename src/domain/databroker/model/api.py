from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


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
    body: dict
    id_: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ApiResult:
    endpoint: str
    parameter: dict
    request_header: dict
    response_id: str
    status: int
    response_header: dict
    body: dict
    id_: str = field(default_factory=lambda: str(uuid4()))
    time_stamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ApiResponseBodyMetadata:
    """
    概要:
        ApiResponse（あるいはApiResult）のbodyには非常に大きなデータが格納されていることがある。
        そのため、ApiResponseのbodyにはデータのメタデータのみを格納し、
        bodyの情報をこのクラスの情報をもとに適宜引き出せるようにする。

    要素:
        response_id:
            絶対必要。
            このidを元に適宜bodyをDBから取り出す。
        endpoint: 
            bodyを取り出しても、それ単体ではどのような加工を行なって分析用DBに移動すればいいかが分からない。
            そのためendpointから内容を判別する必要がある。
        parameter:
            現状では用途は無い。だがパラメータによってレスポンスの内容が大幅に変わるということもあり得るため、
            一応保持しておく。
    """
    endpoint: str
    parameter: dict
    response_id: str