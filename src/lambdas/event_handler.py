from py_aws_core import decorators

from src.api_lambdas import import_all_package_modules
from src.layers import exceptions, logs
from src.layers.routing import get_router

logger = logs.logger
apigw_router = get_router()


# import_all_package_modules('src.api_lambdas')


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(event, context):
    logger.info(f'{__name__}, Incoming event: {event}')
    return apigw_router.handle_event(aws_event=event, aws_context=context)
