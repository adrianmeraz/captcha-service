from dependency_injector import containers, providers

from py_aws_core.router import APIGatewayRouter
from .db_service import DatabaseService
from .twocaptcha.captcha_service import TwoCaptchaService


class Container(containers.DeclarativeContainer):

    api_gw_router = providers.Singleton(APIGatewayRouter)
    db_service = providers.Singleton(DatabaseService)
    captcha_service = providers.Singleton(TwoCaptchaService, db_service=db_service)
