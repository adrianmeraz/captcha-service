from py_aws_core import decorators, utils as aws_utils

from src.layers import exceptions, logs
from src.layers.events import HttpEvent

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = HttpEvent(raw_event)
    response = route_event(event=event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body=response,
        content_type='text/plain;charset=utf-8'
    )


def route_event(event: HttpEvent):
    http_method = event.request_context.http_method
    path = event.request_context.path
    logger.info(f'routing event -> http_method: {http_method}, path: {path}')
