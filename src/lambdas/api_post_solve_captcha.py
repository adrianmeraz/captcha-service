from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, exceptions, logs
from src.layers.captcha import CaptchaInterface
from src.layers.twocaptcha.captcha_impl import TwoCaptchaImpl

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaSolveCaptchaEvent(raw_event)
    process_event(event=event, captcha_service=TwoCaptchaImpl())
    return aws_utils.build_lambda_response(
        status_code=200,
        body='',
    )


def process_event(event: events.TwoCaptchaSolveCaptchaEvent, captcha_service: CaptchaInterface):
    with RetryClient() as client:
        captcha_service.solve_captcha(
            client=client,
            site_key=event.site_key,
            page_url=event.page_url,
            proxy_url=event.proxy_url,
            webhook_url=event.webhook_url
        )
