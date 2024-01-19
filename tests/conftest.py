from os import getenv

import pytest
from dotenv import load_dotenv

from infra.psql.client import PsqlClient

load_dotenv()


@pytest.fixture
def psql_client() -> PsqlClient:
    return PsqlClient(url=getenv('PSQL_URL_TEST'))
