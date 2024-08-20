from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, exceptions, logs
from src.layers.captcha import CaptchaInterface
from src.layers.twocaptcha.captcha_impl import TwoCaptchaImpl

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaPostPingbackEvent(raw_event)
    process_event(event=event, captcha_service=TwoCaptchaImpl())
    return aws_utils.build_lambda_response(
        status_code=200,
        body='',
    )


def process_event(event: events.TwoCaptchaPostPingbackEvent, captcha_service: CaptchaInterface):
    with RetryClient() as client:
        captcha_service.handle_webhook_event(
            client=client,
            captcha_id=event.id,
            code=event.code,
        )
