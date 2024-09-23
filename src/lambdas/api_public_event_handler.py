from py_aws_core import decorators

from src.layers import exceptions, logs
from src.layers.events import HttpEvent
from ._routes import apigw_router

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(event, context):
    logger.info(f'{__name__}, Incoming event: {event}')
    event = HttpEvent(event)
    return route_event(event=event, context=context)


def route_event(event: HttpEvent, context):
    return apigw_router.handle_event(
        http_method=event.request_context.http_method,
        path=event.request_context.path,
        event=event,
        context=context
    )
