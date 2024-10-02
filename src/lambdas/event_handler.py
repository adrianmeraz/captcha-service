from py_aws_core import decorators

from src.layers import exceptions, logs
from src.layers.events import HttpEvent
from src.layers.routing import apigw_router

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(event, context):
    logger.info(f'{__name__}, Incoming event: {event}')
    return route_event(event=event, context=context)


def route_event(event, context):
    http_event = HttpEvent(event)
    return apigw_router.handle_event(
        http_method=http_event.request_context.http_method,
        path=http_event.request_context.path,
        event=event,
        context=context
    )
