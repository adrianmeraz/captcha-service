from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import const, events, exceptions, logs
from src.layers.interfaces import ICaptcha
from src.layers.twocaptcha.captcha import TwoCaptcha

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaPostPingbackEvent(raw_event)
    process_event(event=event, captcha_service=TwoCaptcha())
    return aws_utils.build_lambda_response(
        status_code=200,
        body='',
    )


def process_event(event: events.TwoCaptchaPostPingbackEvent, captcha_service: ICaptcha):
    with RetryClient() as client:
        response = captcha_service.handle_webhook_event(
            http_client=client,
            captcha_id=event.id,
            code=event.code,
            rate=event.rate
        )
        captcha_event = response.captcha_event
        if captcha_event.EventStatus == const.EventStatus.CAPTCHA_ERROR.value:
            # TODO Fix
            captcha_service.solve_captcha(
                http_client=client,
                site_key=event.site_key,
                page_url=event.page_url,
                webhook_url=event.webhook_url,
                webhook_data=event.webhook_data,
                proxy_url=event.proxy_url,
            )
        else:
            captcha_service.send_webhook_event(
                http_client=client,
                captcha_id=event.id,
                captcha_token=event.code,
                webhook_url=captcha_event.WebhookUrl,
                webhook_data=captcha_event.WebhookData
            )
