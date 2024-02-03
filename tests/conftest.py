from os import getenv

import pytest
from dotenv import load_dotenv

from domain.databroker.repository.api import DataBrokerApiRepository
from domain.dataset.repository.asset import AssetRepository
from infra.db.psql import PsqlClient

load_dotenv()


@pytest.fixture
def psql_client() -> PsqlClient:
    url = getenv('PSQL_URL_TEST')
    if url is None:
        raise ValueError("Environment variable PSQL_URL_TEST is not set")
    return PsqlClient(url=url)


@pytest.fixture
def asset_repository():
    return AssetRepository()


@pytest.fixture
def databroker_api_repository(psql_client) -> DataBrokerApiRepository:
    return DataBrokerApiRepository(psql_client)
