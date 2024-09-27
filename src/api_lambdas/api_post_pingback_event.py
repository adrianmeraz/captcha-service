from py_aws_core import utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, logs
from src.layers.database import Database
from src.layers.i_captcha import ICaptcha
from src.layers.twocaptcha.captcha import TwoCaptcha

logger = logs.logger


def lambda_handler(event, context):
    event = events.CSPostPingbackEvent(event)
    captcha_service = TwoCaptcha(database=Database())
    process_event(event=event, captcha_service=captcha_service)
    return aws_utils.build_lambda_response(
        status_code=200,
        body='',
    )


def process_event(event: events.CSPostPingbackEvent, captcha_service: ICaptcha):
    """
    1.  If valid, send webhook event
    2a. If invalid and can retry, send solve captcha
    2b. If invalid and cant retry, send webhook event
    :param event:
    :param captcha_service:
    :return:
    """
    with RetryClient() as client:
        response = captcha_service.handle_webhook_event(
            http_client=client,
            captcha_id=event.id,
            code=event.code,
            rate=event.rate
        )
        captcha_event = response.captcha_event
        if captcha_event.has_captcha_error and captcha_event.can_retry_captcha:
            captcha_service.solve_captcha(
                http_client=client,
                site_key=captcha_event.SiteKey,
                page_url=captcha_event.PageUrl,
                webhook_url=captcha_event.WebhookUrl,
                webhook_data=captcha_event.WebhookData,
                proxy_url=captcha_event.ProxyUrl
            )
        else:
            captcha_service.send_webhook_event(
                http_client=client,
                captcha_id=event.id,
                captcha_token=event.code,
                webhook_url=captcha_event.WebhookUrl,
                webhook_data=captcha_event.WebhookData
            )
