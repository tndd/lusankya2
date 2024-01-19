from os import getenv

import pytest

from infra.psql.client import PsqlClient


@pytest.fixture
def psql_client() -> PsqlClient:
    return PsqlClient(url=getenv('PSQL_URL_TEST'))
