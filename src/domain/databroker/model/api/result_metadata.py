from dataclasses import dataclass

from psycopg2.extras import DictRow


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

    @staticmethod
    def from_fetched_data(fetched_data: DictRow) -> 'ApiResultMetadata':
        """
        "get_query_select_api_result_metadata_should_be_moved"からフェッチしてきたデータを、
        ApiResultMetadataモデルに変換
        """
        return ApiResultMetadata(
            request_id=fetched_data['request_id'],
            endpoint=fetched_data['endpoint'],
            parameter=fetched_data['parameter'],
            request_header=fetched_data['request_header'],
            response_id=fetched_data['response_id'],
            status=fetched_data['status'],
            response_header=fetched_data['response_header']
        )