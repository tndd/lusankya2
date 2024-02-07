from typing import List

from infra.db.psql import PsqlClient
from infra.query.alpaca.create import create_schema_alpaca, create_table_bar
from infra.query.common import create_extension_uuid
from infra.query.databroker.create import (create_schema_databroker,
                                           create_table_api_request,
                                           create_table_api_response)
from infra.query.databroker.view import (
    create_view_latest_api_request_timestamp, create_view_latest_api_response,
    create_view_latest_api_result)


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
        create_extension_uuid(),
    ]


def _queries_schema() -> List[str]:
    """
    スキーマの定義のためのクエリを得る
    """
    return [
        create_schema_alpaca(),
        create_schema_databroker(),
    ]


def _queries_table() -> List[str]:
    """
    テーブルの定義のためのクエリを得る

    Note:
        Table Assetはまだ未実装であるため、作成をスキップしている。
    """
    return [
        create_table_bar(),
        create_table_api_request(),
        create_table_api_response(),
    ]


def _queries_view() -> List[str]:
    """
    ビューの定義のためのクエリを得る
    """
    return [
        create_view_latest_api_request_timestamp(),
        create_view_latest_api_response(),
        create_view_latest_api_result(),
    ]
