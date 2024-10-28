from dependency_injector import containers, providers
from py_aws_core.boto_clients import SSMClient, DynamoTable
from py_aws_core.router import APIGatewayRouter

from .captcha_service import CaptchaService
from .db_service import DatabaseService
from .logs import get_logger
from .secrets import Secrets


class Container(containers.DeclarativeContainer):
    """
    Singleton instances are different if a new Container Instance is made
    https://python-dependency-injector.ets-labs.org/providers/singleton.html
    """

    logger = providers.Resource(lambda: get_logger)

    apigw_router = APIGatewayRouter()
    ssm_client = providers.Factory(SSMClient)
    secrets = providers.Singleton(Secrets, ssm_client=ssm_client)
    dynamo_table = providers.Factory(DynamoTable, ddb_secrets=secrets)
    db_service = providers.Singleton(DatabaseService, dynamo_table=dynamo_table)
    captcha_service = providers.Singleton(CaptchaService, db_service=db_service, secrets=secrets)
