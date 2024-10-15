from dependency_injector import containers, providers
from py_aws_core.router import APIGatewayRouter

from .captcha_service import CaptchaService
from .db_dynamo import DBClient
from .db_service import DatabaseService
from .logs import get_logger
from .secrets import Secrets


class Container(containers.DeclarativeContainer):

    logger = providers.Resource(lambda: get_logger)
    api_gw_router = providers.Singleton(APIGatewayRouter)
    db_client = providers.Singleton(DBClient)
    db_service = providers.Singleton(DatabaseService, db_client=db_client)
    captcha_service = providers.Singleton(CaptchaService, db_service=db_service, logger=logger)
    secrets = providers.Singleton(Secrets)
