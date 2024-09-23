from py_aws_core import decorators

from src.layers import exceptions, logs, router
from src.layers.events import HttpEvent
from . import (
    api_get_pingback_verification_token,
    api_post_pingback_event,
    api_post_report_bad_captcha,
    api_post_report_good_captcha,
    api_post_solve_captcha
)

logger = logs.logger
apigw_router = router.APIGatewayRouter()
apigw_router.add_route(fn=api_get_pingback_verification_token.lambda_handler, http_method='GET', path='/2captcha.txt')
apigw_router.add_route(fn=api_post_pingback_event.lambda_handler, http_method='POST', path='/pingback-event')
apigw_router.add_route(fn=api_post_report_bad_captcha.lambda_handler, http_method='POST', path='/report-bad-captcha')
apigw_router.add_route(fn=api_post_report_good_captcha.lambda_handler, http_method='POST', path='/report-good-captcha')
apigw_router.add_route(fn=api_post_solve_captcha.lambda_handler, http_method='POST', path='/solve-captcha')


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = HttpEvent(raw_event)
    return route_event(event=event, context=context)


def route_event(event: HttpEvent, context):
    return apigw_router.handle_event(
        http_method=event.request_context.http_method,
        path=event.request_context.path,
        event=event,
        context=context
    )
