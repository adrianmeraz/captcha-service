from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, exceptions, logs
from src.layers.twocaptcha import api_twocaptcha

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaSolveCaptchaEvent(raw_event)
    solve_captcha(event=event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body={},
    )


def solve_captcha(event: events.TwoCaptchaSolveCaptchaEvent):
    with RetryClient() as client:
        request = api_twocaptcha.SolveCaptchaId.Request(
            site_key=event.site_key,
            page_url=event.page_url,
            proxy_url=event.proxy_url,
            pingback=event.pingback
        )
        api_twocaptcha.SolveCaptchaId.call(client=client, request=request)
