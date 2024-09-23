from py_aws_core import decorators

from src.layers import exceptions, logs
from src.layers.events import HttpEvent
from . import (
    api_get_pingback_verification_token,
    api_post_pingback_event,
    api_post_report_bad_captcha,
    api_post_report_good_captcha,
    api_post_solve_captcha
)

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = HttpEvent(raw_event)
    return route_event(event=event, context=context)


def route_event(event: HttpEvent, context):
    http_method = event.request_context.http_method
    path = event.request_context.path
    logger.info(f'routing event -> http_method: {http_method}, path: {path}')
    route_lambda_handler_map = {
        'GET': {
            '/2captcha.txt': api_get_pingback_verification_token.lambda_handler
        },
        'POST': {
            '/pingback-event': api_post_pingback_event.lambda_handler,
            '/report-bad-captcha': api_post_report_bad_captcha.lambda_handler,
            '/report-good-captcha': api_post_report_good_captcha.lambda_handler,
            '/solve-captcha': api_post_solve_captcha.lambda_handler,
        }
    }
    try:
        return route_lambda_handler_map[http_method][path](event, context)
    except KeyError:
        raise exceptions.RouteNotFound(http_method, path)
