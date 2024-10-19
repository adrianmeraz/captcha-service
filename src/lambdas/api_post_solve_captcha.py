from dependency_injector.wiring import Provide, inject
from py_aws_core import utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events
from src.layers.captcha_interface import ICaptcha
from src.layers.containers import Container


apigw_router = Container.apigw_router


@apigw_router.route(path='/solve-captcha', http_method='POST')
@inject
def lambda_handler(event, context, captcha_service: ICaptcha = Provide[Container.captcha_service]):
    event = events.CSSolveCaptchaEvent(event)
    process_event(event=event, captcha_service=captcha_service)
    return aws_utils.build_lambda_response(
        status_code=200,
        body='',
    )


def process_event(event: events.CSSolveCaptchaEvent, captcha_service: ICaptcha):
    with RetryClient() as client:
        captcha_service.solve_captcha(
            http_client=client,
            site_key=event.site_key,
            page_url=event.page_url,
            webhook_url=event.webhook_url,
            webhook_data=event.webhook_data,
            proxy_url=event.proxy_url,
        )
