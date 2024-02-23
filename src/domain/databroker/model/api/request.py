import json
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from psycopg2.extras import DictRow


@dataclass
class ApiRequest:
    endpoint: str
    parameter: dict
    header: dict
    id_: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_query_parameter(self) -> dict:
        """
        ApiRequestをクエリ用のパラメータ辞書に変換
        """
        return {
            'id': self.id_,
            'time_stamp': self.timestamp,
            'endpoint': self.endpoint,
            'parameter': json.dumps(self.parameter),
            'header': json.dumps(self.header)
        }

    @staticmethod
    def from_fetched_data(fetched_data: DictRow) -> 'ApiRequest':
        """
        "get_query_select_todo_api_request"からフェッチしてきたデータをApiRequestモデルに変換
        """
        return ApiRequest(
            endpoint=fetched_data['endpoint'],
            parameter=fetched_data['parameter'],
            header=fetched_data['header'],
            id_=fetched_data['id'],
            timestamp=fetched_data['timestamp_request']
        )