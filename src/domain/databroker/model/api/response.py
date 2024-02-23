import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class ApiResponse:
    request_id: str
    status: int
    header: dict
    body: Optional[dict]
    id_: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_query_parameter(self) -> dict:
        """
        ApiResponseをクエリ用のパラメータ辞書に変換

        警告:
            json.dumpsにNoneを渡すと文字列で'null'という値を返してしまう。
            そのため、bodyにNoneを渡す場合には特別な処理が必要となる。
        """
        return {
            'id': self.id_,
            'time_stamp': self.timestamp,
            'request_id': self.request_id,
            'status': self.status,
            'header': json.dumps(self.header),
            'body': json.dumps(self.body) if self.body is not None else None
        }
