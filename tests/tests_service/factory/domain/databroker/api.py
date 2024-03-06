from domain.databroker.repository.api import DataBrokerApiRepository
from infra.db.psql import PsqlClient


def factory_databroker_api_repository(psql_client: PsqlClient):
    return DataBrokerApiRepository(psql_client)
