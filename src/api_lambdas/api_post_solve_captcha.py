from py_aws_core import utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, logs
from src.layers.database import Database
from src.layers.i_captcha import ICaptcha
from src.layers.twocaptcha.captcha import TwoCaptcha
from src.layers.routing import apigw_router

logger = logs.logger


@apigw_router.route(path='/solve-captcha', http_method='POST')
def lambda_handler(event, context):
    event = events.CSSolveCaptchaEvent(event)
    captcha_service = TwoCaptcha(database=Database())
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
