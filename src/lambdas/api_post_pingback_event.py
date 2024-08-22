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
        response = captcha_service.handle_webhook_event(
            http_client=client,
            captcha_id=event.id,
            code=event.code,
        )
        captcha_event = response.captcha_event
        captcha_service.send_webhook_event(
            http_client=client,
            captcha_id=event.id,
            webhook_url=captcha_event.WebhookUrl,
            webhook_data=captcha_event.WebhookData
        )
