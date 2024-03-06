import pytest
from dotenv import load_dotenv

from infra.service.migration import migrate
from tests.tests_service.factory.domain.databroker.api import \
    factory_databroker_api_repository
from tests.tests_service.factory.domain.dataset.asset import \
    factory_asset_repository
from tests.tests_service.factory.infra.db.psql import factory_psql_client
from tests.tests_service.utils import clear_tables


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    # 環境変数の読み込み
    load_dotenv()
    # 環境構築のためのマイグレーション実行
    cli_db = factory_psql_client()
    migrate(cli_db)


@pytest.fixture
def psql_client():
    psql_cli = factory_psql_client()
    # テスト前にテーブルは綺麗にしておく
    clear_tables(psql_cli)
    yield psql_cli


@pytest.fixture
def asset_repository():
    yield factory_asset_repository()


@pytest.fixture
def databroker_api_repository(psql_client):
    yield factory_databroker_api_repository(psql_client)
