from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, exceptions, logs
from src.layers.twocaptcha import api_twocaptcha

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaAddPingbackEvent(raw_event)
    add_pingback(event=event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body=api_twocaptcha.TwoCaptchaAPI.get_pingback_token(),
    )


def add_pingback(event: events.TwoCaptchaAddPingbackEvent):
    with RetryClient() as client:
        request = api_twocaptcha.AddPingback.Request(pingback_url=event.pingback_url)
        api_twocaptcha.AddPingback.call(client=client, request=request)
