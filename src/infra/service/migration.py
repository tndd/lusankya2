from typing import List

from infra.db.psql import PsqlClient
from infra.query.alpaca.create import (get_query_create_schema_alpaca,
                                       get_query_create_table_bar)
from infra.query.common import get_query_create_extension_uuid
from infra.query.databroker.create import (get_query_create_schema_databroker,
                                           get_query_create_table_api_request,
                                           get_query_create_table_api_response)
from infra.query.databroker.view import (
    get_query_create_view_latest_api_request_timestamp,
    get_query_view_latest_api_response, get_query_view_latest_api_result)


def migrate(cli: PsqlClient):
    """
    マイグレーションの実行

    クエリは必要な順番で並んでいるため、
    呼び出し側では頭から適宜実行しなければならない。
    """
    queries = (
        _queries_preparation() +
        _queries_schema() +
        _queries_table() +
        _queries_view()
    )
    cli.execute_queries(queries)


def _queries_preparation() -> List[str]:
    """
    設定などの、DB運用に必要なクエリを得る。

    やること:
        1. uuidを使えるようにする
    """
    return [
        get_query_create_extension_uuid(),
    ]


def _queries_schema() -> List[str]:
    """
    スキーマの定義のためのクエリを得る
    """
    return [
        get_query_create_schema_alpaca(),
        get_query_create_schema_databroker(),
    ]


def _queries_table() -> List[str]:
    """
    テーブルの定義のためのクエリを得る

    Note:
        Table Assetはまだ未実装であるため、作成をスキップしている。
    """
    return [
        get_query_create_table_bar(),
        get_query_create_table_api_request(),
        get_query_create_table_api_response(),
    ]


def _queries_view() -> List[str]:
    """
    ビューの定義のためのクエリを得る
    """
    return [
        get_query_create_view_latest_api_request_timestamp(),
        get_query_view_latest_api_response(),
        get_query_view_latest_api_result(),
    ]
