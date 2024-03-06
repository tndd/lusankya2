from os import getenv

from infra.db.psql import PsqlClient


def factory_psql_client() -> PsqlClient:
    """
    テスト用のPsqlClientを作成する
    """
    url = getenv('PSQL_URL_TEST')
    if url is None:
        raise ValueError("Environment variable PSQL_URL_TEST is not set")
    return PsqlClient(url=url)
