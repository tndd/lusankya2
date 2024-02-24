import pytest
from dotenv import load_dotenv

from domain.databroker.repository.api import DataBrokerApiRepository
from domain.dataset.repository.asset import AssetRepository
from infra.service.migration import migrate
from tests.utils import clear_tables, make_test_psql_client


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    # 環境変数の読み込み
    load_dotenv()
    # 環境構築のためのマイグレーション実行
    cli_db = make_test_psql_client()
    migrate(cli_db)
    # 前回のデータが残存している可能性があるため初期化する
    clear_tables(cli_db)


@pytest.fixture
def psql_client():
    psql_cli = make_test_psql_client()
    yield psql_cli
    # テスト終了毎にテーブルを初期化する
    clear_tables(psql_cli)


@pytest.fixture
def asset_repository():
    yield AssetRepository()


@pytest.fixture
def databroker_api_repository(psql_client):
    yield DataBrokerApiRepository(psql_client)
