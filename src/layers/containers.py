from dependency_injector import containers, providers
from py_aws_core.boto_clients import DynamoDBClientFactory, SSMClientFactory
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
    dynamo_db_client = providers.Factory(DynamoDBClientFactory.new_client)
    ssm_client = providers.Factory(SSMClientFactory.new_client)
    secrets = providers.Singleton(Secrets, boto_client=ssm_client)
    db_service = providers.Singleton(DatabaseService, boto_client=dynamo_db_client, secrets=secrets)
    captcha_service = providers.Singleton(CaptchaService, db_service=db_service, secrets=secrets)

