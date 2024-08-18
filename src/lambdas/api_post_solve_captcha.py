from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, exceptions, logs, secrets
from src.layers.interfaces import CaptchaInterface
from src.layers.twocaptcha.services import TwoCaptchaService

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaSolveCaptchaEvent(raw_event)
    solve_captcha(event=event, captcha_service=TwoCaptchaService())
    return aws_utils.build_lambda_response(
        status_code=200,
        body='',
    )


def solve_captcha(event: events.TwoCaptchaSolveCaptchaEvent, captcha_service: CaptchaInterface):
    with RetryClient() as client:
        captcha_service.solve_captcha(
            client=client,
            site_key=event.site_key,
            page_url=event.page_url,
            proxy_url=event.proxy_url,
            pingback_url=secrets.get_webhook_url(),
            opt_data={
                'webhook_url': event.webhook_url
            }
        )
